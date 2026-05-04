#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/pre-api-freeze.md",
    "docs/current-features.md",
    "docs/canary-policy.md",
    "docs/canary-report-template.md",
    "docs/stop-rules.md",
    "docs/weekly-ops-doctrine.md",
    "docs/evidence-artifact-review.md",
    "formal/Selection.lean",
    "lean-toolchain",
    "scripts/select_eligible.py",
    "scripts/preflight_implementation_agent.py",
    "scripts/create-weekly-snapshot.mjs",
    "scripts/create-snapshot-summary.mjs",
    "scripts/create-public-briefing.mjs",
    "scripts/run-evidence-artifact-smoke.mjs",
    ".github/workflows/weekly-auto-run.yml",
    ".github/workflows/evidence-pipeline-dry-run.yml",
]

REQUIRED_SUBSTRINGS: dict[str, list[str]] = {
    "docs/pre-api-freeze.md": [
        "no automatic merge",
        "no hidden retry",
        "no fallback model",
        "Weekly Auto Run no-eligible workflow",
        "gpt-5-nano",
        "workflow attempts to auto-merge",
    ],
    "docs/canary-policy.md": [
        "model: gpt-5-nano",
        "attempts per candidate: 1",
        "SDK max_retries: 0",
        "fallback model: none",
        "automatic merge: no",
        "max continuation runs per candidate: 1",
    ],
    "docs/stop-rules.md": [
        "more than one implementation-agent attempt for a single candidate",
        "SDK retry is enabled or triggered",
        "fallback model is used",
        "implementation runs when eligible_count = 0",
        "workflow attempts auto-merge",
    ],
    "docs/current-features.md": [
        "real implementation-agent canary: not yet executed",
        "production autonomy: not complete",
        "Run one final no-eligible workflow test before any paid implementation-agent canary.",
    ],
    "docs/weekly-ops-doctrine.md": [
        "Observe → Orient → Decide → Act → Record → Improve",
        "snapshot exists",
        "briefing exists",
        "no voter login list is stored",
    ],
    "docs/evidence-artifact-review.md": [
        "Evidence Pipeline Dry Run",
        "snapshot-v1.2",
        "snapshot-summary-v1.0",
        "Do-not-post checklist",
        "no voter login list appears",
    ],
    "scripts/preflight_implementation_agent.py": [
        "ALLOWED_MODELS = {\"gpt-5-nano\"}",
        "MAX_OUTPUT_TOKENS_LIMIT = 12000",
        "if sdk_max_retries != 0",
        "api_call_limit != 1",
        "validate_env_secret(len(candidates))",
        "api_call_performed",
        "False",
    ],
    "scripts/create-weekly-snapshot.mjs": [
        "snapshot-v1.2",
        "no_change_baseline_candidate",
        "unique_voter_count_available",
        "_voter_logins",
    ],
    "scripts/create-snapshot-summary.mjs": [
        "snapshot-summary-v1.0",
        "forbiddenKeys",
        "duplicate week",
        "metrics.candidate_count must match all_candidates.length",
    ],
    "scripts/create-public-briefing.mjs": [
        "Prompt Vote Lab Briefing",
        "## Observe",
        "## Act",
        "Do not treat it as an automated external post",
    ],
    "scripts/run-evidence-artifact-smoke.mjs": [
        "snapshot-v1.2",
        "snapshot-summary-v1.0",
        "Prompt Vote Lab Briefing",
        "Do-not-post checklist",
    ],
    ".github/workflows/weekly-auto-run.yml": [
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5-nano\"",
        "SDK_MAX_RETRIES: \"0\"",
        "--api-call-limit-per-candidate 1",
        "if: ${{ steps.eligibility.outputs.has_eligible == 'true' }}",
        "No eligible candidates. No implementation-agent attempt will be made.",
        "python -m pip install openai",
        "gh pr create",
    ],
    ".github/workflows/evidence-pipeline-dry-run.yml": [
        "Generate public briefing",
        "weekly-metrics.json",
        "week-${WEEK_ID}.md",
        "Do-not-post checklist",
        "Upload evidence pipeline dry-run artifact",
    ],
}

FORBIDDEN_SUBSTRINGS: dict[str, list[str]] = {
    ".github/workflows/weekly-auto-run.yml": [
        "enable-auto-merge",
        "gh pr merge --auto",
        "SDK_MAX_RETRIES: \"1\"",
        "SDK_MAX_RETRIES: \"2\"",
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5\"",
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5-mini\"",
    ],
    "scripts/preflight_implementation_agent.py": [
        "ALLOWED_MODELS = {\"gpt-5\"}",
        "ALLOWED_MODELS = {\"gpt-5-mini\"}",
        "api_call_performed\": True",
        "sdk_max_retries != 1",
    ],
}


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            failures.append(f"missing required file: {rel}")

    if failures:
        for failure in failures:
            print("ERROR:", failure)
        return 1

    for rel, needles in REQUIRED_SUBSTRINGS.items():
        text = read_text(rel)
        for needle in needles:
            if needle not in text:
                failures.append(f"{rel}: missing required text: {needle}")

    for rel, needles in FORBIDDEN_SUBSTRINGS.items():
        text = read_text(rel)
        for needle in needles:
            if needle in text:
                failures.append(f"{rel}: forbidden text present: {needle}")

    weekly_auto = read_text(".github/workflows/weekly-auto-run.yml")
    require_if_guard(
        weekly_auto,
        "Require implementation secret only if candidates are eligible",
        "steps.eligibility.outputs.has_eligible == 'true'",
        failures,
    )
    require_if_guard(
        weekly_auto,
        "Preflight implementation-agent run",
        "steps.eligibility.outputs.has_eligible == 'true'",
        failures,
    )
    require_if_guard(
        weekly_auto,
        "Install Python dependency",
        "steps.eligibility.outputs.has_eligible == 'true'",
        failures,
    )
    require_if_guard(
        weekly_auto,
        "Create implementation PRs for eligible candidates",
        "steps.eligibility.outputs.has_eligible == 'true'",
        failures,
    )

    if failures:
        for failure in failures:
            print("ERROR:", failure)
        return 1

    print("pre-API freeze audit passed")
    return 0


def require_if_guard(text: str, step_name: str, expected_guard: str, failures: list[str]) -> None:
    marker = f"- name: {step_name}"
    index = text.find(marker)
    if index < 0:
        failures.append(f"weekly-auto-run.yml: missing step: {step_name}")
        return
    next_index = text.find("\n      - name:", index + len(marker))
    block = text[index: next_index if next_index >= 0 else len(text)]
    if expected_guard not in block:
        failures.append(f"weekly-auto-run.yml: step lacks eligible guard: {step_name}")


if __name__ == "__main__":
    raise SystemExit(main())
