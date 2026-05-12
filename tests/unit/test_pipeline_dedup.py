"""Tests for `pipeline.dedup.dedup_items`.

The motivating case is the 2026-05-11 run, where OptimizeRx's programmatic-
EHR launch surfaced twice (yahoo.com + stocktitan.net) and produced two
Sev-4 findings for the same underlying event.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from pipeline.dedup import dedup_items
from schema.raw_item import RawItem
from schema.source import CollectionMethod, SourceType


def _item(
    *,
    url: str,
    title: str,
    competitor: str = "optimizerx",
    canonical_url: str | None = None,
    published_at: datetime | None = None,
    summary: str = "Some summary",
) -> RawItem:
    return RawItem(
        url=url,
        canonical_url=canonical_url,
        title=title,
        summary=summary,
        competitor=competitor,
        source_type=SourceType.NEWSROOM,
        collection_method=CollectionMethod.RSS,
        published_at=published_at,
    )


_BASE_TIME = datetime(2026, 5, 11, 12, 0, 0, tzinfo=timezone.utc)


class TestDedupItems:
    def test_empty_list_returns_empty(self) -> None:
        assert dedup_items([]) == []

    def test_single_item_passes_through(self) -> None:
        item = _item(
            url="https://example.com/a", title="OptimizeRx launches X",
            published_at=_BASE_TIME,
        )
        assert dedup_items([item]) == [item]

    def test_identical_canonical_url_collapses(self) -> None:
        """Two items pointing at the same publisher article URL are the
        same event regardless of title wording."""
        a = _item(
            url="https://news.google.com/rss/articles/AAA",
            canonical_url="https://prnewswire.com/optimizerx-launch",
            title="OptimizeRx Launches Programmatic Access",
            published_at=_BASE_TIME,
        )
        b = _item(
            url="https://news.google.com/rss/articles/BBB",
            canonical_url="https://prnewswire.com/optimizerx-launch",
            title="OptimizeRx Programmatic Launch Hits Market",
            published_at=_BASE_TIME + timedelta(hours=2),
        )
        out = dedup_items([a, b])
        assert len(out) == 1
        # Earlier-published item wins.
        assert out[0].published_at == _BASE_TIME

    def test_different_competitors_never_collapse(self) -> None:
        """Same headline, different competitor → both kept. This guards
        against `OptimizeRx partners with DeepIntent` collapsing two distinct
        feeds covering the same event from their own angles."""
        a = _item(
            url="https://example.com/a",
            title="Programmatic launch in EHR scale",
            competitor="optimizerx",
            published_at=_BASE_TIME,
        )
        b = _item(
            url="https://example.com/b",
            title="Programmatic launch in EHR scale",
            competitor="deepintent",
            published_at=_BASE_TIME + timedelta(hours=1),
        )
        out = dedup_items([a, b])
        assert len(out) == 2

    def test_same_competitor_high_jaccard_within_window_collapses(self) -> None:
        """Two outlets reporting the same event in different words but
        with substantial token overlap collapse to one."""
        a = _item(
            url="https://example.com/a",
            title="OptimizeRx launches programmatic EHR advertising for HCPs",
            published_at=_BASE_TIME,
        )
        b = _item(
            url="https://example.com/b",
            title="Programmatic EHR advertising launch announced for OptimizeRx HCPs",
            published_at=_BASE_TIME + timedelta(hours=6),
        )
        out = dedup_items([a, b])
        assert len(out) == 1

    def test_same_competitor_distinct_events_kept(self) -> None:
        """Two genuinely different stories about the same competitor must
        not collapse. Q3 earnings ≠ product launch."""
        a = _item(
            url="https://example.com/a",
            title="OptimizeRx reports Q3 revenue beat",
            published_at=_BASE_TIME,
        )
        b = _item(
            url="https://example.com/b",
            title="OptimizeRx hires new CMO from Veeva",
            published_at=_BASE_TIME + timedelta(hours=2),
        )
        out = dedup_items([a, b])
        assert len(out) == 2

    def test_outside_window_not_collapsed(self) -> None:
        """Items more than 72h apart are different events even if titles
        share tokens. Two product-launch posts on same theme but a week
        apart aren't a duplicate."""
        a = _item(
            url="https://example.com/a",
            title="OptimizeRx launches programmatic EHR advertising",
            published_at=_BASE_TIME,
        )
        b = _item(
            url="https://example.com/b",
            title="OptimizeRx launches programmatic EHR advertising",
            published_at=_BASE_TIME + timedelta(days=10),
        )
        out = dedup_items([a, b])
        assert len(out) == 2

    def test_three_way_cluster_collapses_to_one(self) -> None:
        a = _item(
            url="https://example.com/a",
            title="OptimizeRx programmatic launch announcement HCP",
            published_at=_BASE_TIME,
        )
        b = _item(
            url="https://example.com/b",
            title="OptimizeRx HCP programmatic launch announcement coverage",
            published_at=_BASE_TIME + timedelta(hours=2),
        )
        c = _item(
            url="https://example.com/c",
            title="HCP programmatic announcement launch by OptimizeRx",
            published_at=_BASE_TIME + timedelta(hours=4),
        )
        out = dedup_items([a, b, c])
        assert len(out) == 1
        assert out[0].url == a.url

    def test_undated_pair_not_collapsed_by_title_alone(self) -> None:
        """Without published_at on both items, title-only similarity is not
        sufficient — we can't tell if it's same day or 3 months apart."""
        a = _item(
            url="https://example.com/a",
            title="OptimizeRx launches programmatic EHR advertising HCP",
            published_at=None,
        )
        b = _item(
            url="https://example.com/b",
            title="OptimizeRx launches programmatic EHR advertising HCP",
            published_at=None,
        )
        out = dedup_items([a, b])
        assert len(out) == 2

    def test_undated_collapses_via_canonical_url(self) -> None:
        """Undated items WITH a matching canonical_url still collapse —
        the URL is the strong signal, no need for time-window check."""
        a = _item(
            url="https://news.google.com/rss/AAA",
            canonical_url="https://prnewswire.com/optimizerx-launch",
            title="OptimizeRx launches programmatic",
            published_at=None,
        )
        b = _item(
            url="https://news.google.com/rss/BBB",
            canonical_url="https://prnewswire.com/optimizerx-launch",
            title="Outlet B headline for OptimizeRx",
            published_at=None,
        )
        out = dedup_items([a, b])
        assert len(out) == 1

    def test_keeps_unique_items_alongside_dedup(self) -> None:
        """In a mixed list, only the duplicate cluster collapses; unrelated
        items are preserved."""
        a = _item(
            url="https://example.com/a",
            title="OptimizeRx programmatic EHR launch HCP",
            published_at=_BASE_TIME,
        )
        b = _item(
            url="https://example.com/b",
            title="Programmatic EHR launch for OptimizeRx HCP",
            published_at=_BASE_TIME + timedelta(hours=1),
        )
        c = _item(
            url="https://example.com/c",
            title="Veradigm signs new health system",
            competitor="veradigm",
            published_at=_BASE_TIME,
        )
        out = dedup_items([a, b, c])
        assert len(out) == 2
        # OptimizeRx pair collapsed to one; Veradigm preserved.
        assert {i.competitor for i in out} == {"optimizerx", "veradigm"}
