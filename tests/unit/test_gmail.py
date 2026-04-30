"""Tests for `clients.gmail.GmailClient`. SDK and credentials mocked."""
from __future__ import annotations

import base64
from unittest.mock import MagicMock

import pytest

from clients.gmail import GmailClient


@pytest.fixture
def gmail_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GMAIL_CLIENT_ID", "fake-client-id")
    monkeypatch.setenv("GMAIL_CLIENT_SECRET", "fake-client-secret")
    monkeypatch.setenv("GMAIL_REFRESH_TOKEN", "fake-refresh-token")
    monkeypatch.setenv("GMAIL_USER_EMAIL", "test@doceree.com")


@pytest.fixture
def fake_service(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Patch googleapiclient.discovery.build so no network call happens."""
    service = MagicMock(name="gmail_service")
    send_call = MagicMock(return_value=MagicMock(execute=lambda: {"id": "msg-12345"}))
    service.users.return_value.messages.return_value.send = MagicMock(
        return_value=send_call.execute.return_value
    )
    # Make .send(...).execute() return {'id': 'msg-12345'}
    service.users.return_value.messages.return_value.send.return_value.execute = MagicMock(
        return_value={"id": "msg-12345"}
    )

    monkeypatch.setattr(
        "clients.gmail.build_service",
        lambda *args, **kwargs: service,
    )
    # Patch the credentials refresh so we don't need a network round trip.
    monkeypatch.setattr(
        "clients.gmail.Credentials.refresh",
        lambda self, request: setattr(self, "token", "fake-access-token"),
    )
    return service


class TestConstruction:
    def test_missing_credentials_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("GMAIL_CLIENT_ID", raising=False)
        monkeypatch.delenv("GMAIL_CLIENT_SECRET", raising=False)
        monkeypatch.delenv("GMAIL_REFRESH_TOKEN", raising=False)
        monkeypatch.delenv("GMAIL_USER_EMAIL", raising=False)
        with pytest.raises(RuntimeError) as exc:
            GmailClient()
        # Lists the missing keys so the operator can fix .env.
        msg = str(exc.value)
        assert "GMAIL_CLIENT_ID" in msg
        assert "GMAIL_REFRESH_TOKEN" in msg

    def test_explicit_args_override_env(
        self, gmail_env: None, fake_service: MagicMock
    ) -> None:
        client = GmailClient(
            client_id="explicit-id",
            client_secret="explicit-secret",
            refresh_token="explicit-token",
            user_email="explicit@doceree.com",
        )
        assert client.client_id == "explicit-id"
        assert client.user_email == "explicit@doceree.com"

    def test_env_picked_up(self, gmail_env: None, fake_service: MagicMock) -> None:
        client = GmailClient()
        assert client.client_id == "fake-client-id"
        assert client.user_email == "test@doceree.com"


class TestMimeBuild:
    def test_plaintext_only(self) -> None:
        msg = GmailClient._build_mime(
            to="to@doceree.com",
            sender="from@doceree.com",
            subject="Subject line",
            plaintext="Hello world",
            html=None,
        )
        assert msg["From"] == "from@doceree.com"
        assert msg["To"] == "to@doceree.com"
        assert msg["Subject"] == "Subject line"
        assert "Hello world" in msg.as_string()
        # Single-part message
        assert not msg.is_multipart()

    def test_with_html_alternative(self) -> None:
        msg = GmailClient._build_mime(
            to="to@doceree.com",
            sender="from@doceree.com",
            subject="Subject",
            plaintext="text body",
            html="<p>html body</p>",
        )
        assert msg.is_multipart()
        body_text = msg.as_string()
        assert "text body" in body_text
        assert "<p>html body</p>" in body_text


@pytest.mark.asyncio
class TestSendMessage:
    async def test_send_returns_id(
        self, gmail_env: None, fake_service: MagicMock
    ) -> None:
        client = GmailClient()
        message_id = await client.send_message(
            to="recipient@doceree.com",
            subject="Test",
            plaintext="Body",
        )
        assert message_id == "msg-12345"

    async def test_send_calls_with_userid_me(
        self, gmail_env: None, fake_service: MagicMock
    ) -> None:
        client = GmailClient()
        await client.send_message(
            to="recipient@doceree.com",
            subject="Test",
            plaintext="Body",
        )
        send = fake_service.users.return_value.messages.return_value.send
        kwargs = send.call_args.kwargs
        assert kwargs["userId"] == "me"
        # The body has a base64url-encoded raw RFC 822 message.
        raw = kwargs["body"]["raw"]
        decoded = base64.urlsafe_b64decode(raw).decode("utf-8")
        assert "To: recipient@doceree.com" in decoded
        assert "Subject: Test" in decoded
        assert "Body" in decoded
