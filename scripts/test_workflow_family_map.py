#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "workflow-family-map.md"
README = ROOT / "docs" / "README.md"
INVENTORY = ROOT / "docs" / "repository-cleanup-inventory.md"

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
    "These are candidates for future consolidation. They are not deletion instructions.",
    "A workflow removal PR must state:",
    "Evidence role:",
    "Canonical or legacy role:",
    "Generated snapshot ownership:",
    "Replacement path:",
    "Affected docs:",
    "Affected contract tests:",
    "Rollback path:",
    "Defer workflow deletion until a release readiness record approves it.",
]

REQUIRED_INVENTORY_TEXT = [
    "Add a workflow-family map",
    "Avoid deleting evidence or fallback code until a release gate is recorded.",
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


def main() -> int:
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    inventory = INVENTORY.read_text(encoding="utf-8")

    require_all(doc, REQUIRED_DOC_TEXT, "workflow family map")
    reject_all(doc, FORBIDDEN_DOC_TEXT, "workflow family map")
    require_all(inventory, REQUIRED_INVENTORY_TEXT, "repository cleanup inventory")
    require_all(readme, ["Repository cleanup inventory"], "docs README")

    if doc.index("## Canonical active workflows") > doc.index("## Weekly active workflows"):
        raise SystemExit("canonical workflows should be listed before weekly active workflows")
    if doc.index("## Weekly active workflows") > doc.index("## Public generated snapshot workflows"):
        raise SystemExit("public generated snapshot workflows should follow weekly active workflows")
    if doc.index("## Test and guard workflows") > doc.index("## Canary evidence workflows"):
        raise SystemExit("canary evidence workflows should follow test and guard workflows")
    if doc.index("## Canary evidence workflows") > doc.index("## Canary-era archive boundary"):
        raise SystemExit("canary-era archive boundary should follow canary evidence workflows")
    if doc.index("## Cleanup candidates") > doc.index("## Removal gate for workflows"):
        raise SystemExit("workflow removal gate should follow cleanup candidates")

    print("workflow family map test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
