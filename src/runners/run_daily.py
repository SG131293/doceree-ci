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

from clients.gemini import GeminiClient
from clients.gmail import GmailClient
from clients.http import HttpClient
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
from render.render import render_plaintext, render_subject
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


# Day-6 cohort. Google News RSS gives us reliable real data without depending
# on competitor RSS endpoints that may not exist. The when:1d clause limits
# to last 24h - matches the filter stage's staleness rule.
DAY6_FEEDS: tuple[CompetitorFeed, ...] = (
    CompetitorFeed(
        competitor="deepintent",
        name="DeepIntent",
        feed_url="https://news.google.com/rss/search?q=%22DeepIntent%22+when:1d&hl=en-US&gl=US&ceid=US:en",
    ),
    CompetitorFeed(
        competitor="optimizerx",
        name="OptimizeRx",
        feed_url="https://news.google.com/rss/search?q=%22OptimizeRx%22+when:1d&hl=en-US&gl=US&ceid=US:en",
    ),
    CompetitorFeed(
        competitor="hippocratic_ai",
        name="Hippocratic AI",
        feed_url="https://news.google.com/rss/search?q=%22Hippocratic+AI%22+when:1d&hl=en-US&gl=US&ceid=US:en",
    ),
)


def write_artifacts(
    out_dir: Path,
    *,
    findings: list[Finding],
    plaintext: str,
    subject: str,
) -> None:
    """Write run artifacts to `out_dir` for upload by GitHub Actions.

    Produces:
      findings.jsonl   one Finding per line (JSON-serialized via pydantic).
      digest.txt       the rendered plaintext body.
      subject.txt      the rendered subject line.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    jsonl_lines = [f.model_dump_json() for f in findings]
    (out_dir / "findings.jsonl").write_text(
        "\n".join(jsonl_lines) + ("\n" if jsonl_lines else ""),
        encoding="utf-8",
    )
    (out_dir / "digest.txt").write_text(plaintext, encoding="utf-8")
    (out_dir / "subject.txt").write_text(subject, encoding="utf-8")


async def run(
    *,
    feeds: tuple[CompetitorFeed, ...] = DAY6_FEEDS,
    max_items_per_feed: int = 10,
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

        # T3 EXTRACT
        findings = await extract_findings(attributed_items, gemini=gemini)
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
    subject = render_subject(kept_findings)

    if out_dir is not None:
        # Write the FULL findings list (including rejected ones) for audit;
        # the renderer only consumed kept_findings.
        write_artifacts(out_dir, findings=findings, plaintext=plaintext, subject=subject)
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
            dry_run=args.dry_run,
            send_to=args.send_to,
            out_dir=args.out_dir,
        )
    )


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
