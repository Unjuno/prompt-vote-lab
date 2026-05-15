#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "weekly-auto-run.yml"

CANONICAL_RUNNER_CALL = "display=f'bash scripts/run_codex_selected_prompt.sh --prompt-file {prompt_file} --candidate-rank {rank}'"
PUBLIC_BUNDLE_BUILD_CALL = "                  build_public_bundle(rank, issue)"
DIAGNOSTICS_COPY_CALL = "                  copy_rank_diagnostics(rank)"
ALWAYS_CANONICAL_ARTIFACT_CONDITION = "always() && steps.eligibility.outputs.has_eligible == 'true' && steps.weekly-vars.outputs.use_canonical == 'true'"

REQUIRED_TEXT = [
    "name: Weekly Auto Run",
    "workflow_dispatch:",
    "schedule:",
    "contents: write",
    "pull-requests: write",
    "issues: read",
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER: \"true\"",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER",
    "USE_CANONICAL_SELECTED_PROMPT_RUNNER=$use_canonical",
    "use_canonical=$use_canonical",
    "Canonical selected-prompt runner",
    "steps.weekly-vars.outputs.use_canonical != 'true'",
    "scripts/openai_lab_run.py",
    "steps.weekly-vars.outputs.use_canonical == 'true'",
    ALWAYS_CANONICAL_ARTIFACT_CONDITION,
    "if use_canonical:",
    "else:",
    "scripts/run_codex_selected_prompt.sh",
    "--prompt-file",
    CANONICAL_RUNNER_CALL,
    PUBLIC_BUNDLE_BUILD_CALL,
    DIAGNOSTICS_COPY_CALL,
    "weekly-selected-prompt-diagnostics",
    "weekly-selected-prompt-public-bundles",
    "weekly-selected-prompt-public-bundles-uploaded",
    "weekly-selected-prompt-uploaded-bundle-verification",
    "Download uploaded weekly selected-prompt public bundles",
    "Verify uploaded weekly selected-prompt public bundles",
    "Upload weekly selected-prompt uploaded bundle verification",
    "scripts/build_public_agent_run_bundle.py",
    "scripts/enrich_public_agent_run_bundle.py",
    "scripts/verify_public_agent_run_bundle.py",
    "scripts/run_gitleaks_public_bundle_scan.sh",
    "public-agent-run-bundle-uploaded-verification.json",
    "public-agent-run-bundle-uploaded-gitleaks.json",
    "public-agent-run-bundle-uploaded-gitleaks-findings.json",
    "Canonical selected-prompt runner: `",
    "gh', 'pr', 'create'",
]

FORBIDDEN_TEXT = [
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER: \"false\"",
    "gh pr merge",
    "auto-merge",
    "--prompt-body",  # weekly canonical path should avoid command-argument prompt bodies
]


def require_all(text: str, required: list[str]) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing weekly auto-run workflow text: {missing}")


def reject_all(text: str, forbidden: list[str]) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"Forbidden weekly auto-run workflow text found: {found}")


def require_block_order(text: str, first: str, second: str, message: str) -> None:
    if text.index(first) > text.index(second):
        raise SystemExit(message)


def require_count_at_least(text: str, marker: str, minimum: int, message: str) -> None:
    count = text.count(marker)
    if count < minimum:
        raise SystemExit(f"{message}: found {count}, expected at least {minimum}")


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    require_all(text, REQUIRED_TEXT)
    reject_all(text, FORBIDDEN_TEXT)
    require_count_at_least(
        text,
        ALWAYS_CANONICAL_ARTIFACT_CONDITION,
        5,
        "weekly canonical artifact/evidence steps should run under always()",
    )

    require_block_order(
        text,
        "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER: \"true\"",
        "Prepare weekly variables",
        "canonical selected-prompt runner default should be declared before weekly variables",
    )
    require_block_order(
        text,
        "steps.weekly-vars.outputs.use_canonical != 'true'",
        "python -m pip install openai",
        "legacy OpenAI dependency install should be gated before the install command",
    )
    require_block_order(
        text,
        "if use_canonical:",
        "scripts/run_codex_selected_prompt.sh",
        "canonical runner invocation should be inside the feature-flag branch",
    )
    require_block_order(
        text,
        "else:",
        "scripts/openai_lab_run.py",
        "legacy runner invocation should be inside the non-canonical branch",
    )
    require_block_order(
        text,
        CANONICAL_RUNNER_CALL,
        PUBLIC_BUNDLE_BUILD_CALL,
        "canonical runner invocation should precede the public bundle build call",
    )
    require_block_order(
        text,
        PUBLIC_BUNDLE_BUILD_CALL,
        DIAGNOSTICS_COPY_CALL,
        "rank diagnostics copy should include public bundle verification reports",
    )
    require_block_order(
        text,
        "scripts/build_public_agent_run_bundle.py",
        "scripts/enrich_public_agent_run_bundle.py",
        "public bundle enrichment should run after bundle build",
    )
    require_block_order(
        text,
        "scripts/enrich_public_agent_run_bundle.py",
        "scripts/verify_public_agent_run_bundle.py",
        "public bundle verification should run after enrichment",
    )
    require_block_order(
        text,
        "scripts/verify_public_agent_run_bundle.py",
        "scripts/run_gitleaks_public_bundle_scan.sh",
        "Gitleaks scan should run after public bundle verification",
    )
    require_block_order(
        text,
        "Upload weekly selected-prompt public bundles",
        "Download uploaded weekly selected-prompt public bundles",
        "uploaded public bundles should be downloaded only after upload",
    )
    require_block_order(
        text,
        "Download uploaded weekly selected-prompt public bundles",
        "Verify uploaded weekly selected-prompt public bundles",
        "uploaded public bundles should be verified after download",
    )
    require_block_order(
        text,
        "Verify uploaded weekly selected-prompt public bundles",
        "Upload weekly selected-prompt uploaded bundle verification",
        "uploaded bundle verification artifact should upload after verification",
    )

    print("weekly auto-run workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())