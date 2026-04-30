"""T2 filter stage: Flash-Lite drops noise.

Each RawItem goes through one Gemini Flash-Lite call with the `filter.txt`
prompt. The model returns `{keep: bool, reason: str}`. Items with keep=False
are dropped; kept items proceed to T3 (extract).

This is a per-item call rather than batched. With 200 items / source / day
and Flash-Lite at 15 RPM, a single source's worth of filtering takes ~14
minutes worst-case - well within a daily budget. Day 13's eval harness will
benchmark whether batching improves throughput without sacrificing F1.
"""
from __future__ import annotations

import logging
from pathlib import Path

from clients.gemini import GeminiClient
from schema.finding_draft import FilterDecision
from schema.raw_item import RawItem

logger = logging.getLogger(__name__)


# The prompt template lives at the repo root under `prompts/filter.txt`.
# We resolve it once at import to fail fast if it's missing.
_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"
_FILTER_PROMPT_PATH = _PROMPTS_DIR / "filter.txt"
if not _FILTER_PROMPT_PATH.exists():  # pragma: no cover - covered by integration
    raise RuntimeError(f"filter.txt prompt missing: {_FILTER_PROMPT_PATH}")
_FILTER_PROMPT_TEMPLATE = _FILTER_PROMPT_PATH.read_text(encoding="utf-8")


def _format_prompt(item: RawItem) -> str:
    return _FILTER_PROMPT_TEMPLATE.format(
        competitor=item.competitor,
        title=item.title,
        summary=item.summary or "(no summary)",
        published=item.published_at.isoformat() if item.published_at else "(unknown)",
    )


async def filter_item(item: RawItem, *, gemini: GeminiClient) -> FilterDecision:
    """Run the filter prompt on a single RawItem.

    Returns a FilterDecision. On any LLM error, returns keep=True with reason
    "filter_error" so we don't drop items because of transient API issues -
    the next stage (extract) will gate them again, and we'd rather process
    a few extra items than miss a real one.
    """
    prompt = _format_prompt(item)
    try:
        decision = await gemini.filter(prompt, response_schema=FilterDecision)
    except Exception as exc:
        logger.warning("filter call failed for %s: %s", item.url, exc)
        return FilterDecision(keep=True, reason="filter_error")
    assert isinstance(decision, FilterDecision)
    logger.debug(
        "filter %s -> keep=%s reason=%s",
        item.url, decision.keep, decision.reason,
    )
    return decision


async def filter_items(
    items: list[RawItem], *, gemini: GeminiClient
) -> list[tuple[RawItem, FilterDecision]]:
    """Filter a batch of RawItems sequentially.

    Sequential rather than concurrent because the GeminiClient's RPM bucket
    serializes calls anyway; running them in parallel just queues them up
    inside the bucket without speed-up.
    """
    out: list[tuple[RawItem, FilterDecision]] = []
    for item in items:
        decision = await filter_item(item, gemini=gemini)
        out.append((item, decision))
    return out


def kept(items_with_decisions: list[tuple[RawItem, FilterDecision]]) -> list[RawItem]:
    """Return only the RawItems whose decision was keep=True."""
    return [item for item, decision in items_with_decisions if decision.keep]
