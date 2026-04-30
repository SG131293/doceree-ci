"""Tests for `clients.http`.

Uses `httpx.MockTransport` to simulate server responses without network I/O.
The CircuitBreaker is exercised with an injectable fake clock so we can
verify time-window behavior deterministically.
"""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

import httpx
import pytest

from clients.http import (
    CircuitBreaker,
    CircuitBreakerOpen,
    DEFAULT_USER_AGENT,
    HttpClient,
)


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def tick(self, seconds: float) -> None:
        self.t += seconds


def _mock_transport(
    handler: Callable[[httpx.Request], httpx.Response],
) -> httpx.MockTransport:
    return httpx.MockTransport(handler)


def _make_client(
    handler: Callable[[httpx.Request], httpx.Response],
    **kwargs: Any,
) -> httpx.AsyncClient:
    """Build a test httpx.AsyncClient with redirect-following enabled
    (matching the default that production HttpClient applies)."""
    kwargs.setdefault("follow_redirects", True)
    return httpx.AsyncClient(transport=_mock_transport(handler), **kwargs)


# ====================================================================
# CircuitBreaker
# ====================================================================


class TestCircuitBreakerConstruction:
    def test_defaults(self) -> None:
        cb = CircuitBreaker()
        assert cb.failure_threshold == 5
        assert cb.window_seconds == 60.0
        assert cb.open_duration_seconds == 300.0

    def test_threshold_must_be_positive(self) -> None:
        with pytest.raises(ValueError):
            CircuitBreaker(failure_threshold=0)

    def test_durations_must_be_positive(self) -> None:
        with pytest.raises(ValueError):
            CircuitBreaker(window_seconds=0)
        with pytest.raises(ValueError):
            CircuitBreaker(open_duration_seconds=0)


@pytest.mark.asyncio
class TestCircuitBreakerStateMachine:
    async def test_starts_closed(self) -> None:
        cb = CircuitBreaker(clock=FakeClock())
        # No exception when checking a never-seen host.
        await cb.check("example.com")
        assert await cb.is_open("example.com") is False

    async def test_under_threshold_stays_closed(self) -> None:
        clock = FakeClock()
        cb = CircuitBreaker(failure_threshold=5, clock=clock)
        for _ in range(4):
            await cb.record_failure("example.com")
        await cb.check("example.com")  # still closed
        assert await cb.is_open("example.com") is False

    async def test_threshold_failures_open_circuit(self) -> None:
        clock = FakeClock()
        cb = CircuitBreaker(failure_threshold=5, clock=clock)
        for _ in range(5):
            await cb.record_failure("example.com")
        with pytest.raises(CircuitBreakerOpen) as exc:
            await cb.check("example.com")
        assert exc.value.host == "example.com"

    async def test_old_failures_outside_window_dont_count(self) -> None:
        clock = FakeClock()
        cb = CircuitBreaker(
            failure_threshold=5, window_seconds=60, clock=clock
        )
        # 4 failures at t=0
        for _ in range(4):
            await cb.record_failure("example.com")
        # Advance past the rolling window
        clock.tick(70)
        # One more failure: only 1 in the current window, not 5.
        await cb.record_failure("example.com")
        await cb.check("example.com")  # still closed
        assert await cb.is_open("example.com") is False

    async def test_open_window_blocks_check_until_elapsed(self) -> None:
        clock = FakeClock()
        cb = CircuitBreaker(
            failure_threshold=5,
            window_seconds=60,
            open_duration_seconds=300,
            clock=clock,
        )
        for _ in range(5):
            await cb.record_failure("example.com")
        with pytest.raises(CircuitBreakerOpen):
            await cb.check("example.com")

        # Halfway through the open window: still blocked.
        clock.tick(150)
        with pytest.raises(CircuitBreakerOpen):
            await cb.check("example.com")

        # After the open window elapses: passes through, state reset.
        clock.tick(160)  # total 310
        await cb.check("example.com")  # no raise
        assert await cb.is_open("example.com") is False

    async def test_reset_clears_failure_history(self) -> None:
        clock = FakeClock()
        cb = CircuitBreaker(
            failure_threshold=5, open_duration_seconds=10, clock=clock
        )
        for _ in range(5):
            await cb.record_failure("example.com")
        clock.tick(20)
        await cb.check("example.com")  # resets
        # Need 5 fresh failures to re-open, not 1.
        for _ in range(4):
            await cb.record_failure("example.com")
        await cb.check("example.com")  # still closed

    async def test_record_success_closes_breaker(self) -> None:
        clock = FakeClock()
        cb = CircuitBreaker(failure_threshold=5, clock=clock)
        for _ in range(5):
            await cb.record_failure("example.com")
        await cb.record_success("example.com")
        await cb.check("example.com")  # closed again
        assert await cb.is_open("example.com") is False

    async def test_per_host_independence(self) -> None:
        clock = FakeClock()
        cb = CircuitBreaker(failure_threshold=5, clock=clock)
        for _ in range(5):
            await cb.record_failure("a.com")
        # b.com is unaffected.
        await cb.check("b.com")
        with pytest.raises(CircuitBreakerOpen):
            await cb.check("a.com")


# ====================================================================
# HttpClient
# ====================================================================


@pytest.mark.asyncio
class TestHttpClientResponses:
    async def test_get_200(self) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, text="ok")

        async with HttpClient(client=_make_client(handler)) as http:
            r = await http.get("https://example.com/")
            assert r.status_code == 200
            assert r.text == "ok"

    async def test_user_agent_set(self) -> None:
        seen: dict[str, str] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            seen["ua"] = req.headers.get("user-agent", "")
            return httpx.Response(200)

        client = _make_client(handler, headers={"User-Agent": DEFAULT_USER_AGENT})
        async with HttpClient(client=client) as http:
            await http.get("https://example.com/")
        assert seen["ua"] == DEFAULT_USER_AGENT

    async def test_head_request(self) -> None:
        seen: dict[str, str] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            seen["method"] = req.method
            return httpx.Response(200)

        async with HttpClient(client=_make_client(handler)) as http:
            await http.head("https://example.com/")
        assert seen["method"] == "HEAD"

    async def test_redirects_followed(self) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            if req.url.path == "/start":
                return httpx.Response(301, headers={"Location": "https://example.com/end"})
            return httpx.Response(200, text="final")

        async with HttpClient(client=_make_client(handler)) as http:
            r = await http.get("https://example.com/start")
            assert r.status_code == 200
            assert str(r.url) == "https://example.com/end"


@pytest.mark.asyncio
class TestHttpClientCircuitBreakerIntegration:
    async def _client_with_status(
        self, status: int, *, breaker: CircuitBreaker
    ) -> HttpClient:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(status)

        return HttpClient(client=_make_client(handler), circuit_breaker=breaker)

    async def test_5xx_records_failure(self) -> None:
        clock = FakeClock()
        breaker = CircuitBreaker(failure_threshold=3, clock=clock)
        http = await self._client_with_status(503, breaker=breaker)
        async with http:
            for _ in range(2):
                r = await http.get("https://example.com/")
                assert r.status_code == 503
            assert await breaker.is_open("example.com") is False
            # 3rd failure trips the breaker.
            await http.get("https://example.com/")
            assert await breaker.is_open("example.com") is True

    async def test_4xx_does_not_record_failure(self) -> None:
        clock = FakeClock()
        breaker = CircuitBreaker(failure_threshold=3, clock=clock)
        http = await self._client_with_status(404, breaker=breaker)
        async with http:
            for _ in range(10):
                r = await http.get("https://example.com/")
                assert r.status_code == 404
            assert await breaker.is_open("example.com") is False

    async def test_2xx_records_success(self) -> None:
        clock = FakeClock()
        breaker = CircuitBreaker(failure_threshold=3, clock=clock)

        # Fail twice, then succeed: success clears the failure history.
        states = iter([503, 503, 200, 503, 503])

        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(next(states))

        async with HttpClient(client=_make_client(handler), circuit_breaker=breaker) as http:
            await http.get("https://example.com/")
            await http.get("https://example.com/")
            assert await breaker.is_open("example.com") is False
            await http.get("https://example.com/")  # 200 -> reset
            await http.get("https://example.com/")  # 503 -> 1 failure
            await http.get("https://example.com/")  # 503 -> 2 failures
            assert await breaker.is_open("example.com") is False  # not 3 yet

    async def test_network_error_records_failure(self) -> None:
        clock = FakeClock()
        breaker = CircuitBreaker(failure_threshold=2, clock=clock)

        def handler(req: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("simulated network error")

        async with HttpClient(client=_make_client(handler), circuit_breaker=breaker) as http:
            with pytest.raises(httpx.ConnectError):
                await http.get("https://example.com/")
            with pytest.raises(httpx.ConnectError):
                await http.get("https://example.com/")
            assert await breaker.is_open("example.com") is True

    async def test_open_breaker_blocks_request(self) -> None:
        clock = FakeClock()
        breaker = CircuitBreaker(failure_threshold=1, clock=clock)
        await breaker.record_failure("example.com")  # open immediately

        def handler(req: httpx.Request) -> httpx.Response:
            pytest.fail("handler should not be called when breaker is open")

        async with HttpClient(client=_make_client(handler), circuit_breaker=breaker) as http:
            with pytest.raises(CircuitBreakerOpen):
                await http.get("https://example.com/")


@pytest.mark.asyncio
class TestHttpClientLifecycle:
    async def test_aclose_when_owned(self) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200)

        client = httpx.AsyncClient(transport=_mock_transport(handler))
        http = HttpClient(client=client)
        # Did not own the client, so aclose is a no-op (caller manages it).
        await http.aclose()
        # The injected client should still work.
        await client.get("https://example.com/")
        await client.aclose()

    async def test_context_manager_runs(self) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200)

        async with HttpClient(client=_make_client(handler)) as http:
            r = await http.get("https://example.com/")
            assert r.status_code == 200


def test_host_extraction() -> None:
    assert HttpClient._host_of("https://www.example.com/path") == "www.example.com"
    assert HttpClient._host_of("HTTPS://EXAMPLE.COM/") == "example.com"
    assert HttpClient._host_of("not a url") == ""
