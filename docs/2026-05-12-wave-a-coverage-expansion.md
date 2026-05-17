# 2026-05-12 — Sprint 8f Wave A: Coverage Expansion (7 Critical Competitors)

## Status

Design approved. Implementation pending.

## Background

After reading the 17 Ask Doceree `competitor-research-*.md` files (the canonical
PMM-approved competitor positioning for each product), an audit identified ~50
competitors documented in the Ask Doceree knowledge base but absent from the
daily-digest monitoring pipeline. Adding all 50 would more than double feed
count and pipeline cost. Decomposition into 3 waves was agreed; this spec
covers Wave A only.

Wave A scope: the smallest-but-highest-leverage cut — competitors that appear
across multiple product files, with high closeness ratings, and that today
constitute structural blind spots in the digest. Sherry's explicit cut after
review:

> "Indegene NEXT is not competition. Add Veeva, Mercalis, AdTheorent, Bombora,
> AssistRx, EVERSANA NAVIGATE, Phreesia."

Indegene NEXT (initially proposed) was rejected as not a real Doceree
competitor. Daily Command (the 17th Doceree product, currently missing from
`prompts/extract.txt`) was explicitly deferred to a later wave per user
instruction.

## Goal

Add 7 critical competitors to the monitoring pipeline so news from each is
visible in the daily digest without inflating cost or false-positive rate.

After Wave A: 45 → 52 unique competitors, 58 → 68 feeds.

## Non-goals

- Adding the long-tail competitors deferred to Waves B and C (Algolia, Coveo,
  Magnite, PubMatic, Adobe Journey Optimizer, Iterable, Braze, Tealium,
  Trilliant Health, Truveta, H1, ZS Associates, Real Chemistry, RxAnte,
  ScriptDrop, etc.).
- Adding the `daily_command` product to `prompts/extract.txt`. Deferred per
  user instruction.
- Adding direct publisher RSS / SEC EDGAR feeds for public competitors
  (Veeva, AdTheorent, Phreesia have CIKs but Google News coverage is good
  enough for Wave A; IR-direct feeds are a Wave C upgrade).
- Adding new R-rules to `prompts/extract.txt`. The existing R1–R16 already
  cover the signal patterns these 7 competitors produce; refinement is
  limited to inline competitor-name examples in already-existing rules.

## Competitors added

| ID | Display name | Aliases | Category | Public co | `related_doceree_products` |
|---|---|---|---|---|---|
| `veeva` | Veeva Systems | Veeva Systems, Veeva Vault CRM, Vault CRM, Veeva Crossix, Veeva Compass | pharma commercial cloud | VEEV (CIK 0001393052) | marketplace, cis, next, daily_command, reptwin |
| `mercalis` | Mercalis (TrialCard) | Mercalis, TrialCard | patient_access_coupon | private | copay_com, pod, spark_for_pharmacy, copay_com_health_systems |
| `adtheorent` | AdTheorent Health | AdTheorent, AdTheorent Health, Cadent | healthcare_dsp | acquired by Cadent (private now) | premium_programmatic, next |
| `bombora` | Bombora | Bombora, Bombora Healthcare Intent | b2b_abm | private | abm, cis |
| `assistrx` | AssistRx | AssistRx, iAssist | patient_access_coupon | private | copay_com, copay_com_health_systems, spark_for_pharmacy |
| `eversana` | EVERSANA | EVERSANA, EVERSANA NAVIGATE | patient_access_coupon | private | copay_com, copay_com_health_systems |
| `phreesia` | Phreesia | Phreesia | dooh_poc_network | PHR (CIK 0001574540) | poc |

Note: `veeva_ai` already exists in `config/competitors.yaml` as a separate id
focused specifically on the Veeva AI Agents launch arc. The new `veeva` id
covers the parent company, Vault CRM journey moves, Crossix product launches,
and Compass RWD updates. Both ids coexist; T4a attribution routes each item
to whichever competitor the title/summary actually references.

## Feed strategy

10 new `CompetitorFeed` entries (some competitors get product-name secondary
queries; T4a.5 dedup collapses syndication overlap):

| Competitor id | Query | Rationale |
|---|---|---|
| `veeva` | `"Veeva Systems"` | Parent company news, M&A, earnings, leadership |
| `veeva` | `"Veeva Crossix"` | Crossix product launches and partnerships |
| `veeva` | `"Veeva Vault CRM"` | Vault CRM journey updates (NEXT competitor) |
| `mercalis` | `"Mercalis pharma"` | Disambiguates from unrelated brands |
| `mercalis` | `"TrialCard"` | Pre-rebrand legacy name still appears in news |
| `adtheorent` | `"AdTheorent"` | Healthcare DSP brand |
| `bombora` | `"Bombora intent"` | "intent" disambiguates from generic noise (Bombora alone matches weather/storm news) |
| `assistrx` | `"AssistRx"` | Single-word brand, distinctive |
| `eversana` | `"EVERSANA NAVIGATE"` | Exact-phrase product name avoids matching unrelated EVERSANA mentions |
| `phreesia` | `"Phreesia"` | Single-word brand, distinctive |

All queries follow the existing `_gnews_feed()` pattern: exact-phrase + `when:7d`.
All ingestion goes through `fetch_rss(max_age_hours=36)` so the 7-day window
is filtered down to fresh items in the pipeline.

## Product-mapping refinement

`prompts/extract.txt` rule changes are minimal — the existing 16 R-rules
already match these competitors' signal patterns. Inline examples are added
to tighten LLM precision:

- **R4 (patient access / ePA / RTBC)** — add "known competitors include
  Mercalis, AssistRx, EVERSANA, CareMetx" as inline examples in the signals
  list.
- **R6 (healthcare ad server / publisher monetization)** — no change (no Wave A
  competitor maps here).
- **R10 (custom HCP audience construction)** — add "Veeva Crossix" as an
  example signal source.
- **R11 (healthcare ABM)** — add "Bombora healthcare-intent integration" as
  an example signal.
- **R14 (generic DSP adding HCP capabilities)** — add AdTheorent as an
  example healthcare-DSP entrant.
- **R3 (omnichannel orchestration / clinical intent)** — add "Veeva Vault CRM
  journey orchestration" as a competitor example.

No new R-rules. No hardcoded competitor → product mapping table. The signal-
pattern approach is preserved.

## Cost projection

Per-run cost increases by 10 Google News fetches + 10 T2 filter calls
(Gemini 2.5 Flash-Lite). Pro-stage costs are unaffected because dedup +
filter + attribution drop most items before they reach extract or synth.

| Stage | Added calls/day | Added cost/day |
|---|---|---|
| RSS fetch | +10 (~free) | $0 |
| T2 filter (Flash-Lite) | +10–30 items | ~$0.005 |
| T4a attribution (Flash) | +0–5 items | ~$0.002 |
| T3 extract (Flash) | +0–3 findings | ~$0.005 |
| T4b adversarial (Pro) | +0–3 findings | ~$0.020 |
| T5 synth (Pro) | minimal | ~$0.005 |

**Total added: ~$0.03–0.05/day → $0.90–1.50/month.** Within original
$0.30–0.50/month estimate (conservative).

## Implementation plan

1. **`config/competitors.yaml`** — append 7 new entries in `tier_2_mvp_cohort`
   with `monitoring_tier: direct`, full alias lists, `related_doceree_products`,
   `sec_cik` where applicable, and category fields aligned to
   `src/schema/competitor.py::CompetitorCategory`.

2. **`src/runners/run_daily.py`** — append 10 `CompetitorFeed` entries to
   `DAY6_FEEDS`. Multi-feed competitors share the same `competitor=` id.

3. **`prompts/extract.txt`** — minimal inline-example tweaks to R3, R4, R10,
   R11, R14 as listed above. No new rules.

4. **No new tests.** `tests/unit/test_competitor_coverage.py` will continue
   to pass because every new id is added to both YAML and feeds.

5. **Validation:** run `python -m pytest tests/ --ignore=tests/unit/test_gemini.py`
   — expect 309 passed (no test count change, just larger feed list).

6. **Smoke test:** count feeds + unique competitors + cross-check YAML↔feeds:
   ```
   from runners.run_daily import DAY6_FEEDS
   assert len({f.competitor for f in DAY6_FEEDS}) == 52
   assert len(DAY6_FEEDS) == 68
   ```

7. **Commit:** single commit, clear message describing the 7 additions and
   the rationale (rejecting Indegene NEXT per user direction, deferring
   Daily Command).

## Risk and mitigations

- **"Veeva" query noise.** Veeva is a large public company; news range is wide.
  Mitigation: three specific queries (Veeva Systems, Veeva Crossix, Veeva Vault
  CRM) instead of bare "Veeva". T4a attribution will reject unrelated mentions.
- **"Bombora" alone matches weather/storm news.** Mitigation: query is
  `"Bombora intent"` exact-phrase, not bare `"Bombora"`.
- **"EVERSANA" alone matches unrelated brands.** Mitigation: query is
  `"EVERSANA NAVIGATE"` exact-phrase.
- **Mercalis ↔ TrialCard rebrand.** Mitigation: both queries are issued so
  pre-rebrand and post-rebrand news both surface; dedup collapses overlap.
- **`veeva` vs `veeva_ai` id confusion.** Mitigation: keep both ids; T4a
  attribution routes per-article. The `name` field in CompetitorFeed
  differentiates in logs (e.g. "Veeva Systems" vs "Veeva AI").
- **Cost overrun.** Mitigation: low ceiling (~$1.50/month worst case). Monitor
  with Gemini API console after first 7 days.

## Out-of-band follow-ups (Wave B and C, not in this spec)

- Add `daily_command` to `prompts/extract.txt` products list and product-
  mapping rules.
- Wave B: data + RWD vendors (Trilliant, Truveta, H1, Crossix-as-standalone),
  CDP/orchestration (Adobe Journey Optimizer, Iterable, Braze, Twilio Engage,
  Tealium), pharma services (ZS, Real Chemistry).
- Wave C: long-tail SSPs (Magnite, PubMatic, OpenX), Publisher AI generics
  (Algolia, Coveo, Glean), DOOH (Place Exchange, Broadsign, Hivestack),
  health-system patient access (TransUnion Healthcare, Experian Health,
  Waystar, Cedar), adherence (RxAnte, ScriptDrop), pharmacy services
  (Inmar, RxSense), consumer savings (SingleCare, RxSaver, WellRx).
- IR / press-release direct RSS for public competitors (Veeva, OptimizeRx,
  IQVIA, Doximity, GoodRx, Trade Desk, Salesforce, Phreesia, etc.).
- SEC 8-K EDGAR feeds for every public competitor with `sec_cik` set.
- Synth Sev gate (skip per-product synth for Sev < 3 findings) — separate
  Sprint 8f P1 item.
