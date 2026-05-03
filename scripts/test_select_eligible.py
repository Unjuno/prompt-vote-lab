#!/usr/bin/env python3
"""Smoke tests for scripts/select_eligible.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "select_eligible.py"


def load_module():
    spec = importlib.util.spec_from_file_location("select_eligible", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load select_eligible.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["select_eligible"] = module
    spec.loader.exec_module(module)
    return module


def candidate(rank: int, issue: int, votes: int, candidate_type: str = "prompt-proposal") -> dict:
    return {
        "rank": rank,
        "issue_number": issue,
        "title": f"candidate {issue}",
        "url": "",
        "vote_count": votes,
        "body": f"prompt {issue}",
        "candidate_type": candidate_type,
    }


def assert_equal(actual, expected, label: str) -> None:
    if actual != expected:
        raise SystemExit(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    sel = load_module()

    baseline_first = [
        candidate(1, 0, 20, "no-change-baseline"),
        candidate(2, 10, 7),
        candidate(3, 11, 6),
    ]
    assert_equal(sel.select_eligible(baseline_first, 0), [], "baseline first no support")
    assert_equal(sel.select_eligible(baseline_first, 5), [], "baseline first support 5")
    assert_equal(sel.select_eligible(baseline_first, 10), [], "baseline first support 10")

    prompt_first = [
        candidate(1, 10, 24),
        candidate(2, 0, 20, "no-change-baseline"),
        candidate(3, 11, 12),
    ]
    eligible = sel.select_eligible(prompt_first, 0)
    assert_equal([c["issue_number"] for c in eligible], [10], "rank 1 only with no support")
    assert_equal([c["run_reason"] for c in eligible], ["normal-weekly-run"], "rank 1 reason")

    prompt_top3 = [
        candidate(1, 10, 30),
        candidate(2, 11, 25),
        candidate(3, 12, 24),
        candidate(4, 0, 20, "no-change-baseline"),
    ]
    assert_equal([c["issue_number"] for c in sel.select_eligible(prompt_top3, 0)], [10], "support 0")
    assert_equal([c["issue_number"] for c in sel.select_eligible(prompt_top3, 5)], [10, 11], "support 5")
    assert_equal([c["issue_number"] for c in sel.select_eligible(prompt_top3, 10)], [10, 11, 12], "support 10")
    assert_equal(
        [c["run_reason"] for c in sel.select_eligible(prompt_top3, 10)],
        ["normal-weekly-run", "support-unlocked-run", "support-unlocked-run"],
        "support run reasons",
    )

    try:
        sel.select_eligible(prompt_top3, -1)
    except ValueError:
        pass
    else:
        raise SystemExit("negative support must fail")

    print("select_eligible smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
