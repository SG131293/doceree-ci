"""Canonical schemas for the Doceree CI pipeline.

The `Finding` model is the contract every stage produces or consumes. The
supporting models (`ProductRef`, `CompetitorRef`, `SourceRef`) and enums
(`Severity`, `SourceType`, `CollectionMethod`, `CompetitorTier`,
`CompetitorCategory`, `JourneyStage`, `FindingStatus`) are imported here for
convenience.

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 3.
"""
from .competitor import (
    CompetitorCategory,
    CompetitorRef,
    CompetitorTier,
    category_display_name,
)
from .finding import Finding, FindingStatus
from .finding_draft import (
    AttributionCheck,
    FilterDecision,
    FindingDraft,
    PerProductSynthesis,
    SeverityAdversarialCheck,
    StrategicSynthesis,
)
from .product import JourneyStage, ProductRef
from .raw_item import RawItem
from .severity import Severity
from .source import CollectionMethod, SourceRef, SourceType

__all__ = [
    "AttributionCheck",
    "CollectionMethod",
    "CompetitorCategory",
    "CompetitorRef",
    "CompetitorTier",
    "FilterDecision",
    "Finding",
    "FindingDraft",
    "FindingStatus",
    "JourneyStage",
    "PerProductSynthesis",
    "ProductRef",
    "RawItem",
    "Severity",
    "SeverityAdversarialCheck",
    "SourceRef",
    "SourceType",
    "StrategicSynthesis",
    "category_display_name",
]
