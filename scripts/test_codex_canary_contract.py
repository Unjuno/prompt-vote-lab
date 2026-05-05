#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "codex-runner-contract.md"
WORKFLOW = ROOT / ".github" / "workflows" / "codex-first-canary-run.yml"

REQUIRED_CONTRACT_LINES = [
    "model: gpt-5.4-nano",
    "candidate_rank: 1",
    "issue_number: 0",
    "vote_count: 0",
    "week: first-canary-001",
    "attempts_per_candidate: 1",
    "retry_policy: none",
    "fallback_policy: none",
    "auto_merge_policy: disabled",
    "allowed_changed_files: lab/index.html, lab/style.css, lab/app.js",
    "changing the model",
    "changing temperature or sampling parameters",
    "adding fallback models",
    "adding retries",
]

REQUIRED_WORKFLOW_LINES = [
    "CODEX_MODEL: gpt-5.4-nano",
    "RUN_WEEK: first-canary-001",
    "--candidate-rank 1",
    "--issue-number 0",
    "--vote-count 0",
    "--attempt-count 1",
    "--retry-policy none",
    "--fallback-policy none",
    "--auto-merge-policy disabled",
    "lab/index.html|lab/style.css|lab/app.js",
]


def main() -> int:
    contract = CONTRACT.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    missing_contract = [line for line in REQUIRED_CONTRACT_LINES if line not in contract]
    missing_workflow = [line for line in REQUIRED_WORKFLOW_LINES if line not in workflow]

    if missing_contract:
        raise SystemExit("Missing contract fixed-condition lines: " + ", ".join(missing_contract))
    if missing_workflow:
        raise SystemExit("Missing workflow fixed-condition lines: " + ", ".join(missing_workflow))

    print("codex canary contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
