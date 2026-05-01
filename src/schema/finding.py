"""Canonical Finding contract.

Every pipeline stage produces or consumes Finding instances:

  T1 ingest         -> raw items (NOT Findings yet — items become Findings at T3)
  T2 filter         -> filtered items (Flash-Lite drops noise)
  T3 extract        -> Finding(status=DRAFT, raw_severity, raw_confidence, ...)
  T4a verify URL    -> drops on non-200
  T4b adversarial   -> may demote raw_severity
  T4c crossvalidate -> sets crossvalidation_disagreement / crossvalidation_skipped
  T4d dedupe        -> drops or kept
  T4e signal-map    -> sets products[]
  T4f severity rules-> sets final_severity / final_confidence
  T5/T6 synthesis   -> reads Finding[] (does not modify)
  T7 render         -> reads Finding[] for HTML + JSONL
  T8 deliver        -> reads Finding[] for Telegram alerts (final_severity == 5)

Master PRD validation rules (Section 12.1) require: competitor, signal_type,
title, summary, evidence (here: url + evidence_quote), severity, confidence,
status, products mapping (or empty list = unmapped).

Sprint 8 additions (Day 8):
- `category` lifts the competitor's market category onto the Finding for
  digest grouping (Agentic Clinical AI, HCP Marketing Platform, etc.).
- `canonical_url` and `publisher_domain` carry the resolved publisher URL
  when the source URL is a Google News redirect or similar wrapper.
- `attribution_confidence`, `extraction_confidence`, `severity_confidence`
  decompose the legacy single `raw_confidence` into three independent signals
  so the email can show the weakest link rather than averaging it away.
- `attribution_verdict` / `attribution_reason` come from stage 4a (Flash
  attribution check). `severity_verdict` / `severity_after_adversarial` /
  `adversarial_reason` come from stage 4b (Pro severity check).

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 3 + Day 8.
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from .source import CollectionMethod, SourceType


class FindingStatus(StrEnum):
    """Lifecycle state of a finding through the pipeline."""

    DRAFT = "draft"  # T3 just emitted it; not yet verified
    VERIFIED = "verified"  # T4 passed all sub-stages; ready for synthesis
    KEPT = "kept"  # T7 included in digest
    DEMOTED = "demoted"  # T4 demoted but kept (e.g., crossvalidation_disagreement)
    REJECTED_URL = "rejected_url"  # T4a non-200 (logged to hallucinated_urls.jsonl)
    REJECTED_DEDUPE = "rejected_dedupe"  # T4d already in last 30d archive
    REJECTED_INVALID = "rejected_invalid"  # malformed JSON / schema violation
    REJECTED_ATTRIBUTION = "rejected_attribution"  # T4a (Sprint 8): wrong subject
    REJECTED_ADVERSARIAL = "rejected_adversarial"  # T4b (Sprint 8): Pro rejected


# Reusable score type: 1-5 inclusive. Used for both severity and confidence.
ScoreLevel = Annotated[int, Field(ge=1, le=5)]


# Adversarial verdict literals. Free-form str on the model (not enum-constrained)
# because Sprint 8 may evolve the verdict vocabulary; documenting the canonical
# values here keeps callers honest.
ATTRIBUTION_VERDICTS = ("yes", "no", "unclear")
SEVERITY_VERDICTS = ("kept", "demoted", "rejected")


class Finding(BaseModel):
    """Canonical Finding contract.

    Two parallel scoring fields:
      raw_severity   -> LLM's initial assessment (T3 extract output)
      final_severity -> after deterministic_floors and crossvalidation
                        adjustments (T4f). None until T4 runs.

    The same pattern applies to raw_confidence / final_confidence.

    `products` is an empty list for unmapped/category-level findings (per
    master PRD 12.1). Downstream consumers should treat empty as "render
    in a Cross-Product Strategic section" rather than "drop".
    """

    model_config = ConfigDict(
        extra="forbid",  # reject unknown fields - pin the contract tightly
        str_strip_whitespace=True,
        validate_assignment=True,  # rerun validators on attribute mutation
    )

    # --- Identity ---
    finding_id: str = Field(
        min_length=8,
        max_length=128,
        description="Deterministic hash (e.g., SHA-256 hex prefix) of url + "
                    "content_hash. Used for dedup against 30-day archive (T4d).",
    )

    # --- Source attribution ---
    url: HttpUrl
    canonical_url: HttpUrl | None = Field(
        default=None,
        description="Resolved publisher URL when `url` is a Google News redirect "
                    "or similar wrapper. None if `url` is already canonical.",
    )
    publisher_domain: str | None = Field(
        default=None,
        max_length=255,
        description="eTLD+1 of canonical_url (or url if no redirect). Drives "
                    "the 'Source: hippocraticai.com' line in the digest and "
                    "the url_health domain-match check in T4a.",
    )
    source_type: SourceType
    collection_method: CollectionMethod
    competitor: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="competitor.id from config/competitors.yaml.",
    )
    category: str | None = Field(
        default=None,
        max_length=64,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Competitor market category lifted from competitors.yaml. "
                    "Used by render to group findings by strategic theme. "
                    "Optional because pre-Sprint-8 findings may not have it.",
    )

    # --- Content ---
    title: str = Field(min_length=1, max_length=500)
    summary: str = Field(
        min_length=10,
        max_length=4000,
        description="LLM-extracted summary. Rendered as the card body.",
    )
    evidence_quote: str = Field(
        min_length=1,
        max_length=2000,
        description="Verbatim quote from the source supporting the finding. "
                    "Used by adversarial-check (T4b) and rendered in cards.",
    )

    # --- Classification ---
    signal_type: str = Field(
        min_length=1,
        max_length=64,
        description="Free-form signal_type label from config/signal-mapping.yaml. "
                    "Not enum-constrained because rules evolve weekly.",
    )
    products: list[str] = Field(
        default_factory=list,
        description="product.id values from config/products.yaml. Empty = "
                    "unmapped/category-level (per master PRD 12.1).",
    )

    # --- Scoring (raw, from T3) ---
    raw_severity: ScoreLevel = Field(description="LLM's initial severity (T3 extract).")
    raw_confidence: ScoreLevel = Field(description="LLM's initial confidence (T3 extract).")

    # --- Confidence decomposition (Sprint 8) ---
    extraction_confidence: ScoreLevel | None = Field(
        default=None,
        description="Confidence that title/summary/evidence faithfully reflect "
                    "the source. Set at extract time.",
    )
    attribution_confidence: ScoreLevel | None = Field(
        default=None,
        description="Confidence that `competitor` is the actual subject of the "
                    "article. Set by stage 4a (Flash attribution check).",
    )
    severity_confidence: ScoreLevel | None = Field(
        default=None,
        description="Confidence that the assigned severity is correct given the "
                    "evidence. Set by stage 4b (Pro severity check).",
    )

    # --- Adversarial outputs (Sprint 8) ---
    attribution_verdict: str | None = Field(
        default=None,
        max_length=16,
        description=f"Stage-4a verdict. Canonical values: {ATTRIBUTION_VERDICTS}.",
    )
    attribution_reason: str | None = Field(
        default=None,
        max_length=1000,
        description="Free-text reason from stage 4a when verdict != 'yes'.",
    )
    severity_verdict: str | None = Field(
        default=None,
        max_length=16,
        description=f"Stage-4b verdict. Canonical values: {SEVERITY_VERDICTS}.",
    )
    severity_after_adversarial: ScoreLevel | None = Field(
        default=None,
        description="Severity Pro would assign given the evidence (may equal "
                    "raw_severity if verdict=kept, or be lower if demoted).",
    )
    adversarial_reason: str | None = Field(
        default=None,
        max_length=2000,
        description="Free-text reasoning from stage 4b. Logged for audit even "
                    "when verdict=kept, so we can spot-check Pro's calls.",
    )

    # --- Scoring (final, from T4) ---
    final_severity: ScoreLevel | None = Field(
        default=None,
        description="Severity after deterministic_floors and adversarial-check "
                    "demotions (T4f). None until T4 runs.",
    )
    final_confidence: ScoreLevel | None = Field(
        default=None,
        description="Confidence after T4 adjustments. None until T4 runs.",
    )

    # --- Verification flags (T4 outputs) ---
    crossvalidation_disagreement: bool = Field(
        default=False,
        description="GPT-5-nano disagreed with confidence >= 4. Demotes "
                    "final_severity by 1 (minimum 3) and renders amber strip.",
    )
    crossvalidation_skipped: bool = Field(
        default=False,
        description="Cross-validation skipped (nano unavailable, or finding "
                    "is Sev <4 and not eligible). Renders 'skipped' chip.",
    )

    # --- Lifecycle ---
    status: FindingStatus = Field(default=FindingStatus.DRAFT)
    captured_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the raw item was ingested (T1). Always timezone-aware.",
    )
    published_at: datetime | None = Field(
        default=None,
        description="When the upstream source published the item (if known). "
                    "Used by filter (T2) to discard items >24h old.",
    )

    # ---- Validators ----

    @field_validator("captured_at", "published_at")
    @classmethod
    def timestamps_must_be_aware(cls, v: datetime | None) -> datetime | None:
        """All timestamps must be timezone-aware to avoid silent UTC drift."""
        if v is not None and v.tzinfo is None:
            raise ValueError("timestamps must be timezone-aware (use datetime.now(timezone.utc))")
        return v

    @field_validator("products")
    @classmethod
    def products_must_be_unique_and_valid_ids(cls, v: list[str]) -> list[str]:
        """Reject duplicate product IDs (would inflate per-product synth) and
        enforce snake_case. Cross-checking against products.yaml at runtime
        is the caller's responsibility (we don't load YAML here)."""
        if len(v) != len(set(v)):
            raise ValueError("products must not contain duplicates")
        for pid in v:
            if not pid or not pid[0].islower() or any(c.isupper() or c == "-" for c in pid):
                raise ValueError(f"product id '{pid}' must be snake_case (lowercase + underscores)")
        return v

    @field_validator("attribution_verdict")
    @classmethod
    def attribution_verdict_must_be_canonical(cls, v: str | None) -> str | None:
        if v is not None and v not in ATTRIBUTION_VERDICTS:
            raise ValueError(
                f"attribution_verdict must be one of {ATTRIBUTION_VERDICTS}, got {v!r}"
            )
        return v

    @field_validator("severity_verdict")
    @classmethod
    def severity_verdict_must_be_canonical(cls, v: str | None) -> str | None:
        if v is not None and v not in SEVERITY_VERDICTS:
            raise ValueError(
                f"severity_verdict must be one of {SEVERITY_VERDICTS}, got {v!r}"
            )
        return v

    # ---- Convenience properties ----

    @property
    def effective_severity(self) -> int:
        """final_severity if set, else severity_after_adversarial if set, else
        raw_severity. The score downstream consumers (render, deliver) should use."""
        if self.final_severity is not None:
            return self.final_severity
        if self.severity_after_adversarial is not None:
            return self.severity_after_adversarial
        return self.raw_severity

    @property
    def effective_confidence(self) -> int:
        """final_confidence if set, else weakest of the three decomposed
        confidence signals if any are set, else raw_confidence."""
        if self.final_confidence is not None:
            return self.final_confidence
        decomposed = [
            c for c in (
                self.extraction_confidence,
                self.attribution_confidence,
                self.severity_confidence,
            ) if c is not None
        ]
        if decomposed:
            return min(decomposed)
        return self.raw_confidence

    @property
    def display_url(self) -> str:
        """URL to show in the rendered digest. Prefers canonical_url over the
        raw (potentially Google News-wrapped) url."""
        return str(self.canonical_url) if self.canonical_url is not None else str(self.url)

    @property
    def is_alert_eligible(self) -> bool:
        """True iff effective_severity == 5 AND status not in rejected/draft.
        Hourly Sev-5 fast-path checks this before firing Telegram."""
        return self.effective_severity == 5 and self.status in (
            FindingStatus.VERIFIED,
            FindingStatus.KEPT,
        )
