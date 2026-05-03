#!/usr/bin/env python3
"""Smoke tests for scripts/collect_votes.py.

No network calls. No GitHub API calls.
Verification trigger: collect-votes-test.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "collect_votes.py"


def load_collect_votes():
    spec = importlib.util.spec_from_file_location("collect_votes", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load collect_votes.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["collect_votes"] = module
    spec.loader.exec_module(module)
    return module


def assert_equal(actual, expected, label: str) -> None:
    if actual != expected:
        raise SystemExit(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    cv = load_collect_votes()

    issue_form_body = """### Voted prompt
Add a round-history panel.

### Expected visible result
A panel is visible.
"""
    assert_equal(
        cv.extract_voted_prompt(issue_form_body, "fallback title"),
        "Add a round-history panel.",
        "issue form h3 extraction",
    )

    legacy_body = """## Voted prompt
Add a compact score card.

## Why
It is visible.
"""
    assert_equal(
        cv.extract_voted_prompt(legacy_body, "fallback title"),
        "Add a compact score card.",
        "legacy h2 extraction",
    )

    exact_prompt_body = """#### Exact prompt
Use a fixed local scoring expression.

#### Notes
No network.
"""
    assert_equal(
        cv.extract_voted_prompt(exact_prompt_body, "fallback title"),
        "Use a fixed local scoring expression.",
        "alternate exact prompt heading extraction",
    )

    no_response_body = """### Voted prompt
_No response_

### Expected visible result
Something.
"""
    assert_equal(
        cv.extract_voted_prompt(no_response_body, "fallback title"),
        "fallback title",
        "no response fallback",
    )

    no_heading_body = """This is just a freeform issue body."""
    assert_equal(
        cv.extract_voted_prompt(no_heading_body, "fallback title"),
        "fallback title",
        "missing heading fallback",
    )

    candidates = [
        cv.Candidate(0, 0, "[Baseline]: No change this week", "", 20, "baseline", "no-change-baseline"),
        cv.Candidate(0, 2, "Issue 2", "https://example.invalid/2", 21, "prompt two", "prompt-proposal"),
        cv.Candidate(0, 1, "Issue 1", "https://example.invalid/1", 21, "prompt one", "prompt-proposal"),
    ]
    candidates.sort(key=lambda c: (-c.vote_count, c.issue_number))
    for index, candidate in enumerate(candidates, start=1):
        candidate.rank = index

    assert_equal(candidates[0].issue_number, 1, "tie-breaker lower issue number wins")
    assert_equal(candidates[1].issue_number, 2, "tie-breaker second issue")
    assert_equal(candidates[2].candidate_type, "no-change-baseline", "baseline rank after higher votes")

    print("collect_votes smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
