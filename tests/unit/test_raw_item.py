"""Tests for `schema.raw_item.RawItem` and `schema.finding_draft`."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from schema import (
    CollectionMethod,
    FilterDecision,
    FindingDraft,
    RawItem,
    SourceType,
)


NOW_UTC = datetime.now(timezone.utc)


@pytest.fixture
def valid_raw_item_kwargs() -> dict:
    return dict(
        url="https://www.deepintent.com/news/cortex",
        title="DeepIntent launches Cortex AI media buying",
        summary="DeepIntent announced Cortex with daily-refreshed health data...",
        competitor="deepintent",
        source_type=SourceType.PRESS_RELEASE,
        collection_method=CollectionMethod.RSS,
        published_at=NOW_UTC,
    )


class TestRawItemValid:
    def test_minimal(self, valid_raw_item_kwargs: dict) -> None:
        item = RawItem(**valid_raw_item_kwargs)
        assert item.competitor == "deepintent"
        assert item.source_type == SourceType.PRESS_RELEASE

    def test_default_fetched_at_is_aware(self, valid_raw_item_kwargs: dict) -> None:
        item = RawItem(**valid_raw_item_kwargs)
        assert item.fetched_at.tzinfo is not None

    def test_summary_optional(self, valid_raw_item_kwargs: dict) -> None:
        valid_raw_item_kwargs["summary"] = ""
        item = RawItem(**valid_raw_item_kwargs)
        assert item.summary == ""

    def test_published_at_optional(self, valid_raw_item_kwargs: dict) -> None:
        del valid_raw_item_kwargs["published_at"]
        item = RawItem(**valid_raw_item_kwargs)
        assert item.published_at is None


class TestRawItemInvalid:
    def test_missing_required(self, valid_raw_item_kwargs: dict) -> None:
        del valid_raw_item_kwargs["competitor"]
        with pytest.raises(ValidationError):
            RawItem(**valid_raw_item_kwargs)

    def test_naive_published_rejected(self, valid_raw_item_kwargs: dict) -> None:
        valid_raw_item_kwargs["published_at"] = datetime.now()  # naive
        with pytest.raises(ValidationError):
            RawItem(**valid_raw_item_kwargs)

    def test_competitor_pattern_enforced(self, valid_raw_item_kwargs: dict) -> None:
        valid_raw_item_kwargs["competitor"] = "DeepIntent"
        with pytest.raises(ValidationError):
            RawItem(**valid_raw_item_kwargs)

    def test_extra_field_forbidden(self, valid_raw_item_kwargs: dict) -> None:
        valid_raw_item_kwargs["extra_thing"] = "nope"
        with pytest.raises(ValidationError):
            RawItem(**valid_raw_item_kwargs)


class TestContentHash:
    def test_stable(self, valid_raw_item_kwargs: dict) -> None:
        a = RawItem(**valid_raw_item_kwargs)
        b = RawItem(**valid_raw_item_kwargs)
        assert a.content_hash == b.content_hash
        assert len(a.content_hash) == 64  # SHA-256 hex

    def test_changes_with_url(self, valid_raw_item_kwargs: dict) -> None:
        a = RawItem(**valid_raw_item_kwargs)
        valid_raw_item_kwargs["url"] = "https://www.deepintent.com/news/cortex2"
        b = RawItem(**valid_raw_item_kwargs)
        assert a.content_hash != b.content_hash

    def test_changes_with_title(self, valid_raw_item_kwargs: dict) -> None:
        a = RawItem(**valid_raw_item_kwargs)
        valid_raw_item_kwargs["title"] = "Different headline"
        b = RawItem(**valid_raw_item_kwargs)
        assert a.content_hash != b.content_hash

    def test_summary_truncated_for_hash(self, valid_raw_item_kwargs: dict) -> None:
        """Trailing changes after 500 chars should not change the hash."""
        valid_raw_item_kwargs["summary"] = "a" * 500
        a = RawItem(**valid_raw_item_kwargs)
        valid_raw_item_kwargs["summary"] = "a" * 500 + "b" * 500
        b = RawItem(**valid_raw_item_kwargs)
        assert a.content_hash == b.content_hash


class TestFindingDraft:
    def test_valid(self) -> None:
        d = FindingDraft(
            title="OptimizeRx adds new EHR partner",
            summary="OptimizeRx announced a new EHR partnership expanding reach.",
            evidence_quote="Today we are partnering with X to expand our network.",
            signal_type="ehr_partnership",
            products=["poc", "spark_for_ehrs"],
            raw_severity=4,
            raw_confidence=4,
        )
        assert d.products == ["poc", "spark_for_ehrs"]

    def test_severity_range(self) -> None:
        with pytest.raises(ValidationError):
            FindingDraft(
                title="x",
                summary="x" * 10,
                evidence_quote="x",
                signal_type="x",
                raw_severity=6,
                raw_confidence=3,
            )

    def test_empty_products_allowed(self) -> None:
        d = FindingDraft(
            title="x",
            summary="x" * 10,
            evidence_quote="x",
            signal_type="x",
            products=[],
            raw_severity=2,
            raw_confidence=2,
        )
        assert d.products == []

    def test_extra_field_forbidden(self) -> None:
        with pytest.raises(ValidationError):
            FindingDraft(
                title="x",
                summary="x" * 10,
                evidence_quote="x",
                signal_type="x",
                raw_severity=2,
                raw_confidence=2,
                weird_field="nope",  # type: ignore[call-arg]
            )


class TestFilterDecision:
    def test_keep_true(self) -> None:
        d = FilterDecision(keep=True, reason="product_launch")
        assert d.keep is True

    def test_keep_false(self) -> None:
        d = FilterDecision(keep=False, reason="marketing_fluff")
        assert d.keep is False

    def test_reason_required(self) -> None:
        with pytest.raises(ValidationError):
            FilterDecision(keep=True, reason="")
