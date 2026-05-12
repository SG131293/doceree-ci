"""Coverage guard: every competitor declared in config/competitors.yaml MUST
have at least one ingest feed in `runners.run_daily.DAY6_FEEDS`.

Sherry's requirement (2026-05-12): "If there is any news, I should know
about it without fail." Means we cannot ever ship a competitor in the
registry that has no monitoring path. This test fires on the first run of
any PR that violates the invariant — preventing the 10-competitor blind
spot we shipped through 2026-05-11 (the entire ai-scribe cluster was in
YAML but had no feed entries).
"""
from __future__ import annotations

import re
from pathlib import Path

from runners.run_daily import DAY6_FEEDS

_YAML_PATH = Path(__file__).resolve().parents[2] / "config" / "competitors.yaml"
_ID_PATTERN = re.compile(r"^\s*-\s*id:\s*(\S+)", re.MULTILINE)


def _yaml_competitor_ids() -> set[str]:
    """Parse competitors.yaml via regex (no PyYAML dep needed here).

    Looks for any `  - id: <slug>` line, which is the canonical way every
    competitor entry starts regardless of which tier section it lives in.
    """
    text = _YAML_PATH.read_text(encoding="utf-8")
    return set(_ID_PATTERN.findall(text))


def test_every_yaml_competitor_has_a_feed() -> None:
    yaml_ids = _yaml_competitor_ids()
    feed_ids = {feed.competitor for feed in DAY6_FEEDS}
    missing = yaml_ids - feed_ids
    assert not missing, (
        f"Competitors in competitors.yaml have no feed in DAY6_FEEDS: "
        f"{sorted(missing)}. Add a CompetitorFeed entry per competitor — "
        "Sherry's coverage requirement is zero blind spots."
    )


def test_every_feed_resolves_to_a_yaml_competitor() -> None:
    """Inverse direction: no feed should reference a competitor that does
    not exist in the registry. Catches typos in the `competitor=` field."""
    yaml_ids = _yaml_competitor_ids()
    feed_ids = {feed.competitor for feed in DAY6_FEEDS}
    orphans = feed_ids - yaml_ids
    assert not orphans, (
        f"DAY6_FEEDS references competitors not in competitors.yaml: "
        f"{sorted(orphans)}. Either add the competitor to YAML or fix the typo."
    )


def test_feed_urls_are_well_formed() -> None:
    """Sanity: every feed_url is an HTTPS Google News RSS URL with a query."""
    for feed in DAY6_FEEDS:
        assert feed.feed_url.startswith("https://news.google.com/rss/search?q="), (
            f"Feed for {feed.competitor} ({feed.name}) has an unexpected URL: "
            f"{feed.feed_url}"
        )
        assert "when:" in feed.feed_url, (
            f"Feed for {feed.competitor} ({feed.name}) is missing a `when:` "
            "time-window constraint — would pull years of archive."
        )
