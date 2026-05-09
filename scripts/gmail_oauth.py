"""One-time Gmail OAuth helper — generates GMAIL_REFRESH_TOKEN for GitHub Actions.

Usage:
    python scripts/gmail_oauth.py

Reads GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET from environment (or .env file).
Opens a browser window for Google sign-in, then prints the refresh token to
copy into your GitHub Actions secrets.

Required GitHub Actions secrets after running this script:
    GMAIL_CLIENT_ID       — from Google Cloud Console
    GMAIL_CLIENT_SECRET   — from Google Cloud Console
    GMAIL_REFRESH_TOKEN   — printed by this script
    GMAIL_USER_EMAIL      — the Gmail address you authorized (e.g. sherry.george@doceree.com)

Prerequisites:
    1. Google Cloud project with Gmail API enabled.
    2. OAuth client of type "Desktop app" created in
       APIs & Services → Credentials.
    3. Your email added as a test user under OAuth consent screen
       (if app is still in Testing mode).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Load .env if present (dev convenience)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass


def main() -> None:
    client_id = os.environ.get("GMAIL_CLIENT_ID", "").strip()
    client_secret = os.environ.get("GMAIL_CLIENT_SECRET", "").strip()

    if not client_id or not client_secret:
        print(
            "ERROR: Set GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET in your "
            "environment or .env file before running this script.\n\n"
            "  $env:GMAIL_CLIENT_ID = 'your-client-id'\n"
            "  $env:GMAIL_CLIENT_SECRET = 'your-client-secret'\n"
            "  python scripts/gmail_oauth.py"
        )
        sys.exit(1)

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("ERROR: google-auth-oauthlib not installed. Run: pip install -r requirements.txt")
        sys.exit(1)

    # Scope: send-only. Principle of least privilege — no read access needed.
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    # Build the client config dict that InstalledAppFlow expects.
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    print("Opening browser for Google sign-in...")
    print("Sign in with: sherry.george@doceree.com")
    print()

    flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
    # run_local_server starts a temporary localhost server to catch the redirect.
    # port=0 picks any free port automatically.
    credentials = flow.run_local_server(port=0, open_browser=True)

    print()
    print("=" * 60)
    print("SUCCESS. Add these three secrets to GitHub Actions:")
    print("https://github.com/SherryGeorge/doceree-ci/settings/secrets/actions")
    print("=" * 60)
    print()
    print(f"GMAIL_CLIENT_ID      = {client_id}")
    print(f"GMAIL_CLIENT_SECRET  = {client_secret}")
    print(f"GMAIL_REFRESH_TOKEN  = {credentials.refresh_token}")
    print(f"GMAIL_USER_EMAIL     = {credentials.token_uri and 'sherry.george@doceree.com'}")
    print()
    print("NOTE: The refresh token does not expire unless you revoke access")
    print("or the OAuth consent screen is reset. Keep it secret.")

    # Also write to a local file so you can copy it even if the terminal
    # scrolls away. File is gitignored.
    out_path = Path(__file__).resolve().parents[1] / ".gmail_token.json"
    out_path.write_text(
        json.dumps(
            {
                "GMAIL_CLIENT_ID": client_id,
                "GMAIL_CLIENT_SECRET": client_secret,
                "GMAIL_REFRESH_TOKEN": credentials.refresh_token,
                "GMAIL_USER_EMAIL": "sherry.george@doceree.com",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Also saved to: {out_path}  (delete after copying to GitHub)")


if __name__ == "__main__":
    main()
