"""Plaintext digest renderer.

Sprint 8 rewrites the renderer to match the structure Sherry asked for:

    Doceree CI Daily Digest - YYYY-MM-DD
    N findings · X sev-4+ · Y products impacted · Z categories

    === TODAY'S TOP MOVES (sev-4+) ===
    Full detail per finding (title, severity, category, impacts, summary,
    evidence quote, publisher source).

    === BY DOCEREE PRODUCT ===
    One block per product touched today. Includes the per_product synthesis
    paragraph + recommended action when available.

    === BY COMPETITOR CATEGORY ===
    One block per category. Bullet list of finding titles grouped by
    competitor within the category.

    === STRATEGIC SYNTHESIS ===
    The cross-product narrative + implied agenda from synth_strategic.

    === WATCHLIST (sev 1-2) ===
    Compact bullet list of low-severity findings the renderer didn't surface
    in the top section.

The renderer accepts optional `per_product` and `strategic` synthesis
inputs. When omitted (e.g., in a degraded run where Pro synthesis failed),
the relevant sections are skipped without breaking the digest.

Day 11 will add the matching HTML template; for now, plaintext only.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from jinja2 import Environment, StrictUndefined

from schema import (
    Finding,
    PerProductSynthesis,
    StrategicSynthesis,
    category_display_name,
)
from util.competitor_registry import get_name as get_competitor_name
from util.product_registry import get_name as get_product_name

_IST = ZoneInfo("Asia/Kolkata")


# --- Section thresholds ---

_TOP_MOVES_MIN_SEVERITY = 4  # sev-4 and sev-5 surface in TOP MOVES
_WATCHLIST_MAX_SEVERITY = 2  # sev-1 and sev-2 surface in WATCHLIST


# --- Helpers ---


def _competitor_label(competitor_id: str) -> str:
    """Friendly competitor name with id fallback."""
    return get_competitor_name(competitor_id) or competitor_id


def _product_label(product_id: str) -> str:
    """Friendly product name with id fallback."""
    return get_product_name(product_id) or product_id


def _category_label(category_id: str | None) -> str:
    if not category_id:
        return "Uncategorized"
    return category_display_name(category_id)


def _publisher_or_url(finding: Finding) -> str:
    """Compact source citation: prefer publisher domain, fall back to URL."""
    if finding.publisher_domain:
        return finding.publisher_domain
    return finding.display_url


def _count_distinct_products(findings: list[Finding]) -> int:
    s: set[str] = set()
    for f in findings:
        for p in f.products:
            s.add(p)
    return len(s)


def _count_distinct_categories(findings: list[Finding]) -> int:
    return len({f.category for f in findings if f.category})


def _count_distinct_competitors(findings: list[Finding]) -> int:
    return len({f.competitor for f in findings})


# --- Template ---

_PLAINTEXT_TEMPLATE = """\
Doceree CI Daily Digest - {{ run_date }}
{{ findings | length }} findings | {{ n_sev4plus }} sev-4+ | {{ n_products }} products impacted | {{ n_categories }} competitor categories | {{ n_competitors }} competitors

{%- if findings | length == 0 %}

No material updates today. (Pipeline ran successfully but produced no findings.)
{%- else %}
{%- if top_moves %}

=== TODAY'S TOP MOVES (sev-4+) ===
{%- for f in top_moves %}

{{ loop.index }}. {{ f.title }}
   Sev {{ f.effective_severity }} | Category: {{ category_label(f.category) }} | Competitor: {{ competitor_label(f.competitor) }}
   {%- if f.products %}
   Impacts: {{ f.products | map('product_label') | join(', ') }}
   {%- endif %}

   {{ f.summary }}

   Evidence: "{{ f.evidence_quote | truncate(400) }}"
   Source: {{ publisher_or_url(f) }} ({{ f.display_url }})
{%- endfor %}
{%- endif %}

{%- if by_product %}

=== BY DOCEREE PRODUCT ===
{%- for product_id, items in by_product.items() %}

{{ product_label(product_id) }} ({{ items | length }} finding{{ 's' if items|length != 1 else '' }})
   {%- if per_product and product_id in per_product %}
   {{ per_product[product_id].impact_summary | wordwrap(76) | indent(3) }}
   -> Action: {{ per_product[product_id].recommended_action | wordwrap(72) | indent(6) }}
   {%- else %}
   {%- for f in items %}
   - [Sev {{ f.effective_severity }}] {{ f.title }} ({{ competitor_label(f.competitor) }})
   {%- endfor %}
   {%- endif %}
{%- endfor %}
{%- endif %}

{%- if by_category %}

=== BY COMPETITOR CATEGORY ===
{%- for category_id, items in by_category.items() %}

{{ category_label(category_id) }} ({{ items | length }} finding{{ 's' if items|length != 1 else '' }})
   {%- for f in items %}
   - [Sev {{ f.effective_severity }}] {{ competitor_label(f.competitor) }}: {{ f.title }}
   {%- endfor %}
{%- endfor %}
{%- endif %}

{%- if strategic %}

=== STRATEGIC SYNTHESIS ===

{{ strategic.pattern | wordwrap(76) }}

Implied agenda: {{ strategic.implied_agenda | wordwrap(76) }}
{%- endif %}

{%- if watchlist %}

--- WATCHLIST (sev 1-2) ---
{%- for f in watchlist %}
- [Sev {{ f.effective_severity }}] {{ competitor_label(f.competitor) }}: {{ f.title }}
{%- endfor %}
{%- endif %}
{%- endif %}

--
Generated by doceree-ci at {{ generated_at_ist }} IST
"""


def _build_env() -> Environment:
    env = Environment(
        autoescape=False,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )
    # Register helpers as filters too, so they work with Jinja's `map(...)`
    # in addition to direct function calls in the template.
    env.filters["product_label"] = _product_label
    env.filters["competitor_label"] = _competitor_label
    env.filters["category_label"] = _category_label
    return env


def _split_top_moves_and_watchlist(
    findings: list[Finding],
) -> tuple[list[Finding], list[Finding]]:
    """Return (top_moves, watchlist).

    top_moves: sev >= 4, sorted by severity desc.
    watchlist: sev <= 2, sorted by severity desc then by title.
    Findings with sev=3 appear in neither (they show up only under
    By-Product and By-Category sections).
    """
    top_moves = sorted(
        (f for f in findings if f.effective_severity >= _TOP_MOVES_MIN_SEVERITY),
        key=lambda f: -f.effective_severity,
    )
    watchlist = sorted(
        (f for f in findings if f.effective_severity <= _WATCHLIST_MAX_SEVERITY),
        key=lambda f: (-f.effective_severity, f.title),
    )
    return top_moves, watchlist


def _group_by_product(findings: list[Finding]) -> dict[str, list[Finding]]:
    """Group findings by every Doceree product they impact.

    Same logic as pipeline.synth.group_findings_by_product but kept local
    to avoid an import cycle and because the renderer cares about *all*
    findings (not just verified ones).
    """
    by_product: dict[str, list[Finding]] = defaultdict(list)
    for f in findings:
        for pid in f.products:
            by_product[pid].append(f)
    for items in by_product.values():
        items.sort(key=lambda x: -x.effective_severity)
    sorted_pairs = sorted(
        by_product.items(),
        key=lambda kv: (
            -max((f.effective_severity for f in kv[1]), default=0),
            kv[0],
        ),
    )
    return dict(sorted_pairs)


def _group_by_category(findings: list[Finding]) -> dict[str, list[Finding]]:
    """Group findings by competitor category.

    Findings with no category fall under the synthetic 'uncategorized' key.
    Categories are ordered by max severity desc, ties broken alphabetically.
    """
    by_category: dict[str, list[Finding]] = defaultdict(list)
    for f in findings:
        key = f.category or "uncategorized"
        by_category[key].append(f)
    for items in by_category.values():
        items.sort(key=lambda x: (-x.effective_severity, x.competitor))
    sorted_pairs = sorted(
        by_category.items(),
        key=lambda kv: (
            -max((f.effective_severity for f in kv[1]), default=0),
            kv[0],
        ),
    )
    return dict(sorted_pairs)


def render_plaintext(
    findings: list[Finding],
    *,
    per_product: dict[str, PerProductSynthesis] | None = None,
    strategic: StrategicSynthesis | None = None,
    run_date: str | None = None,
) -> str:
    """Render the plaintext daily digest.

    Args:
        findings: Today's verified findings (post-adversarial). Findings
            rejected by stage 4b should be excluded by the caller before
            passing in.
        per_product: Optional dict from synth_per_product_batch. When
            provided, the BY DOCEREE PRODUCT section uses Pro's impact
            paragraphs; when None, the section falls back to a bullet list.
        strategic: Optional synth_strategic output. When None, the STRATEGIC
            SYNTHESIS section is omitted.
        run_date: ISO date for the header. Defaults to today in IST.

    Returns:
        Plaintext digest body, ready for `gmail.send_message(plaintext=...)`.
    """
    now_ist = datetime.now(timezone.utc).astimezone(_IST)
    run_date = run_date or now_ist.date().isoformat()

    top_moves, watchlist = _split_top_moves_and_watchlist(findings)
    by_product = _group_by_product(findings)
    by_category = _group_by_category(findings)

    n_sev4plus = sum(1 for f in findings if f.effective_severity >= 4)
    n_products = _count_distinct_products(findings)
    n_categories = _count_distinct_categories(findings)
    n_competitors = _count_distinct_competitors(findings)

    env = _build_env()
    template = env.from_string(_PLAINTEXT_TEMPLATE)
    return template.render(
        findings=findings,
        top_moves=top_moves,
        watchlist=watchlist,
        by_product=by_product,
        by_category=by_category,
        per_product=per_product or {},
        strategic=strategic,
        n_sev4plus=n_sev4plus,
        n_products=n_products,
        n_categories=n_categories,
        n_competitors=n_competitors,
        run_date=run_date,
        generated_at_ist=now_ist.strftime("%Y-%m-%d %H:%M"),
        # Helper functions exposed to the template.
        competitor_label=_competitor_label,
        product_label=_product_label,
        category_label=_category_label,
        publisher_or_url=_publisher_or_url,
    )


def render_subject(findings: list[Finding], *, run_date: str | None = None) -> str:
    """Build the email subject line.

    Format: 'Doceree CI - YYYY-MM-DD - N findings - X sev-4+ across Y products'
    Sherry triages from the subject alone without opening.
    """
    now_ist = datetime.now(timezone.utc).astimezone(_IST)
    run_date = run_date or now_ist.date().isoformat()
    n = len(findings)
    n_sev5 = sum(1 for f in findings if f.effective_severity == 5)
    n_sev4plus = sum(1 for f in findings if f.effective_severity >= 4)
    n_products = _count_distinct_products(findings)

    if n == 0:
        return f"Doceree CI - {run_date} - no findings"

    flag = ""
    if n_sev5 > 0:
        flag = f" - {n_sev5} URGENT"
    elif n_sev4plus > 0:
        flag = f" - {n_sev4plus} sev-4+"

    products_suffix = f" across {n_products} products" if n_products > 0 else ""
    return f"Doceree CI - {run_date} - {n} findings{flag}{products_suffix}"
