"""Gmail API client (T8 deliver).

OAuth refresh-token flow: at construction we exchange the long-lived refresh
token for a short-lived access token using `google-auth`'s
`Credentials.from_authorized_user_info`, then build a `gmail.users` service.
The refresh happens transparently on each call once the access token expires.

`send_message(to, subject, plaintext, html=None)` builds a multipart MIME
message (plaintext-alternative for Gmail, HTML alternative when provided)
and calls `users.messages.send` with `userId=me`.

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 6.
"""
from __future__ import annotations

import asyncio
import base64
import logging
import os
from email.message import EmailMessage
from typing import Any

from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as build_service

logger = logging.getLogger(__name__)


# Send-only scope (minimum needed; matches scripts/generate_gmail_token.py).
GMAIL_SCOPES = ("https://www.googleapis.com/auth/gmail.send",)

TOKEN_URI = "https://oauth2.googleapis.com/token"


class GmailClient:
    """Send-only Gmail client using OAuth refresh-token flow.

    Reads `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`,
    `GMAIL_USER_EMAIL` from kwargs or environment. Fails loudly at
    construction if any are missing.
    """

    def __init__(
        self,
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        refresh_token: str | None = None,
        user_email: str | None = None,
    ) -> None:
        self.client_id = client_id or os.environ.get("GMAIL_CLIENT_ID", "").strip()
        self.client_secret = (
            client_secret or os.environ.get("GMAIL_CLIENT_SECRET", "").strip()
        )
        self.refresh_token = (
            refresh_token or os.environ.get("GMAIL_REFRESH_TOKEN", "").strip()
        )
        self.user_email = user_email or os.environ.get("GMAIL_USER_EMAIL", "").strip()

        missing = [
            name for name, value in [
                ("GMAIL_CLIENT_ID", self.client_id),
                ("GMAIL_CLIENT_SECRET", self.client_secret),
                ("GMAIL_REFRESH_TOKEN", self.refresh_token),
                ("GMAIL_USER_EMAIL", self.user_email),
            ] if not value
        ]
        if missing:
            raise RuntimeError(
                f"Gmail credentials missing: {', '.join(missing)}. "
                "Set in .env or pass to GmailClient(...)."
            )

        self._creds = Credentials(
            token=None,  # forces refresh on first call
            refresh_token=self.refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_uri=TOKEN_URI,
            scopes=list(GMAIL_SCOPES),
        )
        # Lazy: only build the service once we actually send.
        self._service: Any | None = None

    def _ensure_service(self) -> Any:
        if self._service is None:
            # Refresh access token if needed; then build the discovery service.
            if not self._creds.valid:
                self._creds.refresh(GoogleAuthRequest())
            self._service = build_service(
                "gmail",
                "v1",
                credentials=self._creds,
                cache_discovery=False,
            )
        return self._service

    @staticmethod
    def _build_mime(
        *,
        to: str,
        sender: str,
        subject: str,
        plaintext: str,
        html: str | None,
    ) -> EmailMessage:
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(plaintext)
        if html:
            msg.add_alternative(html, subtype="html")
        return msg

    async def send_message(
        self,
        *,
        to: str,
        subject: str,
        plaintext: str,
        html: str | None = None,
    ) -> str:
        """Send an email. Returns the Gmail message ID on success.

        Synchronous Google client is run in a thread executor so the call
        plays nicely with the rest of the async pipeline.
        """
        return await asyncio.to_thread(
            self._send_sync,
            to=to,
            subject=subject,
            plaintext=plaintext,
            html=html,
        )

    def _send_sync(
        self,
        *,
        to: str,
        subject: str,
        plaintext: str,
        html: str | None,
    ) -> str:
        service = self._ensure_service()
        msg = self._build_mime(
            to=to,
            sender=self.user_email,
            subject=subject,
            plaintext=plaintext,
            html=html,
        )
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
        result = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": raw})
            .execute()
        )
        message_id = result.get("id", "")
        logger.info("Gmail send -> %s id=%s", to, message_id)
        return message_id
