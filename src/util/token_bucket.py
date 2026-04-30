"""Async-safe token bucket for rate limiting.

Used by `clients.gemini.GeminiClient` to enforce per-model RPM and shared TPM
limits without relying on server-side 429s. Each acquire() blocks until enough
tokens are available, then consumes them atomically.

Design:
- Refill rate is configured per-minute (e.g., 5 RPM, 250_000 TPM).
- `capacity` defaults to `rate_per_minute` (one minute of burst). Can be
  configured separately for buckets where burst != steady-state (e.g., the
  shared TPM bucket).
- `clock` is injectable so tests can advance time deterministically.
- `asyncio.Lock` serializes acquirers so capacity is never overdrawn under
  concurrent contention.

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 4.
"""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from time import monotonic


class TokenBucket:
    """Async-safe token bucket. Refills at `rate_per_minute` up to `capacity`."""

    def __init__(
        self,
        *,
        rate_per_minute: float,
        capacity: float | None = None,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        if rate_per_minute <= 0:
            raise ValueError(f"rate_per_minute must be > 0; got {rate_per_minute}")
        cap = float(capacity if capacity is not None else rate_per_minute)
        if cap <= 0:
            raise ValueError(f"capacity must be > 0; got {cap}")

        self.rate_per_second: float = rate_per_minute / 60.0
        self.capacity: float = cap
        self._clock: Callable[[], float] = clock
        self._tokens: float = cap
        self._last_refill: float = clock()
        self._lock = asyncio.Lock()

    def _refill(self) -> None:
        """Add tokens accumulated since the last refill (no waiting)."""
        now = self._clock()
        elapsed = now - self._last_refill
        if elapsed > 0:
            self._tokens = min(self.capacity, self._tokens + elapsed * self.rate_per_second)
            self._last_refill = now

    async def acquire(self, n: float = 1.0) -> None:
        """Block until `n` tokens are available, then consume them.

        Raises ValueError if `n` exceeds capacity (would block forever).
        """
        if n <= 0:
            return
        if n > self.capacity:
            raise ValueError(
                f"cannot acquire {n} tokens; bucket capacity is {self.capacity}"
            )

        while True:
            async with self._lock:
                self._refill()
                if self._tokens >= n:
                    self._tokens -= n
                    return
                deficit = n - self._tokens
                wait_seconds = deficit / self.rate_per_second
            # Release lock during sleep so the clock can advance via the
            # injected `clock` callable in tests, and so concurrent acquirers
            # waiting on smaller `n` can make progress between bursts.
            await asyncio.sleep(wait_seconds)

    @property
    def tokens(self) -> float:
        """Current token count after a refill. For inspection / tests only."""
        self._refill()
        return self._tokens
