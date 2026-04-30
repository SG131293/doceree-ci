"""Tests for `pipeline.filter`. GeminiClient is mocked."""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from clients.gemini import GeminiClient
from pipeline.filter import filter_item, filter_items, kept
from schema import CollectionMethod, FilterDecision, RawItem, SourceType


def _item(title: str = "Test", competitor: str = "deepintent") -> RawItem:
    return RawItem(
        url=f"https://www.{competitor}.com/{title.replace(' ', '-')}",
        title=title,
        summary="A short summary",
        competitor=competitor,
        source_type=SourceType.NEWSROOM,
        collection_method=CollectionMethod.RSS,
        published_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def mock_gemini(monkeypatch: pytest.MonkeyPatch) -> GeminiClient:
    """A GeminiClient whose `filter()` method is an AsyncMock."""
    # Patch the SDK constructor so we don't need a real key.
    monkeypatch.setattr(
        "clients.gemini.genai.Client",
        lambda api_key: object(),  # opaque fake; we won't call into it
    )
    client = GeminiClient(api_key="test-key")
    client.filter = AsyncMock()  # type: ignore[method-assign]
    return client


@pytest.mark.asyncio
class TestFilterItem:
    async def test_keep_decision(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.filter.return_value = FilterDecision(  # type: ignore[attr-defined]
            keep=True, reason="product_launch"
        )
        decision = await filter_item(_item(), gemini=mock_gemini)
        assert decision.keep is True
        assert decision.reason == "product_launch"

    async def test_drop_decision(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.filter.return_value = FilterDecision(  # type: ignore[attr-defined]
            keep=False, reason="marketing_fluff"
        )
        decision = await filter_item(_item(), gemini=mock_gemini)
        assert decision.keep is False

    async def test_llm_error_keeps_with_filter_error_reason(
        self, mock_gemini: GeminiClient
    ) -> None:
        mock_gemini.filter.side_effect = RuntimeError("simulated LLM error")  # type: ignore[attr-defined]
        decision = await filter_item(_item(), gemini=mock_gemini)
        assert decision.keep is True  # fail open
        assert decision.reason == "filter_error"

    async def test_prompt_substitution(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.filter.return_value = FilterDecision(  # type: ignore[attr-defined]
            keep=True, reason="ok"
        )
        await filter_item(_item(title="Cortex launch"), gemini=mock_gemini)
        # The prompt passed to gemini.filter should include competitor + title
        call_args = mock_gemini.filter.await_args  # type: ignore[attr-defined]
        prompt_arg = call_args.args[0]
        assert "deepintent" in prompt_arg
        assert "Cortex launch" in prompt_arg


@pytest.mark.asyncio
class TestFilterItems:
    async def test_filters_batch(self, mock_gemini: GeminiClient) -> None:
        # Alternating keep / drop
        mock_gemini.filter.side_effect = [  # type: ignore[attr-defined]
            FilterDecision(keep=True, reason="ok"),
            FilterDecision(keep=False, reason="fluff"),
            FilterDecision(keep=True, reason="ok"),
        ]
        items = [_item(title=f"item{i}") for i in range(3)]
        decisions = await filter_items(items, gemini=mock_gemini)
        assert len(decisions) == 3
        assert [d.keep for _, d in decisions] == [True, False, True]

    async def test_kept_helper(self, mock_gemini: GeminiClient) -> None:
        mock_gemini.filter.side_effect = [  # type: ignore[attr-defined]
            FilterDecision(keep=True, reason="ok"),
            FilterDecision(keep=False, reason="fluff"),
        ]
        items = [_item(title="a"), _item(title="b")]
        decisions = await filter_items(items, gemini=mock_gemini)
        kept_items = kept(decisions)
        assert len(kept_items) == 1
        assert kept_items[0].title == "a"

    async def test_empty_input(self, mock_gemini: GeminiClient) -> None:
        decisions = await filter_items([], gemini=mock_gemini)
        assert decisions == []
        assert kept(decisions) == []
