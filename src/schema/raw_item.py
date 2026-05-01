"""RawItem: the output of T1 (ingest), input to T2 (filter).

A RawItem is what comes out of an RSS feed / sitemap / API source. It carries
enough metadata for the filter and extract stages to reason about the item
without going back to the source. RawItems are NOT persisted to the archive;
only Findings are. RawItems exist only for the duration of a single pipeline
run.

Sprint 8 additions:
- `canonical_url` and `publisher_domain` are populated by the ingester when
  the wire URL is a wrapper (e.g., Google News redirect). Both flow forward
  into the Finding so the renderer can show the publisher domain instead of
  the opaque wrapper URL.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from .source import CollectionMethod, SourceType


class RawItem(BaseModel):
    """Single item produced by an ingester.

    Examples:
      RSS feed entry  -> one RawItem per <item>
      Sitemap diff    -> one RawItem per new URL (after fetching the page)
      SEC EDGAR API   -> one RawItem per filing
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    url: HttpUrl
    canonical_url: HttpUrl | None = Field(
        default=None,
        description="Publisher's article URL if `url` is a wrapper (e.g., a "
                    "Google News redirect). None when `url` is already canonical.",
    )
    publisher_domain: str | None = Field(
        default=None,
        max_length=255,
        description="eTLD+1 of canonical_url (or url). Used by url_health to "
                    "verify the article is actually about the named competitor.",
    )
    title: str = Field(min_length=1, max_length=1000)
    summary: str = Field(default="", max_length=10_000)
    competitor: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="competitor.id from config/competitors.yaml.",
    )
    source_type: SourceType
    collection_method: CollectionMethod
    published_at: datetime | None = Field(
        default=None,
        description="When the upstream source published the item (if known).",
    )
    fetched_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When this RawItem was created (T1 ingest time).",
    )

    @field_validator("published_at", "fetched_at")
    @classmethod
    def timestamps_must_be_aware(cls, v: datetime | None) -> datetime | None:
        if v is not None and v.tzinfo is None:
            raise ValueError("timestamps must be timezone-aware")
        return v

    @property
    def content_hash(self) -> str:
        """Stable SHA-256 hex of url + title + first 500 chars of summary.

        Used as the seed for `Finding.finding_id` and for dedup against the
        30-day archive (T4d). Truncating the summary is a cheap way to keep
        the hash stable when minor whitespace / formatting changes happen
        between fetches of the same item.
        """
        h = sha256()
        h.update(str(self.url).encode("utf-8"))
        h.update(b"\x1f")  # ASCII unit-separator
        h.update(self.title.encode("utf-8"))
        h.update(b"\x1f")
        h.update(self.summary[:500].encode("utf-8"))
        return h.hexdigest()
