#!/usr/bin/env python3
"""Repository audit for the Prompt Vote Lab pre-API freeze.

No network calls. No model calls. No GitHub API calls.

This script checks that the repository contains the required offline gates before
paid implementation-agent API use is allowed by policy.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/pre-api-freeze.md",
    "formal/Selection.lean",
    "lean-toolchain",
    "scripts/collect_votes.py",
    "scripts/test_collect_votes.py",
    "scripts/select_eligible.py",
    "scripts/test_select_eligible.py",
    "scripts/test_weekly_auto_no_eligible.py",
    "scripts/preflight_implementation_agent.py",
    "scripts/test_preflight_implementation_agent.py",
    "scripts/exception_matrix_test.py",
    "scripts/multi_fuzz.py",
    "scripts/safety-check.sh",
    "scripts/static-site-check.sh",
    ".github/workflows/collect-votes-test.yml",
    ".github/workflows/select-eligible-test.yml",
    ".github/workflows/implementation-preflight-test.yml",
    ".github/workflows/lean-proof-test.yml",
    ".github/workflows/exception-matrix-test.yml",
    ".github/workflows/multi-fuzz-test.yml",
    ".github/workflows/weekly-auto-run.yml",
    ".github/workflows/weekly-mock-run.yml",
    ".github/workflows/weekly-report-draft.yml",
]

REQUIRED_TEXT = {
    "docs/pre-api-freeze.md": [
        "no hidden retry",
        "no fallback model",
        "Weekly Auto Run no-eligible workflow",
        "one agent attempt",
        "manual review before merge",
    ],
    "scripts/preflight_implementation_agent.py": [
        "ALLOWED_MODELS = {\"gpt-5-nano\"}",
        "MAX_OUTPUT_TOKENS_LIMIT = 12000",
        "sdk_max_retries must be 0",
        "api_call_limit_per_candidate must be 1",
    ],
    "scripts/select_eligible.py": [
        "if baseline_won(candidates):",
        "return []",
        "support >= 5",
        "support >= 10",
    ],
    ".github/workflows/weekly-auto-run.yml": [
        "python scripts/select_eligible.py",
        "Preflight implementation-agent run",
        "python scripts/preflight_implementation_agent.py",
        "MAX_OUTPUT_TOKENS: \"12000\"",
        "gpt-5-nano",
    ],
    "formal/Selection.lean": [
        "theorem baseline_won_implies_no_eligible",
        "baseline_not_eligible_one",
        "other_not_eligible_one",
        "selectEligible",
    ],
    "scripts/static-site-check.sh": [
        "docs/pre-api-freeze.md",
        "pre-API freeze checklist",
    ],
}

FORBIDDEN_TEXT = {
    ".github/workflows/weekly-auto-run.yml": [
        "max_retries: 1",
        "max_retries: 2",
        "fallback",
        "auto-merge",
    ],
    "docs/pre-api-freeze.md": [
        "automatic merge is allowed",
        "fallback model is allowed",
        "hidden retry is allowed",
    ],
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            failures.append(f"missing required file: {rel}")

    for rel, needles in REQUIRED_TEXT.items():
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"cannot check text; missing file: {rel}")
            continue
        text = read(rel)
        for needle in needles:
            if needle not in text:
                failures.append(f"missing required text in {rel}: {needle}")

    for rel, needles in FORBIDDEN_TEXT.items():
        path = ROOT / rel
        if not path.is_file():
            continue
        text = read(rel)
        for needle in needles:
            if needle in text:
                failures.append(f"forbidden text in {rel}: {needle}")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1

    print("pre-API freeze audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
