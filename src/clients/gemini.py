"""Gemini client wrapper for the Doceree CI pipeline.

Wraps the `google-genai` SDK with:
  - Token-bucket rate limiting: 5 RPM Pro, 10 RPM Flash, 15 RPM Flash-Lite,
    250K TPM shared across all models.
  - Tenacity retry: 3 attempts, jittered exponential backoff 1s/4s/16s.
    Retries on 429 / 5xx; never on 400 / 403.
  - Structured outputs: `response_mime_type="application/json"` plus a Pydantic
    `response_schema` so callers get typed objects back, not raw strings.
  - Per-call-type `thinking_budget`: filter=0, extract=512, adversarial=4096,
    synth=8192. Cheaper stages skip the reasoning compute; expensive stages
    get more.
  - Implicit cache friendliness: prompts are passed as a single string with
    the static prefix first so the SDK's implicit cache can hit it.
  - Explicit cache management: `create_cache()` returns a resource name that
    callers pass back via `cached_content=` for 90 percent token discount on
    Pro synthesis stages.

The wrapper methods (`filter`, `extract`, `adversarial_check`, `synthesize`)
are thin shims over `generate()` that lock in the right call type. Day 6 / 8 /
18 add the actual prompt files; this Day-4 layer only ships the plumbing.

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 4.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

import httpx
from google import genai
from google.genai import errors as genai_errors
from google.genai import types as genai_types
from pydantic import BaseModel
from tenacity import (
    AsyncRetrying,
    before_sleep_log,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

from util.token_bucket import TokenBucket

logger = logging.getLogger(__name__)


# ---- Pinned model identifiers ----
# The build plan's `-001` suffix convention was the Gemini 2.0 stable scheme;
# Gemini 2.5 went stable without a numeric sub-version (the bare name IS
# the pinned stable). We avoid `-latest` aliases so an upstream model bump
# doesn't silently change behavior between runs.
MODEL_FLASH_LITE = "gemini-2.5-flash-lite"
MODEL_FLASH = "gemini-2.5-flash"
MODEL_PRO = "gemini-2.5-pro"


@dataclass(frozen=True)
class CallType:
    """Configuration for one typed call into Gemini.

    Mirrors the schema of `config/prompts.yaml` (added Day 5+). Each pipeline
    stage has its own CallType so the model / temperature / thinking_budget
    are pinned per stage rather than passed ad-hoc.
    """

    name: str
    model: str
    temperature: float
    thinking_budget: int
    max_output_tokens: int


# Defaults per build plan Day 4 + the prompts.yaml example. These match the
# stage names used in the pipeline (filter, extract, adversarial_check, etc.).
CALL_TYPES: dict[str, CallType] = {
    "filter": CallType(
        name="filter",
        model=MODEL_FLASH_LITE,
        temperature=0.0,
        thinking_budget=0,
        max_output_tokens=512,
    ),
    "extract": CallType(
        name="extract",
        model=MODEL_FLASH,
        temperature=0.1,
        thinking_budget=512,
        max_output_tokens=2048,
    ),
    # Sprint 8 stage 4a: cheap attribution check on Flash. Per RawItem,
    # answers "is this competitor actually the subject?" before paying for
    # extract on items the source feed mistakenly tagged.
    "attribution_check": CallType(
        name="attribution_check",
        model=MODEL_FLASH,
        temperature=0.0,
        thinking_budget=0,
        max_output_tokens=256,
    ),
    "adversarial_check": CallType(
        name="adversarial_check",
        model=MODEL_PRO,
        temperature=0.0,
        thinking_budget=4096,
        max_output_tokens=2048,
    ),
    "synth_per_product": CallType(
        name="synth_per_product",
        model=MODEL_PRO,
        temperature=0.3,
        thinking_budget=8192,
        max_output_tokens=8192,
    ),
    "synth_strategic": CallType(
        name="synth_strategic",
        model=MODEL_PRO,
        temperature=0.4,
        thinking_budget=8192,
        max_output_tokens=4096,
    ),
    "pattern_detect": CallType(
        name="pattern_detect",
        model=MODEL_PRO,
        temperature=0.2,
        thinking_budget=4096,
        max_output_tokens=4096,
    ),
    "battlecard_draft": CallType(
        name="battlecard_draft",
        model=MODEL_PRO,
        temperature=0.3,
        thinking_budget=8192,
        max_output_tokens=8192,
    ),
    "new_entrant_discovery": CallType(
        name="new_entrant_discovery",
        model=MODEL_PRO,
        temperature=0.5,
        thinking_budget=16384,
        max_output_tokens=8192,
    ),
}


def _sanitize_schema_for_gemini(schema: object) -> object:
    """Strip JSON-schema fields that Gemini's `response_schema` rejects.

    Gemini accepts a strict subset of JSON Schema. The fields below are emitted
    by Pydantic 2 but are not recognized by Gemini and cause a 400 INVALID_ARGUMENT:
      - `additionalProperties`  Pydantic emits this for `ConfigDict(extra="forbid")`.
      - `$schema`               Pydantic adds this at the top level.
      - `$defs`                 Definitions block for nested models (we inline
                                via `mode="serialization"` instead, but if any
                                slip through, drop them).

    Mutates `schema` in place AND returns it for convenience.
    """
    if isinstance(schema, dict):
        schema.pop("additionalProperties", None)
        schema.pop("$schema", None)
        schema.pop("$defs", None)
        for v in schema.values():
            _sanitize_schema_for_gemini(v)
    elif isinstance(schema, list):
        for v in schema:
            _sanitize_schema_for_gemini(v)
    return schema


def is_retryable(exc: BaseException) -> bool:
    """True iff `exc` is a transient error worth retrying.

    Retry on:
      - `httpx.TimeoutException` and `httpx.NetworkError` (connection-layer
        failures that often clear up on the next attempt).
      - `genai.errors.APIError` with code 429 (RESOURCE_EXHAUSTED) or 5xx
        (server errors).

    Never retry on:
      - 400 INVALID_ARGUMENT (our prompt or schema is wrong - retrying
        won't help).
      - 403 PERMISSION_DENIED (auth / quota config issue).
      - 404 NOT_FOUND.
      - Anything that isn't an APIError or transient network error.
    """
    if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
        return True
    if isinstance(exc, genai_errors.APIError):
        code = getattr(exc, "code", None)
        if code == 429:
            return True
        if isinstance(code, int) and 500 <= code < 600:
            return True
    return False


class GeminiClient:
    """Async Gemini client with rate-limit + retry + structured output.

    Construct once at process start and share across all stages. Internal
    token buckets are per-instance, so spawning multiple instances would
    over-consume the upstream RPM/TPM limits.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        flash_lite_rpm: float = 15,
        flash_rpm: float = 10,
        pro_rpm: float = 5,
        shared_tpm: float = 250_000,
        max_retry_attempts: int = 3,
    ) -> None:
        key = api_key if api_key is not None else os.environ.get("GEMINI_API_KEY", "").strip()
        if not key:
            raise RuntimeError(
                "GEMINI_API_KEY not set. Pass api_key=... or load from .env "
                "before constructing GeminiClient."
            )
        self._client = genai.Client(api_key=key)
        self._max_retry_attempts = max_retry_attempts

        # Per-model RPM buckets. 1 token = 1 request.
        self._buckets: dict[str, TokenBucket] = {
            MODEL_FLASH_LITE: TokenBucket(rate_per_minute=flash_lite_rpm),
            MODEL_FLASH: TokenBucket(rate_per_minute=flash_rpm),
            MODEL_PRO: TokenBucket(rate_per_minute=pro_rpm),
        }
        # Shared TPM bucket. 1 token ~= 1 model token (input + output).
        # Capacity equals the per-minute rate (no extra burst above steady).
        self._tpm_bucket = TokenBucket(
            rate_per_minute=shared_tpm,
            capacity=shared_tpm,
        )

    # ---- Generic call ----

    async def generate(
        self,
        *,
        call_type: str,
        prompt: str,
        response_schema: type[BaseModel] | None = None,
        cached_content: str | None = None,
        max_output_tokens: int | None = None,
        estimate_input_tokens: int | None = None,
    ) -> Any:
        """Single typed call into Gemini.

        Args:
            call_type: Key into `CALL_TYPES` (filter / extract / ...).
            prompt: Full user prompt. Put the static prefix first for the
                    SDK's implicit-cache to hit it.
            response_schema: Pydantic model. If set, the response is parsed
                             and validated against this schema before return.
                             If None, returns the raw text string.
            cached_content: Resource name from `create_cache()`. Pro only.
            max_output_tokens: Override the call type's default cap.
            estimate_input_tokens: Best-effort estimate for the shared TPM
                                   bucket. Defaults to len(prompt) // 4 (a
                                   conservative ~4-chars-per-token approximation).

        Returns:
            An instance of `response_schema` if set, else the raw response text.

        Raises:
            ValueError: unknown `call_type`.
            genai.errors.APIError: 4xx errors that aren't retried (400 / 403 /
                                    404), or any error after 3 retry attempts.
        """
        cfg = CALL_TYPES.get(call_type)
        if cfg is None:
            raise ValueError(f"Unknown call_type: {call_type!r}")

        # 1) RPM bucket: one token per request.
        await self._buckets[cfg.model].acquire(1)

        # 2) TPM bucket: estimate input + output tokens.
        est_in = (
            estimate_input_tokens
            if estimate_input_tokens is not None
            else max(1, len(prompt) // 4)
        )
        est_out = max_output_tokens if max_output_tokens is not None else cfg.max_output_tokens
        # Cap at TPM capacity to avoid the "n > capacity" guard. In practice
        # individual calls stay well under 250K.
        tpm_estimate = min(self._tpm_bucket.capacity, float(est_in + est_out))
        await self._tpm_bucket.acquire(tpm_estimate)

        # 3) Build the SDK config.
        config_kwargs: dict[str, Any] = {
            "temperature": cfg.temperature,
            "max_output_tokens": (
                max_output_tokens if max_output_tokens is not None else cfg.max_output_tokens
            ),
        }
        if cfg.thinking_budget > 0:
            config_kwargs["thinking_config"] = genai_types.ThinkingConfig(
                thinking_budget=cfg.thinking_budget,
            )
        if response_schema is not None:
            config_kwargs["response_mime_type"] = "application/json"
            # Convert to dict + sanitize. Gemini's `response_schema` rejects
            # several JSON Schema fields Pydantic emits by default.
            schema_dict = response_schema.model_json_schema()
            _sanitize_schema_for_gemini(schema_dict)
            config_kwargs["response_schema"] = schema_dict
        if cached_content is not None:
            config_kwargs["cached_content"] = cached_content

        config = genai_types.GenerateContentConfig(**config_kwargs)

        # 4) Call with retry. AsyncRetrying iterates attempts; each yields an
        # AttemptManager whose `with attempt:` block records the outcome.
        response = None
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(self._max_retry_attempts),
            wait=wait_exponential_jitter(initial=1, max=16, exp_base=4),
            retry=retry_if_exception(is_retryable),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        ):
            with attempt:
                response = await self._client.aio.models.generate_content(
                    model=cfg.model,
                    contents=prompt,
                    config=config,
                )

        if response is None:  # pragma: no cover - tenacity reraises on fail
            raise RuntimeError("generate_content returned no response after retries")

        # 5) Parse / return.
        if response_schema is not None:
            return response_schema.model_validate_json(response.text)
        return response.text

    # ---- Stage shims ----

    async def filter(
        self,
        prompt: str,
        *,
        response_schema: type[BaseModel] | None = None,
    ) -> Any:
        """T2 filter call. Flash-Lite, thinking_budget=0, temperature=0."""
        return await self.generate(
            call_type="filter",
            prompt=prompt,
            response_schema=response_schema,
        )

    async def extract(
        self,
        prompt: str,
        *,
        response_schema: type[BaseModel] | None = None,
    ) -> Any:
        """T3 extract call. Flash, thinking_budget=512, temperature=0.1."""
        return await self.generate(
            call_type="extract",
            prompt=prompt,
            response_schema=response_schema,
        )

    async def attribution_check(
        self,
        prompt: str,
        *,
        response_schema: type[BaseModel] | None = None,
    ) -> Any:
        """T4a attribution-check call (Sprint 8). Flash, thinking_budget=0,
        temperature=0. Cheap per-item check that verifies the competitor
        tag before we spend extract tokens."""
        return await self.generate(
            call_type="attribution_check",
            prompt=prompt,
            response_schema=response_schema,
        )

    async def adversarial_check(
        self,
        prompt: str,
        *,
        response_schema: type[BaseModel] | None = None,
    ) -> Any:
        """T4b adversarial-check call. Pro, thinking_budget=4096, temperature=0."""
        return await self.generate(
            call_type="adversarial_check",
            prompt=prompt,
            response_schema=response_schema,
        )

    async def synthesize(
        self,
        prompt: str,
        *,
        strategic: bool = False,
        cached_content: str | None = None,
        response_schema: type[BaseModel] | None = None,
    ) -> Any:
        """T5 / T6 synthesis call. Pro, thinking_budget=8192.

        Pass `strategic=True` for the cross-product top-3 (T6); default is
        per-product synthesis (T5). `cached_content` should be the resource
        name from a `create_cache()` call covering the product spine + signal
        rules - this is the 90 percent token discount path.
        """
        call_type = "synth_strategic" if strategic else "synth_per_product"
        return await self.generate(
            call_type=call_type,
            prompt=prompt,
            response_schema=response_schema,
            cached_content=cached_content,
        )

    # ---- Explicit cache management (Pro only, 2hr TTL by default) ----

    async def create_cache(
        self,
        *,
        contents: list[str],
        ttl_seconds: int = 7200,
        display_name: str = "doceree-ci-cache",
        system_instruction: str | None = None,
    ) -> str:
        """Create an explicit cache. Returns the resource name (e.g.,
        `cachedContents/abc123`) for use with `synthesize(cached_content=...)`.

        Pass the static, large content here (product spine YAML, signal-mapping
        rules, last-30-day patterns). Calls referencing this cache pay 1/10 of
        the input-token cost.
        """
        cfg = genai_types.CreateCachedContentConfig(
            contents=contents,
            ttl=f"{ttl_seconds}s",
            display_name=display_name,
        )
        if system_instruction is not None:
            cfg.system_instruction = system_instruction
        cache = await self._client.aio.caches.create(model=MODEL_PRO, config=cfg)
        if cache.name is None:  # pragma: no cover - SDK invariant
            raise RuntimeError("caches.create returned no resource name")
        return cache.name

    async def delete_cache(self, name: str) -> None:
        """Delete an explicit cache. Safe to call on already-expired caches."""
        await self._client.aio.caches.delete(name=name)
