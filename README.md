# Doceree CI — Daily Competitive-Intelligence Digest

Python pipeline that produces a daily HTML digest at 06:00 IST covering Doceree's 13 products
across 14+ source types. Runs on GitHub Actions (free tier). See
[docs/2026-04-30-lean-ci-build-plan.md](docs/2026-04-30-lean-ci-build-plan.md) for the full
implementation plan and [design-2026-04-30-ci-digest.md](design-2026-04-30-ci-digest.md) for
the design rationale.

## Local setup

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # Windows PowerShell
pip install -r requirements-dev.txt
cp .env.example .env             # then fill in values
python scripts/verify_secrets.py
```

## One-time Gmail OAuth

```
python scripts/generate_gmail_token.py path/to/credentials.json
```

Copy the printed `GMAIL_REFRESH_TOKEN` into your local `.env` and into the GitHub repo secret of
the same name. The token does not expire as long as the OAuth client stays in production status.
