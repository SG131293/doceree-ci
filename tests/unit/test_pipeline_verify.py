"""Tests for `pipeline.verify`. GeminiClient mocked.

Sprint 8 stages:
  4a attribution_check       Flash, drops misattributed items
  4b severity_adversarial    Pro, demotes / rejects severity
"""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from clients.gemini import GeminiClient
from pipeline.verify import (
    attach_attribution_to_finding,
    attribution_check_item,
    attribution_check_items,
    kept_after_attribution,
    kept_after_severity,
    severity_adversarial_finding,
    severity_adversarial_findings,
)
from schema import (
    AttributionCheck,
    CollectionMethod,
    Finding,
    FindingStatus,
    RawItem,
    SeverityAdversarialCheck,
    SourceType,
)


def _item(
    title: str = "Hippocratic AI Launches Polaris 5.0",
    competitor: str = "hippocratic_ai",
) -> RawItem:
    return RawItem(
        url=f"https://news.google.com/rss/articles/{title.replace(' ', '-')}",
        canonical_url="https://hippocraticai.com/news/x",
        publisher_domain="hippocraticai.com",
        title=title,
        summary="A short summary describing the announcement.",
        competitor=competitor,
        source_type=SourceType.NEWSROOM,
        collection_method=CollectionMethod.RSS,
        published_at=datetime.now(timezone.utc),
    )


def _finding(
    *,
    competitor: str = "hippocratic_ai",
    raw_severity: int = 4,
    raw_confidence: int = 4,
) -> Finding:
    return Finding(
        finding_id="abc12345" + "0" * 24,
        url="https://hippocraticai.com/news/polaris",
        source_type=SourceType.NEWSROOM,
        collection_method=CollectionMethod.RSS,
        competitor=competitor,
        category="agentic_clinical_ai",
        title="Polaris 5.0 launch",
        summary="Hippocratic AI launches Polaris 5.0 evidence-based AI.",
        evidence_quote="Hippocratic AI Launches Polaris 5.0...",
        signal_type="product_launch",
        products=["reptwin"],
        raw_severity=raw_severity,
        raw_confidence=raw_confidence,
        status=FindingStatus.DRAFT,
        captured_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def mock_gemini(monkeypatch: pytest.MonkeyPatch) -> GeminiClient:
    monkeypatch.setattr("clients.gemini.genai.Client", lambda api_key: object())
    client = GeminiClient(api_key="test")
    client.attribution_check = AsyncMock()  # type: ignore[method-assign]
    client.adversarial_check = AsyncMock()  # type: ignore[method-assign]
    return client


# =========================================================================
#  Stage 4a: attribution_check
# =========================================================================


@pytest.mark.asyncio
class TestAttributionCheckItem:
    async def test_yes_keeps_item(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.attribution_check.return_value = AttributionCheck(  # type: ignore[attr-defined]
            verdict="yes", confidence=5, reasoning="Headline names them"
        )
        result = await attribution_check_item(_item(), gemini=mock_gemini)
        assert result.kept is True
        assert result.decision.verdict == "yes"

    async def test_no_drops_item(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.attribution_check.return_value = AttributionCheck(  # type: ignore[attr-defined]
            verdict="no",
            confidence=4,
            reasoning="Article is about Aidoc, not Hippocratic AI",
        )
        item = _item(title="Aidoc raises $150M from Goldman Sachs")
        result = await attribution_check_item(item, gemini=mock_gemini)
        assert result.kept is False
        assert result.decision.verdict == "no"

    async def test_unclear_keeps_item_but_marks_uncertain(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.attribution_check.return_value = AttributionCheck(  # type: ignore[attr-defined]
            verdict="unclear", confidence=2, reasoning="Multiple companies named"
        )
        result = await attribution_check_item(_item(), gemini=mock_gemini)
        assert result.kept is True
        assert result.decision.verdict == "unclear"
        assert result.decision.confidence == 2

    async def test_llm_error_fails_open(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.attribution_check.side_effect = RuntimeError("simulated 500")  # type: ignore[attr-defined]
        result = await attribution_check_item(_item(), gemini=mock_gemini)
        assert result.kept is True  # fail open
        assert result.decision.verdict == "unclear"
        assert "error" in result.decision.reasoning

    async def test_invalid_response_fails_open(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.attribution_check.return_value = "garbage"  # type: ignore[attr-defined]
        result = await attribution_check_item(_item(), gemini=mock_gemini)
        assert result.kept is True
        assert result.decision.verdict == "unclear"
        assert "invalid" in result.decision.reasoning

    async def test_prompt_includes_competitor_and_title(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.attribution_check.return_value = AttributionCheck(  # type: ignore[attr-defined]
            verdict="yes", confidence=5, reasoning="ok"
        )
        await attribution_check_item(
            _item(title="Polaris 5.0 launch", competitor="hippocratic_ai"),
            gemini=mock_gemini,
        )
        prompt = mock_gemini.attribution_check.await_args.args[0]  # type: ignore[attr-defined]
        # Either the human-readable name OR the id should appear; we don't
        # care which, just that the LLM has the context.
        assert "Hippocratic AI" in prompt or "hippocratic_ai" in prompt
        assert "Polaris 5.0 launch" in prompt


@pytest.mark.asyncio
class TestAttributionCheckItems:
    async def test_batch(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.attribution_check.side_effect = [  # type: ignore[attr-defined]
            AttributionCheck(verdict="yes", confidence=5, reasoning="ok"),
            AttributionCheck(verdict="no", confidence=5, reasoning="other co"),
            AttributionCheck(verdict="unclear", confidence=2, reasoning="mixed"),
        ]
        items = [
            _item(title="Polaris 5.0"),
            _item(title="Aidoc raises $150M"),
            _item(title="Healthcare AI roundup"),
        ]
        results = await attribution_check_items(items, gemini=mock_gemini)
        assert [r.kept for r in results] == [True, False, True]

    async def test_kept_after_attribution_helper(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.attribution_check.side_effect = [  # type: ignore[attr-defined]
            AttributionCheck(verdict="yes", confidence=5, reasoning="ok"),
            AttributionCheck(verdict="no", confidence=5, reasoning="other"),
        ]
        items = [_item(title="A"), _item(title="B")]
        results = await attribution_check_items(items, gemini=mock_gemini)
        kept = kept_after_attribution(results)
        assert len(kept) == 1
        assert kept[0].title == "A"


class TestAttachAttributionToFinding:
    def test_yes_does_not_set_reason(self) -> None:
        finding = _finding()
        decision = AttributionCheck(
            verdict="yes", confidence=5, reasoning="Headline names them"
        )
        out = attach_attribution_to_finding(finding, decision)
        assert out.attribution_verdict == "yes"
        assert out.attribution_confidence == 5
        # No reason stamped when verdict is 'yes' (it's noise on the email).
        assert out.attribution_reason is None

    def test_unclear_stamps_reason(self) -> None:
        finding = _finding()
        decision = AttributionCheck(
            verdict="unclear", confidence=2, reasoning="Multiple companies named"
        )
        out = attach_attribution_to_finding(finding, decision)
        assert out.attribution_verdict == "unclear"
        assert out.attribution_reason == "Multiple companies named"


# =========================================================================
#  Stage 4b: severity_adversarial
# =========================================================================


@pytest.mark.asyncio
class TestSeverityAdversarialFinding:
    async def test_kept_writes_verdict(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.adversarial_check.return_value = SeverityAdversarialCheck(  # type: ignore[attr-defined]
            verdict="kept",
            severity_after_check=4,
            confidence=4,
            reasoning="Evidence supports the assigned severity.",
        )
        finding = _finding(raw_severity=4)
        out = await severity_adversarial_finding(finding, gemini=mock_gemini)
        assert out.severity_verdict == "kept"
        assert out.severity_after_adversarial == 4
        assert out.severity_confidence == 4
        assert out.status == FindingStatus.DRAFT  # not promoted by 4b

    async def test_demoted_lowers_severity(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.adversarial_check.return_value = SeverityAdversarialCheck(  # type: ignore[attr-defined]
            verdict="demoted",
            severity_after_check=2,
            confidence=4,
            reasoning="Routine corporate disclosure; no material angle.",
        )
        finding = _finding(raw_severity=4)
        out = await severity_adversarial_finding(finding, gemini=mock_gemini)
        assert out.severity_verdict == "demoted"
        assert out.severity_after_adversarial == 2
        # effective_severity reflects the adversarial demotion.
        assert out.effective_severity == 2

    async def test_rejected_marks_status(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.adversarial_check.return_value = SeverityAdversarialCheck(  # type: ignore[attr-defined]
            verdict="rejected",
            severity_after_check=1,
            confidence=5,
            reasoning="Marketing fluff; no signal at all.",
        )
        finding = _finding(raw_severity=3)
        out = await severity_adversarial_finding(finding, gemini=mock_gemini)
        assert out.severity_verdict == "rejected"
        assert out.status == FindingStatus.REJECTED_ADVERSARIAL

    async def test_llm_error_fails_open(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.adversarial_check.side_effect = RuntimeError("simulated 500")  # type: ignore[attr-defined]
        finding = _finding(raw_severity=4)
        out = await severity_adversarial_finding(finding, gemini=mock_gemini)
        assert out.severity_verdict == "kept"  # fail open
        assert out.severity_after_adversarial == 4
        assert out.severity_confidence == 1
        assert "error" in (out.adversarial_reason or "")
        assert out.status == FindingStatus.DRAFT  # not rejected on error

    async def test_invalid_response_fails_open(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.adversarial_check.return_value = "garbage"  # type: ignore[attr-defined]
        finding = _finding(raw_severity=4)
        out = await severity_adversarial_finding(finding, gemini=mock_gemini)
        assert out.severity_verdict == "kept"
        assert out.severity_after_adversarial == 4
        assert out.severity_confidence == 1

    async def test_prompt_includes_evidence_and_severity(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.adversarial_check.return_value = SeverityAdversarialCheck(  # type: ignore[attr-defined]
            verdict="kept", severity_after_check=4, confidence=4, reasoning="ok"
        )
        finding = _finding(raw_severity=4)
        await severity_adversarial_finding(finding, gemini=mock_gemini)
        prompt = mock_gemini.adversarial_check.await_args.args[0]  # type: ignore[attr-defined]
        # Critical context for Pro: the evidence quote and the assigned severity.
        assert finding.evidence_quote in prompt
        assert "4" in prompt  # raw_severity


@pytest.mark.asyncio
class TestSeverityAdversarialFindings:
    async def test_batch(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.adversarial_check.side_effect = [  # type: ignore[attr-defined]
            SeverityAdversarialCheck(
                verdict="kept", severity_after_check=4, confidence=4, reasoning="ok"
            ),
            SeverityAdversarialCheck(
                verdict="rejected",
                severity_after_check=1,
                confidence=5,
                reasoning="fluff",
            ),
        ]
        findings = [_finding(raw_severity=4), _finding(raw_severity=3)]
        out = await severity_adversarial_findings(findings, gemini=mock_gemini)
        assert out[0].severity_verdict == "kept"
        assert out[1].severity_verdict == "rejected"

    async def test_kept_after_severity_helper(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.adversarial_check.side_effect = [  # type: ignore[attr-defined]
            SeverityAdversarialCheck(
                verdict="kept", severity_after_check=4, confidence=4, reasoning="ok"
            ),
            SeverityAdversarialCheck(
                verdict="rejected",
                severity_after_check=1,
                confidence=5,
                reasoning="fluff",
            ),
        ]
        findings = [_finding(raw_severity=4), _finding(raw_severity=3)]
        out = await severity_adversarial_findings(findings, gemini=mock_gemini)
        kept = kept_after_severity(out)
        assert len(kept) == 1
        assert kept[0].severity_verdict == "kept"
