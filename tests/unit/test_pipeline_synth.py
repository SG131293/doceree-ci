"""Tests for `pipeline.synth`. GeminiClient mocked.

Sprint 8 stages:
  T5 synth_per_product   Pro, one paragraph per impacted product
  T6 synth_strategic     Pro, single cross-product narrative (8e)
"""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from clients.gemini import GeminiClient
from pipeline.synth import (
    group_findings_by_product,
    synth_per_product,
    synth_per_product_batch,
    synth_strategic,
)
from schema import (
    CollectionMethod,
    Finding,
    FindingStatus,
    PerProductSynthesis,
    SourceType,
    StrategicSynthesis,
)


def _finding(
    *,
    competitor: str = "hippocratic_ai",
    title: str = "Polaris 5.0 launch",
    raw_severity: int = 4,
    products: list[str] | None = None,
) -> Finding:
    return Finding(
        finding_id="abc12345" + competitor.replace("_", "")[:24].ljust(24, "0"),
        url=f"https://example.com/{title.replace(' ', '-')}",
        source_type=SourceType.NEWSROOM,
        collection_method=CollectionMethod.RSS,
        competitor=competitor,
        category="agentic_clinical_ai",
        title=title,
        summary="Some summary describing the move.",
        evidence_quote="Evidence quote from the source.",
        signal_type="product_launch",
        products=products if products is not None else ["reptwin"],
        raw_severity=raw_severity,
        raw_confidence=4,
        status=FindingStatus.VERIFIED,
        captured_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def mock_gemini(monkeypatch: pytest.MonkeyPatch) -> GeminiClient:
    monkeypatch.setattr("clients.gemini.genai.Client", lambda api_key: object())
    client = GeminiClient(api_key="test")
    client.synthesize = AsyncMock()  # type: ignore[method-assign]
    return client


# =========================================================================
#  group_findings_by_product
# =========================================================================


class TestGroupFindingsByProduct:
    def test_one_finding_one_product(self) -> None:
        f = _finding(products=["reptwin"])
        out = group_findings_by_product([f])
        assert "reptwin" in out
        assert out["reptwin"] == [f]

    def test_finding_appears_under_each_impacted_product(self) -> None:
        f = _finding(products=["reptwin", "spark_for_ehrs", "premium_programmatic"])
        out = group_findings_by_product([f])
        assert set(out.keys()) == {"reptwin", "spark_for_ehrs", "premium_programmatic"}
        assert out["reptwin"] == [f]
        assert out["spark_for_ehrs"] == [f]
        assert out["premium_programmatic"] == [f]

    def test_empty_products_excluded(self) -> None:
        f1 = _finding(products=[])
        f2 = _finding(products=["reptwin"])
        out = group_findings_by_product([f1, f2])
        assert "reptwin" in out
        assert out["reptwin"] == [f2]
        # f1 has no product mapping, so it's not in the dict.
        assert all(f1 not in v for v in out.values())

    def test_findings_sorted_by_severity_within_product(self) -> None:
        low = _finding(title="low", products=["reptwin"], raw_severity=2)
        high = _finding(title="high", products=["reptwin"], raw_severity=5)
        mid = _finding(title="mid", products=["reptwin"], raw_severity=3)
        out = group_findings_by_product([low, high, mid])
        titles = [f.title for f in out["reptwin"]]
        assert titles == ["high", "mid", "low"]

    def test_products_sorted_by_max_severity_desc(self) -> None:
        # reptwin gets sev-5; pod gets sev-2 -> reptwin comes first.
        f_high = _finding(title="A", products=["reptwin"], raw_severity=5)
        f_low = _finding(title="B", products=["pod"], raw_severity=2)
        out = group_findings_by_product([f_low, f_high])
        assert list(out.keys()) == ["reptwin", "pod"]


# =========================================================================
#  synth_per_product
# =========================================================================


@pytest.mark.asyncio
class TestSynthPerProduct:
    async def test_returns_synthesis(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.synthesize.return_value = PerProductSynthesis(  # type: ignore[attr-defined]
            product_id="reptwin",
            impact_summary=(
                "Hippocratic AI's Polaris 5.0 raises the bar for evidence-based "
                "clinical AI, increasing pressure on RepTwin's positioning."
            ),
            recommended_action="Review RepTwin roadmap for evidence-based AI claims.",
        )
        result = await synth_per_product(
            "reptwin", [_finding(products=["reptwin"])], gemini=mock_gemini
        )
        assert result is not None
        assert result.product_id == "reptwin"
        assert "Hippocratic" in result.impact_summary
        assert "RepTwin" in result.recommended_action

    async def test_empty_findings_returns_none(
        self, mock_gemini: GeminiClient
    ) -> None:
        result = await synth_per_product("reptwin", [], gemini=mock_gemini)
        assert result is None
        # Did not call the LLM.
        mock_gemini.synthesize.assert_not_called()  # type: ignore[attr-defined]

    async def test_llm_error_returns_none(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.synthesize.side_effect = RuntimeError("simulated")  # type: ignore[attr-defined]
        result = await synth_per_product(
            "reptwin", [_finding(products=["reptwin"])], gemini=mock_gemini
        )
        assert result is None

    async def test_invalid_response_returns_none(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.synthesize.return_value = "garbage"  # type: ignore[attr-defined]
        result = await synth_per_product(
            "reptwin", [_finding(products=["reptwin"])], gemini=mock_gemini
        )
        assert result is None

    async def test_overrides_echoed_product_id(
        self, mock_gemini: GeminiClient
    ) -> None:
        # If the LLM echoes the wrong id, we overwrite it with the request id
        # so downstream lookups stay consistent.
        mock_gemini.synthesize.return_value = PerProductSynthesis(  # type: ignore[attr-defined]
            product_id="pod",  # wrong
            impact_summary="x" * 50,
            recommended_action="y",
        )
        result = await synth_per_product(
            "reptwin", [_finding(products=["reptwin"])], gemini=mock_gemini
        )
        assert result is not None
        assert result.product_id == "reptwin"

    async def test_prompt_includes_product_name_and_findings(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.synthesize.return_value = PerProductSynthesis(  # type: ignore[attr-defined]
            product_id="reptwin",
            impact_summary="x" * 30,
            recommended_action="y",
        )
        finding = _finding(
            products=["reptwin"], title="Polaris 5.0 launch by Hippocratic AI"
        )
        await synth_per_product("reptwin", [finding], gemini=mock_gemini)
        prompt = mock_gemini.synthesize.await_args.args[0]  # type: ignore[attr-defined]
        # Pro must see: the product (RepTwin/reptwin), some product context,
        # and the finding's title + evidence.
        assert "RepTwin" in prompt or "reptwin" in prompt
        assert "Polaris 5.0" in prompt
        assert "Evidence" in prompt or "evidence" in prompt


@pytest.mark.asyncio
class TestSynthPerProductBatch:
    async def test_runs_for_each_impacted_product(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.synthesize.side_effect = [  # type: ignore[attr-defined]
            PerProductSynthesis(
                product_id="reptwin", impact_summary="x" * 30, recommended_action="a"
            ),
            PerProductSynthesis(
                product_id="pod", impact_summary="y" * 30, recommended_action="b"
            ),
        ]
        findings = [
            _finding(products=["reptwin"], raw_severity=5),
            _finding(products=["pod"], raw_severity=3),
        ]
        out = await synth_per_product_batch(findings, gemini=mock_gemini)
        assert set(out.keys()) == {"reptwin", "pod"}

    async def test_skips_failed_synth(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.synthesize.side_effect = [  # type: ignore[attr-defined]
            PerProductSynthesis(
                product_id="reptwin", impact_summary="x" * 30, recommended_action="a"
            ),
            "garbage",  # invalid response for second product
        ]
        findings = [
            _finding(products=["reptwin"], raw_severity=5),
            _finding(products=["pod"], raw_severity=3),
        ]
        out = await synth_per_product_batch(findings, gemini=mock_gemini)
        # Only the successful one is in the output.
        assert set(out.keys()) == {"reptwin"}

    async def test_no_impacted_products_returns_empty(
        self, mock_gemini: GeminiClient
    ) -> None:
        # Findings with no product mapping → no synthesis to run.
        findings = [_finding(products=[]), _finding(products=[])]
        out = await synth_per_product_batch(findings, gemini=mock_gemini)
        assert out == {}

    async def test_severity_gate_drops_sub_threshold_products(
        self, mock_gemini: GeminiClient
    ) -> None:
        """Sprint 8f fix: products whose only findings are Sev 1-2 (typically
        financial noise demoted by adversarial) must NOT generate per-product
        synth paragraphs. Reproduces the 2026-05-11 bug where a Sev-2 Doximity
        earnings article triggered "strategic opening for NEXT" rhetoric."""
        mock_gemini.synthesize.return_value = PerProductSynthesis(  # type: ignore[attr-defined]
            product_id="reptwin", impact_summary="x" * 30, recommended_action="a"
        )
        findings = [
            # High-sev product launch — should synthesize.
            _finding(products=["reptwin"], raw_severity=4),
            # Sev-2 financial noise mapped to a product — should be gated out.
            _finding(
                competitor="doximity",
                products=["publisher_ai_suite", "next"],
                raw_severity=2,
            ),
        ]
        out = await synth_per_product_batch(findings, gemini=mock_gemini)
        assert set(out.keys()) == {"reptwin"}
        # publisher_ai_suite and next must NOT have synth paragraphs.
        assert "publisher_ai_suite" not in out
        assert "next" not in out
        # The LLM was only invoked once (for reptwin).
        assert mock_gemini.synthesize.await_count == 1  # type: ignore[attr-defined]

    async def test_severity_gate_keeps_mixed_severity_product(
        self, mock_gemini: GeminiClient
    ) -> None:
        """When a product has at least one Sev>=3 finding alongside Sev 1-2
        items, it still gets synthesized — and the prompt sees all findings,
        so lower-sev context can inform the paragraph."""
        mock_gemini.synthesize.return_value = PerProductSynthesis(  # type: ignore[attr-defined]
            product_id="reptwin", impact_summary="x" * 30, recommended_action="a"
        )
        findings = [
            _finding(title="big", products=["reptwin"], raw_severity=4),
            _finding(title="small", products=["reptwin"], raw_severity=2),
        ]
        out = await synth_per_product_batch(findings, gemini=mock_gemini)
        assert "reptwin" in out
        # Both findings should appear in the prompt sent to Pro.
        prompt = mock_gemini.synthesize.await_args.args[0]  # type: ignore[attr-defined]
        assert "big" in prompt
        assert "small" in prompt

    async def test_severity_gate_custom_threshold(
        self, mock_gemini: GeminiClient
    ) -> None:
        """`min_product_severity` is configurable for backfill / debug runs."""
        mock_gemini.synthesize.return_value = PerProductSynthesis(  # type: ignore[attr-defined]
            product_id="pod", impact_summary="x" * 30, recommended_action="a"
        )
        findings = [_finding(products=["pod"], raw_severity=2)]
        # Default threshold (3) would drop this. Lower threshold keeps it.
        out = await synth_per_product_batch(
            findings, gemini=mock_gemini, min_product_severity=2
        )
        assert "pod" in out


# =========================================================================
#  synth_strategic (T6)
# =========================================================================


@pytest.mark.asyncio
class TestSynthStrategic:
    async def test_returns_synthesis(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.synthesize.return_value = StrategicSynthesis(  # type: ignore[attr-defined]
            pattern=(
                "Two of three findings cluster in Agentic Clinical AI, "
                "with funding and product launches concentrating in that "
                "category. Pressure on RepTwin and Spark for EHRs is "
                "accelerating."
            ),
            implied_agenda=(
                "Validate RepTwin's evidence-based AI story against Polaris claims."
            ),
        )
        findings = [_finding(products=["reptwin"], raw_severity=4)]
        result = await synth_strategic(findings, {}, gemini=mock_gemini)
        assert result is not None
        assert "Agentic Clinical AI" in result.pattern
        assert "RepTwin" in result.implied_agenda

    async def test_empty_findings_returns_none(
        self, mock_gemini: GeminiClient
    ) -> None:
        result = await synth_strategic([], {}, gemini=mock_gemini)
        assert result is None
        mock_gemini.synthesize.assert_not_called()  # type: ignore[attr-defined]

    async def test_llm_error_returns_none(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.synthesize.side_effect = RuntimeError("simulated")  # type: ignore[attr-defined]
        result = await synth_strategic(
            [_finding()], {}, gemini=mock_gemini
        )
        assert result is None

    async def test_invalid_response_returns_none(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.synthesize.return_value = "garbage"  # type: ignore[attr-defined]
        result = await synth_strategic([_finding()], {}, gemini=mock_gemini)
        assert result is None

    async def test_prompt_includes_findings_and_per_product(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.synthesize.return_value = StrategicSynthesis(  # type: ignore[attr-defined]
            pattern="x" * 30, implied_agenda="y" * 30
        )
        per_product = {
            "reptwin": PerProductSynthesis(
                product_id="reptwin",
                impact_summary="Pressure on RepTwin from agentic AI launches.",
                recommended_action="Review RepTwin roadmap.",
            )
        }
        findings = [
            _finding(
                products=["reptwin"],
                title="Polaris 5.0 launch by Hippocratic AI",
                raw_severity=4,
            )
        ]
        await synth_strategic(findings, per_product, gemini=mock_gemini)
        prompt = mock_gemini.synthesize.await_args.args[0]  # type: ignore[attr-defined]
        # Pro must see today's findings + the per-product context.
        assert "Polaris 5.0" in prompt
        assert "reptwin" in prompt
        assert "Pressure on RepTwin" in prompt

    async def test_skipped_when_no_sev4_findings(
        self, mock_gemini: GeminiClient
    ) -> None:
        """Sprint 8f fix: strategic synth returns None when nothing today
        clears Sev 4. Stops the hallucinatory "today's primary development"
        rhetoric on quiet-day Sev-2-only inputs."""
        findings = [
            _finding(products=["next"], raw_severity=2),
            _finding(products=["publisher_ai_suite"], raw_severity=1),
        ]
        result = await synth_strategic(findings, {}, gemini=mock_gemini)
        assert result is None
        mock_gemini.synthesize.assert_not_called()  # type: ignore[attr-defined]

    async def test_fires_when_at_least_one_sev4(
        self, mock_gemini: GeminiClient
    ) -> None:
        """One Sev-4 in the day is enough to trigger strategic synthesis,
        even if other findings are Sev 1-2."""
        mock_gemini.synthesize.return_value = StrategicSynthesis(  # type: ignore[attr-defined]
            pattern="x" * 30, implied_agenda="y" * 30
        )
        findings = [
            _finding(title="big", products=["poc"], raw_severity=4),
            _finding(title="small", products=["next"], raw_severity=2),
        ]
        result = await synth_strategic(findings, {}, gemini=mock_gemini)
        assert result is not None

    async def test_custom_alert_threshold(
        self, mock_gemini: GeminiClient
    ) -> None:
        """`min_alert_severity` is configurable for backfill runs."""
        mock_gemini.synthesize.return_value = StrategicSynthesis(  # type: ignore[attr-defined]
            pattern="x" * 30, implied_agenda="y" * 30
        )
        findings = [_finding(products=["poc"], raw_severity=3)]
        # Default (4) would skip this. Lower threshold fires it.
        result = await synth_strategic(
            findings, {}, gemini=mock_gemini, min_alert_severity=3
        )
        assert result is not None
