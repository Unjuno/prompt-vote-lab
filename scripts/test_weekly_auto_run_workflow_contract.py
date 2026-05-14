#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "weekly-auto-run.yml"

REQUIRED_TEXT = [
    "name: Weekly Auto Run",
    "workflow_dispatch:",
    "schedule:",
    "contents: write",
    "pull-requests: write",
    "issues: read",
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER: \"false\"",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER",
    "USE_CANONICAL_SELECTED_PROMPT_RUNNER=$use_canonical",
    "use_canonical=$use_canonical",
    "Canonical selected-prompt runner",
    "steps.weekly-vars.outputs.use_canonical != 'true'",
    "scripts/openai_lab_run.py",
    "steps.weekly-vars.outputs.use_canonical == 'true'",
    "scripts/run_codex_selected_prompt.sh",
    "--prompt-file",
    "weekly-selected-prompt-diagnostics",
    "weekly-selected-prompt-public-bundles",
    "scripts/build_public_agent_run_bundle.py",
    "scripts/enrich_public_agent_run_bundle.py",
    "scripts/verify_public_agent_run_bundle.py",
    "scripts/run_gitleaks_public_bundle_scan.sh",
    "Canonical selected-prompt runner: `",
    "gh', 'pr', 'create'",
]

FORBIDDEN_TEXT = [
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


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    require_all(text, REQUIRED_TEXT)
    reject_all(text, FORBIDDEN_TEXT)

    if text.index("DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER: \"false\"") > text.index("Prepare weekly variables"):
        raise SystemExit("canonical selected-prompt runner default should be declared before weekly variables")

    if text.index("steps.weekly-vars.outputs.use_canonical != 'true'") > text.index("python -m pip install openai"):
        raise SystemExit("legacy OpenAI dependency install should be gated before the install command")

    if text.index("scripts/openai_lab_run.py") > text.index("scripts/run_codex_selected_prompt.sh"):
        raise SystemExit("legacy path should remain before the feature-flagged canonical path in the implementation branch")

    if text.index("scripts/run_codex_selected_prompt.sh") > text.index("scripts/build_public_agent_run_bundle.py"):
        raise SystemExit("canonical runner should execute before public bundle build")

    if text.index("scripts/build_public_agent_run_bundle.py") > text.index("scripts/enrich_public_agent_run_bundle.py"):
        raise SystemExit("public bundle enrichment should run after bundle build")

    if text.index("scripts/enrich_public_agent_run_bundle.py") > text.index("scripts/verify_public_agent_run_bundle.py"):
        raise SystemExit("public bundle verification should run after enrichment")

    if text.index("scripts/verify_public_agent_run_bundle.py") > text.index("scripts/run_gitleaks_public_bundle_scan.sh"):
        raise SystemExit("Gitleaks scan should run after public bundle verification")

    print("weekly auto-run workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
