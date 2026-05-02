"""T3 extract stage: Flash converts a kept item into a structured Finding.

The LLM emits a `FindingDraft` (the fields it can know from the item alone).
We then promote the draft into a full `Finding` by adding pipeline metadata:
finding_id (deterministic hash from the RawItem), source_type and
collection_method (from ingest), competitor (from ingest), captured_at (now),
status (DRAFT). T4 fills the verification flags and final scores.

Sprint 8 additions:
- Forwards `canonical_url` and `publisher_domain` from RawItem onto Finding
  so the renderer can display the publisher domain instead of an opaque
  Google News redirect URL.
- Looks up the competitor's market `category` from competitors.yaml via
  `util.competitor_registry` and stamps it on the Finding for digest grouping.
- Populates `extraction_confidence` from the LLM's `raw_confidence` so
  downstream stages can read the decomposed-confidence path uniformly.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

from clients.gemini import GeminiClient
from schema.finding import Finding, FindingStatus
from schema.finding_draft import FindingDraft
from schema.raw_item import RawItem
from util.competitor_registry import get_category, get_related_products

logger = logging.getLogger(__name__)


_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"
_EXTRACT_PROMPT_PATH = _PROMPTS_DIR / "extract.txt"
if not _EXTRACT_PROMPT_PATH.exists():  # pragma: no cover - covered by integration
    raise RuntimeError(f"extract.txt prompt missing: {_EXTRACT_PROMPT_PATH}")
_EXTRACT_PROMPT_TEMPLATE = _EXTRACT_PROMPT_PATH.read_text(encoding="utf-8")


def _format_prompt(item: RawItem) -> str:
    return _EXTRACT_PROMPT_TEMPLATE.format(
        url=str(item.url),
        competitor=item.competitor,
        title=item.title,
        summary=item.summary or "(no summary)",
    )


def _resolve_products(item: RawItem, draft: FindingDraft) -> list[str]:
    """Return the products[] list for the Finding.

    The Flash extract LLM is conservative and frequently returns an empty
    list even when the article clearly belongs to a known Doceree-product
    competitive bucket. When that happens, we backfill from the competitor's
    `related_doceree_products` in competitors.yaml. This keeps:
      - the BY DOCEREE PRODUCT digest section populated;
      - synth_per_product paragraphs running for the right products;
      - the severity-adversarial prompt grounded in which Doceree products
        are actually exposed (Pro's reasoning quality depends on this).

    If the LLM returned products explicitly, trust it (it had the article
    text in context; we don't). Only backfill on empty.
    """
    if draft.products:
        return draft.products
    related = get_related_products(item.competitor)
    # Cap at 3 to match the extract prompt's "0-3 entries" rule and to
    # avoid one finding flooding the BY-PRODUCT section.
    return related[:3]


def _build_finding(item: RawItem, draft: FindingDraft) -> Finding:
    """Promote a (RawItem, FindingDraft) into a full Finding."""
    finding_id = item.content_hash[:32]  # 32 hex chars = 128 bits
    return Finding(
        finding_id=finding_id,
        url=item.url,
        canonical_url=item.canonical_url,
        publisher_domain=item.publisher_domain,
        source_type=item.source_type,
        collection_method=item.collection_method,
        competitor=item.competitor,
        category=get_category(item.competitor),
        title=draft.title,
        summary=draft.summary,
        evidence_quote=draft.evidence_quote,
        signal_type=draft.signal_type,
        products=_resolve_products(item, draft),
        raw_severity=draft.raw_severity,
        raw_confidence=draft.raw_confidence,
        # Mirror raw_confidence into the decomposed `extraction_confidence`
        # so render and adversarial stages can treat it uniformly. Stages
        # 4a/4b will fill the other two confidence dimensions.
        extraction_confidence=draft.raw_confidence,
        status=FindingStatus.DRAFT,
        captured_at=datetime.now(timezone.utc),
        published_at=item.published_at,
    )


async def extract_finding(item: RawItem, *, gemini: GeminiClient) -> Finding | None:
    """Extract a single Finding from a RawItem.

    Returns None on extraction error (LLM returned malformed JSON or the
    promotion to Finding failed pydantic validation). The caller should
    log + drop None values rather than fail the run.
    """
    prompt = _format_prompt(item)
    try:
        draft = await gemini.extract(prompt, response_schema=FindingDraft)
    except Exception as exc:
        logger.warning("extract call failed for %s: %s", item.url, exc)
        return None
    if not isinstance(draft, FindingDraft):
        logger.warning("extract returned non-FindingDraft for %s: %r", item.url, draft)
        return None
    try:
        return _build_finding(item, draft)
    except Exception as exc:
        logger.warning("extract -> Finding promotion failed for %s: %s", item.url, exc)
        return None


async def extract_findings(
    items: list[RawItem], *, gemini: GeminiClient
) -> list[Finding]:
    """Extract Findings from a batch of RawItems. Skips ones that fail."""
    out: list[Finding] = []
    for item in items:
        finding = await extract_finding(item, gemini=gemini)
        if finding is not None:
            out.append(finding)
    return out
