"""Lazy loader for `config/competitors.yaml`.

Stages that need to look up a competitor's `category`, `name`, or any other
config-time attribute call `get_competitor(id)` here. The YAML is parsed once
and cached for the lifetime of the process; reload by calling `_reload()` in
tests if you need to.

Why a module-level cache rather than passing the loaded config around:
  - Most call sites (extract, render) need a single competitor field, not the
    whole config blob. Threading the dict through every signature would be
    noisy.
  - The registry is read-only at runtime. Mutability concerns don't apply.
  - Tests can override behavior by monkey-patching `_REGISTRY` or `get_competitor`.

This module deliberately does NOT pull in pydantic schemas. The registry's
job is to surface raw YAML records; conversion to typed schemas happens at
the call site if needed.
"""
from __future__ import annotations

import logging
from pathlib import Path
from threading import Lock

logger = logging.getLogger(__name__)


# Path layout: src/util/this_file.py -> ../../config/competitors.yaml
_REPO_ROOT = Path(__file__).resolve().parents[2]
_COMPETITORS_PATH = _REPO_ROOT / "config" / "competitors.yaml"

_REGISTRY: dict[str, dict] | None = None
_LOCK = Lock()


def _load() -> dict[str, dict]:
    """Parse competitors.yaml into {id: record} flattened across tiers."""
    try:
        from ruamel.yaml import YAML
    except ImportError as exc:  # pragma: no cover - covered by integration
        raise RuntimeError(
            "ruamel.yaml not installed; pip install -r requirements.txt"
        ) from exc

    yaml = YAML(typ="safe")
    doc = yaml.load(_COMPETITORS_PATH.read_text(encoding="utf-8"))
    flat: dict[str, dict] = {}
    for group_key in ("tier_1", "tier_2_mvp_cohort", "healthcare_ai_cluster"):
        for entry in doc.get(group_key, []) or []:
            cid = entry.get("id")
            if not cid:
                continue
            # Stash the source group under `_tier` so callers don't need to
            # know which array they came from.
            entry = {**entry, "_tier": group_key}
            flat[cid] = entry
    return flat


def _ensure_loaded() -> dict[str, dict]:
    global _REGISTRY
    if _REGISTRY is None:
        with _LOCK:
            if _REGISTRY is None:
                _REGISTRY = _load()
                logger.debug(
                    "competitor_registry loaded: %d competitors from %s",
                    len(_REGISTRY), _COMPETITORS_PATH,
                )
    return _REGISTRY


def get_competitor(competitor_id: str) -> dict | None:
    """Return the full YAML record for `competitor_id`, or None if missing.

    Treat the result as read-only.
    """
    return _ensure_loaded().get(competitor_id)


def get_category(competitor_id: str) -> str | None:
    """Return the `category` field for `competitor_id`, or None if the
    competitor is unknown or has no category set."""
    rec = get_competitor(competitor_id)
    if rec is None:
        return None
    cat = rec.get("category")
    return cat if isinstance(cat, str) else None


def get_name(competitor_id: str) -> str | None:
    """Return the human-readable name for `competitor_id`, or None."""
    rec = get_competitor(competitor_id)
    if rec is None:
        return None
    name = rec.get("name")
    return name if isinstance(name, str) else None


def get_related_products(competitor_id: str) -> list[str]:
    """Return the `related_doceree_products` list for `competitor_id`. Empty
    list if missing or unknown."""
    rec = get_competitor(competitor_id)
    if rec is None:
        return []
    products = rec.get("related_doceree_products")
    return list(products) if isinstance(products, list) else []


def all_competitor_ids() -> list[str]:
    """Return all known competitor IDs across all tiers."""
    return list(_ensure_loaded().keys())


def _reload() -> None:
    """Re-read the YAML from disk. Useful in tests after monkey-patching the
    file or after edits during long-running dev sessions."""
    global _REGISTRY
    with _LOCK:
        _REGISTRY = None
    _ensure_loaded()
