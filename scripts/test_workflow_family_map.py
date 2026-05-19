#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "workflow-family-map.md"
README = ROOT / "docs" / "README.md"
INVENTORY = ROOT / "docs" / "repository-cleanup-inventory.md"

WEAK_CANARY_WORKFLOWS = [
    ROOT / ".github" / "workflows" / "codex-first-canary-run.yml",
    ROOT / ".github" / "workflows" / "codex-isolated-3file-canary-run.yml",
    ROOT / ".github" / "workflows" / "codex-isolated-3file-relaxed-canary-run.yml",
    ROOT / ".github" / "workflows" / "codex-agent-observed-canary-run.yml",
]

REMOVED_LEGACY_LAUNCH_FILES = [
    ROOT / ".github" / "workflows" / "first-canary-run.yml",
    ROOT / "scripts" / "create_first_canary_candidate.py",
]

GATE = "if: vars.ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS == 'true'"

REQUIRED_DOC_TEXT = [
    "# Workflow family map",
    "Canonical active",
    "Weekly active",
    "Public generated snapshot",
    "Safety gate",
    "Canary evidence",
    "Retired legacy workflow",
    "Legacy script",
    "Test and guard",
    "Cleanup candidate",
    ".github/workflows/codex-selected-prompt-run.yml",
    ".github/workflows/weekly-auto-run.yml",
    "fixed-on canonical selected-prompt implementation path",
    "Runner: codex-cli-selected-prompt-container".replace("selected-prompt-container", "selected-prompt-packet-container"),
    "Canonical selected-prompt runner: true",
    ".github/workflows/support-unlock-export.yml",
    ".github/workflows/public-results-export.yml",
    ".github/workflows/issue-safety-scan.yml",
    ".github/workflows/script-check.yml",
    ".github/workflows/codex-first-canary-run.yml",
    ".github/workflows/codex-policy-agent-canary-run.yml",
    ".github/workflows/codex-task-packet-canary-run.yml",
    ".github/workflows/codex-fixed-issue-instruction-canary-run.yml",
    "## Historical weak canary gate",
    "ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS=true",
    "The gate prevents accidental reruns of old workspace-write or relaxed-sandbox experiments without deleting historical evidence surfaces.",
    "## Canary-era archive boundary",
    "Canary-era names are historical evidence labels, not active canonical status claims.",
    "first-canary",
    "canary-007",
    "canary-008",
    "canary-009",
    "fixed-issue-instruction-canary",
    "Do not rename historical evidence to make it look current.",
    "Do not cite canary-era names as canonical selected-prompt status unless the evidence also contains the canonical runner marker.",
    "## Retired legacy workflow",
    ".github/workflows/first-canary-run.yml",
    "scripts/create_first_canary_candidate.py",
    "removed in the cleanup PR: true",
    "protected evidence removed: no",
    "generated snapshots touched: no",
    "run records touched: no",
    "## Legacy script path",
    "scripts/openai_lab_run.py",
    "non-canonical manual diagnostic / historical fallback",
    "Weekly Auto Run no longer has a legacy API/SDK branch.",
    "Do not reintroduce a weekly legacy override during cleanup.",
    "## Legacy script removal gate",
    "It does not remove `scripts/openai_lab_run.py`.",
    "It does not approve deletion by itself.",
    "ordinary default-on weekly no-eligible run observed",
    "vote summary PR created",
    "implementation PR: none for the no-eligible run",
    "no implementation-agent attempt made for the no-eligible run",
    "no Codex/API call made for the no-eligible run",
    "weekly legacy branch absent from Weekly Auto Run",
    "canonical diagnostics artifact remains verified",
    "canonical public bundle artifact remains verified",
    "canonical uploaded bundle verification artifact remains verified",
    "manual review remains required",
    "auto-merge remains disabled",
    "public docs no longer cite legacy script as an active weekly requirement",
    "maintainer explicitly approves removal",
    "Generated snapshots intentionally untouched: true",
    "Failing any condition means the legacy script remains present and non-canonical.",
    "These are candidates for future consolidation. They are not deletion instructions.",
    "A workflow removal PR must state:",
    "Keep scripts/openai_lab_run.py labeled as non-canonical manual diagnostic / historical fallback.",
]

REQUIRED_INVENTORY_TEXT = [
    "Retired legacy first API canary workflow",
    "Do not reintroduce a weekly legacy override during cleanup.",
    "Historical archive evidence",
    "Do not rename canary-era evidence just to make it look current.",
]

FORBIDDEN_DOC_TEXT = [
    "delete immediately",
    "remove immediately",
    "safe to delete now",
    "auto-delete",
    "bulk delete",
    "remove all canary workflows",
    "rename all canary workflows",
    "legacy fallback removal is approved",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true",
    "weekly feature flag alone must not silently spend",
]


def require_all(text: str, required: list[str], label: str) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing {label} text: {missing}")


def reject_all(text: str, forbidden: list[str], label: str) -> None:
    lowered = text.lower()
    found = [item for item in forbidden if item.lower() in lowered]
    if found:
        raise SystemExit(f"Forbidden {label} text found: {found}")


def require_weak_canary_gates() -> None:
    for path in WEAK_CANARY_WORKFLOWS:
        text = path.read_text(encoding="utf-8")
        if GATE not in text:
            raise SystemExit(f"Weak historical canary workflow is not gated: {path.relative_to(ROOT)}")
        if text.index(GATE) > text.index("runs-on: ubuntu-latest"):
            raise SystemExit(f"Weak canary gate must appear before runs-on: {path.relative_to(ROOT)}")


def require_removed_legacy_launch_files() -> None:
    existing = [str(path.relative_to(ROOT)) for path in REMOVED_LEGACY_LAUNCH_FILES if path.exists()]
    if existing:
        raise SystemExit(f"Retired legacy launch files still exist: {existing}")


def main() -> int:
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    inventory = INVENTORY.read_text(encoding="utf-8")

    require_all(doc, REQUIRED_DOC_TEXT, "workflow family map")
    reject_all(doc, FORBIDDEN_DOC_TEXT, "workflow family map")
    require_all(inventory, REQUIRED_INVENTORY_TEXT, "repository cleanup inventory")
    require_all(readme, ["Repository cleanup inventory"], "docs README")
    require_weak_canary_gates()
    require_removed_legacy_launch_files()

    if doc.index("## Canonical active workflows") > doc.index("## Weekly active workflows"):
        raise SystemExit("canonical workflows should be listed before weekly active workflows")
    if doc.index("## Weekly active workflows") > doc.index("## Public generated snapshot workflows"):
        raise SystemExit("public generated snapshot workflows should follow weekly active workflows")
    if doc.index("## Test and guard workflows") > doc.index("## Canary evidence workflows"):
        raise SystemExit("canary evidence workflows should follow test and guard workflows")
    if doc.index("## Canary evidence workflows") > doc.index("## Historical weak canary gate"):
        raise SystemExit("historical weak canary gate should follow canary evidence workflows")
    if doc.index("## Historical weak canary gate") > doc.index("## Canary-era archive boundary"):
        raise SystemExit("canary-era archive boundary should follow weak canary gate")
    if doc.index("## Retired legacy workflow") > doc.index("## Legacy script path"):
        raise SystemExit("legacy script path should follow retired legacy workflow")
    if doc.index("## Legacy script path") > doc.index("## Legacy script removal gate"):
        raise SystemExit("legacy script removal gate should follow legacy script path")
    if doc.index("## Legacy script removal gate") > doc.index("## Cleanup candidates"):
        raise SystemExit("cleanup candidates should follow legacy script removal gate")
    if doc.index("## Cleanup candidates") > doc.index("## Removal gate for workflows"):
        raise SystemExit("workflow removal gate should follow cleanup candidates")

    print("workflow family map test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
