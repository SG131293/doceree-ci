"""Tests for `render.render`. Pure function tests, no mocks."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from render.render import render_plaintext, render_subject
from schema import (
    CollectionMethod,
    Finding,
    FindingStatus,
    SourceType,
)


def _finding(
    *,
    competitor: str = "deepintent",
    title: str = "Test finding",
    raw_severity: int = 3,
    final_severity: int | None = None,
    products: list[str] | None = None,
) -> Finding:
    return Finding(
        finding_id="abc12345" + "0" * 24,
        url="https://www.deepintent.com/news/x",
        source_type=SourceType.PRESS_RELEASE,
        collection_method=CollectionMethod.RSS,
        competitor=competitor,
        title=title,
        summary="A short summary explaining what happened and why it matters.",
        evidence_quote="Verbatim quote from the source.",
        signal_type="product_launch",
        products=products if products is not None else [],
        raw_severity=raw_severity,
        raw_confidence=4,
        final_severity=final_severity,
        status=FindingStatus.VERIFIED,
        captured_at=datetime.now(timezone.utc),
    )


class TestRenderPlaintext:
    def test_empty_findings(self) -> None:
        body = render_plaintext([], run_date="2026-04-30")
        assert "Doceree CI" in body
        assert "0 findings" in body
        assert "No material updates today" in body

    def test_one_finding(self) -> None:
        body = render_plaintext([_finding()], run_date="2026-04-30")
        assert "1 findings across 1 competitors" in body
        assert "deepintent" in body
        assert "Test finding" in body
        assert "[Sev 3" in body  # severity badge
        assert "https://www.deepintent.com/news/x" in body

    def test_groups_by_competitor(self) -> None:
        findings = [
            _finding(competitor="deepintent", title="A"),
            _finding(competitor="optimizerx", title="B"),
            _finding(competitor="deepintent", title="C"),
        ]
        body = render_plaintext(findings, run_date="2026-04-30")
        # Each competitor appears in a header
        assert "== deepintent (2) ==" in body
        assert "== optimizerx (1) ==" in body

    def test_competitor_with_higher_severity_first(self) -> None:
        findings = [
            _finding(competitor="optimizerx", title="OptimizeRx low", raw_severity=2),
            _finding(competitor="deepintent", title="DeepIntent high", raw_severity=5),
        ]
        body = render_plaintext(findings, run_date="2026-04-30")
        # deepintent (sev-5) should appear before optimizerx (sev-2)
        di_idx = body.index("deepintent")
        ox_idx = body.index("optimizerx")
        assert di_idx < ox_idx

    def test_within_competitor_sort_by_severity(self) -> None:
        findings = [
            _finding(competitor="deepintent", title="lower-sev", raw_severity=2),
            _finding(competitor="deepintent", title="higher-sev", raw_severity=5),
        ]
        body = render_plaintext(findings, run_date="2026-04-30")
        higher_idx = body.index("higher-sev")
        lower_idx = body.index("lower-sev")
        assert higher_idx < lower_idx

    def test_uses_effective_severity(self) -> None:
        # raw=3, final=5 -> effective=5 should be the badge.
        body = render_plaintext(
            [_finding(raw_severity=3, final_severity=5)],
            run_date="2026-04-30",
        )
        assert "[Sev 5" in body
        assert "[Sev 3" not in body

    def test_products_rendered(self) -> None:
        body = render_plaintext(
            [_finding(products=["premium_programmatic", "next"])],
            run_date="2026-04-30",
        )
        assert "Products: premium_programmatic, next" in body

    def test_evidence_quote_rendered(self) -> None:
        body = render_plaintext([_finding()], run_date="2026-04-30")
        assert 'Evidence: "Verbatim quote from the source."' in body


class TestRenderSubject:
    def test_zero_findings(self) -> None:
        s = render_subject([], run_date="2026-04-30")
        assert "no findings" in s
        assert "2026-04-30" in s

    def test_n_findings(self) -> None:
        findings = [_finding(raw_severity=2) for _ in range(3)]
        s = render_subject(findings, run_date="2026-04-30")
        assert "3 findings" in s

    def test_sev5_flagged_in_subject(self) -> None:
        findings = [_finding(raw_severity=2), _finding(raw_severity=5)]
        s = render_subject(findings, run_date="2026-04-30")
        assert "URGENT" in s

    def test_sev4_flagged_in_subject(self) -> None:
        findings = [_finding(raw_severity=2), _finding(raw_severity=4)]
        s = render_subject(findings, run_date="2026-04-30")
        assert "sev-4+" in s

    def test_sev5_takes_precedence_over_sev4(self) -> None:
        findings = [
            _finding(raw_severity=4),
            _finding(raw_severity=5),
        ]
        s = render_subject(findings, run_date="2026-04-30")
        assert "URGENT" in s
        assert "sev-4+" not in s

    def test_uses_effective_severity(self) -> None:
        # raw=2, final=5 -> URGENT
        findings = [_finding(raw_severity=2, final_severity=5)]
        s = render_subject(findings, run_date="2026-04-30")
        assert "URGENT" in s
