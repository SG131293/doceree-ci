"""Day-6 minimum-viable daily run.

Orchestrates: ingest (RSS) -> filter (Flash-Lite) -> extract (Flash) ->
render (plaintext) -> deliver (Gmail). Targets a small set of competitors
per the build plan's Day-6 scope (DeepIntent, OptimizeRx, Hippocratic AI -
Synthio Labs is in the master PRD but lacks a verifiable URL, so we substitute
Hippocratic for the third slot).

For Day 6, RSS feeds are pulled from Google News with a per-competitor query
(`https://news.google.com/rss/search?q={query}+when:1d`). This gives us
real, fresh data without depending on competitor-specific RSS endpoints
that may or may not exist. Day 17 transitions to sitemap diff against the
50-source registry.

CLI:
    python scripts/run_daily.py [--dry-run] [--send-to email] [--max-items N]

  --dry-run       Print the rendered digest to stdout; do not send Gmail.
  --send-to       Override recipient (defaults to GMAIL_USER_EMAIL).
  --max-items     Cap RSS items per competitor (defaults to 10).

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 6.
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from dataclasses import dataclass

from clients.gemini import GeminiClient
from clients.gmail import GmailClient
from clients.http import HttpClient
from pipeline.extract import extract_findings
from pipeline.filter import filter_items, kept
from render.render import render_plaintext, render_subject
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


async def run(
    *,
    feeds: tuple[CompetitorFeed, ...] = DAY6_FEEDS,
    max_items_per_feed: int = 10,
    dry_run: bool = False,
    send_to: str | None = None,
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

        # T3 EXTRACT
        findings = await extract_findings(kept_items, gemini=gemini)
        logger.info("Extract produced %d findings", len(findings))

    # T7 RENDER (T4 verify + T5/T6 synth land Days 8-19)
    plaintext = render_plaintext(findings)
    subject = render_subject(findings)

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
    p = argparse.ArgumentParser(description="Doceree CI daily run (Day 6 MVP).")
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
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)
    return asyncio.run(
        run(
            max_items_per_feed=args.max_items,
            dry_run=args.dry_run,
            send_to=args.send_to,
        )
    )


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
