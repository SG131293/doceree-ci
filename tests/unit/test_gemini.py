"""Tests for `clients.gemini.GeminiClient`.

The actual `google-genai` SDK is mocked out: tests verify that the right
model, thinking_budget, structured-output config, and cached_content are
passed to `aio.models.generate_content`. Live API tests with `pytest-recording`
cassettes land Day 6 alongside the actual prompt files.

Retry behavior is exercised by `is_retryable()` directly plus a synthetic
test that raises a 429 / 5xx and confirms tenacity retries.
"""
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from google.genai import errors as genai_errors
from google.genai import types as genai_types
from pydantic import BaseModel

from clients.gemini import (
    CALL_TYPES,
    MODEL_FLASH,
    MODEL_FLASH_LITE,
    MODEL_PRO,
    GeminiClient,
    is_retryable,
)


# ---- Helpers ----


class _FakeResponse:
    """Minimal duck-type stand-in for `genai_types.GenerateContentResponse`."""

    def __init__(self, text: str) -> None:
        self.text = text


def _api_error(code: int, message: str = "x") -> genai_errors.APIError:
    """Construct an APIError without going through the SDK's internal parser."""
    err = genai_errors.APIError.__new__(genai_errors.APIError)
    err.code = code
    err.status = "ERROR"
    err.message = message
    err.details = {"error": {"message": message}}
    err.response = None
    Exception.__init__(err, f"{code} ERROR. {err.details}")
    return err


@pytest.fixture
def fake_client(monkeypatch: pytest.MonkeyPatch) -> Any:
    """Patch the underlying `genai.Client` so construction does not need a
    real API key and `aio.models.generate_content` is a controllable mock.

    Returns the fake client object; tests can poke its attributes to assert
    against the args passed to generate_content / caches.create / etc.
    """
    fake = MagicMock(name="genai.Client")
    fake.aio = MagicMock(name="aio")
    fake.aio.models = MagicMock(name="models")
    fake.aio.models.generate_content = AsyncMock(
        return_value=_FakeResponse(text='{"ok": true}')
    )
    fake.aio.caches = MagicMock(name="caches")
    fake.aio.caches.create = AsyncMock(return_value=MagicMock(name="cachedContents/abc"))
    fake.aio.caches.delete = AsyncMock(return_value=None)

    def _patched_client(api_key: str) -> Any:
        return fake

    monkeypatch.setattr("clients.gemini.genai.Client", _patched_client)
    return fake


# ---- is_retryable() ----


class TestIsRetryable:
    @pytest.mark.parametrize("code", [429, 500, 502, 503, 504])
    def test_429_and_5xx_retried(self, code: int) -> None:
        assert is_retryable(_api_error(code)) is True

    @pytest.mark.parametrize("code", [400, 401, 403, 404])
    def test_4xx_not_retried(self, code: int) -> None:
        assert is_retryable(_api_error(code)) is False

    def test_httpx_timeout_retried(self) -> None:
        assert is_retryable(httpx.ConnectTimeout("timeout")) is True
        assert is_retryable(httpx.ReadTimeout("timeout")) is True

    def test_httpx_network_error_retried(self) -> None:
        assert is_retryable(httpx.ConnectError("network")) is True

    def test_value_error_not_retried(self) -> None:
        assert is_retryable(ValueError("bad input")) is False

    def test_runtime_error_not_retried(self) -> None:
        assert is_retryable(RuntimeError("boom")) is False


# ---- Construction ----


class TestConstruction:
    def test_requires_api_key(
        self, monkeypatch: pytest.MonkeyPatch, fake_client: Any
    ) -> None:
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with pytest.raises(RuntimeError) as exc:
            GeminiClient()
        assert "GEMINI_API_KEY" in str(exc.value)

    def test_explicit_api_key_overrides_env(self, fake_client: Any) -> None:
        # Should not raise even with no env key, since we pass one explicitly.
        client = GeminiClient(api_key="explicit-key")
        assert client is not None

    def test_env_var_picked_up(
        self, monkeypatch: pytest.MonkeyPatch, fake_client: Any
    ) -> None:
        monkeypatch.setenv("GEMINI_API_KEY", "from-env")
        client = GeminiClient()
        assert client is not None

    def test_buckets_initialized_per_model(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x", flash_lite_rpm=20, flash_rpm=12, pro_rpm=8)
        assert client._buckets[MODEL_FLASH_LITE].rate_per_second == pytest.approx(20 / 60)
        assert client._buckets[MODEL_FLASH].rate_per_second == pytest.approx(12 / 60)
        assert client._buckets[MODEL_PRO].rate_per_second == pytest.approx(8 / 60)

    def test_tpm_bucket_has_full_capacity(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x", shared_tpm=250_000)
        assert client._tpm_bucket.capacity == pytest.approx(250_000)


# ---- generate() ----


@pytest.mark.asyncio
class TestGenerate:
    async def test_unknown_call_type_rejected(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        with pytest.raises(ValueError):
            await client.generate(call_type="not_a_type", prompt="hi")

    async def test_filter_uses_flash_lite_no_thinking(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        await client.generate(call_type="filter", prompt="prompt body")

        kwargs = fake_client.aio.models.generate_content.call_args.kwargs
        assert kwargs["model"] == MODEL_FLASH_LITE
        cfg = kwargs["config"]
        assert isinstance(cfg, genai_types.GenerateContentConfig)
        assert cfg.temperature == 0.0
        assert cfg.max_output_tokens == 512
        # thinking_budget=0 means we never set thinking_config (avoid forcing
        # the SDK to send a zero budget that may not be accepted).
        assert cfg.thinking_config is None

    async def test_extract_uses_flash_with_thinking_512(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        await client.generate(call_type="extract", prompt="prompt body")
        cfg = fake_client.aio.models.generate_content.call_args.kwargs["config"]
        assert fake_client.aio.models.generate_content.call_args.kwargs["model"] == MODEL_FLASH
        assert cfg.thinking_config is not None
        assert cfg.thinking_config.thinking_budget == 512

    async def test_adversarial_uses_pro_with_thinking_4096(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        await client.generate(call_type="adversarial_check", prompt="prompt body")
        kwargs = fake_client.aio.models.generate_content.call_args.kwargs
        assert kwargs["model"] == MODEL_PRO
        assert kwargs["config"].thinking_config.thinking_budget == 4096

    async def test_synth_per_product_uses_pro_with_thinking_8192(
        self, fake_client: Any
    ) -> None:
        client = GeminiClient(api_key="x")
        await client.generate(call_type="synth_per_product", prompt="prompt body")
        kwargs = fake_client.aio.models.generate_content.call_args.kwargs
        assert kwargs["model"] == MODEL_PRO
        assert kwargs["config"].thinking_config.thinking_budget == 8192

    async def test_response_schema_sets_json_mime(self, fake_client: Any) -> None:
        class Out(BaseModel):
            ok: bool

        fake_client.aio.models.generate_content.return_value = _FakeResponse(
            text='{"ok": true}'
        )

        client = GeminiClient(api_key="x")
        result = await client.generate(
            call_type="filter", prompt="x", response_schema=Out
        )
        cfg = fake_client.aio.models.generate_content.call_args.kwargs["config"]
        assert cfg.response_mime_type == "application/json"
        # The class is converted to a sanitized dict before being passed to
        # the Gemini SDK (Gemini rejects pydantic's `additionalProperties`).
        assert isinstance(cfg.response_schema, dict)
        assert cfg.response_schema.get("type") == "object"
        assert "additionalProperties" not in cfg.response_schema
        # Response is parsed back into the original class.
        assert isinstance(result, Out)
        assert result.ok is True

    async def test_response_schema_strips_additional_properties(
        self, fake_client: Any
    ) -> None:
        """Pydantic models with ConfigDict(extra='forbid') must not leak
        `additionalProperties: false` into the schema sent to Gemini."""
        from pydantic import ConfigDict

        class Strict(BaseModel):
            model_config = ConfigDict(extra="forbid")
            ok: bool

        fake_client.aio.models.generate_content.return_value = _FakeResponse(
            text='{"ok": true}'
        )
        client = GeminiClient(api_key="x")
        await client.generate(call_type="filter", prompt="x", response_schema=Strict)
        cfg = fake_client.aio.models.generate_content.call_args.kwargs["config"]
        assert "additionalProperties" not in cfg.response_schema
        assert "$schema" not in cfg.response_schema

    async def test_no_schema_returns_raw_text(self, fake_client: Any) -> None:
        fake_client.aio.models.generate_content.return_value = _FakeResponse(
            text="hello there"
        )
        client = GeminiClient(api_key="x")
        result = await client.generate(call_type="filter", prompt="x")
        assert result == "hello there"

    async def test_cached_content_passed_through(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        await client.generate(
            call_type="synth_per_product",
            prompt="x",
            cached_content="cachedContents/abc123",
        )
        cfg = fake_client.aio.models.generate_content.call_args.kwargs["config"]
        assert cfg.cached_content == "cachedContents/abc123"

    async def test_max_output_tokens_override(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        await client.generate(
            call_type="extract", prompt="x", max_output_tokens=1024
        )
        cfg = fake_client.aio.models.generate_content.call_args.kwargs["config"]
        assert cfg.max_output_tokens == 1024


# ---- Retry behavior ----


@pytest.mark.asyncio
class TestRetry:
    async def test_retries_on_429_then_succeeds(
        self, fake_client: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """First call returns 429; second succeeds. Total: 2 invocations."""
        # tenacity's wait_exponential_jitter sleeps; short-circuit it.
        async def no_sleep(_seconds: float) -> None:  # noqa: D401
            return None

        monkeypatch.setattr("asyncio.sleep", no_sleep)

        responses = [_api_error(429, "rate limit"), _FakeResponse(text="ok")]

        async def side_effect(*_args: Any, **_kwargs: Any) -> _FakeResponse:
            r = responses.pop(0)
            if isinstance(r, BaseException):
                raise r
            return r

        fake_client.aio.models.generate_content.side_effect = side_effect

        client = GeminiClient(api_key="x")
        result = await client.generate(call_type="filter", prompt="x")
        assert result == "ok"
        assert fake_client.aio.models.generate_content.call_count == 2

    async def test_retries_on_503_then_succeeds(
        self, fake_client: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        async def no_sleep(_seconds: float) -> None:
            return None

        monkeypatch.setattr("asyncio.sleep", no_sleep)

        responses: list[Any] = [_api_error(503), _FakeResponse(text="ok")]

        async def side_effect(*_args: Any, **_kwargs: Any) -> _FakeResponse:
            r = responses.pop(0)
            if isinstance(r, BaseException):
                raise r
            return r

        fake_client.aio.models.generate_content.side_effect = side_effect

        client = GeminiClient(api_key="x")
        result = await client.generate(call_type="filter", prompt="x")
        assert result == "ok"
        assert fake_client.aio.models.generate_content.call_count == 2

    async def test_does_not_retry_on_400(
        self, fake_client: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        async def no_sleep(_seconds: float) -> None:
            return None

        monkeypatch.setattr("asyncio.sleep", no_sleep)
        fake_client.aio.models.generate_content.side_effect = _api_error(400, "bad")

        client = GeminiClient(api_key="x")
        with pytest.raises(genai_errors.APIError) as exc:
            await client.generate(call_type="filter", prompt="x")
        assert exc.value.code == 400
        # Only one attempt, no retry.
        assert fake_client.aio.models.generate_content.call_count == 1

    async def test_gives_up_after_3_attempts(
        self, fake_client: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        async def no_sleep(_seconds: float) -> None:
            return None

        monkeypatch.setattr("asyncio.sleep", no_sleep)
        fake_client.aio.models.generate_content.side_effect = _api_error(429, "rate")

        client = GeminiClient(api_key="x", max_retry_attempts=3)
        with pytest.raises(genai_errors.APIError):
            await client.generate(call_type="filter", prompt="x")
        assert fake_client.aio.models.generate_content.call_count == 3


# ---- Wrapper methods ----


@pytest.mark.asyncio
class TestWrapperMethods:
    async def test_filter_uses_filter_call_type(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        await client.filter("body")
        kwargs = fake_client.aio.models.generate_content.call_args.kwargs
        assert kwargs["model"] == CALL_TYPES["filter"].model

    async def test_extract_uses_extract_call_type(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        await client.extract("body")
        kwargs = fake_client.aio.models.generate_content.call_args.kwargs
        assert kwargs["model"] == CALL_TYPES["extract"].model

    async def test_adversarial_check_uses_pro(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        await client.adversarial_check("body")
        kwargs = fake_client.aio.models.generate_content.call_args.kwargs
        assert kwargs["model"] == MODEL_PRO

    async def test_synthesize_strategic_routes_to_synth_strategic(
        self, fake_client: Any
    ) -> None:
        client = GeminiClient(api_key="x")
        await client.synthesize("body", strategic=True)
        kwargs = fake_client.aio.models.generate_content.call_args.kwargs
        assert kwargs["model"] == MODEL_PRO
        # synth_strategic config has temperature 0.4 (vs 0.3 for per_product)
        assert kwargs["config"].temperature == pytest.approx(0.4)

    async def test_synthesize_default_routes_to_synth_per_product(
        self, fake_client: Any
    ) -> None:
        client = GeminiClient(api_key="x")
        await client.synthesize("body")
        kwargs = fake_client.aio.models.generate_content.call_args.kwargs
        assert kwargs["config"].temperature == pytest.approx(0.3)

    async def test_synthesize_passes_cached_content(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        await client.synthesize("body", cached_content="cachedContents/xyz")
        kwargs = fake_client.aio.models.generate_content.call_args.kwargs
        assert kwargs["config"].cached_content == "cachedContents/xyz"


# ---- Cache management ----


@pytest.mark.asyncio
class TestCacheManagement:
    async def test_create_cache_returns_resource_name(self, fake_client: Any) -> None:
        fake_cache = MagicMock()
        fake_cache.name = "cachedContents/spine-v1"
        fake_client.aio.caches.create.return_value = fake_cache

        client = GeminiClient(api_key="x")
        name = await client.create_cache(contents=["product spine yaml..."])
        assert name == "cachedContents/spine-v1"

        kwargs = fake_client.aio.caches.create.call_args.kwargs
        assert kwargs["model"] == MODEL_PRO
        cfg = kwargs["config"]
        assert cfg.ttl == "7200s"
        assert cfg.contents == ["product spine yaml..."]

    async def test_create_cache_custom_ttl(self, fake_client: Any) -> None:
        fake_cache = MagicMock()
        fake_cache.name = "cachedContents/x"
        fake_client.aio.caches.create.return_value = fake_cache

        client = GeminiClient(api_key="x")
        await client.create_cache(contents=["x"], ttl_seconds=3600)
        cfg = fake_client.aio.caches.create.call_args.kwargs["config"]
        assert cfg.ttl == "3600s"

    async def test_delete_cache(self, fake_client: Any) -> None:
        client = GeminiClient(api_key="x")
        await client.delete_cache("cachedContents/abc")
        fake_client.aio.caches.delete.assert_awaited_once_with(name="cachedContents/abc")
