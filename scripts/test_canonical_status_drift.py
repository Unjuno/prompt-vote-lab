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

LEGACY_REQUIRED = [
    "scripts/openai_lab_run.py",
    "non-canonical",
]

DEFAULT_REQUIRED = [
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER",
]

FORBIDDEN_PHRASES = [
    "scripts/openai_lab_run.py path is canonical",
    "scripts/openai_lab_run.py is canonical",
    "openai_lab_run.py is canonical",
    "canonical_selected_prompt_runner: true for scripts/openai_lab_run.py",
    "auto-merge enabled for weekly runs",
    "automatic merge enabled for implementation PRs",
    "weekly canonical selected-prompt runner is default-on",
    "canonical weekly default: default-on",
    "safe to delete legacy fallback now",
    "remove scripts/openai_lab_run.py now",
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
    if text.index(CANONICAL_MARKER[0]) > text.index(CANONICAL_MARKER[1]):
        raise SystemExit(f"Canonical marker order is wrong in {label}")


def main() -> int:
    docs = read_docs()
    all_text = "\n".join(docs.values())

    require_all(docs["drift_check"], [
        "# Canonical status drift check",
        "Stable status contract",
        "## Source-of-truth map",
        "Repository-wide canonical, legacy, default-off, auto-merge, manual-review, and release-gate status",
        "Technical implementation boundary",
        "Participant/reviewer evidence decision rule",
        "Weekly workflow operation",
        "Maintainer operating procedure and stop rules",
        "Cleanup and deletion boundaries",
        "Pointer docs may summarize status, but they should not become a second source of truth for release-gate wording.",
        "legacy fallback status: non-canonical migration fallback",
        "weekly default status: default-off during migration",
        "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
        "auto-merge status: disabled",
        "manual review status: required",
        "Do not call scripts/openai_lab_run.py canonical.",
        "Do not imply the weekly canonical selected-prompt runner is already default-on.",
        "Do not say auto-merge is enabled.",
        "Do not treat a useful lab diff as sufficient canonical evidence.",
        "A PR that changes any canonical/legacy/default status should state:",
    ], "canonical status drift doc")

    require_all(docs["weekly_automation"], [
        "Repository-wide canonical, legacy, default-off, auto-merge, manual-review, and release-gate status is governed by [Canonical status drift check](./canonical-status-drift-check.md).",
        "This page is the weekly workflow operation detail, not a second status source of truth.",
    ], "weekly automation status source pointer")

    require_all(docs["operator_runbook"], [
        "Repository-wide canonical, legacy, default-off, auto-merge, manual-review, and release-gate status is governed by [Canonical status drift check](./canonical-status-drift-check.md).",
        "This runbook is the operating procedure, not a second status source of truth.",
    ], "operator runbook status source pointer")

    for name in ["readme", "current_path", "evidence_guide", "weekly_automation", "operator_runbook"]:
        require_marker_pair(docs[name], name)

    for name in ["readme", "current_path", "evidence_guide", "weekly_automation", "operator_runbook", "workflow_family_map"]:
        require_all(docs[name], LEGACY_REQUIRED, name)

    for name in ["current_path", "weekly_automation", "operator_runbook", "drift_check"]:
        require_all(docs[name], DEFAULT_REQUIRED, name)

    require_all(docs["weekly_automation"], [
        "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
        "Still not default-on",
        "legacy fallback documented as non-canonical",
        "auto-merge remains disabled",
    ], "weekly automation default status")

    require_all(docs["operator_runbook"], [
        "Still not default-on",
        "legacy runner removal",
        "auto-merge",
        "Default-on means changing the repository/workflow default",
        "Never leave the canonical weekly runner enabled unintentionally before default-on release approval.",
    ], "operator runbook default status")

    require_all(docs["current_path"], [
        "The weekly eligible implementation workflow has a canonical selected-prompt path behind a default-off feature flag.",
        "legacy `openai_lab_run.py` path remains available only as a non-canonical fallback",
        "A non-canonical API/JSON run may be recorded, but it must be labeled non-canonical",
    ], "current path migration status")

    require_all(docs["evidence_guide"], [
        "A run is not canonical merely because it produced a small valid lab diff.",
        "If those lines are missing, treat the run as non-canonical until proven otherwise.",
        "It does not satisfy the selected-prompt canonical runner requirement",
        "Do not flip the weekly canonical selected-prompt runner to default-on",
    ], "evidence guide decision status")

    require_all(docs["workflow_family_map"], [
        "It is non-canonical.",
        "It should not be removed until the default-on release gate explicitly approves removal.",
        "They are not deletion instructions.",
    ], "workflow family map legacy status")

    require_all(docs["cleanup_inventory"], [
        "Not-yet-removable",
        "scripts/openai_lab_run.py",
        "Broad canonical selected-prompt weekly execution is default-on and verified across normal operation",
    ], "cleanup inventory removal gate")

    reject_all(all_text, FORBIDDEN_PHRASES, "canonical status docs")

    print("canonical status drift test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
