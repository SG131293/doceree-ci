"""Shared HTTP client with per-host circuit breaker.

Wraps `httpx.AsyncClient` with:
  - HTTP/2 enabled (cuts head-of-line blocking when fanning out to many hosts).
  - Connect / read / write / pool timeouts (10s connect, 30s read).
  - Connection-pool cap of 20.
  - Per-host circuit breaker: 5 failures in 60s opens for 5 minutes.
  - A friendly User-Agent identifying the project for site operators.
  - Automatic redirect-following so callers see the final URL on response.url.

The circuit breaker prevents the pipeline from hammering a host that's down,
which would burn the run's wall-clock budget on retries that will all fail.
After the 5-minute open window elapses, the host's failure history is reset
and traffic resumes (matching the build plan's spec).

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 5.
"""
from __future__ import annotations

import asyncio
import logging
import time
from collections import defaultdict
from collections.abc import Callable
from types import TracebackType
from typing import Any
from urllib.parse import urlsplit

import httpx

logger = logging.getLogger(__name__)


class CircuitBreakerOpen(Exception):
    """Raised when a request is blocked because the host's circuit is open."""

    def __init__(self, host: str, opened_at: float, until: float) -> None:
        self.host = host
        self.opened_at = opened_at
        self.until = until
        super().__init__(
            f"Circuit breaker open for host {host!r} "
            f"(opened at t={opened_at:.1f}, reopens after t={until:.1f})"
        )


class CircuitBreaker:
    """Per-host circuit breaker.

    Defaults match the build plan: 5 failures in 60 seconds opens the
    breaker for 300 seconds (5 minutes). After the open window elapses,
    state is fully reset for that host - the next call goes through and the
    failure window starts fresh.

    Network errors and 5xx responses count as failures; 4xx responses do
    not (the request reached the server, so the host is up).
    """

    def __init__(
        self,
        *,
        failure_threshold: int = 5,
        window_seconds: float = 60.0,
        open_duration_seconds: float = 300.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if failure_threshold < 1:
            raise ValueError(f"failure_threshold must be >= 1; got {failure_threshold}")
        if window_seconds <= 0 or open_duration_seconds <= 0:
            raise ValueError("window_seconds and open_duration_seconds must be > 0")

        self.failure_threshold = failure_threshold
        self.window_seconds = window_seconds
        self.open_duration_seconds = open_duration_seconds
        self._clock = clock
        self._failures: dict[str, list[float]] = defaultdict(list)
        self._opened_at: dict[str, float] = {}
        self._lock = asyncio.Lock()

    async def check(self, host: str) -> None:
        """Raise if `host` is currently blocked. No-op otherwise.

        Side effect: if the open window has elapsed, fully reset state for
        the host (transition back to CLOSED with empty failure history).
        """
        async with self._lock:
            opened_at = self._opened_at.get(host)
            if opened_at is None:
                return
            now = self._clock()
            until = opened_at + self.open_duration_seconds
            if now < until:
                raise CircuitBreakerOpen(host, opened_at, until)
            del self._opened_at[host]
            self._failures.pop(host, None)
            logger.info("Circuit breaker for %s reset (open window elapsed)", host)

    async def record_success(self, host: str) -> None:
        """Clear failure history for `host` (transitions to CLOSED)."""
        async with self._lock:
            self._failures.pop(host, None)
            self._opened_at.pop(host, None)

    async def record_failure(self, host: str) -> None:
        """Record a failure. Opens the circuit if `failure_threshold` failures
        accumulated in the rolling `window_seconds` window."""
        async with self._lock:
            now = self._clock()
            cutoff = now - self.window_seconds
            failures = self._failures[host]
            failures[:] = [t for t in failures if t > cutoff]
            failures.append(now)
            if len(failures) >= self.failure_threshold and host not in self._opened_at:
                self._opened_at[host] = now
                logger.warning(
                    "Circuit breaker OPEN for %s: %d failures in %.1fs",
                    host,
                    len(failures),
                    self.window_seconds,
                )

    async def is_open(self, host: str) -> bool:
        """Inspect whether the breaker is currently open for `host`. Tests-only."""
        async with self._lock:
            opened_at = self._opened_at.get(host)
            if opened_at is None:
                return False
            until = opened_at + self.open_duration_seconds
            return self._clock() < until


DEFAULT_USER_AGENT = "doceree-ci/0.1 (+https://doceree.com; competitive-intel)"
DEFAULT_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"


class HttpClient:
    """Shared `httpx.AsyncClient` with circuit-breaker protection.

    Use as an async context manager so the underlying client is closed
    cleanly on shutdown:

        async with HttpClient() as http:
            response = await http.get("https://www.optimizerx.com/")

    For tests, pass `transport=httpx.MockTransport(handler)` to the
    constructor (the kwarg is forwarded to `httpx.AsyncClient`).
    """

    def __init__(
        self,
        *,
        connect_timeout: float = 10.0,
        read_timeout: float = 30.0,
        pool_size: int = 20,
        http2: bool = True,
        user_agent: str = DEFAULT_USER_AGENT,
        circuit_breaker: CircuitBreaker | None = None,
        client: httpx.AsyncClient | None = None,
        **httpx_kwargs: Any,
    ) -> None:
        if client is not None:
            self._client = client
            self._owns_client = False
        else:
            timeout = httpx.Timeout(
                connect=connect_timeout,
                read=read_timeout,
                write=read_timeout,
                pool=connect_timeout,
            )
            limits = httpx.Limits(
                max_connections=pool_size,
                max_keepalive_connections=pool_size,
            )
            headers = {
                "User-Agent": user_agent,
                "Accept": DEFAULT_ACCEPT,
                "Accept-Language": "en",
            }
            self._client = httpx.AsyncClient(
                http2=http2,
                timeout=timeout,
                limits=limits,
                follow_redirects=True,
                headers=headers,
                **httpx_kwargs,
            )
            self._owns_client = True

        self.breaker = circuit_breaker if circuit_breaker is not None else CircuitBreaker()

    # ---- Context manager ----

    async def __aenter__(self) -> HttpClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    # ---- Internals ----

    @staticmethod
    def _host_of(url: str) -> str:
        return (urlsplit(url).hostname or "").lower()

    async def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Make a request through the circuit breaker.

        Records a failure on `httpx.NetworkError` / `httpx.TimeoutException`
        or any 5xx status. Records a success on any other completed response
        (including 4xx, since the host is up).

        Raises:
            CircuitBreakerOpen: the host is currently blocked.
            httpx.HTTPError: any underlying network or protocol error after
                the breaker has been told.
        """
        host = self._host_of(url)
        await self.breaker.check(host)
        try:
            response = await self._client.request(method, url, **kwargs)
        except (httpx.NetworkError, httpx.TimeoutException):
            await self.breaker.record_failure(host)
            raise

        if 500 <= response.status_code < 600:
            await self.breaker.record_failure(host)
        else:
            await self.breaker.record_success(host)
        return response

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        return await self.request("GET", url, **kwargs)

    async def head(self, url: str, **kwargs: Any) -> httpx.Response:
        return await self.request("HEAD", url, **kwargs)
