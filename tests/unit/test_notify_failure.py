"""Tests for `runners.notify_failure`. httpx is mocked via MockTransport
so no real Telegram API call leaves the test process."""
from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest

from runners.notify_failure import build_text, main, send


# ---- build_text ----


class TestBuildText:
    def test_with_run_url(self) -> None:
        out = build_text(workflow_name="daily-digest", run_url="https://gh.example/run/123")
        assert "daily-digest" in out
        assert "https://gh.example/run/123" in out
        assert "run.log" in out  # mentions where to find logs

    def test_without_run_url(self) -> None:
        out = build_text(workflow_name="daily-digest", run_url="")
        assert "daily-digest" in out
        assert "No run URL" in out

    def test_default_workflow_name(self) -> None:
        out = build_text(workflow_name="", run_url="https://gh.example/run/123")
        # Empty string falls back to a sensible default.
        assert "doceree-ci" in out


# ---- send() ----


def _make_client(
    handler: Callable[[httpx.Request], httpx.Response],
) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler))


class TestSend:
    def test_posts_to_telegram_with_correct_payload(self) -> None:
        captured: dict[str, object] = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["url"] = str(req.url)
            captured["json"] = req.read().decode("utf-8")
            return httpx.Response(200, json={"ok": True})

        with _make_client(handler) as client:
            send(token="abc-token", chat_id="42", text="hello", client=client)
        assert "/bot" in captured["url"]
        assert "abc-token" in captured["url"]
        assert "/sendMessage" in captured["url"]
        body = captured["json"]
        assert isinstance(body, str)
        # httpx serializes without whitespace; just verify the field/value pairs exist.
        import json as _json

        decoded = _json.loads(body)
        assert decoded["chat_id"] == "42"
        assert decoded["text"] == "hello"
        assert decoded["disable_web_page_preview"] is True

    def test_raises_on_4xx(self) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"ok": False, "description": "Unauthorized"})

        with _make_client(handler) as client:
            with pytest.raises(httpx.HTTPStatusError):
                send(token="bad", chat_id="42", text="hi", client=client)

    def test_raises_on_5xx(self) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(503)

        with _make_client(handler) as client:
            with pytest.raises(httpx.HTTPStatusError):
                send(token="x", chat_id="42", text="hi", client=client)


# ---- main() ----


class TestMain:
    def test_missing_token_returns_1(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "42")
        assert main([]) == 1

    def test_missing_chat_id_returns_1(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "x")
        monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
        assert main([]) == 1

    def test_send_failure_returns_2(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "x")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "42")
        monkeypatch.setenv("WORKFLOW_RUN_URL", "https://gh.example/run/123")
        monkeypatch.setenv("WORKFLOW_NAME", "daily-digest")

        def fake_send(**kwargs):
            raise RuntimeError("simulated network failure")

        monkeypatch.setattr("runners.notify_failure.send", fake_send)
        assert main([]) == 2

    def test_success_returns_0(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "x")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "42")
        monkeypatch.setenv("WORKFLOW_RUN_URL", "https://gh.example/run/123")
        monkeypatch.setenv("WORKFLOW_NAME", "daily-digest")

        called: list[dict[str, object]] = []

        def fake_send(**kwargs):
            called.append(kwargs)

        monkeypatch.setattr("runners.notify_failure.send", fake_send)
        assert main([]) == 0
        assert len(called) == 1
        assert called[0]["token"] == "x"
        assert called[0]["chat_id"] == "42"
        text = called[0]["text"]
        assert isinstance(text, str)
        assert "https://gh.example/run/123" in text
        assert "daily-digest" in text
