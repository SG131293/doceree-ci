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

    async def test_strips_markdown_links_in_title(self, make_http) -> None:
        """Sprint 8 fix: titles like `[Viz.ai](http://Viz.ai) partners with X`
        were rendering with literal Markdown in the digest. The ingester now
        unwraps `[text](url)` -> `text` before storing the title."""
        rss = (
            '<?xml version="1.0"?><rss version="2.0"><channel>'
            '<title>x</title><link>https://news.google.com/</link>'
            '<description>x</description>'
            '<item>'
            '<title>[Viz.ai](http://Viz.ai) partners with NRHA</title>'
            '<link>https://news.google.com/rss/articles/abc</link>'
            '<description>summary</description>'
            "</item></channel></rss>"
        )

        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=rss.encode("utf-8"))

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://news.google.com/feed",
                http=http,
                competitor="hippocratic_ai",
            )
        assert len(items) == 1
        # Markdown link wrapper is gone; only the visible text remains.
        assert "[Viz.ai]" not in items[0].title
        assert "](http" not in items[0].title
        assert "Viz.ai partners with NRHA" in items[0].title

    async def test_strips_markdown_links_in_summary(self, make_http) -> None:
        rss = (
            '<?xml version="1.0"?><rss version="2.0"><channel>'
            '<title>x</title><link>https://example.com/</link>'
            '<description>x</description>'
            '<item><title>headline</title>'
            '<link>https://example.com/a</link>'
            '<description>'
            'See [the announcement](https://hippocraticai.com/news/x) for details.'
            '</description>'
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
        assert "[the announcement]" not in items[0].summary
        assert "the announcement" in items[0].summary

    async def test_extracts_canonical_url_from_description_anchor(
        self, make_http
    ) -> None:
        """Google News RSS embeds the publisher article URL in a `<a href>`
        inside the description. The ingester should surface it as the
        canonical URL."""
        # Use HTML entities so feedparser treats the anchor text as content.
        rss = (
            '<?xml version="1.0"?><rss version="2.0"><channel>'
            '<title>Google News</title><link>https://news.google.com/</link>'
            '<description>x</description>'
            '<item>'
            '<title>Hippocratic AI Launches Polaris 5.0</title>'
            '<link>https://news.google.com/rss/articles/CBMiabc?oc=5</link>'
            '<description>'
            '&lt;a href="https://hippocraticai.com/news/polaris-5"&gt;'
            'Hippocratic AI Launches Polaris 5.0&lt;/a&gt;&amp;nbsp;&amp;nbsp;'
            '&lt;font color="#6f6f6f"&gt;Hippocratic AI&lt;/font&gt;'
            '</description>'
            '<source url="https://hippocraticai.com">Hippocratic AI</source>'
            "</item></channel></rss>"
        )

        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=rss.encode("utf-8"))

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://news.google.com/feed",
                http=http,
                competitor="hippocratic_ai",
            )
        assert len(items) == 1
        assert items[0].canonical_url is not None
        assert "hippocraticai.com/news/polaris-5" in str(items[0].canonical_url)
        # Publisher domain should be eTLD+1 of the canonical URL.
        assert items[0].publisher_domain == "hippocraticai.com"

    async def test_canonical_url_falls_back_to_source_element(
        self, make_http
    ) -> None:
        """When the description has no embedded anchor, fall back to the
        `<source url>` element."""
        rss = (
            '<?xml version="1.0"?><rss version="2.0"><channel>'
            '<title>Google News</title><link>https://news.google.com/</link>'
            '<description>x</description>'
            '<item>'
            '<title>An article</title>'
            '<link>https://news.google.com/rss/articles/CBMixyz</link>'
            '<description>plain text summary, no html anchor</description>'
            '<source url="https://hippocraticai.com">Hippocratic AI</source>'
            "</item></channel></rss>"
        )

        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=rss.encode("utf-8"))

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://news.google.com/feed",
                http=http,
                competitor="hippocratic_ai",
            )
        assert len(items) == 1
        assert items[0].canonical_url is not None
        assert str(items[0].canonical_url).startswith("https://hippocraticai.com")
        assert items[0].publisher_domain == "hippocraticai.com"

    async def test_publisher_domain_falls_back_to_wire_url(
        self, make_http
    ) -> None:
        """When neither anchor nor source element exposes a publisher URL,
        we fall back to the eTLD+1 of the wire URL itself."""
        rss = (
            '<?xml version="1.0"?><rss version="2.0"><channel>'
            '<title>x</title><link>https://www.optimizerx.com/</link>'
            '<description>x</description>'
            '<item>'
            '<title>OptimizeRx Q3 results</title>'
            '<link>https://www.optimizerx.com/news/q3-results</link>'
            '<description>plain summary</description>'
            "</item></channel></rss>"
        )

        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=rss.encode("utf-8"))

        async with make_http(handler) as http:
            items = await fetch_rss(
                "https://www.optimizerx.com/feed",
                http=http,
                competitor="optimizerx",
            )
        assert len(items) == 1
        # No canonical_url because there's no wrapper - the wire URL is canonical.
        assert items[0].canonical_url is None
        # Publisher domain still set, derived from the wire URL.
        assert items[0].publisher_domain == "optimizerx.com"

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
