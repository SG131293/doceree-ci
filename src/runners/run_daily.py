"""Daily run orchestrator.

Pipeline (Sprint 8 layout):

    T1 ingest       -> RawItems from configured feeds
    T2 filter       -> Flash-Lite drops noise
    T4a attribution -> Flash drops misattributed items (Sprint 8)
    T3 extract      -> Flash promotes RawItem -> Finding
    T4b adversarial -> Pro challenges severity, may demote / reject (Sprint 8)
    T7 render       -> plaintext digest (renderer rewrite lands in 8f)
    T8 deliver      -> Gmail (or stdout in --dry-run)

Targets a small set of competitors per the build plan's Day-6 scope; will
expand once the source registry is fully RSS-ready.

For Day 6 / Sprint 8, RSS feeds are pulled from Google News with a per-
competitor query (`https://news.google.com/rss/search?q={query}+when:1d`).
This gives us real, fresh data without depending on competitor-specific
RSS endpoints that may or may not exist. Day 17 will transition to sitemap
diff against the 50-source registry.

CLI:
    python scripts/run_daily.py [--dry-run] [--send-to email] [--max-items N]

  --dry-run       Print the rendered digest to stdout; do not send Gmail.
  --send-to       Override recipient (defaults to GMAIL_USER_EMAIL).
  --max-items     Cap RSS items per competitor (defaults to 10).

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 6 + Day 8.
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from clients.gemini import GeminiClient
from clients.gmail import GmailClient
from clients.http import HttpClient
from pipeline.dedup import dedup_items
from pipeline.extract import extract_findings
from pipeline.filter import filter_items, kept
from pipeline.synth import synth_per_product_batch, synth_strategic
from pipeline.verify import (
    attach_attribution_to_finding,
    attribution_check_items,
    kept_after_attribution,
    kept_after_severity,
    severity_adversarial_findings,
)
from render.render import render_html, render_plaintext, render_subject
from schema.finding import Finding
from schema.source import SourceType
from sources.rss import fetch_rss

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CompetitorFeed:
    """One RSS feed bound to a competitor.id from competitors.yaml."""

    competitor: str
    name: str
    feed_url: str
    source_type: SourceType = SourceType.NEWSROOM


# Daily cohort: all competitors with monitoring_tier: direct from
# config/competitors.yaml, per docs/COMPETITION_BY_PRODUCT.md "High / Direct"
# product matrix. Polled via Google News RSS with `when:1d`.
# Attribution check (T4a) filters misattributed items.
#
# Why Google News (still): direct competitor newsroom RSS feeds don't exist
# for most healthcare vendors; sitemap-based ingest lands in a future sprint.
def _gnews_feed(query: str) -> str:
    """Encode a Google News RSS URL for an exact-phrase competitor query
    over the last 7 days.

    `query` is URL-encoded and wrapped in quotes for Google News exact-phrase
    matching. Uses `urllib.parse.quote` so compound names with punctuation
    (commas, slashes, ampersands) encode correctly.

    Why `when:7d` and not `when:1d`:
    Empirical observation from the 2026-05-10 run — `when:1d` returned ZERO
    entries for 24 of 35 competitors (DeepIntent, OptimizeRx, Veradigm,
    Hippocratic AI, etc.) even when those companies had posted news. Google
    News' freshness signal is unreliable for niche / B2B publishers because
    indexing lag and rank thresholds wipe out recent results. `when:7d` gives
    Google News a wider candidate pool to rank from. The pipeline then
    applies a strict 36-hour `max_age_hours` filter inside `fetch_rss` so we
    only process truly fresh items but do not lose them to the indexer's
    freshness opacity.

    Boolean OR is NOT supported in Google News RSS queries — it is treated
    as a literal search term. For disambiguation of generic company names
    (e.g. "Change Healthcare"), rely on the T4a attribution check stage
    rather than query-level operators.
    """
    phrase = quote(f'"{query}"', safe="")
    return f"https://news.google.com/rss/search?q={phrase}+when:7d&hl=en-US&gl=US&ceid=US:en"


# Daily cohort = all competitors with monitoring_tier: direct in competitors.yaml
# (per docs/COMPETITION_BY_PRODUCT.md "High / Direct" matrix). Variable name
# kept as DAY6_FEEDS for git-blame continuity.
#
# Notes on specific entries:
#   iqvia_digital  - query "IQVIA Digital" (formerly Lasso); distinct from "IQVIA"
#   synthio_labs   - small startup; low daily signal volume expected
#   roserx         - agentic pharma; low signal volume expected
#   google_ad_manager - infrastructure benchmark; search "Google Ad Manager"
#   relayhealth_change - search "Change Healthcare" (most news-visible name post-
#                        UnitedHealth acquisition)
#   relevate_health - "Relevate Health" search; confirms EHR campaign signals
#   checkedup      - small DOOH network; monitor for partnerships / POC wins
DAY6_FEEDS: tuple[CompetitorFeed, ...] = (
    # ── Healthcare DSP / Programmatic ─────────────────────────────────
    # Note: exact-phrase queries are the primary disambiguation layer.
    # Boolean OR is NOT supported in Google News RSS — extra terms must
    # be AND-only (each term narrows results). T4a attribution check
    # handles remaining false matches without inflating query complexity.
    CompetitorFeed(competitor="deepintent",        name="DeepIntent",        feed_url=_gnews_feed("DeepIntent")),
    CompetitorFeed(competitor="pulsepoint",        name="PulsePoint",        feed_url=_gnews_feed("PulsePoint")),
    CompetitorFeed(competitor="stackadapt",        name="StackAdapt",        feed_url=_gnews_feed("StackAdapt")),
    CompetitorFeed(competitor="trade_desk",        name="The Trade Desk",    feed_url=_gnews_feed("The Trade Desk")),
    CompetitorFeed(competitor="swoop",             name="Swoop",             feed_url=_gnews_feed("Swoop healthcare")),
    # ── Healthcare Data & Analytics ───────────────────────────────────
    CompetitorFeed(competitor="iqvia",             name="IQVIA",             feed_url=_gnews_feed("IQVIA")),
    CompetitorFeed(competitor="iqvia_digital",     name="IQVIA Digital",     feed_url=_gnews_feed("IQVIA Digital")),
    CompetitorFeed(competitor="komodo_health",     name="Komodo Health",     feed_url=_gnews_feed("Komodo Health")),
    CompetitorFeed(competitor="definitive_healthcare", name="Definitive Healthcare", feed_url=_gnews_feed("Definitive Healthcare")),
    # ── HCP Marketing Platform / POC / EHR ────────────────────────────
    CompetitorFeed(competitor="optimizerx",        name="OptimizeRx",        feed_url=_gnews_feed("OptimizeRx")),
    CompetitorFeed(competitor="veradigm",          name="Veradigm",          feed_url=_gnews_feed("Veradigm")),
    CompetitorFeed(competitor="relevate_health",   name="Relevate Health",   feed_url=_gnews_feed("Relevate Health")),
    # ── HCP Publisher / Destination ───────────────────────────────────
    CompetitorFeed(competitor="doximity",          name="Doximity",          feed_url=_gnews_feed("Doximity")),
    CompetitorFeed(competitor="medscape",          name="Medscape",          feed_url=_gnews_feed("Medscape")),
    CompetitorFeed(competitor="openevidence",      name="OpenEvidence",      feed_url=_gnews_feed("OpenEvidence")),
    # ── Patient Access / Coupon ───────────────────────────────────────
    CompetitorFeed(competitor="covermymeds",       name="CoverMyMeds",       feed_url=_gnews_feed("CoverMyMeds")),
    CompetitorFeed(competitor="connectiverx",      name="ConnectiveRx",      feed_url=_gnews_feed("ConnectiveRx")),
    # "Change Healthcare" alone matches unrelated companies; T4a handles
    # false attributions (Teladoc/Lantheus/Alignment).
    CompetitorFeed(competitor="relayhealth_change", name="Change Healthcare", feed_url=_gnews_feed("Change Healthcare")),
    # ── Pharmacy Software / POD ───────────────────────────────────────
    CompetitorFeed(competitor="redsail_technologies", name="RedSail Technologies", feed_url=_gnews_feed("RedSail Technologies")),
    # ── DOOH / Point-of-Care ──────────────────────────────────────────
    CompetitorFeed(competitor="patientpoint",      name="PatientPoint",      feed_url=_gnews_feed("PatientPoint")),
    CompetitorFeed(competitor="checkedup",         name="CheckedUp",         feed_url=_gnews_feed("CheckedUp healthcare")),
    CompetitorFeed(competitor="vistar_media",      name="Vistar Media",      feed_url=_gnews_feed("Vistar Media")),
    # ── Admanager benchmark ───────────────────────────────────────────
    CompetitorFeed(competitor="google_ad_manager", name="Google Ad Manager", feed_url=_gnews_feed("Google Ad Manager")),
    # ── Agentic Pharma Engagement (RepTwin direct) ────────────────────
    CompetitorFeed(competitor="roserx",            name="RoseRx",            feed_url=_gnews_feed("RoseRx")),
    CompetitorFeed(competitor="synthio_labs",      name="Synthio Labs",      feed_url=_gnews_feed("Synthio Labs")),
    CompetitorFeed(competitor="prescriberpoint",   name="PrescriberPoint",   feed_url=_gnews_feed("PrescriberPoint")),
    CompetitorFeed(competitor="aktana",            name="Aktana",            feed_url=_gnews_feed("Aktana pharma")),
    CompetitorFeed(competitor="salesforce_agentforce", name="Salesforce Agentforce", feed_url=_gnews_feed("Salesforce Agentforce")),
    CompetitorFeed(competitor="veeva_ai",          name="Veeva AI",          feed_url=_gnews_feed("Veeva AI")),
    # ── RepTwin competitors ──────────────────────────────────────────────
    CompetitorFeed(competitor="hippocratic_ai",    name="Hippocratic AI",    feed_url=_gnews_feed("Hippocratic AI")),
    # ── Patient Access / Affordability ───────────────────────────────────
    CompetitorFeed(competitor="goodrx",            name="GoodRx",            feed_url=_gnews_feed("GoodRx")),
    # ── Pharmacy / POD competitors ───────────────────────────────────────
    CompetitorFeed(competitor="drfirst",           name="DrFirst",           feed_url=_gnews_feed("DrFirst pharmacy")),
    CompetitorFeed(competitor="medadvisor",        name="MedAdvisor",        feed_url=_gnews_feed("MedAdvisor Solutions")),
    # ── ABM competitors ──────────────────────────────────────────────────
    CompetitorFeed(competitor="demandbase",        name="Demandbase",        feed_url=_gnews_feed("Demandbase healthcare")),
    CompetitorFeed(competitor="six_sense",         name="6sense",            feed_url=_gnews_feed("6sense life sciences")),
)


def write_artifacts(
    out_dir: Path,
    *,
    findings: list[Finding],
    plaintext: str,
    html: str,
    subject: str,
) -> None:
    """Write run artifacts to `out_dir` for upload by GitHub Actions.

    Produces:
      findings.jsonl   one Finding per line (JSON-serialized via pydantic).
      digest.txt       the rendered plaintext body.
      digest.html      the rendered HTML body (open in browser to preview).
      subject.txt      the rendered subject line.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    jsonl_lines = [f.model_dump_json() for f in findings]
    (out_dir / "findings.jsonl").write_text(
        "\n".join(jsonl_lines) + ("\n" if jsonl_lines else ""),
        encoding="utf-8",
    )
    (out_dir / "digest.txt").write_text(plaintext, encoding="utf-8")
    (out_dir / "digest.html").write_text(html, encoding="utf-8")
    (out_dir / "subject.txt").write_text(subject, encoding="utf-8")


async def run(
    *,
    feeds: tuple[CompetitorFeed, ...] = DAY6_FEEDS,
    max_items_per_feed: int = 10,
    max_age_hours: int = 36,
    dry_run: bool = False,
    send_to: str | None = None,
    out_dir: Path | None = None,
) -> int:
    """Execute one daily run end to end. Returns process exit code."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    async with HttpClient() as http:
        gemini = GeminiClient()  # reads GEMINI_API_KEY from env

        # T1 INGEST
        all_items = []
        for feed in feeds:
            items = await fetch_rss(
                feed.feed_url,
                http=http,
                competitor=feed.competitor,
                source_type=feed.source_type,
                max_items=max_items_per_feed,
                max_age_hours=max_age_hours,
            )
            logger.info("Ingested %d items from %s", len(items), feed.name)
            all_items.extend(items)

        logger.info("Total ingested: %d items", len(all_items))

        # T2 FILTER
        decisions = await filter_items(all_items, gemini=gemini)
        kept_items = kept(decisions)
        logger.info("Filter kept %d / %d items", len(kept_items), len(all_items))

        # T4a ATTRIBUTION CHECK (Sprint 8)
        # Drops items whose claimed competitor is not the actual subject.
        attribution_results = await attribution_check_items(kept_items, gemini=gemini)
        attributed_items = kept_after_attribution(attribution_results)
        logger.info(
            "Attribution check kept %d / %d items",
            len(attributed_items), len(kept_items),
        )
        # Map url -> decision so we can stamp the verdict on each Finding
        # after extract. URLs are unique per item so this is a stable join key.
        attribution_by_url = {
            str(r.item.url): r.decision for r in attribution_results if r.kept
        }

        # T4a.5 SAME-EVENT DEDUP (Sprint 8f, post-2026-05-11 fix)
        # Collapses syndicated copies of the same announcement (e.g. yahoo.com
        # + stocktitan.net for one OptimizeRx launch) BEFORE extract so we
        # pay Flash cost once per unique event and the digest count reflects
        # events, not wire copies.
        deduped_items = dedup_items(attributed_items)
        if len(deduped_items) != len(attributed_items):
            logger.info(
                "Dedup kept %d / %d unique events",
                len(deduped_items), len(attributed_items),
            )

        # T3 EXTRACT
        findings = await extract_findings(deduped_items, gemini=gemini)
        logger.info("Extract produced %d findings", len(findings))

        # Stamp attribution onto each Finding.
        for finding in findings:
            decision = attribution_by_url.get(str(finding.url))
            if decision is not None:
                attach_attribution_to_finding(finding, decision)

        # T4b SEVERITY ADVERSARIAL (Sprint 8)
        findings = await severity_adversarial_findings(findings, gemini=gemini)
        kept_findings = kept_after_severity(findings)
        n_rejected = len(findings) - len(kept_findings)
        logger.info(
            "Severity adversarial kept %d / %d findings (%d rejected)",
            len(kept_findings), len(findings), n_rejected,
        )

        # T5 SYNTH PER PRODUCT (Sprint 8)
        per_product = await synth_per_product_batch(kept_findings, gemini=gemini)
        # T6 SYNTH STRATEGIC (Sprint 8)
        strategic = await synth_strategic(kept_findings, per_product, gemini=gemini)

    # T7 RENDER (Sprint 8 redesigned digest structure)
    plaintext = render_plaintext(
        kept_findings, per_product=per_product, strategic=strategic
    )
    html = render_html(
        kept_findings, per_product=per_product, strategic=strategic
    )
    subject = render_subject(kept_findings)

    if out_dir is not None:
        # Write the FULL findings list (including rejected ones) for audit;
        # the renderer only consumed kept_findings.
        write_artifacts(
            out_dir,
            findings=findings,
            plaintext=plaintext,
            html=html,
            subject=subject,
        )
        logger.info("Wrote artifacts to %s", out_dir)

    if dry_run:
        print(f"\n=== Subject ===\n{subject}\n")
        print(f"=== Body ===\n{plaintext}")
        return 0

    # T8 DELIVER
    gmail = GmailClient()
    recipient = send_to or gmail.user_email
    message_id = await gmail.send_message(
        to=recipient,
        subject=subject,
        plaintext=plaintext,
        html=html,
    )
    logger.info("Sent digest to %s (Gmail id=%s)", recipient, message_id)
    return 0


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Doceree CI daily run.")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the digest to stdout instead of sending via Gmail.",
    )
    p.add_argument(
        "--send-to",
        type=str,
        default=None,
        help="Override recipient address (defaults to GMAIL_USER_EMAIL).",
    )
    p.add_argument(
        "--max-items",
        type=int,
        default=10,
        help="Max RSS items per competitor feed (default 10).",
    )
    p.add_argument(
        "--max-age-hours",
        type=int,
        default=36,
        help="Drop RSS entries older than this many hours from now "
             "(default 36 = 24h + indexing-lag buffer). Pass a larger value "
             "for backfill / debugging runs.",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="If set, write findings.jsonl + digest.txt + subject.txt to this "
             "directory. Used by the GitHub Actions workflow for artifact upload.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)
    return asyncio.run(
        run(
            max_items_per_feed=args.max_items,
            max_age_hours=args.max_age_hours,
            dry_run=args.dry_run,
            send_to=args.send_to,
            out_dir=args.out_dir,
        )
    )


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
