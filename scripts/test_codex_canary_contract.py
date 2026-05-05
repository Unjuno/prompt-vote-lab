#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "codex-runner-contract.md"
WORKFLOW = ROOT / ".github" / "workflows" / "codex-first-canary-run.yml"
RUNNER = ROOT / "scripts" / "run_codex_first_canary.sh"

REQUIRED_CONTRACT_LINES = [
    "model: gpt-5.4-nano",
    "model_provider: openai",
    "model_reasoning_effort: medium",
    "model_reasoning_summary: auto",
    "model_verbosity: medium",
    "model_max_output_tokens: 5000",
    "temperature: unset/forbidden",
    "top_p: unset/forbidden",
    "logprobs: unset/forbidden",
    "seed: unset/forbidden",
    "web_search: disabled",
    "sandbox_mode: workspace-write",
    "approval_policy: never",
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
    "changing model_reasoning_effort",
    "changing model_reasoning_summary",
    "changing model_verbosity",
    "changing model_max_output_tokens",
    "adding temperature, top_p, logprobs, seed, or other sampling controls",
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

FORBIDDEN_WORKFLOW_LINES = [
    "CODEX_MODEL: gpt-5.1-codex",
    "CODEX_MODEL: gpt-5.1-codex-max",
    "temperature:",
    "top_p:",
    "logprobs:",
    "seed:",
]

REQUIRED_RUNNER_LINES = [
    "${CODEX_MODEL:-gpt-5.4-nano}",
    "--sandbox workspace-write",
]

FORBIDDEN_RUNNER_LINES = [
    "${CODEX_MODEL:-gpt-5.1-codex}",
    "gpt-5.1-codex-max",
    "--full-auto",
    "codex apply",
    "--temperature",
    "--top-p",
    "--logprobs",
    "--seed",
]


def main() -> int:
    contract = CONTRACT.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    runner = RUNNER.read_text(encoding="utf-8")

    missing_contract = [line for line in REQUIRED_CONTRACT_LINES if line not in contract]
    missing_workflow = [line for line in REQUIRED_WORKFLOW_LINES if line not in workflow]
    forbidden_workflow = [line for line in FORBIDDEN_WORKFLOW_LINES if line in workflow]
    missing_runner = [line for line in REQUIRED_RUNNER_LINES if line not in runner]
    forbidden_runner = [line for line in FORBIDDEN_RUNNER_LINES if line in runner]

    if missing_contract:
        raise SystemExit("Missing contract fixed-condition lines: " + ", ".join(missing_contract))
    if missing_workflow:
        raise SystemExit("Missing workflow fixed-condition lines: " + ", ".join(missing_workflow))
    if forbidden_workflow:
        raise SystemExit("Forbidden workflow lines present: " + ", ".join(forbidden_workflow))
    if missing_runner:
        raise SystemExit("Missing runner fixed-condition lines: " + ", ".join(missing_runner))
    if forbidden_runner:
        raise SystemExit("Forbidden runner lines present: " + ", ".join(forbidden_runner))

    print("codex canary contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
