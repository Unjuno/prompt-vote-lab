#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DOCS = {
    "readme": ROOT / "docs" / "README.md",
    "current_path": ROOT / "docs" / "current-codex-implementation-path.md",
    "evidence_guide": ROOT / "docs" / "canonical-runner-evidence-guide.md",
    "weekly_automation": ROOT / "docs" / "weekly-automation.md",
    "operator_runbook": ROOT / "docs" / "operator-runbook.md",
    "workflow_family_map": ROOT / "docs" / "workflow-family-map.md",
    "cleanup_inventory": ROOT / "docs" / "repository-cleanup-inventory.md",
    "drift_check": ROOT / "docs" / "canonical-status-drift-check.md",
}

CANONICAL_MARKER = [
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
]

LEGACY_SCRIPT_TEXT = [
    "scripts/openai_lab_run.py",
    "non-canonical",
]

FIXED_WEEKLY_TEXT = [
    "weekly default status: canonical selected-prompt runner fixed-on",
    "weekly legacy override: removed from Weekly Auto Run",
]

FORBIDDEN_PHRASES = [
    "canonical weekly default: not default-on",
    "weekly default status: default-off during migration",
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "weekly feature flag alone must not silently spend",
    "can reach legacy weekly fallback path",
    "weekly legacy fallback path",
    "first-canary workflow requires confirm_legacy_api_canary",
    "legacy fallback removal is approved",
    "scripts/openai_lab_run.py is canonical",
    "openai_lab_run.py is canonical",
    "auto-merge enabled",
]


def read_docs() -> dict[str, str]:
    return {name: path.read_text(encoding="utf-8") for name, path in DOCS.items()}


def require_all(text: str, required: list[str], label: str) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing {label} text: {missing}")


def reject_all(text: str, forbidden: list[str], label: str) -> None:
    lowered = text.lower()
    found = [item for item in forbidden if item.lower() in lowered]
    if found:
        raise SystemExit(f"Forbidden {label} text found: {found}")


def require_marker_pair(text: str, label: str) -> None:
    require_all(text, CANONICAL_MARKER, label)
    pair = CANONICAL_MARKER[0] + "\n" + CANONICAL_MARKER[1]
    if pair not in text:
        raise SystemExit(f"Canonical marker pair is missing in {label}")


def main() -> int:
    docs = read_docs()
    all_text = "\n".join(docs.values())

    require_all(docs["drift_check"], [
        "# Canonical status drift check",
        "Stable status contract",
        "weekly default status: canonical selected-prompt runner fixed-on",
        "weekly feature flag override: removed",
        "weekly legacy override: removed from Weekly Auto Run",
        "legacy fallback script: scripts/openai_lab_run.py",
        "legacy fallback status: non-canonical manual diagnostic / historical fallback",
        "manual review status: required",
        "auto-merge status: disabled",
        "ordinary default-on weekly no-eligible observation: PASS",
        "workflow deletion status: obsolete Legacy First API Canary Run retired",
        "Do not call scripts/openai_lab_run.py canonical.",
        "Do not reintroduce a weekly legacy override without an explicit rollback PR.",
        "Do not describe legacy fallback removal as approved before the explicit legacy fallback removal gate passes.",
    ], "canonical status drift doc")

    for name in ["readme", "current_path", "evidence_guide", "weekly_automation", "operator_runbook", "drift_check"]:
        require_marker_pair(docs[name], name)

    for name in ["readme", "current_path", "evidence_guide", "weekly_automation", "operator_runbook", "workflow_family_map", "cleanup_inventory"]:
        require_all(docs[name], LEGACY_SCRIPT_TEXT, name)

    for name in ["current_path", "weekly_automation", "operator_runbook", "workflow_family_map", "drift_check"]:
        require_all(docs[name], FIXED_WEEKLY_TEXT, name)

    require_all(docs["weekly_automation"], [
        "Weekly Auto Run no longer has a legacy API/SDK branch.",
        "scripts/run_codex_selected_prompt.sh",
        "ordinary default-on weekly no-eligible observation: PASS",
        "support unlock file: data/support-unlocks/2026-W20.json",
        "vote summary PR: #333",
        "implementation-agent attempt: none",
    ], "weekly automation fixed status")

    require_all(docs["operator_runbook"], [
        "Do not remove `scripts/openai_lab_run.py` during ordinary cleanup.",
        "Do not reintroduce a weekly legacy override during cleanup.",
        "manual review remains required",
        "auto-merge remains disabled",
    ], "operator runbook fixed status")

    require_all(docs["workflow_family_map"], [
        "Retired legacy workflow",
        ".github/workflows/first-canary-run.yml",
        "scripts/create_first_canary_candidate.py",
        "removed in the cleanup PR",
        "Generated snapshots intentionally untouched: true",
    ], "workflow family cleanup record")

    require_all(docs["cleanup_inventory"], [
        "Retired legacy first API canary workflow",
        ".github/workflows/first-canary-run.yml",
        "scripts/create_first_canary_candidate.py",
        "Do not delete protected public evidence casually.",
    ], "cleanup inventory retired workflow record")

    reject_all(all_text, FORBIDDEN_PHRASES, "canonical status docs")

    print("canonical status drift test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
