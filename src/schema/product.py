"""Doceree product reference model and journey-stage enum.

Aligned with `config/products.yaml`. Master PRD reference: Section 2 (Product
Journey Map), Section 3 (Master Product Registry).
"""
from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class JourneyStage(StrEnum):
    """Doceree journey stages from master PRD Section 2.

    Demand-side stages (audience_matching through refills) flow left-to-right
    along the HCP journey. Supply-side stages (audience_prioritization, supply)
    are cross-product or publisher/EHR/PMS-vendor-facing.
    """

    AUDIENCE_MATCHING = "audience_matching"
    ACCOUNT_INFLUENCE = "account_influence"
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    INTERACTION = "interaction"
    CLINICAL_DECISION = "clinical_decision"
    ORCHESTRATION = "orchestration"
    MEASUREMENT = "measurement"
    ACCESS = "access"
    ACTIVATION = "activation"
    ADHERENCE = "adherence"
    REFILLS = "refills"
    AUDIENCE_PRIORITIZATION = "audience_prioritization"
    SUPPLY = "supply"


class ProductRef(BaseModel):
    """Reference to a products.yaml entry.

    Lightweight projection of a Doceree product. The full product record
    (claims, keywords, competitor refs) lives in config/products.yaml and
    is loaded on-demand by stages that need it (synth_per_product, render).
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(
        min_length=1,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Snake-case ID matching config/products.yaml.",
    )
    name: str = Field(min_length=1, max_length=200)
    journey_stages: list[JourneyStage] = Field(
        default_factory=list,
        description="One or more journey stages this product occupies.",
    )
