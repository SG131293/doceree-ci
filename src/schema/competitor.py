"""Competitor reference model, tier enum, and market-category enum.

Aligned with `config/competitors.yaml` group structure: tier_1, tier_2_mvp_cohort,
healthcare_ai_cluster.

Tiers describe monitoring cadence (Tier-1 = daily, Tier-2 = weekly).
Categories describe what *market* a competitor competes in — orthogonal to tier.
The render layer groups findings by `category` (HCP Marketing Platform,
Healthcare DSP, Agentic Clinical AI, etc.) so Sherry can scan the digest by
strategic theme rather than by raw competitor name.
"""
from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CompetitorTier(StrEnum):
    """Competitor groups in config/competitors.yaml.

    Matches master PRD Section 2 (Competitor Tiering Framework) plus the
    build-plan-mandated healthcare-AI-agents cluster.
    """

    TIER_1 = "tier_1"
    TIER_2_MVP_COHORT = "tier_2_mvp_cohort"
    HEALTHCARE_AI_CLUSTER = "healthcare_ai_cluster"


class CompetitorCategory(StrEnum):
    """Market category groupings for the digest renderer.

    Each competitor in competitors.yaml carries exactly one `category`. The
    renderer groups findings by category in the "By Competitor Category"
    section so Sherry can scan the strategic landscape by theme instead of
    by individual vendor name.

    Display labels live in `category_display_name()` below — the StrEnum
    values stay snake_case for round-trip safety.
    """

    AGENTIC_CLINICAL_AI = "agentic_clinical_ai"
    HEALTHCARE_DSP = "healthcare_dsp"
    HEALTHCARE_DATA_ANALYTICS = "healthcare_data_analytics"
    HCP_MARKETING_PLATFORM = "hcp_marketing_platform"
    HCP_PUBLISHER_DESTINATION = "hcp_publisher_destination"
    PATIENT_ACCESS_COUPON = "patient_access_coupon"
    DOOH_POC_NETWORK = "dooh_poc_network"
    PHARMACY_SOFTWARE = "pharmacy_software"
    B2B_ABM = "b2b_abm"
    EHR_WORKFLOW = "ehr_workflow"


_CATEGORY_DISPLAY_NAMES: dict[CompetitorCategory, str] = {
    CompetitorCategory.AGENTIC_CLINICAL_AI: "Agentic Clinical AI",
    CompetitorCategory.HEALTHCARE_DSP: "Healthcare DSP / Programmatic",
    CompetitorCategory.HEALTHCARE_DATA_ANALYTICS: "Healthcare Data & Analytics",
    CompetitorCategory.HCP_MARKETING_PLATFORM: "HCP Marketing Platform",
    CompetitorCategory.HCP_PUBLISHER_DESTINATION: "HCP Publisher / Destination",
    CompetitorCategory.PATIENT_ACCESS_COUPON: "Patient Access / Coupon",
    CompetitorCategory.DOOH_POC_NETWORK: "DOOH / Point-of-Care Network",
    CompetitorCategory.PHARMACY_SOFTWARE: "Pharmacy Software",
    CompetitorCategory.B2B_ABM: "ABM (Generic B2B)",
    CompetitorCategory.EHR_WORKFLOW: "EHR Workflow",
}


def category_display_name(category: CompetitorCategory | str) -> str:
    """Human-readable label for a category. Used by the renderer."""
    if isinstance(category, str):
        try:
            category = CompetitorCategory(category)
        except ValueError:
            return category  # unknown - render as-is
    return _CATEGORY_DISPLAY_NAMES.get(category, str(category))


class CompetitorRef(BaseModel):
    """Reference to a competitors.yaml entry.

    Carries just enough to render in a digest card (id, name, tier, category)
    without requiring the full competitor object (which is heavyweight:
    rss_feeds, sitemaps, related_doceree_products, etc.).
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(
        min_length=1,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Snake-case ID matching config/competitors.yaml.",
    )
    name: str = Field(min_length=1, max_length=200)
    tier: CompetitorTier
    category: CompetitorCategory | None = Field(
        default=None,
        description="Market category for digest grouping. Optional for back-"
                    "compat with code paths that pre-date Sprint 8.",
    )
