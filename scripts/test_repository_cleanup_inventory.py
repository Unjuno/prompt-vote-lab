#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "repository-cleanup-inventory.md"
README = ROOT / "docs" / "README.md"
POLICY = ROOT / "docs" / "repository-5s-and-language-policy.md"

REQUIRED_DOC_TEXT = [
    "# Repository cleanup inventory",
    "It is intentionally conservative.",
    "No file should be deleted only because it looks old.",
    "Protected evidence",
    "Canonical active",
    "Legacy fallback",
    "Historical archive evidence",
    "Generated snapshot",
    "Cleanup candidate",
    "Not-yet-removable",
    "They should not be deleted in cleanup PRs:",
    "scripts/run_codex_selected_prompt.sh",
    ".github/workflows/codex-selected-prompt-run.yml",
    "scripts/openai_lab_run.py",
    "Keep until the release plan explicitly removes it",
    "## Historical archive evidence",
    "Historical archive evidence explains past canary decisions, model-policy transitions, run records, and migration boundaries.",
    "It is not active canonical status.",
    "Canary-era names should be preserved when they identify old evidence:",
    "first-canary",
    "canary-007",
    "canary-008",
    "canary-009",
    "fixed-issue-instruction-canary",
    "Do not rename canary-era evidence just to make it look current.",
    "Do not delete canary-era evidence just because the current canonical runner is different.",
    "Do not cite historical archive evidence as current canonical evidence unless the canonical marker is present.",
    "Historical evidence role:",
    "Current active role, if any:",
    "Canonical status claim: none / explicit marker present",
    "Affected run records:",
    "Affected public docs:",
    "Affected contract tests:",
    "Generated snapshots are not source-of-truth policy.",
    "These are candidates for future cleanup work. They are not deletion instructions.",
    "Protected evidence check:",
    "Canonical/legacy check:",
    "Generated snapshot check:",
    "Removal gate:",
    "Rollback path:",
    "Add a workflow-family map",
    "Avoid deleting evidence or fallback code until a release gate is recorded.",
]

REQUIRED_README_TEXT = [
    "Repository 5S and language policy",
]

REQUIRED_POLICY_TEXT = [
    "Do not delete protected public evidence casually.",
    "If a file is legacy but still needed as a migration fallback, label it as legacy and non-canonical rather than deleting it.",
]

FORBIDDEN_DOC_TEXT = [
    "delete immediately",
    "remove immediately",
    "safe to delete now",
    "auto-delete",
    "bulk delete",
    "rename all canary evidence",
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
    policy = POLICY.read_text(encoding="utf-8")

    require_all(doc, REQUIRED_DOC_TEXT, "repository cleanup inventory")
    reject_all(doc, FORBIDDEN_DOC_TEXT, "repository cleanup inventory")
    require_all(readme, REQUIRED_README_TEXT, "docs README")
    require_all(policy, REQUIRED_POLICY_TEXT, "repository 5S policy")

    if doc.index("## Protected evidence") > doc.index("## Canonical active surfaces"):
        raise SystemExit("protected evidence should be listed before active surfaces")
    if doc.index("## Canonical active surfaces") > doc.index("## Legacy fallback surfaces"):
        raise SystemExit("legacy fallback should follow canonical active surfaces")
    if doc.index("## Legacy fallback surfaces") > doc.index("## Historical archive evidence"):
        raise SystemExit("historical archive evidence should follow legacy fallback surfaces")
    if doc.index("## Cleanup candidates") > doc.index("## Not-yet-removable items"):
        raise SystemExit("not-yet-removable items should follow cleanup candidates")

    print("repository cleanup inventory test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
