"""Tests for `render.render`. Pure function tests, no mocks.

Sprint 8 redesigned the digest structure. Tests assert on the new sections:
  - Header counts (findings, sev-4+, products, categories, competitors)
  - TOP MOVES (sev-4+)
  - BY DOCEREE PRODUCT
  - BY COMPETITOR CATEGORY
  - STRATEGIC SYNTHESIS (when synth provided)
  - WATCHLIST (sev 1-2)
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from render.render import render_plaintext, render_subject
from schema import (
    CollectionMethod,
    Finding,
    FindingStatus,
    PerProductSynthesis,
    SourceType,
    StrategicSynthesis,
)


def _finding(
    *,
    competitor: str = "deepintent",
    title: str = "Test finding",
    raw_severity: int = 3,
    final_severity: int | None = None,
    products: list[str] | None = None,
    category: str | None = None,
    publisher_domain: str | None = None,
) -> Finding:
    return Finding(
        finding_id="abc12345" + "0" * 24,
        url="https://www.deepintent.com/news/x",
        publisher_domain=publisher_domain,
        source_type=SourceType.PRESS_RELEASE,
        collection_method=CollectionMethod.RSS,
        competitor=competitor,
        category=category,
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


# =========================================================================
#  render_plaintext
# =========================================================================


class TestRenderPlaintextHeader:
    def test_empty_findings(self) -> None:
        body = render_plaintext([], run_date="2026-04-30")
        assert "Doceree CI" in body
        assert "0 findings" in body
        assert "No material updates today" in body

    def test_header_counts_with_findings(self) -> None:
        findings = [
            _finding(
                competitor="hippocratic_ai",
                title="A",
                raw_severity=4,
                products=["reptwin"],
                category="agentic_clinical_ai",
            ),
            _finding(
                competitor="optimizerx",
                title="B",
                raw_severity=2,
                products=["poc"],
                category="hcp_marketing_platform",
            ),
        ]
        body = render_plaintext(findings, run_date="2026-04-30")
        assert "2 findings" in body
        assert "1 sev-4+" in body
        assert "2 products" in body
        assert "2 competitor categories" in body
        assert "2 competitors" in body


class TestRenderTopMoves:
    def test_sev4_in_top_moves(self) -> None:
        body = render_plaintext(
            [_finding(raw_severity=4, title="Major launch")],
            run_date="2026-04-30",
        )
        assert "TODAY'S TOP MOVES" in body
        assert "Major launch" in body
        assert "Sev 4" in body

    def test_sev3_not_in_top_moves(self) -> None:
        # sev-3 is the "material" tier — appears under By Product / By Category
        # but not in the TOP MOVES headline section.
        body = render_plaintext(
            [_finding(raw_severity=3, title="Material move")],
            run_date="2026-04-30",
        )
        assert "TODAY'S TOP MOVES" not in body
        # But it's still in the digest somewhere.
        assert "Material move" in body

    def test_top_moves_sorted_by_severity_desc(self) -> None:
        findings = [
            _finding(raw_severity=4, title="Strategic A"),
            _finding(raw_severity=5, title="Urgent B"),
            _finding(raw_severity=4, title="Strategic C"),
        ]
        body = render_plaintext(findings, run_date="2026-04-30")
        urgent_idx = body.index("Urgent B")
        strat_a_idx = body.index("Strategic A")
        assert urgent_idx < strat_a_idx

    def test_evidence_in_top_moves(self) -> None:
        body = render_plaintext(
            [_finding(raw_severity=5)], run_date="2026-04-30"
        )
        assert 'Evidence: "Verbatim quote from the source."' in body

    def test_publisher_domain_shown_when_set(self) -> None:
        body = render_plaintext(
            [_finding(raw_severity=4, publisher_domain="hippocraticai.com")],
            run_date="2026-04-30",
        )
        assert "hippocraticai.com" in body


class TestRenderByProduct:
    def test_section_appears_when_findings_have_products(self) -> None:
        body = render_plaintext(
            [_finding(products=["reptwin"], raw_severity=4)],
            run_date="2026-04-30",
        )
        assert "BY DOCEREE PRODUCT" in body
        assert "RepTwin" in body  # product display name

    def test_section_omitted_when_no_findings_have_products(self) -> None:
        body = render_plaintext(
            [_finding(products=[], raw_severity=4)],
            run_date="2026-04-30",
        )
        assert "BY DOCEREE PRODUCT" not in body

    def test_product_synthesis_used_when_provided(self) -> None:
        per_product = {
            "reptwin": PerProductSynthesis(
                product_id="reptwin",
                impact_summary="Pressure on RepTwin from agentic AI launches.",
                recommended_action="Review RepTwin roadmap for evidence-based AI claims.",
            )
        }
        body = render_plaintext(
            [_finding(products=["reptwin"], raw_severity=4)],
            per_product=per_product,
            run_date="2026-04-30",
        )
        assert "Pressure on RepTwin from agentic AI launches" in body
        assert "Review RepTwin roadmap" in body
        assert "Action" in body

    def test_product_section_falls_back_to_bullets_without_synth(self) -> None:
        body = render_plaintext(
            [_finding(products=["reptwin"], raw_severity=4, title="Polaris launch")],
            run_date="2026-04-30",
        )
        # Without per_product synth, fall back to bullets of finding titles.
        assert "Polaris launch" in body


class TestRenderByCategory:
    def test_section_appears_with_category(self) -> None:
        body = render_plaintext(
            [_finding(category="agentic_clinical_ai", raw_severity=4)],
            run_date="2026-04-30",
        )
        assert "BY COMPETITOR CATEGORY" in body
        # Category display name (not the snake_case id).
        assert "Agentic Clinical AI" in body

    def test_category_groups_multiple_competitors(self) -> None:
        findings = [
            _finding(
                competitor="hippocratic_ai",
                category="agentic_clinical_ai",
                title="Polaris 5.0 launch",
                raw_severity=4,
            ),
            _finding(
                competitor="abridge",
                category="agentic_clinical_ai",
                title="Abridge Epic deal",
                raw_severity=3,
            ),
        ]
        body = render_plaintext(findings, run_date="2026-04-30")
        # Both findings appear in the same category block.
        assert "Polaris 5.0 launch" in body
        assert "Abridge Epic deal" in body


class TestRenderStrategic:
    def test_strategic_section_when_provided(self) -> None:
        # Use short strings so wordwrap doesn't split them mid-phrase across
        # lines — that's a real email-client rendering decision; the assertion
        # just cares that the content is present.
        strategic = StrategicSynthesis(
            pattern="Two findings cluster in clinical AI category today.",
            implied_agenda="Review RepTwin positioning.",
        )
        body = render_plaintext(
            [_finding(raw_severity=4)],
            strategic=strategic,
            run_date="2026-04-30",
        )
        assert "STRATEGIC SYNTHESIS" in body
        assert "Two findings cluster" in body
        assert "Implied agenda" in body
        assert "Review RepTwin" in body

    def test_strategic_section_omitted_when_none(self) -> None:
        body = render_plaintext(
            [_finding(raw_severity=4)],
            strategic=None,
            run_date="2026-04-30",
        )
        assert "STRATEGIC SYNTHESIS" not in body


class TestRenderWatchlist:
    def test_watchlist_for_sev1_2(self) -> None:
        body = render_plaintext(
            [
                _finding(raw_severity=1, title="Routine SEC filing"),
                _finding(raw_severity=2, title="Adjacent industry move"),
            ],
            run_date="2026-04-30",
        )
        assert "WATCHLIST" in body
        assert "Routine SEC filing" in body
        assert "Adjacent industry move" in body

    def test_no_watchlist_when_only_high_severity(self) -> None:
        body = render_plaintext(
            [_finding(raw_severity=5, title="Urgent")],
            run_date="2026-04-30",
        )
        assert "WATCHLIST" not in body


# =========================================================================
#  render_subject
# =========================================================================


class TestRenderSubject:
    def test_zero_findings(self) -> None:
        s = render_subject([], run_date="2026-04-30")
        assert "no findings" in s
        assert "2026-04-30" in s

    def test_n_findings(self) -> None:
        findings = [_finding(raw_severity=2) for _ in range(3)]
        s = render_subject(findings, run_date="2026-04-30")
        assert "3 findings" in s

    def test_sev5_flagged(self) -> None:
        findings = [_finding(raw_severity=2), _finding(raw_severity=5)]
        s = render_subject(findings, run_date="2026-04-30")
        assert "URGENT" in s

    def test_sev4_flagged(self) -> None:
        findings = [_finding(raw_severity=2), _finding(raw_severity=4)]
        s = render_subject(findings, run_date="2026-04-30")
        assert "sev-4+" in s

    def test_sev5_takes_precedence(self) -> None:
        findings = [_finding(raw_severity=4), _finding(raw_severity=5)]
        s = render_subject(findings, run_date="2026-04-30")
        assert "URGENT" in s
        assert "sev-4+" not in s

    def test_uses_effective_severity(self) -> None:
        findings = [_finding(raw_severity=2, final_severity=5)]
        s = render_subject(findings, run_date="2026-04-30")
        assert "URGENT" in s

    def test_products_count_when_present(self) -> None:
        findings = [
            _finding(raw_severity=4, products=["reptwin"]),
            _finding(raw_severity=4, products=["spark_for_ehrs"]),
        ]
        s = render_subject(findings, run_date="2026-04-30")
        # 2 distinct products.
        assert "across 2 products" in s

    def test_no_products_suffix_when_unmapped(self) -> None:
        findings = [_finding(raw_severity=4, products=[])]
        s = render_subject(findings, run_date="2026-04-30")
        assert "products" not in s
