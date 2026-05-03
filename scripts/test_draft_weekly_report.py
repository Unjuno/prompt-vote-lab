#!/usr/bin/env python3
"""Smoke tests for scripts/draft_weekly_report.py.

No network calls. No model calls.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "draft_weekly_report.py"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def main() -> int:
    ok_path = ROOT / "runs" / "week-test-report.md"
    if ok_path.exists():
        ok_path.unlink()

    ok = run([
        "--week", "week-test",
        "--selected-prompt", "Test prompt",
        "--issue-number", "1",
        "--pr-number", "2",
        "--candidate-rank", "1",
        "--vote-count", "21",
        "--baseline-votes", "20",
        "--outcome", "merged",
        "--expectation-gap", "Hit",
        "--run-reason", "test",
    ])
    if ok.returncode != 0:
        print(ok.stdout)
        raise SystemExit("expected valid report draft to pass")
    if not ok_path.exists():
        raise SystemExit("expected report file to be written")
    text = ok_path.read_text(encoding="utf-8")
    if "Weekly Prompt Game Report: week-test" not in text:
        raise SystemExit("report title missing")
    if "Expectation gap: Hit" not in text:
        raise SystemExit("expectation gap missing")
    ok_path.unlink()

    bad_week = run(["--week", "../escape", "--selected-prompt", "bad"])
    if bad_week.returncode == 0:
        raise SystemExit("expected unsafe week label to fail")

    bad_out = run(["--week", "week-test", "--selected-prompt", "bad", "--out", "README.md"])
    if bad_out.returncode == 0:
        raise SystemExit("expected non-runs output path to fail")

    print("draft_weekly_report smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
