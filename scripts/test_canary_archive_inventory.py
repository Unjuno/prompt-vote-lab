#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "canary-archive-inventory.md"
README = ROOT / "docs" / "README.md"
WORKFLOW_MAP = ROOT / "docs" / "workflow-family-map.md"

REQUIRED_DOC_TEXT = [
    "# Canary archive inventory",
    "This inventory classifies historical canary workflows and canary-era docs before any further cleanup.",
    "It is a deletion-prevention map.",
    "Do not delete historical canary evidence merely because the canonical selected-prompt runner is fixed-on.",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "## Inventory states",
    "Canonical active",
    "Historical gated evidence",
    "Historical evidence",
    "Boundary evidence",
    "Non-canonical compatibility evidence",
    "Cleanup candidate",
    ".github/workflows/codex-selected-prompt-run.yml",
    ".github/workflows/weekly-auto-run.yml",
    ".github/workflows/codex-first-canary-run.yml",
    ".github/workflows/codex-isolated-3file-canary-run.yml",
    ".github/workflows/codex-isolated-3file-relaxed-canary-run.yml",
    ".github/workflows/codex-agent-observed-canary-run.yml",
    ".github/workflows/codex-writeback-canary-run.yml",
    ".github/workflows/codex-offline-json-canary-run.yml",
    ".github/workflows/canary-007-policy-feasibility.yml",
    ".github/workflows/codex-policy-agent-canary-run.yml",
    ".github/workflows/codex-task-packet-canary-run.yml",
    ".github/workflows/codex-fixed-issue-instruction-canary-run.yml",
    "docs/codex-path-005-vs-007.md",
    "docs/canary-007-policy-enforced-agent.md",
    "docs/canary-008-selected-prompt-task-packet.md",
    "docs/canary-009-selected-issue-instructions.md",
    "docs/canary-policy.md",
    "docs/first-canary-readiness.md",
    "docs/first-canary-prompt.md",
    "docs/first-canary-report-template.md",
    "docs/stop-rules.md",
    "docs/pre-api-freeze.md",
    "ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS=true",
    "## Removal gate for historical canary workflows",
    "Protected evidence check:",
    "Generated snapshot check:",
    "Run record check:",
    "Maintainer approval:",
    "Do not delete run records, public bundles, support unlock records, comparison dashboards, or history pages.",
]

REQUIRED_README_TEXT = [
    "[Canary archive inventory](./canary-archive-inventory.md)",
    "historical canary workflows and canary-era docs before further cleanup",
]

REQUIRED_WORKFLOW_MAP_TEXT = [
    "Canary evidence workflows",
    "Historical weak canary gate",
    "Cleanup candidates",
]

FORBIDDEN_DOC_TEXT = [
    "delete all canary workflows",
    "safe to delete historical canary evidence",
    "remove run records",
    "remove public bundles",
    "remove generated snapshots",
    "auto-delete",
]


def require_all(text: str, required: list[str], label: str) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing {label} text: {missing}")


def reject_all(text: str, forbidden: list[str], label: str) -> None:
    found = [item for item in forbidden if item.lower() in text.lower()]
    if found:
        raise SystemExit(f"Forbidden {label} text found: {found}")


def main() -> int:
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    workflow_map = WORKFLOW_MAP.read_text(encoding="utf-8")

    require_all(doc, REQUIRED_DOC_TEXT, "canary archive inventory")
    require_all(readme, REQUIRED_README_TEXT, "docs README")
    require_all(workflow_map, REQUIRED_WORKFLOW_MAP_TEXT, "workflow family map")
    reject_all(doc, FORBIDDEN_DOC_TEXT, "canary archive inventory")

    if doc.index("## Current rule") > doc.index("## Inventory states"):
        raise SystemExit("current rule should appear before inventory states")
    if doc.index("## Inventory states") > doc.index("## Workflow inventory"):
        raise SystemExit("workflow inventory should follow inventory states")
    if doc.index("## Workflow inventory") > doc.index("## Doc inventory"):
        raise SystemExit("doc inventory should follow workflow inventory")
    if doc.index("## Gated weak canary rule") > doc.index("## Removal gate for historical canary workflows"):
        raise SystemExit("removal gate should follow gated weak canary rule")
    if doc.index("## Removal gate for historical canary workflows") > doc.index("## Safe next actions"):
        raise SystemExit("safe next actions should follow removal gate")

    print("canary archive inventory test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
