"""T4 verify stage: two adversarial gates layered between filter and synth.

Sprint 8 introduces verification in two passes:

    T4a attribution_check (Flash, cheap)
        Per RawItem (after T2 filter, before T3 extract). Answers:
        "Is the named competitor actually the SUBJECT of this article?"
        Items with verdict='no' are dropped here so we don't pay extract
        tokens on misattributed items. verdict='unclear' passes through but
        the resulting Finding gets a low attribution_confidence.

    T4b severity_adversarial (Pro, deep)
        Per Finding (after T3 extract). Answers:
        "Does the evidence quote support the assigned severity?"
        Pro can demote (e.g., raw=4 -> 2) or reject outright. Decisions are
        written back to the Finding (severity_verdict, severity_after_
        adversarial, severity_confidence, adversarial_reason) so the
        renderer + downstream stages can see Pro's reasoning.

Both stages are fail-open on LLM errors: if Gemini returns an error or
malformed JSON, we keep the item / Finding rather than drop it. Better to
emit a noisy email than a silent one.

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 8.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from clients.gemini import GeminiClient
from schema.finding import Finding, FindingStatus
from schema.finding_draft import AttributionCheck, SeverityAdversarialCheck
from schema.raw_item import RawItem
from util.competitor_registry import get_name

logger = logging.getLogger(__name__)


_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"
_ATTRIBUTION_PROMPT_PATH = _PROMPTS_DIR / "attribution_check.txt"
_SEVERITY_PROMPT_PATH = _PROMPTS_DIR / "severity_adversarial.txt"
if not _ATTRIBUTION_PROMPT_PATH.exists():  # pragma: no cover
    raise RuntimeError(f"attribution_check.txt prompt missing: {_ATTRIBUTION_PROMPT_PATH}")
if not _SEVERITY_PROMPT_PATH.exists():  # pragma: no cover
    raise RuntimeError(f"severity_adversarial.txt prompt missing: {_SEVERITY_PROMPT_PATH}")
_ATTRIBUTION_PROMPT_TEMPLATE = _ATTRIBUTION_PROMPT_PATH.read_text(encoding="utf-8")
_SEVERITY_PROMPT_TEMPLATE = _SEVERITY_PROMPT_PATH.read_text(encoding="utf-8")


# ---- Stage 4a: attribution check ----


@dataclass(frozen=True)
class AttributionResult:
    """The outcome of one attribution check on a RawItem."""

    item: RawItem
    decision: AttributionCheck
    kept: bool  # False iff verdict == "no"


def _format_attribution_prompt(item: RawItem) -> str:
    return _ATTRIBUTION_PROMPT_TEMPLATE.format(
        competitor_name=get_name(item.competitor) or item.competitor,
        competitor_id=item.competitor,
        title=item.title,
        summary=item.summary or "(no summary)",
        url=str(item.url),
        publisher_domain=item.publisher_domain or "(unknown)",
    )


async def attribution_check_item(
    item: RawItem, *, gemini: GeminiClient
) -> AttributionResult:
    """Run stage 4a on one RawItem.

    On any LLM error we fail open: keep the item with verdict='unclear' and
    confidence=1, so the next stage gets a chance to decide. Better noisy
    than silent.
    """
    prompt = _format_attribution_prompt(item)
    try:
        decision = await gemini.attribution_check(
            prompt, response_schema=AttributionCheck
        )
    except Exception as exc:
        logger.warning("attribution_check failed for %s: %s", item.url, exc)
        decision = AttributionCheck(
            verdict="unclear",
            confidence=1,
            reasoning="attribution_check_error",
        )
    if not isinstance(decision, AttributionCheck):
        logger.warning(
            "attribution_check returned non-AttributionCheck for %s: %r",
            item.url, decision,
        )
        decision = AttributionCheck(
            verdict="unclear",
            confidence=1,
            reasoning="attribution_check_invalid_response",
        )
    kept = decision.verdict != "no"
    if not kept:
        logger.info(
            "attribution_check dropped %s (competitor=%s): %s",
            item.url, item.competitor, decision.reasoning,
        )
    return AttributionResult(item=item, decision=decision, kept=kept)


async def attribution_check_items(
    items: list[RawItem], *, gemini: GeminiClient
) -> list[AttributionResult]:
    """Run stage 4a on a batch of RawItems sequentially."""
    out: list[AttributionResult] = []
    for item in items:
        out.append(await attribution_check_item(item, gemini=gemini))
    return out


def kept_after_attribution(
    results: list[AttributionResult],
) -> list[RawItem]:
    """Return only the items whose attribution verdict was 'yes' or 'unclear'."""
    return [r.item for r in results if r.kept]


def attach_attribution_to_finding(
    finding: Finding,
    decision: AttributionCheck,
) -> Finding:
    """Stamp the attribution-check result onto a Finding.

    Called by run_daily after extract: for each Finding, look up the
    AttributionResult that produced its source item, and apply the verdict
    and confidence. Returns the mutated finding (it's mutated in place but
    we return for fluent style).
    """
    finding.attribution_verdict = decision.verdict
    finding.attribution_confidence = decision.confidence
    if decision.verdict != "yes":
        # Surface the reasoning so the renderer and audit log can read it.
        finding.attribution_reason = decision.reasoning
    return finding


# ---- Stage 4b: severity adversarial check ----


def _format_severity_prompt(finding: Finding) -> str:
    return _SEVERITY_PROMPT_TEMPLATE.format(
        competitor_name=get_name(finding.competitor) or finding.competitor,
        competitor_id=finding.competitor,
        category=finding.category or "(uncategorized)",
        title=finding.title,
        summary=finding.summary,
        evidence_quote=finding.evidence_quote,
        signal_type=finding.signal_type,
        raw_severity=finding.raw_severity,
        products=", ".join(finding.products) if finding.products else "(none)",
    )


async def severity_adversarial_finding(
    finding: Finding, *, gemini: GeminiClient
) -> Finding:
    """Run stage 4b on one Finding. Mutates and returns the Finding.

    On LLM error we fail open: leave the Finding's severity untouched but
    write severity_verdict='kept' and severity_confidence=1 so downstream
    consumers can see the check ran but couldn't reach a verdict.
    """
    prompt = _format_severity_prompt(finding)
    try:
        decision = await gemini.adversarial_check(
            prompt, response_schema=SeverityAdversarialCheck
        )
    except Exception as exc:
        logger.warning("severity_adversarial failed for %s: %s", finding.url, exc)
        finding.severity_verdict = "kept"
        finding.severity_after_adversarial = finding.raw_severity
        finding.severity_confidence = 1
        finding.adversarial_reason = "severity_adversarial_error"
        return finding
    if not isinstance(decision, SeverityAdversarialCheck):
        logger.warning(
            "severity_adversarial returned non-SeverityAdversarialCheck for %s: %r",
            finding.url, decision,
        )
        finding.severity_verdict = "kept"
        finding.severity_after_adversarial = finding.raw_severity
        finding.severity_confidence = 1
        finding.adversarial_reason = "severity_adversarial_invalid_response"
        return finding

    finding.severity_verdict = decision.verdict
    finding.severity_after_adversarial = decision.severity_after_check
    finding.severity_confidence = decision.confidence
    finding.adversarial_reason = decision.reasoning
    if decision.verdict == "rejected":
        finding.status = FindingStatus.REJECTED_ADVERSARIAL
        logger.info(
            "severity_adversarial rejected %s: %s",
            finding.url, decision.reasoning,
        )
    elif decision.verdict == "demoted":
        logger.info(
            "severity_adversarial demoted %s: %d -> %d (%s)",
            finding.url,
            finding.raw_severity,
            decision.severity_after_check,
            decision.reasoning,
        )
    return finding


async def severity_adversarial_findings(
    findings: list[Finding], *, gemini: GeminiClient
) -> list[Finding]:
    """Run stage 4b on a batch of Findings sequentially."""
    out: list[Finding] = []
    for finding in findings:
        out.append(await severity_adversarial_finding(finding, gemini=gemini))
    return out


def kept_after_severity(findings: list[Finding]) -> list[Finding]:
    """Return only the findings that were not rejected by stage 4b."""
    return [f for f in findings if f.status != FindingStatus.REJECTED_ADVERSARIAL]
