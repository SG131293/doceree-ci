"""T5 / T6 synthesis stages.

Sprint 8 introduces two synthesis passes that turn a flat list of findings
into the narrative the daily email actually wants:

    T5 synth_per_product (Pro)
        For each Doceree product impacted by today's findings, generate a
        2-3 sentence "what does this mean for product X" paragraph plus a
        one-line recommended action. Powers the "By Doceree Product"
        section of the digest.

    T6 synth_strategic (Pro)
        Single cross-product narrative covering the meta-pattern across
        all of today's findings. Powers the "Strategic Synthesis" section.

Both run AFTER the adversarial gates so the synthesis only sees verified,
correctly-attributed findings. Both use the explicit Pro-cache discount
path (cached_content) when available; for Day 8 we don't yet build the
cache (it lands when the prompt prefix stabilises in Day 11+) so we just
pay full token cost.

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 8 + Day 11.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from pathlib import Path

from clients.gemini import GeminiClient
from schema.finding import Finding
from schema.finding_draft import PerProductSynthesis, StrategicSynthesis
from util.product_registry import (
    get_confirmed_claims,
    get_name as get_product_name,
    get_one_line as get_product_one_line,
)

logger = logging.getLogger(__name__)


_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"
_SYNTH_PER_PRODUCT_PATH = _PROMPTS_DIR / "synth_per_product.txt"
_SYNTH_STRATEGIC_PATH = _PROMPTS_DIR / "synth_strategic.txt"
if not _SYNTH_PER_PRODUCT_PATH.exists():  # pragma: no cover
    raise RuntimeError(
        f"synth_per_product.txt prompt missing: {_SYNTH_PER_PRODUCT_PATH}"
    )
if not _SYNTH_STRATEGIC_PATH.exists():  # pragma: no cover
    raise RuntimeError(
        f"synth_strategic.txt prompt missing: {_SYNTH_STRATEGIC_PATH}"
    )
_SYNTH_PER_PRODUCT_TEMPLATE = _SYNTH_PER_PRODUCT_PATH.read_text(encoding="utf-8")
_SYNTH_STRATEGIC_TEMPLATE = _SYNTH_STRATEGIC_PATH.read_text(encoding="utf-8")


# ---- Helpers ----


def group_findings_by_product(
    findings: list[Finding],
) -> dict[str, list[Finding]]:
    """Index findings by impacted Doceree product.

    A finding with `products=["spark_for_ehrs", "reptwin"]` appears under
    BOTH keys. Findings with empty `products` are NOT included; they
    belong in the cross-product strategic section.

    The returned dict is sorted: products are ordered by max severity
    desc, ties broken alphabetically; findings within each list are
    sorted by effective_severity desc.
    """
    by_product: dict[str, list[Finding]] = defaultdict(list)
    for f in findings:
        for pid in f.products:
            by_product[pid].append(f)
    # Sort findings within each product by severity desc.
    for items in by_product.values():
        items.sort(key=lambda x: -x.effective_severity)
    # Sort products by max-severity desc, then alphabetically.
    sorted_pairs = sorted(
        by_product.items(),
        key=lambda kv: (
            -max((f.effective_severity for f in kv[1]), default=0),
            kv[0],
        ),
    )
    return dict(sorted_pairs)


def _format_findings_block(findings: list[Finding]) -> str:
    """Render the findings list section of the per-product synthesis prompt.

    Each finding gets a compact 4-line block: severity, title, evidence quote,
    competitor + signal_type. Pro reads this and generates the impact paragraph.
    """
    lines: list[str] = []
    for f in findings:
        lines.append(
            f"  [Sev {f.effective_severity}] {f.competitor} "
            f"({f.category or 'uncategorized'}) — {f.signal_type}\n"
            f"    Title: {f.title}\n"
            f"    Evidence: \"{f.evidence_quote}\"\n"
            f"    Summary: {f.summary}\n"
        )
    return "\n".join(lines) if lines else "  (none)"


def _format_per_product_prompt(
    product_id: str, findings: list[Finding]
) -> str:
    name = get_product_name(product_id) or product_id
    one_line = get_product_one_line(product_id) or "(no description on file)"
    claims = get_confirmed_claims(product_id) or []
    claims_block = "\n".join(f"    - {c}" for c in claims) or "    (none on file)"
    return _SYNTH_PER_PRODUCT_TEMPLATE.format(
        product_id=product_id,
        product_name=name,
        product_one_line=one_line,
        product_claims=claims_block,
        findings_block=_format_findings_block(findings),
    )


# ---- T5: synth_per_product ----


async def synth_per_product(
    product_id: str,
    findings: list[Finding],
    *,
    gemini: GeminiClient,
) -> PerProductSynthesis | None:
    """Generate the per-product impact paragraph for one product.

    Returns None on LLM error or invalid response. Callers should treat
    None as "skip this product's section in the digest" rather than failing
    the whole run.
    """
    if not findings:
        return None
    prompt = _format_per_product_prompt(product_id, findings)
    try:
        result = await gemini.synthesize(
            prompt,
            strategic=False,
            response_schema=PerProductSynthesis,
        )
    except Exception as exc:
        logger.warning("synth_per_product failed for %s: %s", product_id, exc)
        return None
    if not isinstance(result, PerProductSynthesis):
        logger.warning(
            "synth_per_product returned non-PerProductSynthesis for %s: %r",
            product_id, result,
        )
        return None
    # Normalize: the LLM occasionally echoes the wrong product_id back.
    if result.product_id != product_id:
        logger.debug(
            "synth_per_product echoed product_id=%r; overwriting with %r",
            result.product_id, product_id,
        )
        result = result.model_copy(update={"product_id": product_id})
    return result


async def synth_per_product_batch(
    findings: list[Finding],
    *,
    gemini: GeminiClient,
) -> dict[str, PerProductSynthesis]:
    """Run synth_per_product for every Doceree product touched by `findings`.

    Returns {product_id: PerProductSynthesis}. Products that couldn't be
    synthesized (LLM error, invalid response) are silently omitted.
    """
    by_product = group_findings_by_product(findings)
    out: dict[str, PerProductSynthesis] = {}
    for pid, product_findings in by_product.items():
        synth = await synth_per_product(pid, product_findings, gemini=gemini)
        if synth is not None:
            out[pid] = synth
    logger.info(
        "synth_per_product produced %d / %d product paragraphs",
        len(out), len(by_product),
    )
    return out


# ---- T6: synth_strategic ----


def _format_strategic_findings_block(findings: list[Finding]) -> str:
    """Render the findings list for the strategic-synthesis prompt.

    Compact: severity, competitor (name), category, signal, evidence quote.
    No need for full summaries — Pro should reason about the pattern, not
    re-extract content.
    """
    if not findings:
        return "  (no findings today)"
    # Local import to avoid circulars; competitor_registry already loads YAML
    # at first call.
    from util.competitor_registry import get_name as get_competitor_name

    lines: list[str] = []
    for f in findings:
        cname = get_competitor_name(f.competitor) or f.competitor
        lines.append(
            f"  [Sev {f.effective_severity}] {cname} ({f.category or 'uncategorized'}) "
            f"— {f.signal_type}: {f.title}\n"
            f"    Evidence: \"{f.evidence_quote}\""
        )
    return "\n".join(lines)


def _format_per_product_block(
    per_product: dict[str, PerProductSynthesis],
) -> str:
    """Render the per-product synthesis dict as context for the strategic
    pass. Lets Pro see the per-product paragraphs already written so the
    strategic narrative complements rather than repeats."""
    if not per_product:
        return "  (no per-product synthesis ran)"
    lines: list[str] = []
    for pid, synth in per_product.items():
        lines.append(
            f"  {pid}: {synth.impact_summary}\n"
            f"    Action: {synth.recommended_action}"
        )
    return "\n".join(lines)


def _format_strategic_prompt(
    findings: list[Finding],
    per_product: dict[str, PerProductSynthesis],
) -> str:
    return _SYNTH_STRATEGIC_TEMPLATE.format(
        findings_block=_format_strategic_findings_block(findings),
        per_product_block=_format_per_product_block(per_product),
    )


async def synth_strategic(
    findings: list[Finding],
    per_product: dict[str, PerProductSynthesis],
    *,
    gemini: GeminiClient,
) -> StrategicSynthesis | None:
    """Generate the cross-product strategic narrative.

    Returns None on LLM error, invalid response, or when there are no
    findings. The renderer should treat None as "skip the strategic section."
    """
    if not findings:
        return None
    prompt = _format_strategic_prompt(findings, per_product)
    try:
        result = await gemini.synthesize(
            prompt,
            strategic=True,
            response_schema=StrategicSynthesis,
        )
    except Exception as exc:
        logger.warning("synth_strategic failed: %s", exc)
        return None
    if not isinstance(result, StrategicSynthesis):
        logger.warning(
            "synth_strategic returned non-StrategicSynthesis: %r", result
        )
        return None
    return result
