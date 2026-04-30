"""Entry-point wrapper for the daily run.

Sets up sys.path so `from runners.run_daily import main` resolves to
`src/runners/run_daily.py`, loads `.env` from the repo root so API keys are
available, then delegates to the runner's main(). Pass any CLI args through.

Usage:
    python scripts/run_daily.py [--dry-run] [--send-to email] [--max-items N]
"""
from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    src_dir = repo_root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    # Load .env if present (no-op if missing).
    try:
        from dotenv import load_dotenv

        env_path = repo_root / ".env"
        if env_path.exists():
            load_dotenv(env_path)
    except ImportError:  # pragma: no cover
        pass


_bootstrap()

from runners.run_daily import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
