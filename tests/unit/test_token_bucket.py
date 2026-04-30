"""Tests for `util.token_bucket.TokenBucket`.

Uses an injectable `clock` callable so we can advance time deterministically
without sleeping. Asyncio.sleep is monkey-patched in tests that need to
short-circuit waits.
"""
from __future__ import annotations

import asyncio

import pytest

from util.token_bucket import TokenBucket


class FakeClock:
    """A fake monotonic clock that only advances when `tick()` is called."""

    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def tick(self, seconds: float) -> None:
        self.t += seconds


# ---- Construction & validation ----


class TestConstruction:
    def test_default_capacity_equals_rate(self) -> None:
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, clock=clock)
        assert b.capacity == 60.0
        assert b.tokens == 60.0  # starts full

    def test_explicit_capacity(self) -> None:
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, capacity=10, clock=clock)
        assert b.capacity == 10.0
        assert b.tokens == 10.0

    def test_rate_must_be_positive(self) -> None:
        with pytest.raises(ValueError):
            TokenBucket(rate_per_minute=0)
        with pytest.raises(ValueError):
            TokenBucket(rate_per_minute=-1)

    def test_capacity_must_be_positive(self) -> None:
        with pytest.raises(ValueError):
            TokenBucket(rate_per_minute=60, capacity=0)


# ---- Acquire ----


@pytest.mark.asyncio
class TestAcquire:
    async def test_acquire_one_when_full(self) -> None:
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, clock=clock)
        await b.acquire(1)
        assert b.tokens == pytest.approx(59.0)

    async def test_acquire_multiple(self) -> None:
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, clock=clock)
        await b.acquire(5)
        assert b.tokens == pytest.approx(55.0)

    async def test_acquire_zero_is_noop(self) -> None:
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, clock=clock)
        await b.acquire(0)
        assert b.tokens == 60.0

    async def test_acquire_more_than_capacity_raises(self) -> None:
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, clock=clock)
        with pytest.raises(ValueError):
            await b.acquire(100)

    async def test_acquire_exact_capacity_succeeds(self) -> None:
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, clock=clock)
        await b.acquire(60)
        assert b.tokens == pytest.approx(0.0)


# ---- Refill ----


@pytest.mark.asyncio
class TestRefill:
    async def test_tokens_refill_over_time(self) -> None:
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, clock=clock)
        await b.acquire(60)  # drain
        assert b.tokens == pytest.approx(0.0)

        clock.tick(30)  # 30 seconds at 1 token/s
        assert b.tokens == pytest.approx(30.0)

    async def test_refill_capped_at_capacity(self) -> None:
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, clock=clock)
        await b.acquire(10)
        assert b.tokens == pytest.approx(50.0)

        clock.tick(120)  # would refill 120 tokens, but cap is 60
        assert b.tokens == pytest.approx(60.0)

    async def test_partial_refill(self) -> None:
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=120, clock=clock)  # 2 tokens/s
        await b.acquire(120)  # drain
        clock.tick(0.5)  # 1 token
        assert b.tokens == pytest.approx(1.0)


# ---- Blocking under contention ----


@pytest.mark.asyncio
class TestBlocking:
    async def test_acquire_blocks_until_refill(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When the bucket is empty, acquire(1) waits until 1 token has
        refilled. We monkey-patch asyncio.sleep to advance the fake clock
        by the requested duration instead of actually sleeping."""
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, clock=clock)  # 1 token/s
        await b.acquire(60)  # drain
        assert b.tokens == pytest.approx(0.0)

        sleeps: list[float] = []

        async def fake_sleep(seconds: float) -> None:
            sleeps.append(seconds)
            clock.tick(seconds)

        monkeypatch.setattr("asyncio.sleep", fake_sleep)
        await b.acquire(1)
        # We slept ~1 second to refill the 1 token we needed.
        assert sleeps and sleeps[0] == pytest.approx(1.0, abs=0.01)
        assert b.tokens == pytest.approx(0.0, abs=0.01)

    async def test_high_tpm_bucket_serves_large_acquires(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The shared TPM bucket (250K/min, capacity 250K) should serve a
        single acquire of, say, 4000 tokens immediately (no wait)."""
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=250_000, capacity=250_000, clock=clock)

        sleeps: list[float] = []

        async def fake_sleep(seconds: float) -> None:
            sleeps.append(seconds)

        monkeypatch.setattr("asyncio.sleep", fake_sleep)
        await b.acquire(4000)
        assert sleeps == []  # no waits
        assert b.tokens == pytest.approx(246_000.0)

    async def test_concurrent_acquire_serialized(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Two concurrent acquires that together exceed capacity must NOT
        deadlock; the second one waits for refill."""
        clock = FakeClock()
        b = TokenBucket(rate_per_minute=60, clock=clock)  # 1 token/s, cap 60

        async def fake_sleep(seconds: float) -> None:
            clock.tick(seconds)

        monkeypatch.setattr("asyncio.sleep", fake_sleep)
        await b.acquire(60)  # drain
        # Now run two concurrent acquires of 30 each. Each needs 30s of refill.
        await asyncio.gather(b.acquire(30), b.acquire(30))
        # After both succeed, tokens should be ~0 again.
        assert b.tokens == pytest.approx(0.0, abs=0.5)
