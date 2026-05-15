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

GATE = "if: vars.ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS == 'true'"

REQUIRED_DOC_TEXT = [
    "# Workflow family map",
    "It is not a removal plan.",
    "Canonical active",
    "Weekly active",
    "Public generated snapshot",
    "Safety gate",
    "Canary evidence",
    "Legacy fallback",
    "Test and guard",
    "Cleanup candidate",
    ".github/workflows/codex-selected-prompt-run.yml",
    ".github/workflows/weekly-auto-run.yml",
    "default-on canonical selected-prompt implementation path",
    "Runner: codex-cli-selected-prompt-packet-container",
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
    "The gate does not apply to the current canonical selected-prompt path:",
    "## Canary-era archive boundary",
    "Canary-era names are historical evidence labels, not active canonical status claims.",
    "first-canary",
    "canary-007",
    "canary-008",
    "canary-009",
    "fixed-issue-instruction-canary",
    "Do not rename historical evidence to make it look current.",
    "Do not cite canary-era names as canonical selected-prompt status unless the evidence also contains the canonical runner marker.",
    "Historical evidence role:",
    "Current active role, if any:",
    "Canonical status claim: none / explicit marker present",
    "Affected run records:",
    "Replacement evidence path:",
    "scripts/openai_lab_run.py",
    "It is non-canonical.",
    "It should not be removed merely because the canonical weekly runner is default-on.",
    "Removal requires a separate legacy-removal gate after ordinary default-on operation is verified.",
    "These are candidates for future consolidation. They are not deletion instructions.",
    "A workflow removal PR must state:",
    "Evidence role:",
    "Canonical or legacy role:",
    "Generated snapshot ownership:",
    "Replacement path:",
    "Affected docs:",
    "Affected contract tests:",
    "Rollback path:",
    "Keep weak historical canary workflows gated unless a maintainer intentionally enables ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS=true.",
    "Defer legacy fallback removal until a separate legacy-removal gate exists.",
]

REQUIRED_INVENTORY_TEXT = [
    "Verify the first ordinary scheduled canonical default-on weekly run.",
    "Avoid deleting evidence or fallback code until a separate legacy-removal gate is recorded.",
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


def main() -> int:
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    inventory = INVENTORY.read_text(encoding="utf-8")

    require_all(doc, REQUIRED_DOC_TEXT, "workflow family map")
    reject_all(doc, FORBIDDEN_DOC_TEXT, "workflow family map")
    require_all(inventory, REQUIRED_INVENTORY_TEXT, "repository cleanup inventory")
    require_all(readme, ["Repository cleanup inventory"], "docs README")
    require_weak_canary_gates()

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
    if doc.index("## Cleanup candidates") > doc.index("## Removal gate for workflows"):
        raise SystemExit("workflow removal gate should follow cleanup candidates")

    print("workflow family map test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())