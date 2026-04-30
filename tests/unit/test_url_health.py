"""Tests for `util.url_health`.

Uses `httpx.MockTransport` to drive the HEAD/GET probe against scripted
responses. Verifies the domain-match logic against realistic Doceree
competitor URL shapes (subdomain redirects, www-stripping, totally
different domains).
"""
from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest

from clients.http import CircuitBreaker, HttpClient
from util.url_health import HealthResult, check, registered_domain


# ====================================================================
# registered_domain()
# ====================================================================


class TestRegisteredDomain:
    @pytest.mark.parametrize(
        "url,expected",
        [
            ("https://www.deepintent.com/news", "deepintent.com"),
            ("https://deepintent.com/", "deepintent.com"),
            ("https://blog.doximity.com/posts/abc", "doximity.com"),
            ("https://investors.optimizerx.com/news-releases", "optimizerx.com"),
            ("https://news.example.co.uk/", "example.co.uk"),
            ("https://EXAMPLE.COM/Path", "example.com"),
        ],
    )
    def test_extracts_etld_plus_one(self, url: str, expected: str) -> None:
        assert registered_domain(url) == expected

    def test_invalid_returns_empty(self) -> None:
        # No suffix
        assert registered_domain("https://localhost/") == ""
        # Junk
        assert registered_domain("not-a-url") == ""


# ====================================================================
# check() with mocked HTTP
# ====================================================================


def _mock_transport(
    handler: Callable[[httpx.Request], httpx.Response],
) -> httpx.MockTransport:
    return httpx.MockTransport(handler)


def _make_client(handler: Callable[[httpx.Request], httpx.Response]) -> httpx.AsyncClient:
    """Build a test httpx.AsyncClient with redirect-following enabled
    (matching the default that production HttpClient applies to its own
    client)."""
    return httpx.AsyncClient(transport=_mock_transport(handler), follow_redirects=True)


@pytest.fixture
def make_http():
    """Factory: pass a request handler, get a configured HttpClient.

    Each test creates its own client so circuit-breaker state doesn't leak
    between tests.
    """
    created: list[HttpClient] = []

    def _factory(handler: Callable[[httpx.Request], httpx.Response]) -> HttpClient:
        http = HttpClient(client=_make_client(handler), circuit_breaker=CircuitBreaker())
        created.append(http)
        return http

    yield _factory


# ---- Live cases ----


@pytest.mark.asyncio
class TestLive:
    async def test_200_head_same_domain(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            assert req.method == "HEAD"
            return httpx.Response(200)

        http = make_http(handler)
        async with http:
            result = await check("https://www.deepintent.com/news/cortex", http=http)
        assert result.is_live is True
        assert result.status_code == 200
        assert result.reason == ""

    async def test_200_after_redirect_same_etld_plus_one(self, make_http) -> None:
        """www-stripping redirect counts as same registered domain."""

        def handler(req: httpx.Request) -> httpx.Response:
            if req.url.host == "www.deepintent.com":
                return httpx.Response(
                    301, headers={"Location": "https://deepintent.com/news/cortex"}
                )
            return httpx.Response(200)

        http = make_http(handler)
        async with http:
            result = await check("https://www.deepintent.com/news/cortex", http=http)
        assert result.is_live is True
        assert result.final_url is not None
        assert "deepintent.com" in result.final_url

    async def test_subdomain_redirect_same_registered_domain(self, make_http) -> None:
        """Apex -> subdomain redirect (e.g., -> blog.) is same registered domain."""

        def handler(req: httpx.Request) -> httpx.Response:
            if req.url.host == "doximity.com":
                return httpx.Response(
                    301, headers={"Location": "https://blog.doximity.com/posts/x"}
                )
            return httpx.Response(200)

        http = make_http(handler)
        async with http:
            result = await check("https://doximity.com/posts/x", http=http)
        assert result.is_live is True


# ---- Method fallback ----


@pytest.mark.asyncio
class TestMethodFallback:
    async def test_head_405_falls_back_to_get(self, make_http) -> None:
        seen_methods: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            seen_methods.append(req.method)
            if req.method == "HEAD":
                return httpx.Response(405)
            return httpx.Response(200)

        http = make_http(handler)
        async with http:
            result = await check("https://www.example.com/", http=http)
        assert seen_methods == ["HEAD", "GET"]
        assert result.is_live is True

    async def test_head_501_falls_back_to_get(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(501) if req.method == "HEAD" else httpx.Response(200)

        http = make_http(handler)
        async with http:
            result = await check("https://www.example.com/", http=http)
        assert result.is_live is True

    async def test_method_fallback_disabled(self, make_http) -> None:
        seen_methods: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            seen_methods.append(req.method)
            return httpx.Response(405)

        http = make_http(handler)
        async with http:
            result = await check(
                "https://www.example.com/", http=http, method_fallback=False
            )
        assert seen_methods == ["HEAD"]
        assert result.is_live is False
        assert result.reason == "non_200_status_405"


# ---- Non-live cases ----


@pytest.mark.asyncio
class TestNonLive:
    async def test_404_drops_finding(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(404)

        http = make_http(handler)
        async with http:
            result = await check("https://www.example.com/missing", http=http)
        assert result.is_live is False
        assert result.status_code == 404
        assert result.reason == "non_200_status_404"

    async def test_500_drops_finding(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(500)

        http = make_http(handler)
        async with http:
            result = await check("https://www.example.com/", http=http)
        assert result.is_live is False
        assert result.reason == "non_200_status_500"

    async def test_domain_mismatch_after_redirect(self, make_http) -> None:
        """Redirect to a different registered domain -> not live (potential
        hallucination or cross-domain tracker)."""

        def handler(req: httpx.Request) -> httpx.Response:
            if req.url.host == "www.deepintent.com":
                return httpx.Response(
                    301, headers={"Location": "https://malicious-tracker.com/redirect"}
                )
            return httpx.Response(200)

        http = make_http(handler)
        async with http:
            result = await check("https://www.deepintent.com/x", http=http)
        assert result.is_live is False
        assert "domain_mismatch" in result.reason
        assert result.status_code == 200  # 200 reached, but wrong host

    async def test_domain_match_check_can_be_disabled(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            if req.url.host == "www.deepintent.com":
                return httpx.Response(
                    301, headers={"Location": "https://other-domain.com/"}
                )
            return httpx.Response(200)

        http = make_http(handler)
        async with http:
            result = await check(
                "https://www.deepintent.com/x",
                http=http,
                require_domain_match=False,
            )
        assert result.is_live is True

    async def test_network_error(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("simulated DNS failure")

        http = make_http(handler)
        async with http:
            result = await check("https://www.example.com/", http=http)
        assert result.is_live is False
        assert "network_error" in result.reason

    async def test_timeout(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            raise httpx.ReadTimeout("simulated timeout")

        http = make_http(handler)
        async with http:
            result = await check("https://www.example.com/", http=http)
        assert result.is_live is False
        assert "timeout" in result.reason

    async def test_circuit_breaker_open(self, make_http) -> None:
        breaker = CircuitBreaker(failure_threshold=1)
        await breaker.record_failure("blocked.com")

        def handler(req: httpx.Request) -> httpx.Response:
            pytest.fail("handler should not run while breaker is open")

        http = HttpClient(client=_make_client(handler), circuit_breaker=breaker)
        async with http:
            result = await check("https://blocked.com/x", http=http)
        assert result.is_live is False
        assert "circuit_breaker_open" in result.reason


# ---- HealthResult helper ----


class TestHealthResultDomainMatches:
    def test_no_final_url_means_no_match(self) -> None:
        r = HealthResult(cited_url="https://x.com/", is_live=False)
        assert r.domain_matches is False

    def test_same_etld_plus_one(self) -> None:
        r = HealthResult(
            cited_url="https://www.deepintent.com/news",
            final_url="https://deepintent.com/news",
            is_live=True,
        )
        assert r.domain_matches is True

    def test_different_etld_plus_one(self) -> None:
        r = HealthResult(
            cited_url="https://example.com/",
            final_url="https://other.com/",
            is_live=False,
        )
        assert r.domain_matches is False
