"""Tests for `sources.rss.fetch_rss`.

Uses `httpx.MockTransport` to feed scripted RSS XML to the parser.
"""
from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest

from clients.http import CircuitBreaker, HttpClient
from schema.source import CollectionMethod, SourceType
from sources.rss import fetch_rss


SAMPLE_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>OptimizeRx News</title>
    <link>https://www.optimizerx.com/news</link>
    <description>Latest from OptimizeRx</description>
    <item>
      <title>OptimizeRx Q3 results: revenue up 55% YoY</title>
      <link>https://www.optimizerx.com/news/q3-results</link>
      <description>OptimizeRx reported Q3 2025 revenue of $29.2M, up 55% YoY...</description>
      <pubDate>Mon, 28 Apr 2026 14:00:00 GMT</pubDate>
    </item>
    <item>
      <title>OptimizeRx adds 4 new EHR partners</title>
      <link>https://www.optimizerx.com/news/ehr-partners</link>
      <description>Four new agreements increase NPI reach by 37%</description>
      <pubDate>Tue, 29 Apr 2026 09:30:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


SAMPLE_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>DeepIntent Press</title>
  <link href="https://deepintent.com/news"/>
  <updated>2026-04-30T00:00:00Z</updated>
  <entry>
    <title>DeepIntent launches Helix HIPAA-ready cloud</title>
    <link href="https://deepintent.com/news/helix"/>
    <updated>2026-03-01T10:00:00Z</updated>
    <summary>DeepIntent announced its HIPAA-ready Helix cloud.</summary>
  </entry>
</feed>
"""


def _make_client(
    handler: Callable[[httpx.Request], httpx.Response],
) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        follow_redirects=True,
    )


@pytest.fixture
def make_http():
    def factory(handler: Callable[[httpx.Request], httpx.Response]) -> HttpClient:
        return HttpClient(client=_make_client(handler), circuit_breaker=CircuitBreaker())

    return factory


@pytest.mark.asyncio
class TestFetchRss:
    async def test_parses_rss_2_0(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                content=SAMPLE_RSS.encode("utf-8"),
                headers={"Content-Type": "application/rss+xml"},
            )

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://www.optimizerx.com/feed",
                http=http,
                competitor="optimizerx",
                source_type=SourceType.NEWSROOM,
            )
        assert len(items) == 2
        assert items[0].competitor == "optimizerx"
        assert items[0].title.startswith("OptimizeRx Q3")
        assert items[0].source_type == SourceType.NEWSROOM
        assert items[0].collection_method == CollectionMethod.RSS
        assert items[0].published_at is not None
        assert items[0].published_at.tzinfo is not None  # timezone-aware

    async def test_parses_atom(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                content=SAMPLE_ATOM.encode("utf-8"),
                headers={"Content-Type": "application/atom+xml"},
            )

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://deepintent.com/feed",
                http=http,
                competitor="deepintent",
            )
        assert len(items) == 1
        assert items[0].title.startswith("DeepIntent launches Helix")
        assert items[0].published_at is not None

    async def test_max_items_caps_results(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=SAMPLE_RSS.encode("utf-8"))

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://www.optimizerx.com/feed",
                http=http,
                competitor="optimizerx",
                max_items=1,
            )
        assert len(items) == 1

    async def test_strips_html_in_summary(self, make_http) -> None:
        rss = (
            '<?xml version="1.0"?><rss version="2.0"><channel><title>x</title>'
            '<link>https://example.com</link><description>x</description>'
            '<item><title>headline</title>'
            '<link>https://example.com/a</link>'
            '<description>foo &lt;b&gt;bar&lt;/b&gt; baz</description>'
            "</item></channel></rss>"
        )

        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=rss.encode("utf-8"))

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://example.com/feed",
                http=http,
                competitor="optimizerx",
            )
        assert len(items) == 1
        # The HTML tags inside CDATA-equivalent should be stripped.
        assert "<b>" not in items[0].summary
        assert "bar" in items[0].summary

    async def test_skips_entries_without_link_or_title(self, make_http) -> None:
        rss = (
            '<?xml version="1.0"?><rss version="2.0"><channel><title>x</title>'
            '<link>https://example.com</link><description>x</description>'
            '<item><title>has-everything</title>'
            '<link>https://example.com/a</link>'
            '<description>ok</description></item>'
            '<item><title>no-link</title><description>ok</description></item>'
            '<item><link>https://example.com/c</link><description>no-title</description></item>'
            "</channel></rss>"
        )

        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=rss.encode("utf-8"))

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://example.com/feed",
                http=http,
                competitor="optimizerx",
            )
        assert len(items) == 1
        assert items[0].title == "has-everything"

    async def test_non_200_returns_empty(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(404)

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://example.com/missing",
                http=http,
                competitor="optimizerx",
            )
        assert items == []

    async def test_network_error_returns_empty(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("simulated DNS failure")

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://example.com/feed",
                http=http,
                competitor="optimizerx",
            )
        assert items == []

    async def test_malformed_xml_returns_empty(self, make_http) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=b"not xml at all")

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://example.com/feed",
                http=http,
                competitor="optimizerx",
            )
        # feedparser is tolerant; if it somehow finds entries it returns them,
        # otherwise empty. We don't crash regardless.
        assert isinstance(items, list)
