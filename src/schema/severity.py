"""Finding severity enum (1-5).

Aligned with master PRD severity guidance and the build plan's deterministic
severity-floor logic in config/severity-rules.yaml (added Day 10).
"""
from __future__ import annotations

from enum import IntEnum


class Severity(IntEnum):
    """Finding severity. Higher = more strategic urgency.

    1 - Informational. Low signal-to-noise; archive only.
    2 - Notable. Worth tracking, no immediate action.
    3 - Material. PMM should review this week.
    4 - Strategic. Sherry should review today; potential CEO/Sales relevance.
        Goes through GPT-5-nano cross-validation (T4c).
    5 - Urgent. Immediate Telegram alert; battlecard impact.
        Reserved for Doceree-named comparison pages, major M&A, etc.
        Goes through GPT-5-nano cross-validation (T4c).
    """

    INFORMATIONAL = 1
    NOTABLE = 2
    MATERIAL = 3
    STRATEGIC = 4
    URGENT = 5

    @classmethod
    def is_alert_eligible(cls, value: int) -> bool:
        """Sev 5 fires Telegram alerts (per build plan hourly_sev5 fast path)."""
        return value == cls.URGENT.value

    @classmethod
    def needs_crossvalidation(cls, value: int) -> bool:
        """Sev 4 and 5 go through GPT-5-nano cross-validation."""
        return value in (cls.STRATEGIC.value, cls.URGENT.value)
