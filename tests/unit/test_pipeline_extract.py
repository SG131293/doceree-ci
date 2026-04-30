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
