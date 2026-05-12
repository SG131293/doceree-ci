"""Same-event deduplication (between T4a attribution and T3 extract).

When Google News syndicates the same event across multiple outlets we get
N copies of essentially the same story with different headlines. The
2026-05-11 run, for example, produced two findings for OptimizeRx's
programmatic-EHR launch — one from yahoo.com and one from stocktitan.net.
Both were correctly attributed, both passed filter, and both survived
extract / adversarial. The digest then showed them as two separate Sev-4
events when they were actually one underlying announcement.

This module collapses such duplicates BEFORE T3 extract, so:
  - we pay extract / adversarial cost for each unique event once, not N times
  - per-product synth and strategic synth see one consolidated finding
  - the digest's `n findings` count reflects events, not wire copies

Two collapse signals:
  1. `canonical_url` exact match (when both items have non-None
     canonical_url not pointing at Google News). This catches direct
     re-syndications where the underlying publisher article URL is
     the same.
  2. Same competitor + title-token Jaccard >= 0.30 + published_at
     within 72 hours. This catches the more common case where the
     same wire story is rewritten by multiple outlets.

The retained item per cluster is the one with the EARLIEST `published_at`
(proxy for "original source"); ties are broken by item index for
determinism. Items lacking `published_at` are sorted last.

Known limitations (v1):
- True news rewrites with disjoint vocabulary (different verbs / nouns
  describing the same event — e.g. "Launches X" vs "Y enables Z") will
  NOT be caught by simple token Jaccard. Catching those would need
  LLM clustering or semantic embeddings. v1 ships the cheap heuristic;
  we accept some false-negatives and revisit if syndication noise stays
  high.
- Cross-competitor "same event" cases (e.g., a partnership announcement
  posted from both companies' angles) are NOT collapsed — by design;
  the renderer groups by competitor and we want both perspectives
  if both feeds surfaced it.
"""
from __future__ import annotations

import logging
import re
from datetime import timedelta

from schema.raw_item import RawItem

logger = logging.getLogger(__name__)


# Lightweight English stopword set — just the function words and copulas that
# add no semantic signal to a news headline. Deliberately small; the goal is
# not perfect NLP, just to stop "to", "the", "of" from inflating Jaccard.
_STOPWORDS: frozenset[str] = frozenset({
    "the", "a", "an", "and", "or", "but", "for", "to", "of", "in", "on",
    "at", "by", "with", "from", "is", "are", "was", "were", "be", "as",
    "this", "that", "these", "those", "it", "its", "their", "they",
    "have", "has", "had", "will", "would", "can", "could", "should",
    "via", "into", "onto", "upon", "over", "under", "after", "before",
    "new", "amid", "amidst", "while", "during",
})

_TOKEN_PATTERN = re.compile(r"[a-z0-9]+")

# Window inside which two items from the same competitor can be considered
# the same event. 72h gives a buffer for slow re-syndicators while still
# preventing collapse across unrelated weekly news cycles.
_SAME_EVENT_WINDOW = timedelta(hours=72)

# Title-token Jaccard threshold for same-event matching. 0.30 is empirically
# permissive enough to catch standard wire re-syndications (where outlets
# share most nouns) while staying strict enough that two distinct events
# about the same competitor don't accidentally collapse.
_TITLE_JACCARD_THRESHOLD = 0.30


def _normalize_tokens(text: str, drop_tokens: frozenset[str]) -> frozenset[str]:
    """Lowercased, stopword-filtered, length>=3 token set for similarity.

    `drop_tokens` is used to remove the competitor name from the token set;
    otherwise every title would share the competitor token and Jaccard
    would be inflated.
    """
    raw = _TOKEN_PATTERN.findall(text.lower())
    return frozenset(
        t for t in raw
        if len(t) >= 3 and t not in _STOPWORDS and t not in drop_tokens
    )


def _title_jaccard(
    title_a: str, title_b: str, competitor: str,
) -> float:
    drop = frozenset(_TOKEN_PATTERN.findall(competitor.lower()))
    a = _normalize_tokens(title_a, drop)
    b = _normalize_tokens(title_b, drop)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _published_within_window(a: RawItem, b: RawItem) -> bool:
    """True if both items have published_at and they are within
    `_SAME_EVENT_WINDOW` of each other.

    Items lacking published_at return False here — we don't speculatively
    collapse them via title alone, because the freshness gate upstream
    already kept them and they may well be different days' news.
    """
    if a.published_at is None or b.published_at is None:
        return False
    return abs(a.published_at - b.published_at) <= _SAME_EVENT_WINDOW


def _is_same_event(a: RawItem, b: RawItem) -> bool:
    """Pairwise same-event predicate.

    Order of cheap-to-expensive checks:
      1. Different competitor → False
      2. Same canonical_url (non-None on both) → True
      3. Title Jaccard >= threshold AND within 72h pubdate window → True
      4. Otherwise False
    """
    if a.competitor != b.competitor:
        return False
    if (
        a.canonical_url is not None
        and b.canonical_url is not None
        and str(a.canonical_url) == str(b.canonical_url)
    ):
        return True
    if not _published_within_window(a, b):
        return False
    jaccard = _title_jaccard(a.title, b.title, a.competitor)
    return jaccard >= _TITLE_JACCARD_THRESHOLD


def _sort_key(item: RawItem) -> tuple[int, float]:
    """Sort key for picking the cluster representative.

    Earliest published_at wins (proxy for original source). Items with no
    published_at sort last. Tie-broken by length so the shortest title
    (typically the headline form, not the SEO-bloated rewrite) wins.
    """
    has_date = 0 if item.published_at is not None else 1
    timestamp = item.published_at.timestamp() if item.published_at else float("inf")
    return (has_date, timestamp, len(item.title))


def dedup_items(items: list[RawItem]) -> list[RawItem]:
    """Collapse same-event RawItems to one representative per cluster.

    Pure function — no I/O, deterministic given input order. Designed to
    be called between T4a (attribution) and T3 (extract) so extract pays
    once per unique event.

    Algorithm:
      1. Sort items by `_sort_key` (earliest-published first) so the cluster
         representative is deterministic.
      2. For each item, check against the already-kept representatives; if
         it matches one via `_is_same_event`, drop it (record at INFO log).
      3. Otherwise add it as a new representative.

    Complexity: O(n^2) on pairwise comparisons. Fine for daily runs at
    O(50) items; revisit if we ever ingest at scale per call.
    """
    if not items:
        return []
    # Stable, deterministic ordering by sort key.
    sorted_items = sorted(enumerate(items), key=lambda pair: _sort_key(pair[1]))

    kept: list[RawItem] = []
    n_dropped = 0
    for _orig_idx, item in sorted_items:
        match = next((k for k in kept if _is_same_event(item, k)), None)
        if match is not None:
            n_dropped += 1
            logger.info(
                "Dedup: dropping %r as same-event-as %r (competitor=%s)",
                item.title, match.title, item.competitor,
            )
            continue
        kept.append(item)

    if n_dropped:
        logger.info(
            "Dedup collapsed %d duplicate event(s) from %d items -> %d unique",
            n_dropped, len(items), len(kept),
        )
    return kept
