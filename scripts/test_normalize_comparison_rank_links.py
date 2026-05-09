#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "normalize_comparison_rank_links.py"


def run_normalizer(index: Path, week_id: str | None = None) -> None:
    cmd = [sys.executable, str(SCRIPT), "--index", str(index)]
    if week_id:
        cmd.extend(["--week-id", week_id])
    subprocess.run(cmd, check=True, cwd=ROOT)


def assert_links(text: str, week_id: str) -> None:
    required = [
        'href="../../../history/"',
        'href="../"',
        'href="../../../../data/public-results.json"',
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError(f"missing normalized links: {missing}")

    forbidden = [
        'href="./history/"',
        f'href="./comparisons/{week_id}/"',
        'href="../data/public-results.json"',
    ]
    found = [item for item in forbidden if item in text]
    if found:
        raise AssertionError(f"root-lab links remain: {found}")


def test_explicit_week() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        index = Path(tmp) / "index.html"
        index.write_text(
            '<a href="./history/">History</a>\n'
            '<a href="./comparisons/2026-W21/">Latest</a>\n'
            '<a href="../data/public-results.json">Results</a>\n',
            encoding="utf-8",
        )
        run_normalizer(index, "2026-W21")
        assert_links(index.read_text(encoding="utf-8"), "2026-W21")


def test_inferred_week() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        rank_root = Path(tmp) / "lab" / "comparisons" / "2026-W22" / "rank-3"
        rank_root.mkdir(parents=True)
        index = rank_root / "index.html"
        index.write_text(
            '<a href="./history/">History</a>\n'
            '<a href="./comparisons/2026-W22/">Latest</a>\n'
            '<a href="../data/public-results.json">Results</a>\n',
            encoding="utf-8",
        )
        run_normalizer(index)
        assert_links(index.read_text(encoding="utf-8"), "2026-W22")


def main() -> int:
    test_explicit_week()
    test_inferred_week()
    print("comparison rank link normalizer test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
