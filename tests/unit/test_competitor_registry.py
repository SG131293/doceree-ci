"""Tests for `util.competitor_registry`. Loads the real competitors.yaml so
this file doubles as a smoke test that the YAML is shaped as expected after
Sprint 8 (every competitor has a `category`, etc.)."""
from __future__ import annotations

import pytest

from util import competitor_registry


@pytest.fixture(autouse=True)
def _reset_registry():
    """Clear the cache before each test so any in-flight monkey-patches don't
    leak between cases."""
    competitor_registry._REGISTRY = None  # type: ignore[attr-defined]
    yield
    competitor_registry._REGISTRY = None  # type: ignore[attr-defined]


class TestGetCompetitor:
    def test_returns_record_for_known_id(self) -> None:
        rec = competitor_registry.get_competitor("optimizerx")
        assert rec is not None
        assert rec["id"] == "optimizerx"
        assert rec["name"] == "OptimizeRx"

    def test_returns_none_for_unknown_id(self) -> None:
        assert competitor_registry.get_competitor("not_a_real_company") is None

    def test_records_carry_their_tier(self) -> None:
        rec = competitor_registry.get_competitor("optimizerx")
        assert rec is not None
        assert rec["_tier"] == "tier_1"

        rec_ai = competitor_registry.get_competitor("hippocratic_ai")
        assert rec_ai is not None
        assert rec_ai["_tier"] == "healthcare_ai_cluster"


class TestGetCategory:
    def test_known_categories(self) -> None:
        # A handful of spot-checks across tiers and categories. If these
        # break, the config edit went wrong.
        assert competitor_registry.get_category("optimizerx") == "hcp_marketing_platform"
        assert competitor_registry.get_category("deepintent") == "healthcare_dsp"
        assert competitor_registry.get_category("iqvia") == "healthcare_data_analytics"
        assert competitor_registry.get_category("hippocratic_ai") == "agentic_clinical_ai"
        assert competitor_registry.get_category("doximity") == "hcp_publisher_destination"
        assert competitor_registry.get_category("goodrx") == "patient_access_coupon"
        assert competitor_registry.get_category("redsail_technologies") == "pharmacy_software"
        assert competitor_registry.get_category("patientpoint") == "dooh_poc_network"
        assert competitor_registry.get_category("demandbase") == "b2b_abm"
        assert competitor_registry.get_category("veradigm") == "ehr_workflow"

    def test_unknown_competitor_returns_none(self) -> None:
        assert competitor_registry.get_category("not_a_real_company") is None


class TestEveryCompetitorHasCategory:
    def test_no_competitor_missing_category(self) -> None:
        """Every competitor in the registry must have a category (Sprint 8
        invariant). The renderer's grouping breaks if any are missing."""
        missing: list[str] = []
        for cid in competitor_registry.all_competitor_ids():
            if competitor_registry.get_category(cid) is None:
                missing.append(cid)
        assert missing == [], f"competitors missing `category`: {missing}"


class TestGetRelatedProducts:
    def test_returns_list_for_known_competitor(self) -> None:
        # OptimizeRx is mapped to several Doceree products in the YAML.
        products = competitor_registry.get_related_products("optimizerx")
        assert isinstance(products, list)
        assert "poc" in products

    def test_unknown_competitor_returns_empty_list(self) -> None:
        assert competitor_registry.get_related_products("not_a_real_company") == []


class TestGetName:
    def test_known(self) -> None:
        assert competitor_registry.get_name("hippocratic_ai") == "Hippocratic AI"

    def test_unknown(self) -> None:
        assert competitor_registry.get_name("not_a_real_company") is None
