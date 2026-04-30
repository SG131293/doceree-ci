"""Telegram failure notifier (skeleton).

Called from the `if: failure()` step of GitHub Actions workflows. Sends a
short alert pointing at the run URL so Sherry can open the job and read
the full logs from the artifact bundle.

Day 22 will replace this skeleton with a richer Telegram client (MarkdownV2
formatting, message chunking, gh-pages archive links). For Day 7 the goal
is just "if the workflow dies, Sherry hears about it."

Environment:
  TELEGRAM_BOT_TOKEN    Bot API token.
  TELEGRAM_CHAT_ID      Chat ID for Sherry's alerts channel.
  WORKFLOW_RUN_URL      URL of the failed run (set by the workflow).
  WORKFLOW_NAME         Workflow name (e.g., "daily-digest").

Exit codes:
  0  alert sent
  1  required env var missing
  2  Telegram API call failed
"""
from __future__ import annotations

import logging
import os
import sys

import httpx

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def build_text(*, workflow_name: str, run_url: str) -> str:
    """Compose the Telegram message body. Plaintext (no MarkdownV2 yet)."""
    name = workflow_name or "doceree-ci"
    if run_url:
        return (
            f"Doceree CI failure: {name}\n"
            f"Run: {run_url}\n"
            f"Check the run's artifact bundle for run.log."
        )
    return (
        f"Doceree CI failure: {name}\n"
        f"(No run URL provided. Check GitHub Actions for the failed run.)"
    )


def send(
    *,
    token: str,
    chat_id: str,
    text: str,
    timeout: float = 15.0,
    client: httpx.Client | None = None,
) -> None:
    """Synchronously POST to Telegram sendMessage. Raises on HTTP error.

    `client` may be injected for tests; callers in production let httpx
    create a one-shot client.
    """
    url = TELEGRAM_API_URL.format(token=token)
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
    }
    if client is None:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=payload)
    else:
        response = client.post(url, json=payload)
    response.raise_for_status()


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    run_url = os.environ.get("WORKFLOW_RUN_URL", "").strip()
    workflow_name = os.environ.get("WORKFLOW_NAME", "").strip()

    missing = [
        name for name, val in [
            ("TELEGRAM_BOT_TOKEN", token),
            ("TELEGRAM_CHAT_ID", chat_id),
        ] if not val
    ]
    if missing:
        logger.error("Required env var(s) missing: %s", ", ".join(missing))
        return 1

    text = build_text(workflow_name=workflow_name, run_url=run_url)
    try:
        send(token=token, chat_id=chat_id, text=text)
    except Exception as exc:
        logger.error("Telegram send failed: %s", exc)
        return 2

    logger.info("Telegram alert sent to chat_id=%s", chat_id)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
