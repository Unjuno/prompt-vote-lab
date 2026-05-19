#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_MODEL = "gpt-5.4-nano"
WEEKLY_WORKFLOW = ".github/workflows/weekly-auto-run.yml"

REQUIRED_FILES = [
    "docs/current-features.md",
    "docs/weekly-ops-doctrine.md",
    "docs/evidence-artifact-review.md",
    "runs/evidence-review-template.md",
    "formal/Selection.lean",
    "formal/Canary.lean",
    "lean-toolchain",
    "scripts/select_eligible.py",
    "scripts/preflight_implementation_agent.py",
    "scripts/create-weekly-snapshot.mjs",
    "scripts/create-snapshot-summary.mjs",
    "scripts/create-public-briefing.mjs",
    "scripts/run-evidence-artifact-smoke.mjs",
    "scripts/validate-evidence-artifact.mjs",
    WEEKLY_WORKFLOW,
    ".github/workflows/evidence-pipeline-dry-run.yml",
]

REMOVED_FILES = [
    ".github/workflows/first-canary-run.yml",
    "scripts/create_first_canary_candidate.py",
]

REQUIRED_SUBSTRINGS: dict[str, list[str]] = {
    "docs/current-features.md": [
        "no-eligible production workflow path: verified",
        "Support Unlock Export live path: verified",
        "canonical selected-prompt canary: verified",
        "canonical weekly fixed-on: approved",
        "ordinary post-default-on weekly observation: PASS",
        "weekly legacy API/SDK fallback branch",
        "removed workflow: .github/workflows/first-canary-run.yml",
        "removed helper: scripts/create_first_canary_candidate.py",
        "protected evidence removed: no",
        "generated snapshots touched: no",
        ACTIVE_MODEL,
        "Evidence Pipeline Dry Run",
        "source=live",
    ],
    "docs/weekly-ops-doctrine.md": [
        "Observe → Orient → Decide → Act → Record → Improve",
        "snapshot exists",
        "briefing exists",
        "no voter login list is stored",
    ],
    "docs/evidence-artifact-review.md": [
        "Evidence Pipeline Dry Run",
        "validate-evidence-artifact.mjs",
        "runs/evidence-review-template.md",
        "snapshot-v1.2",
        "snapshot-summary-v1.0",
        "Do-not-post checklist",
        "no voter login list appears",
    ],
    "runs/evidence-review-template.md": [
        "Evidence Review Record Template",
        "validator_result: PASS | FAIL",
        "human_review: PASS | FAIL | UNCERTAIN",
        "final_decision: PASS | FAIL | UNCERTAIN",
        "Live evidence path is verified",
        "Do not proceed to implementation-agent canary",
    ],
    "formal/Canary.lean": [
        "def safeCanary",
        "safe_canary_scope_lab_only",
        "safe_canary_one_attempt",
        "safe_canary_no_sdk_retry",
        "safe_canary_one_api_call",
        "safe_canary_no_fallback",
        "safe_canary_no_auto_merge",
        "safe_canary_no_external_publishing",
    ],
    "scripts/preflight_implementation_agent.py": [
        f"ALLOWED_MODELS = {{\"{ACTIVE_MODEL}\"}}",
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
        "scripts/validate-evidence-artifact.mjs",
        "create-weekly-snapshot.mjs",
        "create-snapshot-summary.mjs",
        "create-public-briefing.mjs",
        "create-hn-draft.mjs",
    ],
    "scripts/validate-evidence-artifact.mjs": [
        "snapshot-v1.2",
        "snapshot-summary-v1.0",
        "Prompt Vote Lab Briefing",
        "Do-not-post checklist",
        "weekly_snapshot_started",
        "weekly_snapshot_finished",
        "no_change_baseline_candidate",
    ],
    WEEKLY_WORKFLOW: [
        f"AUTO_IMPLEMENTATION_MODEL: \"{ACTIVE_MODEL}\"",
        f"IMPLEMENTATION_MODEL: {ACTIVE_MODEL}",
        "SDK_MAX_RETRIES: \"0\"",
        "--api-call-limit-per-candidate 1",
        "if: ${{ steps.eligibility.outputs.has_eligible == 'true' }}",
        "No eligible candidates. No implementation-agent attempt will be made.",
        "scripts/run_codex_selected_prompt.sh",
        "--prompt-file",
        "gh pr create",
    ],
    ".github/workflows/evidence-pipeline-dry-run.yml": [
        "Generate public briefing",
        "weekly-metrics.json",
        "week-${WEEK_ID}.md",
        "Do-not-post checklist",
        "validate-evidence-artifact.mjs",
        "Upload evidence pipeline dry-run artifact",
    ],
}

FORBIDDEN_SUBSTRINGS: dict[str, list[str]] = {
    WEEKLY_WORKFLOW: [
        "enable-auto-merge",
        "gh pr merge --auto",
        "MAX_OUTPUT_TOKENS",
        "--max-output-tokens",
        "Install Python dependency",
        "python -m pip install",
        "use_canonical",
        "allow_legacy",
        "ALLOW_LEGACY",
        "PROMPT_VOTE_LAB_ALLOW_LEGACY",
        "legacy-",
        "_lab_run.py",
        "SDK_MAX_RETRIES: \"1\"",
        "SDK_MAX_RETRIES: \"2\"",
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5\"",
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5-mini\"",
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5-nano\"",
    ],
    "scripts/preflight_implementation_agent.py": [
        "ALLOWED_MODELS = {\"gpt-5\"}",
        "ALLOWED_MODELS = {\"gpt-5-mini\"}",
        "ALLOWED_MODELS = {\"gpt-5-nano\"}",
        "MAX_OUTPUT_TOKENS",
        "max-output-tokens",
        "output_token_cap_enforced",
        "legacy_max_output_tokens_input_present",
        "api_call_performed\": True",
        "sdk_max_retries != 1",
    ],
    "docs/current-features.md": [
        "ordinary post-default-on weekly observation: pending",
        "Observe the next ordinary weekly run.",
    ],
}


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def require_if_guard(workflow: str, step_name: str, expected_guard: str, failures: list[str]) -> None:
    step = f"      - name: {step_name}\n"
    start = workflow.find(step)
    if start < 0:
        failures.append(f"{WEEKLY_WORKFLOW}: missing step: {step_name}")
        return
    next_step = workflow.find("\n      - name:", start + len(step))
    block = workflow[start:next_step if next_step >= 0 else len(workflow)]
    if expected_guard not in block:
        failures.append(f"{WEEKLY_WORKFLOW}: step {step_name!r} missing guard {expected_guard!r}")


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            failures.append(f"missing required file: {rel}")

    for rel in REMOVED_FILES:
        if (ROOT / rel).exists():
            failures.append(f"retired legacy launch file still exists: {rel}")

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

    weekly_auto = read_text(WEEKLY_WORKFLOW)
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


if __name__ == "__main__":
    raise SystemExit(main())
