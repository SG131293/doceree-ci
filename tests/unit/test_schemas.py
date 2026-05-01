"""Tests for the canonical schemas in src/schema/.

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 3.

Run: `pytest tests/unit/test_schemas.py -v`
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from schema import (
    CollectionMethod,
    CompetitorCategory,
    CompetitorRef,
    CompetitorTier,
    Finding,
    FindingStatus,
    JourneyStage,
    ProductRef,
    Severity,
    SourceRef,
    SourceType,
    category_display_name,
)


# ---------- Fixtures ----------

NOW_UTC = datetime.now(timezone.utc)


@pytest.fixture
def valid_finding_kwargs() -> dict:
    """Minimum-required Finding payload with realistic Doceree values."""
    return dict(
        finding_id="abc123de" + "f" * 20,  # 28 chars; passes min_length=8
        url="https://www.deepintent.com/news/cortex-launch",
        source_type=SourceType.PRESS_RELEASE,
        collection_method=CollectionMethod.SITEMAP,
        competitor="deepintent",
        title="DeepIntent launches Cortex AI media buying",
        summary="DeepIntent announced Cortex, an AI-powered media buying engine "
                "with daily-refreshed health data, positioning against orchestration "
                "platforms.",
        evidence_quote="Cortex uses daily-refreshed health data to drive "
                       "AI-powered media buying decisions.",
        signal_type="dsp_capability",
        products=["premium_programmatic", "next"],
        raw_severity=4,
        raw_confidence=4,
        captured_at=NOW_UTC,
    )


# ========== Severity enum ==========


class TestSeverity:
    def test_values_1_through_5(self) -> None:
        assert Severity.INFORMATIONAL == 1
        assert Severity.NOTABLE == 2
        assert Severity.MATERIAL == 3
        assert Severity.STRATEGIC == 4
        assert Severity.URGENT == 5

    def test_alert_eligible_only_sev5(self) -> None:
        assert Severity.is_alert_eligible(5) is True
        assert Severity.is_alert_eligible(4) is False
        assert Severity.is_alert_eligible(1) is False

    def test_crossvalidation_for_sev4_and_5(self) -> None:
        assert Severity.needs_crossvalidation(4) is True
        assert Severity.needs_crossvalidation(5) is True
        assert Severity.needs_crossvalidation(3) is False
        assert Severity.needs_crossvalidation(1) is False


# ========== Reference models ==========


class TestProductRef:
    def test_valid(self) -> None:
        p = ProductRef(
            id="reptwin",
            name="RepTwin",
            journey_stages=[JourneyStage.INTERACTION],
        )
        assert p.id == "reptwin"
        assert JourneyStage.INTERACTION in p.journey_stages

    def test_id_must_be_snake_case(self) -> None:
        with pytest.raises(ValidationError):
            ProductRef(id="RepTwin", name="RepTwin")  # capital R rejected
        with pytest.raises(ValidationError):
            ProductRef(id="rep-twin", name="RepTwin")  # hyphen rejected

    def test_extra_fields_forbidden(self) -> None:
        with pytest.raises(ValidationError):
            ProductRef(id="reptwin", name="RepTwin", color="teal")  # type: ignore[call-arg]

    def test_journey_stages_default_empty(self) -> None:
        p = ProductRef(id="pod", name="POD")
        assert p.journey_stages == []


class TestCompetitorRef:
    def test_valid_each_tier(self) -> None:
        for tier in CompetitorTier:
            c = CompetitorRef(id="optimizerx", name="OptimizeRx", tier=tier)
            assert c.tier == tier
            assert c.category is None  # default

    def test_id_pattern(self) -> None:
        with pytest.raises(ValidationError):
            CompetitorRef(id="OptimizeRx", name="OptimizeRx", tier=CompetitorTier.TIER_1)

    def test_with_category(self) -> None:
        c = CompetitorRef(
            id="hippocratic_ai",
            name="Hippocratic AI",
            tier=CompetitorTier.HEALTHCARE_AI_CLUSTER,
            category=CompetitorCategory.AGENTIC_CLINICAL_AI,
        )
        assert c.category == CompetitorCategory.AGENTIC_CLINICAL_AI

    def test_invalid_category_rejected(self) -> None:
        with pytest.raises(ValidationError):
            CompetitorRef(
                id="optimizerx",
                name="OptimizeRx",
                tier=CompetitorTier.TIER_1,
                category="not_a_category",  # type: ignore[arg-type]
            )


class TestCompetitorCategory:
    def test_all_categories_have_display_names(self) -> None:
        # Every enum value should resolve to a human-readable label.
        for cat in CompetitorCategory:
            label = category_display_name(cat)
            assert isinstance(label, str)
            assert len(label) > 0
            # Display names are NOT snake_case (they're titles).
            assert label != cat.value

    def test_display_name_accepts_string(self) -> None:
        assert category_display_name("agentic_clinical_ai") == "Agentic Clinical AI"

    def test_display_name_unknown_returns_input(self) -> None:
        assert category_display_name("unknown_category") == "unknown_category"

    def test_no_duplicate_display_names(self) -> None:
        labels = [category_display_name(cat) for cat in CompetitorCategory]
        assert len(set(labels)) == len(labels), f"duplicate labels: {labels}"


class TestSourceRef:
    def test_valid(self) -> None:
        s = SourceRef(
            rank=1,
            competitor="optimizerx",
            url="https://www.optimizerx.com/",
            source_type=SourceType.HOMEPAGE,
            collection_method=CollectionMethod.CRAWLER,
        )
        assert s.rank == 1
        assert s.source_type == SourceType.HOMEPAGE

    def test_rejects_unknown_source_type(self) -> None:
        with pytest.raises(ValidationError):
            SourceRef(
                rank=1,
                competitor="optimizerx",
                url="https://www.optimizerx.com/",
                source_type="linkedin_company_page",  # excluded by SCOPE_LOCK
                collection_method=CollectionMethod.CRAWLER,
            )

    def test_invalid_url_rejected(self) -> None:
        with pytest.raises(ValidationError):
            SourceRef(
                rank=1,
                competitor="optimizerx",
                url="not-a-url",
                source_type=SourceType.HOMEPAGE,
                collection_method=CollectionMethod.CRAWLER,
            )

    def test_rank_must_be_positive(self) -> None:
        with pytest.raises(ValidationError):
            SourceRef(
                rank=0,
                competitor="optimizerx",
                url="https://www.optimizerx.com/",
                source_type=SourceType.HOMEPAGE,
                collection_method=CollectionMethod.CRAWLER,
            )


# ========== Finding (the main contract) ==========


class TestFindingValid:
    def test_minimal_valid_finding(self, valid_finding_kwargs: dict) -> None:
        f = Finding(**valid_finding_kwargs)
        assert f.competitor == "deepintent"
        assert f.raw_severity == 4
        assert f.status == FindingStatus.DRAFT  # default
        assert f.crossvalidation_disagreement is False  # default
        assert f.crossvalidation_skipped is False  # default
        assert f.final_severity is None  # default
        assert f.final_confidence is None  # default

    def test_effective_severity_falls_back_to_raw(self, valid_finding_kwargs: dict) -> None:
        f = Finding(**valid_finding_kwargs)
        assert f.effective_severity == 4
        assert f.effective_confidence == 4

    def test_effective_severity_uses_final_when_set(self, valid_finding_kwargs: dict) -> None:
        f = Finding(**valid_finding_kwargs, final_severity=3, final_confidence=2)
        assert f.effective_severity == 3
        assert f.effective_confidence == 2

    def test_alert_eligible_requires_sev5_and_verified(self, valid_finding_kwargs: dict) -> None:
        # raw_severity=4, status=DRAFT -> not alert eligible
        f = Finding(**valid_finding_kwargs)
        assert f.is_alert_eligible is False

        # final_severity=5 but still DRAFT -> not eligible
        f.final_severity = 5
        assert f.is_alert_eligible is False

        # final_severity=5 and VERIFIED -> eligible
        f.status = FindingStatus.VERIFIED
        assert f.is_alert_eligible is True

        # KEPT also eligible
        f.status = FindingStatus.KEPT
        assert f.is_alert_eligible is True

    def test_unmapped_finding_has_empty_products(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["products"] = []
        f = Finding(**valid_finding_kwargs)
        assert f.products == []

    def test_published_at_optional(self, valid_finding_kwargs: dict) -> None:
        f = Finding(**valid_finding_kwargs)
        assert f.published_at is None

        valid_finding_kwargs["published_at"] = NOW_UTC - timedelta(hours=2)
        f = Finding(**valid_finding_kwargs)
        assert f.published_at is not None

    def test_assignment_revalidates(self, valid_finding_kwargs: dict) -> None:
        """validate_assignment=True means setattr re-runs validators."""
        f = Finding(**valid_finding_kwargs)
        with pytest.raises(ValidationError):
            f.raw_severity = 6  # type: ignore[assignment]


class TestFindingInvalid:
    def test_missing_required_field(self, valid_finding_kwargs: dict) -> None:
        del valid_finding_kwargs["competitor"]
        with pytest.raises(ValidationError) as exc:
            Finding(**valid_finding_kwargs)
        assert "competitor" in str(exc.value)

    @pytest.mark.parametrize("bad_severity", [0, 6, -1, 99])
    def test_severity_out_of_range(self, valid_finding_kwargs: dict, bad_severity: int) -> None:
        valid_finding_kwargs["raw_severity"] = bad_severity
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    @pytest.mark.parametrize("bad_confidence", [0, 6, -1])
    def test_confidence_out_of_range(self, valid_finding_kwargs: dict, bad_confidence: int) -> None:
        valid_finding_kwargs["raw_confidence"] = bad_confidence
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_invalid_url(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["url"] = "not://a real url with spaces"
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_url_must_be_http_or_https(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["url"] = "ftp://files.optimizerx.com/data.zip"
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_naive_datetime_rejected(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["captured_at"] = datetime.now()  # naive!
        with pytest.raises(ValidationError) as exc:
            Finding(**valid_finding_kwargs)
        assert "timezone-aware" in str(exc.value)

    def test_naive_published_at_rejected(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["published_at"] = datetime.now()  # naive!
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_competitor_must_be_snake_case(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["competitor"] = "DeepIntent"
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_competitor_no_hyphen(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["competitor"] = "deep-intent"
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_products_must_be_unique(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["products"] = ["reptwin", "reptwin"]
        with pytest.raises(ValidationError) as exc:
            Finding(**valid_finding_kwargs)
        assert "duplicates" in str(exc.value)

    def test_product_id_must_be_snake_case(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["products"] = ["RepTwin"]
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_unknown_source_type_rejected(self, valid_finding_kwargs: dict) -> None:
        # SCOPE_LOCK forbids LinkedIn — not in SourceType enum
        valid_finding_kwargs["source_type"] = "linkedin_company_page"
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_extra_fields_forbidden(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["unauthorized_field"] = "should be rejected"
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_finding_id_too_short(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["finding_id"] = "abc"  # min_length=8
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_summary_too_short(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["summary"] = "short"  # min_length=10
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_evidence_quote_required(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["evidence_quote"] = ""
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)


class TestFindingStatusEnum:
    def test_all_lifecycle_states_present(self) -> None:
        # Sanity check the state machine has every lifecycle state the
        # build plan / error matrix references. Sprint 8 added the two
        # adversarial-rejection states.
        names = {s.name for s in FindingStatus}
        assert names == {
            "DRAFT",
            "VERIFIED",
            "KEPT",
            "DEMOTED",
            "REJECTED_URL",
            "REJECTED_DEDUPE",
            "REJECTED_INVALID",
            "REJECTED_ATTRIBUTION",
            "REJECTED_ADVERSARIAL",
        }


class TestFindingSprint8Additions:
    """Sprint 8 added category, canonical_url, publisher_domain, decomposed
    confidence, and adversarial verdict fields. All are optional for back-
    compat with pre-Sprint-8 callers."""

    def test_new_fields_default_none(self, valid_finding_kwargs: dict) -> None:
        f = Finding(**valid_finding_kwargs)
        assert f.category is None
        assert f.canonical_url is None
        assert f.publisher_domain is None
        assert f.attribution_confidence is None
        assert f.extraction_confidence is None
        assert f.severity_confidence is None
        assert f.attribution_verdict is None
        assert f.attribution_reason is None
        assert f.severity_verdict is None
        assert f.severity_after_adversarial is None
        assert f.adversarial_reason is None

    def test_category_snake_case_enforced(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["category"] = "Agentic_AI"  # Capital
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_category_accepts_valid_value(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["category"] = "agentic_clinical_ai"
        f = Finding(**valid_finding_kwargs)
        assert f.category == "agentic_clinical_ai"

    def test_canonical_url_optional(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["canonical_url"] = "https://hippocraticai.com/news/polaris-5"
        f = Finding(**valid_finding_kwargs)
        assert str(f.canonical_url).startswith("https://hippocraticai.com")

    def test_publisher_domain(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["publisher_domain"] = "hippocraticai.com"
        f = Finding(**valid_finding_kwargs)
        assert f.publisher_domain == "hippocraticai.com"

    def test_attribution_verdict_canonical_values(
        self, valid_finding_kwargs: dict
    ) -> None:
        for v in ("yes", "no", "unclear"):
            valid_finding_kwargs["attribution_verdict"] = v
            f = Finding(**valid_finding_kwargs)
            assert f.attribution_verdict == v

    def test_attribution_verdict_invalid_rejected(
        self, valid_finding_kwargs: dict
    ) -> None:
        valid_finding_kwargs["attribution_verdict"] = "maybe"
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_severity_verdict_canonical_values(
        self, valid_finding_kwargs: dict
    ) -> None:
        for v in ("kept", "demoted", "rejected"):
            valid_finding_kwargs["severity_verdict"] = v
            f = Finding(**valid_finding_kwargs)
            assert f.severity_verdict == v

    def test_severity_verdict_invalid_rejected(
        self, valid_finding_kwargs: dict
    ) -> None:
        valid_finding_kwargs["severity_verdict"] = "approve"
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_decomposed_confidence_range(self, valid_finding_kwargs: dict) -> None:
        valid_finding_kwargs["attribution_confidence"] = 6  # out of range
        with pytest.raises(ValidationError):
            Finding(**valid_finding_kwargs)

    def test_effective_confidence_uses_min_of_decomposed(
        self, valid_finding_kwargs: dict
    ) -> None:
        # Decomposed confidence: extraction=5, attribution=2, severity=4 -> min=2
        valid_finding_kwargs["raw_confidence"] = 5
        valid_finding_kwargs["extraction_confidence"] = 5
        valid_finding_kwargs["attribution_confidence"] = 2
        valid_finding_kwargs["severity_confidence"] = 4
        f = Finding(**valid_finding_kwargs)
        assert f.effective_confidence == 2

    def test_effective_confidence_falls_back_to_raw_when_no_decomposed(
        self, valid_finding_kwargs: dict
    ) -> None:
        valid_finding_kwargs["raw_confidence"] = 4
        f = Finding(**valid_finding_kwargs)
        assert f.effective_confidence == 4

    def test_effective_severity_uses_after_adversarial_when_set(
        self, valid_finding_kwargs: dict
    ) -> None:
        valid_finding_kwargs["raw_severity"] = 4
        valid_finding_kwargs["severity_after_adversarial"] = 2
        f = Finding(**valid_finding_kwargs)
        assert f.effective_severity == 2

    def test_effective_severity_final_overrides_adversarial(
        self, valid_finding_kwargs: dict
    ) -> None:
        # final_severity wins over severity_after_adversarial.
        valid_finding_kwargs["raw_severity"] = 4
        valid_finding_kwargs["severity_after_adversarial"] = 2
        valid_finding_kwargs["final_severity"] = 3
        f = Finding(**valid_finding_kwargs)
        assert f.effective_severity == 3

    def test_display_url_prefers_canonical(
        self, valid_finding_kwargs: dict
    ) -> None:
        valid_finding_kwargs["url"] = (
            "https://news.google.com/rss/articles/CBMiabc123def"
        )
        valid_finding_kwargs["canonical_url"] = "https://hippocraticai.com/news/x"
        f = Finding(**valid_finding_kwargs)
        assert f.display_url == "https://hippocraticai.com/news/x"

    def test_display_url_falls_back_to_url(self, valid_finding_kwargs: dict) -> None:
        f = Finding(**valid_finding_kwargs)
        assert f.display_url == str(f.url)


class TestFindingStatusSprint8Additions:
    def test_new_rejection_states_present(self) -> None:
        names = {s.name for s in FindingStatus}
        assert "REJECTED_ATTRIBUTION" in names
        assert "REJECTED_ADVERSARIAL" in names


class TestRoundTripJSON:
    """Findings must serialize to JSON cleanly — they're written to JSONL
    archives daily (T7) and pinned in pytest-recording cassettes."""

    def test_round_trip(self, valid_finding_kwargs: dict) -> None:
        f1 = Finding(**valid_finding_kwargs)
        as_json = f1.model_dump_json()
        f2 = Finding.model_validate_json(as_json)
        assert f1 == f2

    def test_url_serializes_as_string(self, valid_finding_kwargs: dict) -> None:
        f = Finding(**valid_finding_kwargs)
        d = f.model_dump(mode="json")
        assert isinstance(d["url"], str)
        assert d["url"].startswith("https://")

    def test_datetime_serializes_iso(self, valid_finding_kwargs: dict) -> None:
        f = Finding(**valid_finding_kwargs)
        d = f.model_dump(mode="json")
        # ISO 8601 with timezone
        assert "T" in d["captured_at"]
        assert d["captured_at"].endswith(("+00:00", "Z"))
