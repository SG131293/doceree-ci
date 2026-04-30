"""Entry-point wrapper for the failure notifier.

Sets up sys.path so `from runners.notify_failure import main` resolves to
`src/runners/notify_failure.py`. Loads .env if present (no-op in CI).

Usage from GitHub Actions:
    python scripts/notify_failure.py
"""
from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    src_dir = repo_root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    try:
        from dotenv import load_dotenv

        env_path = repo_root / ".env"
        if env_path.exists():
            load_dotenv(env_path)
    except ImportError:  # pragma: no cover
        pass


_bootstrap()

from runners.notify_failure import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
