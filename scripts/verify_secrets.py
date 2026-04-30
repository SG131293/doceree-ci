"""Verify all required secrets are set in the local environment.

Reads from os.environ, loading a .env file from the repo root if present.
Prints PASS/FAIL per secret with a redacted preview, then a one-line summary.
Exits 0 on all-pass, 1 on any miss.

Usage:
    python scripts/verify_secrets.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install -r requirements.txt")
    sys.exit(2)


REQUIRED = [
    "GEMINI_API_KEY",
    "OPENAI_API_KEY",
    "GMAIL_CLIENT_ID",
    "GMAIL_CLIENT_SECRET",
    "GMAIL_REFRESH_TOKEN",
    "GMAIL_USER_EMAIL",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
]


def redact(value: str) -> str:
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:3]}...{value[-4:]} (len={len(value)})"


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    env_path = repo_root / ".env"
    loaded = load_dotenv(env_path) if env_path.exists() else False

    if env_path.exists():
        print(f"Loaded .env from {env_path}: {loaded}")
    else:
        print("No .env file found; reading from process environment only.")
    print()

    missing: list[str] = []
    for key in REQUIRED:
        value = os.environ.get(key, "").strip()
        if not value:
            print(f"  MISS  {key}")
            missing.append(key)
        else:
            print(f"  PASS  {key:<22} {redact(value)}")

    print()
    if missing:
        print(f"FAIL: {len(missing)} of {len(REQUIRED)} secrets missing: {', '.join(missing)}")
        return 1
    print(f"OK: all {len(REQUIRED)} required secrets present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
