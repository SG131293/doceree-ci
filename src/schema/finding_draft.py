"""FindingDraft: the LLM-fillable subset of a Finding.

The extract stage (T3) prompts Gemini Flash to fill these fields from a
RawItem. The runner then promotes a (RawItem, FindingDraft) pair into a full
Finding by adding the metadata the LLM cannot know (finding_id, source_type,
collection_method, competitor, captured_at, status).

Keeping Draft and Finding separate lets us:
  - Use FindingDraft as the `response_schema` for Gemini structured output
    without leaking pipeline-internal fields into the prompt context.
  - Apply provenance / lifecycle defaults deterministically rather than
    trusting the LLM to fill them.
"""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

ScoreLevel = Annotated[int, Field(ge=1, le=5)]


class FindingDraft(BaseModel):
    """LLM extract output. Promoted to a Finding by `pipeline.extract`."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    title: str = Field(min_length=1, max_length=500)
    summary: str = Field(min_length=10, max_length=4000)
    evidence_quote: str = Field(min_length=1, max_length=2000)
    signal_type: str = Field(min_length=1, max_length=64)
    products: list[str] = Field(default_factory=list, max_length=8)
    raw_severity: ScoreLevel
    raw_confidence: ScoreLevel


class FilterDecision(BaseModel):
    """LLM filter output. `keep=False` means the item is dropped from T2."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    keep: bool
    reason: str = Field(min_length=1, max_length=64)
