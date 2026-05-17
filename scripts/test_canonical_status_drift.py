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

LEGACY_REMOVAL_GATE_REQUIRED = [
    "legacy fallback removal status: not approved until the explicit legacy fallback removal gate passes",
    "legacy fallback removal: not approved until the explicit legacy fallback removal gate passes",
    "## Required legacy fallback removal gate",
    "The legacy fallback removal gate is a deletion-prevention gate, not a deletion approval by itself.",
    "ordinary default-on weekly no-eligible run observed",
    "vote summary PR created",
    "no implementation-agent attempt made for no-eligible run",
    "no Codex/API call made for no-eligible run",
    "legacy API/SDK runner not reached for no-eligible run",
    "eligible canonical run has selected-prompt canary evidence or a next natural eligible-run observation plan",
    "canonical evidence artifacts remain verified",
    "rollback plan exists",
    "public docs no longer cite legacy fallback as an active requirement",
    "maintainer explicitly approves removal",
    "Until those conditions are recorded, `scripts/openai_lab_run.py` and related legacy API/SDK references remain present, non-canonical, and gated.",
]

FORBIDDEN_PHRASES = [
    "scripts/openai_lab_run.py path is canonical",
    "scripts/openai_lab_run.py is canonical",
    "openai_lab_run.py is canonical",
    "canonical_selected_prompt_runner: true for scripts/openai_lab_run.py",
    "auto-merge enabled for weekly runs",
    "automatic merge enabled for implementation PRs",
    "canonical weekly default: not default-on",
    "weekly default status: default-off during migration",
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "safe to delete legacy fallback now",
    "remove scripts/openai_lab_run.py now",
    "legacy fallback removal is approved",
]

README_FORBIDDEN_STATUS_DETAILS = [
    "Support Unlock Export -> data/support-unlocks/2026-W19.json",
    "Weekly Auto Run -> runs/week-2026-W19-vote-summary.md",
    "Weekly Auto Run -> run 25858202166",
    "selected Issue #282",
    "summary PR #283",
    "implementation PR #284",
    "artifacts present: diagnostics, public bundle, uploaded bundle verification",
    "Issue safety scan\n→ optional manual rescan",
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

    require_all(docs["readme"], [
        "This README is a navigation entry point, not a release-gate source of truth.",
        "current status contract -> docs/canonical-status-drift-check.md",
        "weekly workflow operation -> docs/weekly-automation.md",
        "maintainer operating procedure -> docs/operator-runbook.md",
        "canonical evidence decision rule -> docs/canonical-runner-evidence-guide.md",
        "Broad default-on canonical weekly execution is approved; manual review remains required and auto-merge remains disabled.",
    ], "README source-of-truth entry status")
    reject_all(docs["readme"], README_FORBIDDEN_STATUS_DETAILS, "README detailed release evidence")

    require_all(docs["drift_check"], [
        "# Canonical status drift check",
        "Stable status contract",
        "## Source-of-truth map",
        "Repository-wide canonical, legacy, default-on, auto-merge, manual-review, and release-gate status",
        "Technical implementation boundary",
        "Participant/reviewer evidence decision rule",
        "Weekly workflow operation",
        "Maintainer operating procedure and stop rules",
        "Cleanup and deletion boundaries",
        "Pointer docs may summarize status, but they should not become a second source of truth for release-gate wording.",
        "legacy fallback status: non-canonical migration fallback",
        "weekly default status: canonical selected-prompt runner default-on",
        "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true",
        "auto-merge status: disabled",
        "manual review status: required",
        "Do not call scripts/openai_lab_run.py canonical.",
        "Do not imply the weekly canonical selected-prompt runner is still default-off.",
        "Do not say auto-merge is enabled.",
        "Do not treat a useful lab diff as sufficient canonical evidence.",
        "Do not describe legacy fallback removal as approved before the explicit legacy fallback removal gate passes.",
        "## Required release gate language",
        "legacy fallback documented as non-canonical",
        "operator runbook feature-flag cleanup documented",
        "weekly canonical default-on release: approved",
        "A PR that changes any canonical/legacy/default status should state:",
    ], "canonical status drift doc")
    require_all(docs["drift_check"], LEGACY_REMOVAL_GATE_REQUIRED, "canonical status drift legacy removal gate")

    require_all(docs["weekly_automation"], [
        "Repository-wide canonical, legacy, default-on, auto-merge, manual-review, and release-gate status is governed by [Canonical status drift check](./canonical-status-drift-check.md).",
        "This page is the weekly workflow operation detail, not a second status source of truth.",
    ], "weekly automation status source pointer")

    require_all(docs["operator_runbook"], [
        "Repository-wide canonical, legacy, default-on, auto-merge, manual-review, and release-gate status is governed by [Canonical status drift check](./canonical-status-drift-check.md).",
        "This runbook is the operating procedure, not a second status source of truth.",
        "Do not remove `scripts/openai_lab_run.py` during ordinary cleanup.",
        "A future legacy fallback removal PR may be opened only after the explicit legacy fallback removal gate in [Workflow family map](./workflow-family-map.md) passes.",
        "If any item is missing, keep the legacy fallback present, non-canonical, and gated.",
    ], "operator runbook status source pointer")

    for name in ["readme", "current_path", "evidence_guide", "weekly_automation", "operator_runbook"]:
        require_marker_pair(docs[name], name)

    for name in ["readme", "current_path", "evidence_guide", "weekly_automation", "operator_runbook", "workflow_family_map"]:
        require_all(docs[name], LEGACY_REQUIRED, name)

    for name in ["current_path", "weekly_automation", "operator_runbook", "drift_check"]:
        require_all(docs[name], DEFAULT_REQUIRED, name)

    require_all(docs["weekly_automation"], [
        "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true",
        "The weekly selected-prompt path now defaults to the canonical Docker/Codex runner:",
        "The complete release-gate checklist is owned by [Canonical status drift check](./canonical-status-drift-check.md).",
        "Weekly workflow default-on release result:",
        "weekly feature-flag canary with eligible candidate: PASS",
        "weekly diagnostics artifact: present",
        "weekly public bundle artifact: present",
        "weekly uploaded bundle verification artifact: present",
        "bounded lab diff: PASS",
        "auto-merge remains disabled",
        "weekly canonical default-on release: approved",
    ], "weekly automation default status")

    require_all(docs["operator_runbook"], [
        "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true",
        "Canonical selected-prompt implementation is verified and default-on for eligible weekly implementation candidates:",
        "legacy runner removal",
        "auto-merge",
        "Default-on means the repository/workflow default now uses the canonical runner unless explicitly overridden for rollback.",
        "Never leave `PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false` unintentionally after a diagnostic run.",
    ], "operator runbook default status")

    require_all(docs["current_path"], [
        "The weekly eligible implementation workflow now uses the canonical selected-prompt path by default.",
        "legacy `openai_lab_run.py` path remains available only as a non-canonical fallback through an explicit rollback override",
        "A non-canonical API/JSON run may be recorded, but it must be labeled non-canonical",
    ], "current path migration status")

    require_all(docs["evidence_guide"], [
        "A run is not canonical merely because it produced a small valid lab diff.",
        "If those lines are missing, treat the run as non-canonical until proven otherwise.",
        "It does not satisfy the selected-prompt canonical runner requirement",
        "The weekly canonical selected-prompt runner is default-on after the release gate passed:",
    ], "evidence guide decision status")

    require_all(docs["workflow_family_map"], [
        "It is non-canonical.",
        "It should not be removed merely because the canonical weekly runner is default-on.",
        "Removal requires a separate legacy-removal gate after ordinary default-on operation is verified.",
        "## Legacy fallback removal gate",
        "It does not approve deletion by itself.",
        "Generated snapshots intentionally untouched: true",
        "Failing any condition means the legacy fallback remains present, non-canonical, and gated.",
        "They are not deletion instructions.",
    ], "workflow family map legacy status")

    require_all(docs["cleanup_inventory"], [
        "Not-yet-removable",
        "scripts/openai_lab_run.py",
        "First ordinary scheduled canonical default-on run is verified, rollback need is reviewed, and a separate legacy-removal PR updates docs/tests",
    ], "cleanup inventory removal gate")

    reject_all(all_text, FORBIDDEN_PHRASES, "canonical status docs")

    print("canonical status drift test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())