"""Canonical schemas for the Doceree CI pipeline.

The `Finding` model is the contract every stage produces or consumes. The
supporting models (`ProductRef`, `CompetitorRef`, `SourceRef`) and enums
(`Severity`, `SourceType`, `CollectionMethod`, `CompetitorTier`,
`JourneyStage`, `FindingStatus`) are imported here for convenience.

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 3.
"""
from .competitor import CompetitorRef, CompetitorTier
from .finding import Finding, FindingStatus
from .product import JourneyStage, ProductRef
from .severity import Severity
from .source import CollectionMethod, SourceRef, SourceType

__all__ = [
    "CollectionMethod",
    "CompetitorRef",
    "CompetitorTier",
    "Finding",
    "FindingStatus",
    "JourneyStage",
    "ProductRef",
    "Severity",
    "SourceRef",
    "SourceType",
]
