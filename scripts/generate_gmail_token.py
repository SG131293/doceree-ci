"""Generate a Gmail API OAuth refresh token (one-shot, run locally).

Opens a browser to complete Google's OAuth consent flow, then prints the
refresh token. Copy it into:
  1. Your local .env as GMAIL_REFRESH_TOKEN
  2. GitHub repo secrets as GMAIL_REFRESH_TOKEN

The credentials JSON is the OAuth Client (Desktop App) file you downloaded
from Google Cloud Console > APIs & Services > Credentials.

Usage:
    python scripts/generate_gmail_token.py path/to/credentials.json

Requires: google-auth-oauthlib (in requirements.txt).

Scopes:
    https://www.googleapis.com/auth/gmail.send  -- send-only, minimum needed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("ERROR: google-auth-oauthlib not installed. Run: pip install -r requirements.txt")
    sys.exit(2)


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "credentials_path",
        type=Path,
        help="Path to OAuth client JSON downloaded from Google Cloud Console",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=0,
        help="Local server port for the OAuth redirect (0 = pick a free port)",
    )
    args = parser.parse_args()

    if not args.credentials_path.exists():
        print(f"ERROR: credentials file not found: {args.credentials_path}")
        return 1

    try:
        with args.credentials_path.open() as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in credentials file: {e}")
        return 1

    if "installed" not in data and "web" not in data:
        print("ERROR: credentials file is not a Desktop or Web OAuth client")
        print("       Re-download from Google Cloud Console > Credentials")
        return 1

    flow = InstalledAppFlow.from_client_secrets_file(str(args.credentials_path), SCOPES)
    creds = flow.run_local_server(port=args.port, prompt="consent", access_type="offline")

    if not creds.refresh_token:
        print("ERROR: no refresh_token returned. The OAuth client may already be authorized.")
        print("       Revoke at https://myaccount.google.com/permissions and re-run.")
        return 1

    client_block = data.get("installed") or data.get("web") or {}
    print()
    print("=" * 60)
    print("SUCCESS - copy these into your local .env and GitHub secrets:")
    print("=" * 60)
    print(f"GMAIL_CLIENT_ID={client_block.get('client_id', '')}")
    print(f"GMAIL_CLIENT_SECRET={client_block.get('client_secret', '')}")
    print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
    print("=" * 60)
    print()
    print("Verify with: python scripts/verify_secrets.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
