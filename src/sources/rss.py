"""RSS source ingester (T1 sub-stage).

Fetches an RSS / Atom feed via the shared `HttpClient` (so it benefits from
the per-host circuit breaker and HTTP/2), then parses with `feedparser` which
tolerates malformed feeds. Returns a list of `RawItem` instances ready for
the filter stage.

This module is deliberately stateless — the runner passes in the http client
and the competitor / source-type metadata; the ingester just produces items.

Master-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 6.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser
import httpx

from clients.http import CircuitBreakerOpen, HttpClient
from schema.raw_item import RawItem
from schema.source import CollectionMethod, SourceType

logger = logging.getLogger(__name__)


def _coerce_published(entry: feedparser.FeedParserDict) -> datetime | None:
    """Best-effort published-at extraction from a feedparser entry."""
    # feedparser builds `published_parsed` (struct_time) for most feeds.
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed is not None:
        try:
            return datetime(*parsed[:6], tzinfo=timezone.utc)
        except (TypeError, ValueError):
            pass
    # Fallback: parse the raw string with email.utils (handles RFC 2822).
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
    """Cheap inline HTML strip for the summary preview.

    Real HTML cleaning happens in extract; here we just want a readable
    string for the filter prompt and for logging.
    """
    if not s or "<" not in s:
        return s
    # selectolax is overkill for inline summaries; a regex-free strip works.
    import re

    return re.sub(r"<[^>]+>", " ", s).strip()


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
        summary = _strip_html(entry.get("summary") or entry.get("description") or "")

        try:
            item = RawItem(
                url=link,
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
