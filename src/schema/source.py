"""Source-type and collection-method enums + SourceRef model.

Keep `SourceType` in sync with `config/source-registry.yaml` `source_types_allowed`.
Keep `CollectionMethod` in sync with the registry's `collection_method` values.

Master PRD reference: Section 7 (Source Type Taxonomy), Section 9 (Collection
Method Policy). SCOPE_LOCK.md governs which source types may be automated.
"""
from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class SourceType(StrEnum):
    """Approved source types per master PRD Section 7 + SCOPE_LOCK.md.

    Excluded source types (linkedin_company_page, paywalled_analyst_report,
    gated_webinar, etc.) are intentionally omitted from this enum so that
    no automated stage can produce a Finding from a non-compliant source.
    """

    HOMEPAGE = "homepage"
    PRODUCT_PAGE = "product_page"
    SOLUTION_PAGE = "solution_page"
    PRICING_PAGE = "pricing_page"
    BLOG = "blog"
    RESOURCE_CENTER = "resource_center"
    NEWSROOM = "newsroom"
    PRESS_RELEASE = "press_release"
    CASE_STUDY = "case_study"
    CUSTOMER_STORY = "customer_story"
    DOCS = "docs"
    RELEASE_NOTES = "release_notes"
    PARTNER_PAGE = "partner_page"
    INTEGRATION_PAGE = "integration_page"
    EVENTS_WEBINARS = "events_webinars"
    CAREERS = "careers"
    INVESTOR_RELATIONS = "investor_relations"
    YOUTUBE = "youtube"
    PODCAST = "podcast"
    SEC_FILING = "sec_filing"
    GITHUB_REPO = "github_repo"
    REDDIT_THREAD = "reddit_thread"
    USPTO_PATENT = "uspto_patent"
    COMPARISON_PAGE = "comparison_page"


class CollectionMethod(StrEnum):
    """How a raw item was retrieved. Drives source-health tracking and the
    error-matrix routing (e.g., circuit-break a host on RSS failures)."""

    RSS = "rss"
    SITEMAP = "sitemap"
    CRAWLER = "crawler"
    ATS_API = "ats_api"
    SEC_EDGAR = "sec_edgar"
    GITHUB_API = "github_api"
    REDDIT_API = "reddit_api"
    YOUTUBE_API = "youtube_api"
    USPTO_API = "uspto_api"
    MANUAL_UPLOAD = "manual_upload"


class SourceRef(BaseModel):
    """Reference to a source-registry entry.

    Used by Finding.source_ref (optional) and by the ingest stage to record
    which registry row produced an item. Validates against the approved
    SourceType / CollectionMethod enums.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    rank: int = Field(ge=1, description="Rank in source-registry.yaml (1-50 in v1).")
    competitor: str = Field(
        min_length=1,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="competitor.id from competitors.yaml",
    )
    url: HttpUrl
    source_type: SourceType
    collection_method: CollectionMethod
