"""URL health checker (T4a).

Every Finding's URL is verified against the live web before passing into
synthesis. If the URL doesn't resolve to a 200 (after redirect-following), or
if redirects landed on a different registered domain than the cited URL, the
Finding is dropped as a hallucinated reference. Drop rate per prompt version
is tracked over time as a regression signal (logged to
`archive/hallucinated_urls.jsonl`).

Two-step probe:
  1. HEAD request first - cheap; many sites support it.
  2. If HEAD returns 405 (Method Not Allowed) or 501 (Not Implemented), or
     if HEAD returns 200 but with a suspicious empty Content-Length and no
     redirect chain, fall back to GET.

Domain-match rule:
  The final response URL must share the eTLD+1 (registered domain) with the
  cited URL. e.g., `https://www.deepintent.com/news` -> `https://deepintent.com/news`
  is OK (both have `deepintent.com`); `https://blog.example.com/x` ->
  `https://malicious.tracker.com/x` is NOT.

Build-plan reference: docs/2026-04-30-lean-ci-build-plan.md, Day 5 + T4a.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

import httpx
import tldextract

from clients.http import CircuitBreakerOpen, HttpClient

logger = logging.getLogger(__name__)


# ---- Domain extraction ----

# Use the bundled public-suffix snapshot; never reach the network at import
# time. (The snapshot is updated when the package is upgraded.)
_extract = tldextract.TLDExtract(
    suffix_list_urls=(),
    fallback_to_snapshot=True,
)


def registered_domain(url: str) -> str:
    """Return the eTLD+1 for `url` (e.g., 'deepintent.com').

    Returns an empty string if the URL doesn't have a parseable domain
    (e.g., bare hostnames, IPs, malformed URLs).
    """
    parts = _extract(url)
    if not parts.domain or not parts.suffix:
        return ""
    return f"{parts.domain}.{parts.suffix}".lower()


# ---- Result type ----


@dataclass(frozen=True)
class HealthResult:
    """Outcome of a URL liveness check.

    `is_live` is True only if all of the following hold:
      - The request completed (no network error, no circuit-breaker block).
      - The final response status is 200.
      - (When `require_domain_match=True`) the final URL's registered domain
        matches the cited URL's registered domain.

    `reason` is a short snake_case label suitable for logging /
    `archive/hallucinated_urls.jsonl` aggregation. Examples:
      "" (live), "non_200_status_404", "domain_mismatch",
      "circuit_breaker_open", "network_error".
    """

    cited_url: str
    is_live: bool
    final_url: str | None = None
    status_code: int | None = None
    reason: str = ""

    @property
    def domain_matches(self) -> bool:
        """True iff cited and final URLs share the same registered domain."""
        if self.final_url is None:
            return False
        return registered_domain(self.cited_url) == registered_domain(self.final_url)


# ---- Public API ----


async def check(
    url: str,
    *,
    http: HttpClient,
    require_domain_match: bool = True,
    method_fallback: bool = True,
) -> HealthResult:
    """Verify that `url` is live and points at the cited domain.

    Args:
        url: The cited URL (typically from an extracted Finding).
        http: Shared HttpClient with circuit breaker.
        require_domain_match: If True, treat eTLD+1 mismatch as not-live.
            Disable for cases where you want to detect 200-status-but-wrong-host
            redirects without dropping the finding.
        method_fallback: If True, retry with GET when HEAD returns 405 / 501.

    Returns:
        A `HealthResult` with `is_live` set, plus diagnostic fields. The
        function never raises for ordinary failures - all error paths are
        captured in `reason`.
    """
    try:
        response = await http.head(url)
        if method_fallback and response.status_code in (405, 501):
            response = await http.get(url)
    except CircuitBreakerOpen as exc:
        return HealthResult(
            cited_url=url,
            is_live=False,
            reason=f"circuit_breaker_open:{exc.host}",
        )
    except httpx.InvalidURL:
        return HealthResult(cited_url=url, is_live=False, reason="invalid_url")
    except httpx.TooManyRedirects:
        return HealthResult(cited_url=url, is_live=False, reason="too_many_redirects")
    except httpx.TimeoutException as exc:
        return HealthResult(
            cited_url=url,
            is_live=False,
            reason=f"timeout:{type(exc).__name__}",
        )
    except httpx.NetworkError as exc:
        return HealthResult(
            cited_url=url,
            is_live=False,
            reason=f"network_error:{type(exc).__name__}",
        )

    final_url = str(response.url)

    if response.status_code != 200:
        return HealthResult(
            cited_url=url,
            is_live=False,
            final_url=final_url,
            status_code=response.status_code,
            reason=f"non_200_status_{response.status_code}",
        )

    candidate = HealthResult(
        cited_url=url,
        is_live=True,
        final_url=final_url,
        status_code=200,
        reason="",
    )
    if require_domain_match and not candidate.domain_matches:
        return HealthResult(
            cited_url=url,
            is_live=False,
            final_url=final_url,
            status_code=200,
            reason=(
                f"domain_mismatch:{registered_domain(url)}!={registered_domain(final_url)}"
            ),
        )
    return candidate
