"""T3 extract stage: Flash converts a kept item into a structured Finding.

The LLM emits a `FindingDraft` (the fields it can know from the item alone).
We then promote the draft into a full `Finding` by adding pipeline metadata:
finding_id (deterministic hash from the RawItem), source_type and
collection_method (from ingest), competitor (from ingest), captured_at (now),
status (DRAFT). T4 fills the verification flags and final scores.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

from clients.gemini import GeminiClient
from schema.finding import Finding, FindingStatus
from schema.finding_draft import FindingDraft
from schema.raw_item import RawItem

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


def _build_finding(item: RawItem, draft: FindingDraft) -> Finding:
    """Promote a (RawItem, FindingDraft) into a full Finding."""
    finding_id = item.content_hash[:32]  # 32 hex chars = 128 bits
    return Finding(
        finding_id=finding_id,
        url=item.url,
        source_type=item.source_type,
        collection_method=item.collection_method,
        competitor=item.competitor,
        title=draft.title,
        summary=draft.summary,
        evidence_quote=draft.evidence_quote,
        signal_type=draft.signal_type,
        products=draft.products,
        raw_severity=draft.raw_severity,
        raw_confidence=draft.raw_confidence,
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
