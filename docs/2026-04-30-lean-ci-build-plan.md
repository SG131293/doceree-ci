# Doceree CI Daily Digest — Lean Implementation Plan

> **For Claude Code:** This is the source-of-truth implementation plan. Execute task-by-task. After each task, run the verification step before moving on. Commit at every task boundary with the specified commit message.

**Goal:** Ship a Python pipeline running on GitHub Actions that produces a beautifully-rendered HTML email at 6:00 AM IST daily, organized by Doceree's 13 products, covering competitor moves across 14+ source types, with cross-validated findings (Gemini Flash + Pro adversarial + GPT-5-nano second opinion), 30-day pattern detection, weekly new-entrant discovery, and Friday battlecard auto-drafts. Operational cost: ~₹0-400/month.

**Architecture:** 8-tier pipeline (ingest → filter → extract → verify → synthesize per product → synthesize strategic → render → deliver). Gemini 2.5 Flash-Lite/Flash/Pro for intelligence, GPT-5-nano for cross-validation on Sev 4-5, GitHub Actions for orchestration, Gmail API for delivery, Telegram for Sev-5 alerts, GitHub Pages for searchable archive.

**Tech Stack:** Python 3.12, google-genai, openai, httpx, feedparser, selectolax, pydantic 2, jinja2, premailer, pyyaml (ruamel), tenacity, tinydb, google-api-python-client, python-telegram-bot, pytest + pytest-recording.

**Build Duration:** 4 weeks (28 days), assuming 2-4 hours/day of focused build with Claude Code as the assistant.

---

## Pivot decision (read first)

The existing repo at this path is a **Next.js + Prisma + Postgres scaffold from Codex Milestones 0-12**. It does not fit the new constraints (₹0/month, no DB, no dashboard, GitHub Actions only). The clean path forward:

1. **Archive the existing scaffold.** Move `src/`, `prisma/`, `next.config.ts`, `tsconfig.json`, `package.json`, `node_modules/`, `.next/`, `playwright.config.ts` into a `legacy/` subfolder with a README explaining the pivot.
2. **Reuse what's valuable.** Keep `docs/` (PRD reference, scope-lock rules, signal-mapping research) and `source/docs/DOCEREE_MASTER_PRD.md.md` (master PRD). These are the IP. Everything else is plumbing for the wrong architecture.
3. **Build the Python repo at the project root.** New `pyproject.toml`, `requirements.txt`, `src/`, `config/`, `evals/`, `tests/`. The PRD docs in `docs/` and `source/docs/` remain alongside as reference material.

If this pivot is uncomfortable, an alternative is to clone this repo's `docs/` and PRD files into a brand-new repo and start completely fresh. Either works. The point: do not graft Python onto the Next.js codebase.

---

## Stack decisions and rationale

| Decision | Choice | Why |
|---|---|---|
| Language | Python 3.12 | Mature LLM ecosystem, Gemini SDK is reference-quality, eval tooling (pytest, deepeval) is Python-heavy, GitHub Actions native support |
| Gemini SDK | `google-genai>=0.8` | Official, async, supports `thinking_budget`, response schemas, implicit + explicit cache |
| OpenAI SDK | `openai>=1.50` | Official, Responses API with structured outputs |
| HTTP | `httpx[http2]` | Async, retries, HTTP/2; lighter than aiohttp |
| RSS parsing | `feedparser` | Tolerates malformed feeds; pure Python |
| HTML parsing | `selectolax` | 5-10x faster than BeautifulSoup for sitemap/meta extraction |
| Schemas | `pydantic>=2.7` | Validates LLM JSON output; canonical Finding contract |
| Templates | `jinja2` | Standard for HTML email |
| CSS inlining | `premailer` | Mandatory for Gmail rendering |
| Config | `ruamel.yaml` | Preserves comments — humans edit YAML configs |
| Retry | `tenacity` | Cleaner than rolling our own; jittered backoff |
| Local archive | JSONL + `tinydb` | No DB needed; querying via simple file reads |
| Gmail | `google-api-python-client` + OAuth refresh-token | One-time auth, GH-secret-stored, no interactive flow in CI |
| Telegram | `python-telegram-bot>=21` | Async, simple `send_message` |
| Tests | `pytest` + `pytest-recording` | VCR cassettes pin LLM responses for regression tests |
| Hosting | GitHub Actions free tier | 2,000 min/month for private; unlimited for public. Recommend public repo (with secrets, no proprietary data in code) |
| Archive hosting | GitHub Pages (free) | Searchable HTML archive for permanent reference |

**Excluded explicitly:**
- No `playwright`/`selenium` — no rendered scraping per source policy
- No `pandas` — overkill for this volume
- No `langchain`/`crewai` — unnecessary abstraction, we control 8 stages directly
- No vendor data feeds (Apify, Crayon, Bright Data) — eliminated by spec

---

## Directory structure

```
doceree-ci/                                  # repo root (pivot from existing)
├── .github/
│   └── workflows/
│       ├── daily-digest.yml                 # 00:30 UTC = 06:00 IST, daily
│       ├── hourly-sev5.yml                  # every hour, lightweight scan
│       ├── weekly-discovery.yml             # Sun 22:00 UTC, new entrants
│       ├── friday-battlecard.yml            # Fri 02:30 UTC = 08:00 IST
│       └── eval-on-pr.yml                   # PRs touching prompts/pipeline
├── src/
│   ├── __init__.py
│   ├── pipeline/
│   │   ├── ingest.py                        # T1: RSS, sitemap, public APIs
│   │   ├── filter.py                        # T2: Flash-Lite noise discard
│   │   ├── extract.py                       # T3: Flash structured findings
│   │   ├── verify.py                        # T4: URL liveness + adversarial Pro + nano
│   │   ├── synth_per_product.py             # T5: Pro per-product synthesis
│   │   ├── synth_strategic.py               # T6: cross-product top-3
│   │   ├── render.py                        # T7: HTML + JSONL + Pages publish
│   │   └── deliver.py                       # T8: Gmail + Telegram
│   ├── clients/
│   │   ├── gemini.py                        # caching, retry, rate limit
│   │   ├── openai.py                        # nano cross-check
│   │   ├── gmail.py                         # OAuth + send_message
│   │   ├── telegram.py                      # bot send + chunk long alerts
│   │   └── http.py                          # shared httpx client + circuit breaker
│   ├── sources/
│   │   ├── rss.py                           # generic RSS
│   │   ├── sitemap.py                       # sitemap.xml diff
│   │   ├── sec_edgar.py                     # SEC EDGAR free API
│   │   ├── github_repos.py                  # GitHub API (free)
│   │   ├── jobs_greenhouse.py               # Greenhouse public JSON
│   │   ├── jobs_lever.py                    # Lever public JSON
│   │   ├── jobs_ashby.py                    # Ashby public JSON
│   │   ├── reddit.py                        # Reddit API (free)
│   │   ├── youtube.py                       # YouTube Data API (free tier)
│   │   ├── uspto_patents.py                 # USPTO PatentsView API (free)
│   │   └── conferences.py                   # static conference calendar + RSS
│   ├── schema/
│   │   ├── finding.py                       # canonical Finding pydantic model
│   │   ├── product.py
│   │   ├── competitor.py
│   │   ├── severity.py                      # 1-5 enum + decision rules
│   │   └── source.py
│   ├── mapping/
│   │   ├── product_mapper.py                # rule + LLM hybrid: finding → product[]
│   │   └── signal_rules.py                  # loads signal-mapping.yaml
│   ├── archive/
│   │   ├── jsonl_store.py                   # append-only daily JSONL + read API
│   │   ├── pattern_detect.py                # 30-day rolling cluster detection
│   │   └── dedupe.py                        # URL + content-hash dedup
│   ├── render/
│   │   ├── templates/
│   │   │   ├── email_base.html.j2
│   │   │   ├── email_digest.html.j2
│   │   │   ├── partials/
│   │   │   │   ├── _header.html.j2
│   │   │   │   ├── _strategic_top3.html.j2
│   │   │   │   ├── _product_section.html.j2
│   │   │   │   ├── _finding_card.html.j2
│   │   │   │   ├── _severity_badge.html.j2
│   │   │   │   ├── _confidence_chip.html.j2
│   │   │   │   ├── _empty_state.html.j2
│   │   │   │   └── _footer.html.j2
│   │   │   ├── battlecard.html.j2
│   │   │   ├── weekly_discovery.html.j2
│   │   │   └── pages_index.html.j2
│   │   ├── inline_css.py                    # premailer wrapper
│   │   └── styles.css                       # source CSS, inlined at build
│   ├── prompts/                             # versioned prompt files (text)
│   │   ├── filter.txt
│   │   ├── extract.txt
│   │   ├── adversarial_check.txt
│   │   ├── crossvalidate_nano.txt
│   │   ├── synth_per_product.txt
│   │   ├── synth_strategic.txt
│   │   ├── pattern_detect.txt
│   │   ├── battlecard_draft.txt
│   │   └── new_entrant_discovery.txt
│   ├── runners/
│   │   ├── run_daily.py                     # entry: T1->T8
│   │   ├── run_hourly_sev5.py               # entry: T1->T4 fast path
│   │   ├── run_weekly_discovery.py          # entry: discovery
│   │   ├── run_friday_battlecard.py         # entry: battlecard
│   │   └── notify_failure.py                # called on workflow failure
│   └── util/
│       ├── logging.py                       # structured JSON logs
│       ├── url_health.py                    # HEAD then GET fallback
│       ├── time_ist.py                      # IST conversions
│       └── secrets.py                       # reads from env, fails loudly
├── config/
│   ├── products.yaml                        # 13 Doceree products
│   ├── competitors.yaml                     # tier-1 + RepTwin AI cluster
│   ├── signal-mapping.yaml                  # 30+ signal mapping rules
│   ├── source-registry.yaml                 # 50+ approved sources
│   ├── severity-rules.yaml                  # 1-5 deterministic floors
│   ├── prompts.yaml                         # prompt -> model + budget
│   └── delivery.yaml                        # recipients, telegram, send window
├── evals/
│   ├── golden/
│   │   ├── filter/                          # 30 hand-labeled examples
│   │   ├── extract/                         # 30 examples per source type
│   │   ├── product_mapping/                 # 50 examples
│   │   ├── severity/                        # 30 examples
│   │   └── verify/                          # 20 examples
│   ├── run_evals.py
│   ├── metrics.py
│   ├── baselines.json                       # per-stage F1 baseline
│   └── cassettes/                           # VCR pinned LLM responses
├── archive/                                 # gitignored except .gitkeep
│   └── 2026/04/30/findings.jsonl
├── docs-pages/                              # generated, pushed to gh-pages
│   ├── index.html
│   └── archives/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── scripts/
│   ├── seed_archive.py
│   ├── ops_health.py
│   ├── verify_secrets.py
│   ├── generate_gmail_token.py              # one-shot OAuth flow (run locally)
│   └── label_finding.py                     # CLI to add to golden set
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## The 4-week build sequence

Each week ends with a working, demoable system. Each day's tasks are 2-4 hours of focused build time.

### Week 1: Foundation + first end-to-end shippable digest

**Day 1: Pivot, scaffolding, secrets**
- Archive existing scaffold to `legacy/`
- Initialize `pyproject.toml`, `requirements.txt`, `.gitignore`
- Set up GitHub repo (private or public; recommend public for unlimited Actions)
- Add secrets: `GEMINI_API_KEY`, `OPENAI_API_KEY` (placeholder), `GMAIL_*`, `TELEGRAM_*`
- Run `verify_secrets.py` from CLI; confirms all secrets readable
- Commit: `chore: initialize lean ci-digest scaffold`

**Day 2: Configs (the IP layer)**
- Write `config/products.yaml` for all 13 Doceree products with: id, name, one_line, journey_stages, confirmed_claims, inferred_claims, keywords, negative_keywords, competitors_primary, competitors_adjacent
- Write `config/competitors.yaml`: 10 tier-1 + 9 healthcare-AI-agents cluster (Synthio, Hippocratic, Glass, Suki, Abridge, Nabla, Ambience, DeepScribe, Curai). Each has: id, name, canonical_domain, rss_feeds, sitemaps, sec_cik (if public), public_jobs_boards, related_doceree_products, rep_priority
- Write `config/source-registry.yaml`: ~50 sources covering primary RSS, blogs, newsrooms, public APIs
- Write `config/signal-mapping.yaml`: starter set of 15-20 rules (will grow to 30 by week 3)
- Commit: `config: add Doceree products, competitors, sources, signal rules`

**Day 3: Pydantic schemas — the contract**
- Implement `src/schema/finding.py`: `Finding` model with url, source, competitor, summary, evidence_quote, signal_type, raw_severity, raw_confidence, products[], crossvalidation_disagreement, captured_at
- Implement `src/schema/product.py`, `src/schema/competitor.py`, `src/schema/source.py`, `src/schema/severity.py` (enum 1-5)
- Write unit tests in `tests/unit/test_schemas.py`: validate sample findings, reject invalid ones
- Run: `pytest tests/unit/test_schemas.py -v`
- Expected: all pass
- Commit: `feat: pydantic schemas for canonical Finding contract`

**Day 4: Gemini client wrapper**
- Implement `src/clients/gemini.py` with:
  - `GeminiClient` class wrapping `google-genai`
  - Methods: `filter()`, `extract()`, `adversarial_check()`, `synthesize()` etc.
  - In-memory token bucket (5 RPM Pro, 10 RPM Flash, 15 RPM Flash-Lite, all share 250K TPM)
  - `tenacity` retry: 3 attempts, exponential backoff 1s-4s-16s, jittered
  - Retry on 429/5xx, never on 400/403
  - Implicit cache via prompt structure (static prefix on top)
  - Explicit `cached_content` for synthesis stages (Pro only, 2hr TTL)
  - Structured outputs via `response_mime_type="application/json"` + pydantic schema
  - `thinking_budget` per call type (filter=0, extract=512, adversarial=4096, synth=8192)
- Unit tests with `pytest-recording` cassettes
- Commit: `feat: Gemini client wrapper with caching, retry, rate limiting`

**Day 5: HTTP utilities + URL health checker**
- Implement `src/clients/http.py`: shared `httpx.AsyncClient`, HTTP/2, 10s connect / 30s read, pool=20, per-host circuit breaker (5 failures in 60s = open for 5 min)
- Implement `src/util/url_health.py`: HEAD then GET fallback, must return 200, follows redirects, validates final URL shares registered domain with cited URL
- Unit tests for both
- Commit: `feat: HTTP client and URL health checker`

**Day 6: First end-to-end RSS-only run (3 competitors)**
- Implement `src/sources/rss.py`: fetch via httpx, parse via feedparser, return list of items (title, link, summary, published, source_competitor)
- Implement `src/pipeline/ingest.py`: orchestrates source-specific ingesters per source-registry.yaml
- Implement minimal `src/pipeline/filter.py` with `filter.txt` prompt: takes raw items, returns kept[]
- Implement minimal `src/pipeline/extract.py` with `extract.txt` prompt: takes kept items, returns Finding[]
- Implement `src/render/render.py` minimal: jinja2 renders findings to text-only email body
- Implement `src/clients/gmail.py`: OAuth refresh-token flow, `send_message(html, plaintext, subject, to)`
- Implement `src/runners/run_daily.py`: orchestrates ingest → filter → extract → render → deliver for 3 competitors only (DeepIntent, OptimizeRx, Synthio Labs)
- Run locally: `python -m src.runners.run_daily`
- Verify email lands in Sherry's inbox
- Commit: `feat: minimum-viable end-to-end pipeline for 3 competitors, text-only`

**Day 7: GitHub Actions deployment**
- Write `.github/workflows/daily-digest.yml` with cron `30 0 * * *` (06:00 IST)
- Configure `concurrency` group, `cancel-in-progress: false`
- Set `timeout-minutes: 50`
- Set `permissions: contents: write` for gh-pages later
- Add `if: failure()` step calling `notify_failure.py` (skeleton)
- Add `if: always()` step uploading run artifacts (logs, JSONL, HTML) for 30-day retention
- Trigger via `workflow_dispatch` for manual testing
- Verify: trigger manually, confirm email lands, confirm artifacts uploaded
- Commit: `feat: GitHub Actions daily workflow + manual trigger`

**Week 1 exit criterion:** Sherry receives a real text-only email at 6 AM IST for 7 consecutive days from RSS sources for 3 competitors. URL drops from extraction (hallucinations) <50%. No false 9 AM panic emails.

---

### Week 2: Verification, cross-validation, HTML, eval harness

**Day 8: Adversarial Pro self-check**
- Write `prompts/adversarial_check.txt`: prompt asks Pro to challenge each finding — does evidence support severity? Is URL canonical source? Could this be marketing fluff?
- Implement `src/pipeline/verify.py` stage 4b: runs adversarial check on every finding, returns annotated finding (kept, demoted, or rejected with reason)
- Unit tests with VCR cassettes
- Commit: `feat: adversarial Pro self-check on every finding`

**Day 9: GPT-5-nano cross-validation**
- Implement `src/clients/openai.py`: `cross_validate(finding) -> Verdict` with structured output `{agree: bool, confidence: 1-5, dissent_reason: str | null}`
- `tenacity` retry; budget cap 100 calls/day = $0.20/day max
- Implement `src/pipeline/verify.py` stage 4c: only Sev 4-5 findings go through nano
- Disagreement handling: if nano disagrees with confidence ≥4, demote severity by 1 (minimum 3) and tag `crossvalidation_disagreement=true`. Render flag in card later.
- Commit: `feat: GPT-5-nano cross-validation on Sev 4-5 findings`

**Day 10: URL liveness + signal-mapping rules + severity rules**
- Implement `src/pipeline/verify.py` stage 4a: every finding's URL pinged via `url_health.check()`. Drop finding if not 200. Log dropped URLs to `archive/hallucinated_urls.jsonl`.
- Implement `src/mapping/signal_rules.py`: load signal-mapping.yaml, apply rules, return mapped products[]
- Implement `src/mapping/product_mapper.py`: hybrid — apply rules first, then LLM call for unmatched findings
- Implement deterministic severity floor logic from `severity-rules.yaml`
- Commit: `feat: URL verification, signal mapping, severity rules`

**Day 11: HTML email template (the polish)**
- Write `src/render/templates/email_base.html.j2` with dark-mode `@media` query in `<head>` (un-inlined)
- Write `src/render/styles.css` with light-mode default styles
- Write all partials: `_header`, `_strategic_top3`, `_product_section`, `_finding_card`, `_severity_badge`, `_confidence_chip`, `_empty_state`, `_footer`
- Implement `src/render/inline_css.py`: premailer wrapper, inlines styles.css into final HTML
- Use Doceree-brand colors (verify with Sherry: primary teal, accent orange, background neutrals)
- Mobile-perfect: 600px max-width, single column, system fonts only, 16px body min, 24px headings, 44px touch targets
- Generate plaintext alternative via `email_digest.txt.j2`
- Test render: feed sample findings, save HTML, open in browser, verify mobile rendering at 375px width
- Test in actual Gmail clients: send test email to yourself, view in Gmail Web, Gmail iOS, Gmail Android
- Commit: `feat: HTML email template with dark-mode and mobile-perfect rendering`

**Day 12: Empty states + verification badges + integration**
- Implement empty-state rendering: products with zero findings get "No material updates today" line
- Implement disagreement badges: cross-validation flag renders amber strip on cards
- Wire all of Week 2's pieces together in `run_daily.py`
- Run locally end-to-end with all 10 tier-1 competitors + RSS only
- Verify HTML email looks good, verify all URLs in email are clickable and live
- Commit: `feat: empty states, disagreement badges, integrated daily run`

**Day 13: Eval harness foundation**
- Implement `evals/run_evals.py`: loads golden examples, runs through the relevant stage, computes metrics
- Implement `evals/metrics.py`: precision, recall, F1, regression detection
- Write 10 hand-labeled examples for `evals/golden/filter/` (5 keep, 5 discard)
- Write 10 examples for `evals/golden/extract/`
- Run: `python -m evals.run_evals --suite all`
- Commit baselines to `evals/baselines.json`
- Commit: `feat: eval harness with initial golden examples`

**Day 14: PR-gated eval workflow**
- Write `.github/workflows/eval-on-pr.yml`: triggers on PRs touching `src/prompts/**`, `src/pipeline/**`, `config/signal-mapping.yaml`. Runs eval suite. Fails if any stage drops >3 F1 points vs baseline. Maintainer can update baseline with commit message starting `[baseline]`.
- Test by submitting a deliberate-regression PR; confirm it fails
- Commit: `ci: PR-gated eval regression detection`

**Week 2 exit criterion:** Eval F1 ≥ 0.85 on extract stage; HTML email mobile-perfect on Gmail iOS/Android/Web; cross-validation flagging working; URL drops <15%.

---

### Week 3: Full coverage, synthesis, memory, discovery

**Day 15: All 13 products + signal mapping expansion**
- Expand `config/signal-mapping.yaml` to 30+ rules covering: jobs (capability investment), partnerships (Epic/Cerner/Veeva), pricing changes, comparison pages (any "vs Doceree" → Sev 5), regulatory filings, M&A, leadership changes, customer wins, ePA/RTBC mentions, EHR integrations, MeSH taxonomy mentions
- Add severity floors per signal type
- Write 30 examples in `evals/golden/product_mapping/`
- Run eval suite; aim multi-label F1 ≥ 0.80
- Commit: `feat: complete signal-mapping rules for all 13 products`

**Day 16: Public API sources (jobs, SEC, GitHub, USPTO, Reddit, YouTube)**
- Implement `src/sources/jobs_greenhouse.py`, `_lever.py`, `_ashby.py`: hit public board JSON APIs (free)
- Implement `src/sources/sec_edgar.py`: SEC EDGAR full-text search API (free)
- Implement `src/sources/github_repos.py`: GitHub API for healthcare-AI cluster repo activity
- Implement `src/sources/uspto_patents.py`: USPTO PatentsView API (free)
- Implement `src/sources/reddit.py`: Reddit JSON API for r/healthcareIT, r/medicine, r/pharma
- Implement `src/sources/youtube.py`: YouTube Data API for executive video appearances
- Update `config/source-registry.yaml` to include these sources
- Commit: `feat: public API sources for jobs, SEC, GitHub, USPTO, Reddit, YouTube`

**Day 17: Sitemap diff for website-change detection**
- Implement `src/sources/sitemap.py`: fetch sitemap.xml, diff against previous day's sitemap (stored in `archive/sitemaps/{competitor}.xml`)
- New URLs are change candidates; fetch each via httpx, extract title + meta description + first 2 paragraphs via selectolax
- Pipe through filter and extract
- Commit: `feat: sitemap-diff change detection for competitor websites`

**Day 18: Per-product synthesis (Pro)**
- Write `prompts/synth_per_product.txt`: takes day's findings + product spine context (cached) + last 30-day patterns → returns top insight per product
- Implement `src/pipeline/synth_per_product.py`: 1 batched Pro call covering all 13 products (90 RPD budget is tight; single-call variant first; A/B for 13 separate calls if quality drops)
- Use explicit `cached_content` for product spine + signal mapping rules (90% discount)
- Commit: `feat: per-product synthesis with explicit caching`

**Day 19: Strategic top-3 cross-product synthesis**
- Write `prompts/synth_strategic.txt`: reads all per-product insights → returns 3-sentence strategic summary at email top
- Implement `src/pipeline/synth_strategic.py`: 1 Pro call/day
- Render `_strategic_top3.html.j2` partial at top of email
- Commit: `feat: strategic top-3 cross-product synthesis`

**Day 20: 30-day pattern detection**
- Implement `src/archive/jsonl_store.py`: append-only daily JSONL writes, indexed reads
- Implement `src/archive/pattern_detect.py`: read last 30 days, identify clusters (e.g., "DeepIntent has 3 EHR-integration jobs in 14 days")
- Use Gemini Pro 1M context to read the full archive in one call
- Pattern flags appear in finding cards as colored chips
- Implement `src/archive/dedupe.py`: URL + content-hash dedup against last 30 days
- Commit: `feat: 30-day pattern detection and dedup`

**Day 21: Weekly new-entrant discovery**
- Write `prompts/new_entrant_discovery.txt`: per Doceree product category, search "new [category] startups 2026", "AI agents for healthcare marketing", etc. Profile each: name, founders, funding, traction, threat assessment
- Implement `src/runners/run_weekly_discovery.py`: 13 Pro grounded calls (one per product category) on Sunday evening
- Persist candidates to `archive/discovery/{YYYY-MM-DD}.jsonl`
- Render in Monday's digest as new "New entrants this week" section
- Write `.github/workflows/weekly-discovery.yml`: Sunday 22:00 UTC cron
- Commit: `feat: weekly new-entrant discovery agent`

**Week 3 exit criterion:** Full daily run covers 13 products + 19 competitors with 14 source types; strategic top-3 reads coherently; 30-day patterns surfacing; Monday digest includes new entrants section.

---

### Week 4: Real-time alerts, battlecards, polish, launch

**Day 22: Hourly Sev-5 fast-path**
- Implement `src/runners/run_hourly_sev5.py`: T1→T4 abbreviated, only RSS + SEC (highest-signal sources)
- Telegram alert ONLY if Sev-5 finding is fresh (not seen in last 24h archive)
- Write `.github/workflows/hourly-sev5.yml`: cron `0 * * * *`
- Implement `src/clients/telegram.py`: bot send, MarkdownV2 formatting, chunk long messages, includes link to gh-pages archive entry
- Verify: trigger manually, plant a fake Sev-5 in test, confirm Telegram alert fires
- Commit: `feat: hourly Sev-5 fast-path with Telegram alerts`

**Day 23: GitHub Pages archive**
- Implement `src/render/render.py` extension: writes daily digest HTML to `docs-pages/archives/{YYYY}/{MM}/{DD}.html` and updates `docs-pages/index.html` with searchable table of contents
- Add `peaceiris/actions-gh-pages@v4` step to daily workflow with `keep_files: true`
- Configure Pages source: `gh-pages` branch, `/` root
- Verify: published archive accessible at `https://[username].github.io/doceree-ci/`
- Commit: `feat: GitHub Pages searchable archive`

**Day 24: Friday battlecard auto-draft**
- Write `prompts/battlecard_draft.txt`: reads last 7 days of findings, groups by competitor, drafts updated battlecard sections (positioning, features, weaknesses, win-against)
- Implement `src/runners/run_friday_battlecard.py`: 1 Pro call per relevant competitor (those with findings this week)
- Output: opens GitHub Issue (NOT email — battlecards need human edits before circulation) with draft as body
- Write `.github/workflows/friday-battlecard.yml`: Friday 02:30 UTC cron
- Commit: `feat: Friday battlecard auto-draft as GitHub Issues`

**Day 25: Manual LinkedIn forward workflow**
- Implement Gmail watch: Apps Script or Python checking Gmail every hour for emails forwarded with subject prefix `LI:`
- Process forwarded LinkedIn post text + URL through filter → extract → verify pipeline as if it were any other source
- Append to next day's brief
- Document the workflow in `README.md` so Sherry knows to forward LinkedIn posts to her own address with `LI:` prefix
- Commit: `feat: manual LinkedIn forward-to-self ingestion workflow`

**Day 26: Eval harness expansion (full coverage)**
- Expand `evals/golden/` to 30+ examples per stage: filter, extract (per source type), product_mapping (50), severity (30), verify (20)
- Run full eval suite: `python -m evals.run_evals --suite all`
- Aim: filter F1 ≥ 0.92, extract F1 ≥ 0.85, mapping F1 ≥ 0.80, severity ±1 accuracy ≥ 0.90, verify F1 ≥ 0.95
- Commit baselines: `[baseline] eval golden set v1.0 — 130 examples, F1 above thresholds`
- Commit: `feat: full eval harness coverage`

**Day 27: Self-improving prompt loop + ops health**
- Implement weekly: read eval results, propose prompt updates via Gemini Pro, save proposals to `proposals/` folder
- Sherry reviews proposals, accepts via PR (eval gate ensures no regression)
- Implement `scripts/ops_health.py`: checks API key validity, RPD usage today, last successful run timestamp, gh-pages publish status. Run daily as first step of workflow.
- Commit: `feat: self-improving prompt loop and ops health dashboard`

**Day 28: Launch acceptance**
- Write `runbook.md`: what to do when Telegram fires a failure alert, how to debug a daily-digest miss, how to update prompts safely, how to add a new competitor or source
- Write `README.md`: project overview, how to set up locally, how to add to golden set, how to update baselines
- Run final acceptance: 5 consecutive days of green workflows, eval suite passing, manual smoke test of all four workflows
- Document known limitations and future enhancements
- Commit: `chore: launch documentation and runbook`
- **Production launch.**

**Week 4 exit criterion:** All four workflows green for 5 consecutive days. Eval harness gating PRs. Battlecard issues land Friday. Sherry has run the system for one full week post-launch with no manual intervention required.

---

## Configuration schema details

### `config/products.yaml`

```yaml
version: 1
products:
  - id: marketplace
    name: Marketplace
    one_line: "Programmatic HCP marketplace for pharma demand-side"
    journey_stages: [awareness, consideration, decision]
    confirmed_claims:
      - "Reaches 2M+ HCPs across NPI-verified networks"
    inferred_claims: []
    needs_confirmation_claims: []
    keywords: [marketplace, programmatic, dsp, ssp, hcp inventory, NPI]
    negative_keywords: [retail marketplace, amazon, etsy]
    competitors_primary: [optimizerx, deepintent, pulsepoint]
    competitors_adjacent: [veradigm, doximity]
  - id: reptwin
    name: RepTwin
    one_line: "AI virtual brand rep for pharma sales"
    journey_stages: [awareness, consideration]
    confirmed_claims: []
    keywords: [ai rep, virtual rep, brand rep, sales ai, pharma ai agent]
    competitors_primary: [synthio, hippocratic, glass_health, suki, abridge]
    competitors_adjacent: [nabla, ambience, deepscribe, curai]
  # 11 more products
```

### `config/competitors.yaml`

```yaml
version: 1
tier_1:
  - id: optimizerx
    name: OptimizeRx
    canonical_domain: optimizerx.com
    rss_feeds: [https://www.optimizerx.com/feed/]
    sitemaps: [https://www.optimizerx.com/sitemap.xml]
    sec_cik: '0001448431'
    public_jobs_boards: [{provider: greenhouse, slug: optimizerx}]
    related_doceree_products: [marketplace, abm, premium_programmatic, poc]
    rep_priority: 5
  # 9 more
healthcare_ai_cluster:
  - id: synthio
    name: Synthio Labs
    canonical_domain: synthiolabs.com
    related_doceree_products: [reptwin]
    funding_status: "5M seed Nov 2025, YC + Elevation + Peak XV"
    threat_level: high
  # 8 more
```

### `config/signal-mapping.yaml`

```yaml
version: 1
rules:
  - id: rule_001
    if: { source_type: jobs, title_contains: ['ai scribe', 'ambient documentation', 'clinical ai'] }
    map_to_products: [reptwin]
    severity_floor: 3
  - id: rule_002
    if: { source_type: news, body_contains: ['point-of-care', 'POC', 'in-EHR'] }
    map_to_products: [poc]
    severity_floor: 3
  - id: rule_005
    if: { competitor: covermymeds, source_type: news, body_contains: [copay, coupon, ePA] }
    map_to_products: [copay_com]
    severity_floor: 4
  - id: rule_010
    if: { source_type: sec, form_type: ['8-K', 'S-1'] }
    map_to_products: ['*']
    severity_floor: 4
  - id: rule_015
    if: { content_contains: ['vs Doceree', 'Doceree alternative', 'compare to Doceree'] }
    map_to_products: ['*']
    severity_floor: 5
  # 25+ more rules
```

### `config/severity-rules.yaml`

```yaml
version: 1
deterministic_floors:
  - if: { source_type: sec }
    floor: 4
  - if: { signal_type: pricing_change }
    floor: 4
  - if: { signal_type: doceree_named }
    floor: 5
  - if: { signal_type: layoff }
    floor: 3
  - if: { signal_type: funding_round, amount_usd: { gte: 50000000 } }
    floor: 4
adjustments:
  - if: { confidence: { lt: 3 } }
    severity_delta: -1
  - if: { crossvalidation_disagreement: true }
    severity_delta: -1
```

### `config/prompts.yaml`

```yaml
filter:
  model: gemini-2.5-flash-lite-001
  temperature: 0.0
  thinking_budget: 0
  max_output_tokens: 512
extract:
  model: gemini-2.5-flash-001
  temperature: 0.1
  thinking_budget: 512
  max_output_tokens: 2048
adversarial_check:
  model: gemini-2.5-pro-001
  temperature: 0.0
  thinking_budget: 4096
crossvalidate_nano:
  model: gpt-5-nano
  temperature: 0.0
synth_per_product:
  model: gemini-2.5-pro-001
  temperature: 0.3
  thinking_budget: 8192
synth_strategic:
  model: gemini-2.5-pro-001
  temperature: 0.4
  thinking_budget: 8192
new_entrant_discovery:
  model: gemini-2.5-pro-001
  temperature: 0.5
  thinking_budget: 16384
  use_grounding: true
```

### `config/delivery.yaml`

```yaml
recipients:
  primary: sherry.george@doceree.com
  cc: []
allowlist: [sherry.george@doceree.com]
telegram:
  chat_id_env: TELEGRAM_CHAT_ID
  alert_min_severity: 5
send_window_ist: { earliest: '06:00', latest: '07:30' }
weekly_discovery_day: monday
friday_battlecard_day: friday
```

---

## Pipeline data flow

```
config/source-registry.yaml + competitors.yaml
                |
                v
T1 INGEST (no LLM)
  RSS, sitemap, public APIs (SEC, jobs, GitHub, USPTO, Reddit, YouTube)
  -> raw items (URL, text excerpt, source_type, ts)
                |
                v
T2 FILTER (Gemini Flash-Lite)
  Discard: marketing fluff, dupes, off-topic, age >24h, NDA/social
  -> kept_items[]
                |
                v
T3 EXTRACT (Gemini Flash)
  JSON schema: Finding{url, source, competitor, summary, evidence_quote,
    signal_type, raw_severity, raw_confidence, products[]}
                |
                v
T4 VERIFY (parallel sub-stages)
  4a URL liveness HEAD/GET -> 200 (else drop)
  4b Pro adversarial self-check (does evidence support severity?)
  4c GPT-5-nano second opinion (Sev 4-5 only)
  4d Dedupe vs last 30d archive
  4e signal-mapping rules apply -> products mapped
  4f severity-rules.yaml applied -> final severity 1-5
  -> verified_findings[]
                |
                +-- fast-path Sev-5 -> Telegram (hourly job only)
                |
                v
T5 SYNTH PER PRODUCT (Pro, explicit cache)
  1 batched call covering all 13 products
                |
                v
T6 SYNTH STRATEGIC TOP-3 (Pro)
                |
                v
T7 RENDER
  jinja2 -> HTML
  premailer -> inline CSS
  JSONL append to archive
  HTML copy to docs-pages/
                |
                v
T8 DELIVER
  Gmail API -> Sherry
  gh-pages publish
```

---

## Error handling matrix

| Failure mode | Detection | Response |
|---|---|---|
| Gemini API down | tenacity exhausts retries | Mark stage degraded; if T5/T6 fail, fall back to Flash; if Flash fails, ship "system status" email with last-good link |
| Gemini RPD exhausted | 429 with RESOURCE_EXHAUSTED | Switch tier (Pro→Flash, Flash→Flash-Lite). Banner: "Pro quota exhausted; degraded synthesis." |
| OpenAI nano down | client error | Skip cross-validation. Tag findings `crossvalidation_skipped=true`. Render chip in card. Ship anyway. |
| RSS feed broken | feedparser bozo or HTTP error | Circuit-break that host 5min; record source-health failure; continue. After 3 days of failures, file GitHub Issue. |
| Hallucinated URL | T4a non-200 | Drop finding entirely. Log to `archive/hallucinated_urls.jsonl` for prompt regression analysis. |
| Malformed LLM JSON | pydantic ValidationError | One re-call with schema-violation note; if still bad, drop with structured log. |
| GH Actions runner failure | workflow job fails | `if: failure()` Telegram alert with run URL; artifacts uploaded via `if: always()`. |
| Email send fails | Gmail API error | Retry once; if still fails, post to gh-pages and Telegram link. Brief still ships. |
| Pages quota exceeded | push fails | Trim retention to 90 days; archive older to `_archive/`; ship anyway. |
| Schema regression after model update | eval F1 drop | Pin model versions explicitly (gemini-2.5-pro-001 not -latest). |

**Principle:** every stage has a degraded-but-shipping path. Sherry's 6 AM email always arrives. Worst case: it says "system status" with last-good link.

---

## Critical risks and mitigations

| Risk | Mitigation |
|---|---|
| Gemini free-tier cut again (Dec 2025 already cut Pro to 100 RPD) | Single-Pro-call synthesis variant from day 1; Flash fallback ready; small ($5/mo) Anthropic/OpenAI emergency budget |
| Hallucinated URLs | T4a mandatory live verification; drop on fail; track drop rate per prompt version; alert if >15% |
| Rate-limit spike during noisy news cycles | Pre-filter cap: 200 items per source per day; filter stage budgets ≤500 Flash-Lite calls; token-bucket queueing |
| Prompt drift from model updates | Pin model versions with explicit IDs; eval harness on every PR; 5 canary golden examples in production daily |
| Gmail OAuth expiry | Refresh-token flow; rotate annually; `verify_secrets.py` runs first in workflow; Telegram fallback if email fails |
| Existing Next.js scaffold drift | Archive in `legacy/` with explicit README; do not maintain two stacks |

---

## Acceptance criteria (final)

System is production-ready when ALL of:

1. Daily digest workflow green for 7 consecutive days
2. Hourly Sev-5 workflow green for 7 consecutive days
3. Weekly discovery workflow green for 2 consecutive Sundays
4. Friday battlecard workflow green for 2 consecutive Fridays
5. Eval suite passes with F1 thresholds: filter ≥0.92, extract ≥0.85, mapping ≥0.80, severity ≥0.90, verify ≥0.95
6. Sherry can answer "yes" to: "Did the digest catch every meaningful competitor move you cared about this week?"
7. CEO has either confirmed daily reading OR opted for weekly synthesis (decision made, not assumed)
8. Runbook exists and has been tested by a deliberate workflow failure simulation
9. Operational cost is verified at <$5/month for the past 7 days
10. README onboards a new contributor (or future Sherry-replacement) in <30 minutes

---

## Execution handoff

Plan complete and saved. Two execution options:

1. **Delegated execution in this session** — I dispatch tasks to fresh subagents per phase, review between phases, fast iteration in real-time as we build.
2. **Separate Claude Code session** — You open a new session pointing at this plan, execute task-by-task with checkpoints, full control over pacing.

Recommend option 2 for a build of this scope. The 28-day spec is too long for a single session; you'll want to checkpoint daily.

For option 2: open Claude Code in this repo, paste the prompt:

> "Read `docs/2026-04-30-lean-ci-build-plan.md`. Begin execution at Day 1, Task 1. After each task: run the verification step, commit with the specified message, then ask me before starting the next task."

Claude Code will execute one task at a time, you review between tasks, and the build progresses safely.
