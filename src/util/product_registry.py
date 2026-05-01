"""Lazy loader for `config/products.yaml`.

Mirrors `competitor_registry` for the product spine. Stages that need the
human name, one-line description, confirmed claims, or keyword list for a
product call into here rather than re-parsing YAML.

The synthesis stages (T5 synth_per_product, T6 synth_strategic) lean on
this heavily — they need to prime Pro with what each Doceree product
actually IS so the synthesis paragraph is grounded in reality rather than
hallucinated marketing copy.
"""
from __future__ import annotations

import logging
from pathlib import Path
from threading import Lock

logger = logging.getLogger(__name__)


_REPO_ROOT = Path(__file__).resolve().parents[2]
_PRODUCTS_PATH = _REPO_ROOT / "config" / "products.yaml"

_REGISTRY: dict[str, dict] | None = None
_LOCK = Lock()


def _load() -> dict[str, dict]:
    """Parse products.yaml into {id: record}."""
    try:
        from ruamel.yaml import YAML
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "ruamel.yaml not installed; pip install -r requirements.txt"
        ) from exc

    yaml = YAML(typ="safe")
    doc = yaml.load(_PRODUCTS_PATH.read_text(encoding="utf-8"))
    flat: dict[str, dict] = {}
    for entry in doc.get("products", []) or []:
        pid = entry.get("id")
        if pid:
            flat[pid] = entry
    return flat


def _ensure_loaded() -> dict[str, dict]:
    global _REGISTRY
    if _REGISTRY is None:
        with _LOCK:
            if _REGISTRY is None:
                _REGISTRY = _load()
                logger.debug(
                    "product_registry loaded: %d products from %s",
                    len(_REGISTRY), _PRODUCTS_PATH,
                )
    return _REGISTRY


def get_product(product_id: str) -> dict | None:
    """Return the full YAML record for `product_id`, or None if missing."""
    return _ensure_loaded().get(product_id)


def get_name(product_id: str) -> str | None:
    rec = get_product(product_id)
    if rec is None:
        return None
    name = rec.get("name")
    return name if isinstance(name, str) else None


def get_one_line(product_id: str) -> str | None:
    rec = get_product(product_id)
    if rec is None:
        return None
    one_line = rec.get("one_line")
    return one_line if isinstance(one_line, str) else None


def get_confirmed_claims(product_id: str) -> list[str]:
    rec = get_product(product_id)
    if rec is None:
        return []
    claims = rec.get("confirmed_claims")
    return list(claims) if isinstance(claims, list) else []


def all_product_ids() -> list[str]:
    return list(_ensure_loaded().keys())


def _reload() -> None:
    """Re-read the YAML from disk. Useful in tests."""
    global _REGISTRY
    with _LOCK:
        _REGISTRY = None
    _ensure_loaded()
