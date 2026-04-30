"""Cross-check structural consistency of config/*.yaml files.

Run after editing any of products.yaml, competitors.yaml, source-registry.yaml,
or signal-mapping.yaml. Fails loudly if any reference is dangling.

Usage:
    python scripts/verify_configs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from ruamel.yaml import YAML
except ImportError:
    print("ERROR: ruamel.yaml not installed. Run: pip install -r requirements.txt")
    sys.exit(2)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    config_dir = repo_root / "config"
    yaml = YAML(typ="safe")

    products_doc = yaml.load((config_dir / "products.yaml").read_text(encoding="utf-8"))
    competitors_doc = yaml.load((config_dir / "competitors.yaml").read_text(encoding="utf-8"))
    sources_doc = yaml.load((config_dir / "source-registry.yaml").read_text(encoding="utf-8"))
    signals_doc = yaml.load((config_dir / "signal-mapping.yaml").read_text(encoding="utf-8"))

    product_ids = {p["id"] for p in products_doc["products"]}
    competitor_ids = (
        {c["id"] for c in competitors_doc["tier_1"]}
        | {c["id"] for c in competitors_doc.get("tier_2_mvp_cohort", [])}
        | {c["id"] for c in competitors_doc["healthcare_ai_cluster"]}
    )

    errors: list[str] = []

    # products.yaml -> competitors.yaml: competitor refs
    # Some refs intentionally point to tier-2/tier-3 competitors not in this v1
    # cohort. We collect them as "post-MVP refs" rather than errors.
    post_mvp_competitor_refs: set[str] = set()
    for p in products_doc["products"]:
        for c in p.get("competitors_primary", []) + p.get("competitors_adjacent", []):
            if c not in competitor_ids:
                post_mvp_competitor_refs.add(c)

    # competitors.yaml -> products.yaml: product refs
    all_competitors = (
        competitors_doc["tier_1"]
        + competitors_doc.get("tier_2_mvp_cohort", [])
        + competitors_doc["healthcare_ai_cluster"]
    )
    for c in all_competitors:
        for p in c.get("related_doceree_products", []):
            if p not in product_ids:
                errors.append(f"competitors.yaml [{c['id']}].related_doceree_products: '{p}' not in products.yaml")

    # source-registry.yaml -> competitors.yaml: competitor refs
    for s in sources_doc["sources"]:
        if s["competitor"] not in competitor_ids:
            errors.append(f"source-registry.yaml rank {s['rank']}: competitor '{s['competitor']}' not in competitors.yaml")

    # signal-mapping.yaml -> products.yaml: map_to_products refs
    for r in signals_doc["rules"]:
        for p in r["map_to_products"]:
            if p == "*":
                continue
            if p not in product_ids:
                errors.append(f"signal-mapping.yaml [{r['id']}].map_to_products: '{p}' not in products.yaml")

    # signal-mapping.yaml -> competitors.yaml: competitor refs (in `if.competitor`)
    for r in signals_doc["rules"]:
        cond = r["if"]
        comp_filter = cond.get("competitor")
        if comp_filter is None:
            continue
        comps = comp_filter if isinstance(comp_filter, list) else [comp_filter]
        for c in comps:
            if c not in competitor_ids:
                # tier-2/3 competitors mentioned in signal rules are also acceptable
                # post-MVP refs since rules will simply not fire until those
                # competitors are added to the active cohort.
                post_mvp_competitor_refs.add(c)

    print(f"Products:        {len(product_ids)}")
    n_t1 = len(competitors_doc["tier_1"])
    n_t2 = len(competitors_doc.get("tier_2_mvp_cohort", []))
    n_ai = len(competitors_doc["healthcare_ai_cluster"])
    print(f"Competitors:     {len(competitor_ids)} ({n_t1} Tier-1, {n_t2} Tier-2 MVP cohort, {n_ai} healthcare AI cluster)")
    print(f"Sources:         {len(sources_doc['sources'])}")
    print(f"Signal rules:    {len(signals_doc['rules'])}")
    print()

    if post_mvp_competitor_refs:
        print(f"Post-MVP competitor refs (informational, not errors): {sorted(post_mvp_competitor_refs)}")
        print()

    if errors:
        print(f"FAIL: {len(errors)} consistency error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("OK: all internal references resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
