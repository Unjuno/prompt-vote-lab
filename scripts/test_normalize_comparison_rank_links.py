#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "normalize_comparison_rank_links.py"


def test_normalize_comparison_rank_links() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        index = Path(tmp) / "index.html"
        index.write_text(
            """<!doctype html>
<a href="./history/">History</a>
<a href="./comparisons/2026-W20/">Latest comparison</a>
<a href="../data/public-results.json">Public results JSON</a>
<a href="https://github.com/Unjuno/prompt-vote-lab/issues/195">Issue</a>
""",
            encoding="utf-8",
        )
        subprocess.run([sys.executable, str(SCRIPT), "--index", str(index)], check=True, cwd=ROOT)
        text = index.read_text(encoding="utf-8")

    required = [
        'href="../../../history/"',
        'href="../"',
        'href="../../../../data/public-results.json"',
        'href="https://github.com/Unjuno/prompt-vote-lab/issues/195"',
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError(f"normalized index missing expected links: {missing}")

    forbidden = [
        'href="./history/"',
        'href="./comparisons/2026-W20/"',
        'href="../data/public-results.json"',
    ]
    found = [item for item in forbidden if item in text]
    if found:
        raise AssertionError(f"rank-root index still has root-lab relative links: {found}")


def main() -> int:
    test_normalize_comparison_rank_links()
    print("comparison rank link normalizer test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
