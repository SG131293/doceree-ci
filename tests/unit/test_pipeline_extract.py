"""Tests for `pipeline.extract`. GeminiClient mocked."""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from clients.gemini import GeminiClient
from pipeline.extract import extract_finding, extract_findings
from schema import (
    CollectionMethod,
    Finding,
    FindingDraft,
    FindingStatus,
    RawItem,
    SourceType,
)


def _item(title: str = "DeepIntent launches Cortex") -> RawItem:
    return RawItem(
        url=f"https://www.deepintent.com/{title.replace(' ', '-')}",
        title=title,
        summary="A summary describing the news",
        competitor="deepintent",
        source_type=SourceType.PRESS_RELEASE,
        collection_method=CollectionMethod.RSS,
        published_at=datetime.now(timezone.utc),
    )


def _draft(**overrides) -> FindingDraft:
    base = dict(
        title="DeepIntent launches Cortex AI media buying",
        summary="DeepIntent announced Cortex with daily-refreshed health data.",
        evidence_quote="Cortex is the AI media buying engine for HCP campaigns.",
        signal_type="product_launch",
        products=["premium_programmatic", "next"],
        raw_severity=4,
        raw_confidence=4,
    )
    base.update(overrides)
    return FindingDraft(**base)


@pytest.fixture
def mock_gemini(monkeypatch: pytest.MonkeyPatch) -> GeminiClient:
    monkeypatch.setattr("clients.gemini.genai.Client", lambda api_key: object())
    client = GeminiClient(api_key="test")
    client.extract = AsyncMock()  # type: ignore[method-assign]
    return client


@pytest.mark.asyncio
class TestExtractFinding:
    async def test_promotes_draft_to_finding(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.extract.return_value = _draft()  # type: ignore[attr-defined]
        item = _item()
        finding = await extract_finding(item, gemini=mock_gemini)
        assert finding is not None
        assert isinstance(finding, Finding)
        assert finding.competitor == "deepintent"
        assert finding.source_type == SourceType.PRESS_RELEASE
        assert finding.collection_method == CollectionMethod.RSS
        assert finding.status == FindingStatus.DRAFT
        assert finding.raw_severity == 4
        assert finding.products == ["premium_programmatic", "next"]
        assert finding.captured_at.tzinfo is not None
        assert finding.published_at == item.published_at

    async def test_category_populated_from_registry(
        self, mock_gemini: GeminiClient
    ) -> None:
        """extract.py should look up the competitor's category from
        competitors.yaml and stamp it on the Finding."""
        mock_gemini.extract.return_value = _draft()  # type: ignore[attr-defined]
        finding = await extract_finding(_item(), gemini=mock_gemini)
        assert finding is not None
        # `deepintent` is in the healthcare_dsp category per Sprint 8 config.
        assert finding.category == "healthcare_dsp"

    async def test_extraction_confidence_mirrors_raw_confidence(
        self, mock_gemini: GeminiClient
    ) -> None:
        """Extract sets `extraction_confidence` from `raw_confidence` so the
        decomposed-confidence path is uniformly populated."""
        mock_gemini.extract.return_value = _draft(raw_confidence=4)  # type: ignore[attr-defined]
        finding = await extract_finding(_item(), gemini=mock_gemini)
        assert finding is not None
        assert finding.extraction_confidence == 4

    async def test_canonical_url_forwarded_from_raw_item(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.extract.return_value = _draft()  # type: ignore[attr-defined]
        item = RawItem(
            url="https://news.google.com/rss/articles/CBMiabc",
            canonical_url="https://deepintent.com/news/cortex",
            publisher_domain="deepintent.com",
            title="DeepIntent launches Cortex",
            summary="...",
            competitor="deepintent",
            source_type=SourceType.PRESS_RELEASE,
            collection_method=CollectionMethod.RSS,
            published_at=datetime.now(timezone.utc),
        )
        finding = await extract_finding(item, gemini=mock_gemini)
        assert finding is not None
        assert str(finding.canonical_url) == "https://deepintent.com/news/cortex"
        assert finding.publisher_domain == "deepintent.com"

    async def test_products_kept_when_llm_returns_them(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.extract.return_value = _draft(  # type: ignore[attr-defined]
            products=["premium_programmatic", "next"]
        )
        finding = await extract_finding(_item(), gemini=mock_gemini)
        assert finding is not None
        assert finding.products == ["premium_programmatic", "next"]

    async def test_products_backfilled_from_competitor_when_llm_empty(
        self, mock_gemini: GeminiClient
    ) -> None:
        """When the LLM returns an empty products list (Flash is too
        conservative), backfill from the competitor's `related_doceree_products`
        so the BY-PRODUCT digest section + per-product synth still run."""
        mock_gemini.extract.return_value = _draft(products=[])  # type: ignore[attr-defined]
        # _item() uses competitor="deepintent" which maps to
        # [premium_programmatic, next, poc, spark_for_ehrs, spark_for_dooh].
        # Capped at 3.
        finding = await extract_finding(_item(), gemini=mock_gemini)
        assert finding is not None
        assert len(finding.products) > 0
        assert len(finding.products) <= 3
        # Should include at least one of DeepIntent's known related products.
        assert any(
            p in finding.products
            for p in ("premium_programmatic", "next", "poc", "spark_for_ehrs")
        )

    async def test_products_backfill_capped_at_three(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.extract.return_value = _draft(products=[])  # type: ignore[attr-defined]
        # OptimizeRx maps to 5 products; backfill should cap at 3.
        item = RawItem(
            url="https://example.com/oprx",
            title="x",
            summary="x",
            competitor="optimizerx",
            source_type=SourceType.PRESS_RELEASE,
            collection_method=CollectionMethod.RSS,
            published_at=datetime.now(timezone.utc),
        )
        finding = await extract_finding(item, gemini=mock_gemini)
        assert finding is not None
        assert len(finding.products) <= 3

    async def test_finding_id_is_deterministic_hash_of_item(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.extract.return_value = _draft()  # type: ignore[attr-defined]
        item = _item()
        finding = await extract_finding(item, gemini=mock_gemini)
        assert finding is not None
        # finding_id is the first 32 chars of item.content_hash
        assert finding.finding_id == item.content_hash[:32]

    async def test_llm_error_returns_none(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.extract.side_effect = RuntimeError("simulated LLM error")  # type: ignore[attr-defined]
        finding = await extract_finding(_item(), gemini=mock_gemini)
        assert finding is None

    async def test_validation_failure_returns_none(
        self, mock_gemini: GeminiClient
    ) -> None:
        # Draft has bad raw_severity that the schema would catch
        mock_gemini.extract.return_value = "not a FindingDraft"  # type: ignore[attr-defined]
        finding = await extract_finding(_item(), gemini=mock_gemini)
        assert finding is None

    async def test_prompt_includes_item_metadata(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.extract.return_value = _draft()  # type: ignore[attr-defined]
        await extract_finding(_item(title="Helix launch"), gemini=mock_gemini)
        prompt_arg = mock_gemini.extract.await_args.args[0]  # type: ignore[attr-defined]
        assert "deepintent" in prompt_arg
        assert "Helix launch" in prompt_arg


@pytest.mark.asyncio
class TestExtractFindings:
    async def test_skips_failed_extractions(self, mock_gemini: GeminiClient) -> None:
        # 1st item succeeds, 2nd fails (bad return type), 3rd succeeds
        mock_gemini.extract.side_effect = [  # type: ignore[attr-defined]
            _draft(),
            "garbage",
            _draft(),
        ]
        items = [_item(title=f"i{i}") for i in range(3)]
        findings = await extract_findings(items, gemini=mock_gemini)
        assert len(findings) == 2

    async def test_empty(self, mock_gemini: GeminiClient) -> None:
        findings = await extract_findings([], gemini=mock_gemini)
        assert findings == []
