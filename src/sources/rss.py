"""RSS source ingester (T1 sub-stage).

Fetches an RSS / Atom feed via the shared `HttpClient` (so it benefits from
the per-host circuit breaker and HTTP/2), then parses with `feedparser` which
tolerates malformed feeds. Returns a list of `RawItem` instances ready for
the filter stage.

Sprint 8 additions:
- `_strip_html` now also unwraps Markdown links (`[text](url)` -> `text`)
  to fix the bleed we saw in Day-7 output where Google News emitted literal
  Markdown that was passed through to the rendered email.
- For Google News-style feeds, we look for the publisher's canonical URL in
  two places:
    1. The first `<a href>` inside the entry description (Google News
       embeds the publisher article link there).
    2. The `<source url>` element exposed by feedparser as `entry.source`.
  Whatever we find is stamped on `RawItem.canonical_url`. The eTLD+1 of
  whichever URL we ship goes onto `RawItem.publisher_domain`.

This module is deliberately stateless - the runner passes in the http client
and the competitor / source-type metadata; the ingester just produces items.

Master-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 6 + Day 8.
"""
from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser
import httpx

from clients.http import CircuitBreakerOpen, HttpClient
from schema.raw_item import RawItem
from schema.source import CollectionMethod, SourceType
from util.url_health import registered_domain

logger = logging.getLogger(__name__)


# ---- Helpers ----

# Pattern matches `[link text](https://anything)` and captures the link text.
# Must run AFTER HTML tag stripping so we don't accidentally eat genuine
# bracket/paren content inside HTML attributes.
_MD_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(\s*[^)]+\)")
# Pattern to find the first `<a href="...">` URL in a chunk of HTML. Greedy
# enough for Google News' inline anchor; we don't need to handle every edge
# case because this is a best-effort canonical-URL hint.
_FIRST_HREF_PATTERN = re.compile(r'<a[^>]+href=["\']([^"\']+)["\']', re.IGNORECASE)
_HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


def _coerce_published(entry: feedparser.FeedParserDict) -> datetime | None:
    """Best-effort published-at extraction from a feedparser entry."""
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed is not None:
        try:
            return datetime(*parsed[:6], tzinfo=timezone.utc)
        except (TypeError, ValueError):
            pass
    raw = entry.get("published") or entry.get("updated")
    if raw:
        try:
            dt = parsedate_to_datetime(raw)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except (TypeError, ValueError):
            pass
    return None


def _strip_html(s: str) -> str:
    """Cheap inline HTML strip + Markdown-link unwrap.

    Order matters: HTML first (so any inline `<a>` tags are removed), THEN
    the Markdown-link unwrap (so any `[text](url)` left behind is reduced
    to its visible text). Real HTML cleaning happens in extract; here we
    just want a readable string for the filter prompt + for logging.
    """
    if not s:
        return s
    # 1) Strip HTML tags if any are present.
    if "<" in s and ">" in s:
        s = _HTML_TAG_PATTERN.sub(" ", s)
    # 2) Unwrap Markdown link syntax if any survived.
    if "[" in s and "(" in s:
        s = _MD_LINK_PATTERN.sub(r"\1", s)
    return s.strip()


def _extract_canonical_url(entry: feedparser.FeedParserDict) -> str | None:
    """Best-effort extraction of the publisher's article URL from a feed entry.

    Google News RSS wraps real publisher links inside `<a href>` tags within
    the entry description. Other feeds may expose the same info via the
    `<source url>` element (feedparser surfaces it as `entry.source.href`).

    Returns None if we can't find a plausible canonical URL.
    """
    # 1. Try the embedded anchor in description / summary first - that's the
    #    article link, not just the publisher homepage.
    for field in ("summary", "description", "content"):
        raw = entry.get(field)
        if isinstance(raw, list) and raw:
            # feedparser sometimes nests content in `[{value: ...}]`.
            raw = raw[0].get("value", "") if isinstance(raw[0], dict) else str(raw[0])
        if not isinstance(raw, str) or not raw:
            continue
        m = _FIRST_HREF_PATTERN.search(raw)
        if m:
            href = m.group(1).strip()
            if href.startswith("http"):
                return href

    # 2. Fall back to <source url> if present. This is usually the publisher
    #    homepage, not the article URL, but it still beats news.google.com.
    source = entry.get("source")
    if isinstance(source, dict):
        href = source.get("href") or source.get("url")
        if isinstance(href, str) and href.startswith("http"):
            return href

    return None


async def fetch_rss(
    feed_url: str,
    *,
    http: HttpClient,
    competitor: str,
    source_type: SourceType = SourceType.NEWSROOM,
    max_items: int = 50,
) -> list[RawItem]:
    """Fetch and parse one RSS feed into RawItems.

    Args:
        feed_url: Absolute URL of the feed (RSS 2.0 or Atom).
        http: Shared HttpClient.
        competitor: competitor.id from competitors.yaml. Stamped onto every
                    item produced by this feed.
        source_type: SourceType enum for the items. Most RSS feeds are press
                     or newsroom; pass `SourceType.BLOG` for blog feeds, etc.
        max_items: Cap on items returned (per build plan: pre-filter cap of
                   200 / source / day; we go lower per call).

    Returns:
        A list of RawItem instances. May be empty if the feed had no items
        or if fetching / parsing failed (errors are logged, not raised, so
        the runner can continue with other feeds).
    """
    try:
        response = await http.get(feed_url)
    except CircuitBreakerOpen:
        logger.warning("RSS fetch blocked by circuit breaker: %s", feed_url)
        return []
    except (httpx.NetworkError, httpx.TimeoutException) as exc:
        logger.warning("RSS fetch failed %s: %s", feed_url, exc)
        return []

    if response.status_code != 200:
        logger.warning("RSS fetch %s -> HTTP %d", feed_url, response.status_code)
        return []

    parsed = feedparser.parse(response.content)
    if parsed.bozo and not parsed.entries:
        logger.warning(
            "RSS parse error %s: %s",
            feed_url,
            getattr(parsed, "bozo_exception", "unknown"),
        )
        return []

    items: list[RawItem] = []
    for entry in parsed.entries[:max_items]:
        link = entry.get("link") or ""
        title = entry.get("title") or ""
        if not link or not title:
            continue
        # Strip HTML/Markdown from BOTH summary AND title (Google News emits
        # publisher names as Markdown links in titles, e.g. "[Viz.ai](http://Viz.ai)
        # partners with NRHA").
        title = _strip_html(title)
        summary = _strip_html(entry.get("summary") or entry.get("description") or "")

        canonical_url = _extract_canonical_url(entry)
        # Publisher domain: prefer canonical URL; fall back to the wire URL.
        # Empty string from registered_domain becomes None on the model.
        domain_source = canonical_url or link
        publisher_domain = registered_domain(domain_source) or None

        try:
            item = RawItem(
                url=link,
                canonical_url=canonical_url,
                publisher_domain=publisher_domain,
                title=title[:1000],
                summary=summary[:5000],
                competitor=competitor,
                source_type=source_type,
                collection_method=CollectionMethod.RSS,
                published_at=_coerce_published(entry),
            )
        except Exception as exc:  # pydantic ValidationError or invalid URL
            logger.debug("Skipping RSS entry from %s: %s", feed_url, exc)
            continue
        items.append(item)

    logger.info("RSS %s: parsed %d/%d entries", feed_url, len(items), len(parsed.entries))
    return items
