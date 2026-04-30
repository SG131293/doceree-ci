"""Competitor reference model and tier enum.

Aligned with `config/competitors.yaml` group structure: tier_1, tier_2_mvp_cohort,
healthcare_ai_cluster.
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


class CompetitorRef(BaseModel):
    """Reference to a competitors.yaml entry.

    Carries just enough to render in a digest card (id, name, tier) without
    requiring the full competitor object (which is heavyweight: rss_feeds,
    sitemaps, related_doceree_products, etc.).
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(
        min_length=1,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Snake-case ID matching config/competitors.yaml.",
    )
    name: str = Field(min_length=1, max_length=200)
    tier: CompetitorTier
