#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "local-release-verification.md"
README = ROOT / "docs" / "README.md"

REQUIRED_DOC_TEXT = [
    "# Local release verification",
    "Local verification is not a replacement for GitHub Actions, GitHub Pages smoke checks, weekly workflow evidence, or manual review.",
    "Local pass is necessary but not sufficient.",
    "GitHub Actions pass is required.",
    "GitHub Pages public rendering must be checked.",
    "Manual review remains required.",
    "Auto-merge remains disabled.",
    "git clone https://github.com/Unjuno/prompt-vote-lab.git",
    "git pull --ff-only origin main",
    "nothing to commit, working tree clean",
    "python -m py_compile",
    "node --check",
    "bash -n",
    "python scripts/test_canonical_status_drift.py",
    "python scripts/test_current_codex_path_doc.py",
    "python scripts/test_canonical_runner_evidence_guide.py",
    "python scripts/test_repository_cleanup_inventory.py",
    "python scripts/test_workflow_family_map.py",
    "python scripts/test_canary_archive_inventory.py",
    "python scripts/test_weekly_operator_docs.py",
    "python scripts/test_local_release_verification.py",
    "python scripts/test_script_check_workflow_contract.py",
    "python -m http.server 8000",
    "http://localhost:8000/",
    "http://localhost:8000/lab/",
    "Where do I submit a prompt?",
    "Where do I vote?",
    "What does 👍 mean?",
    "What is the no-change baseline?",
    "Where is the canonical status contract?",
    "Where is the weekly automation runbook?",
    "Where is the selected-prompt evidence guide?",
    "Pre-API Freeze Audit: success",
    "Static Site Check: success",
    "Lab PR Scope Check: success",
    "Script Check: success",
    "https://unjuno.github.io/prompt-vote-lab/",
    "https://unjuno.github.io/prompt-vote-lab/lab/",
    "Soft release is acceptable when:",
    "Public release should wait until:",
    "Do not release if any of these are true:",
    "working tree is dirty",
    "GitHub Actions fail",
    "legacy script is described as canonical",
    "protected evidence, run records, generated snapshots, or history pages were deleted without a gate",
]

REQUIRED_README_TEXT = [
    "[Local release verification](./local-release-verification.md)",
    "local clone, contract checks, GitHub Actions, GitHub Pages, and soft-release gate",
]

FORBIDDEN_DOC_TEXT = [
    "local pass is sufficient",
    "skip GitHub Actions",
    "skip GitHub Pages",
    "enable auto-merge",
    "auto-merge may be enabled",
    "release from a dirty working tree",
    "legacy script is canonical",
    "delete run records before release",
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

    require_all(doc, REQUIRED_DOC_TEXT, "local release verification doc")
    require_all(readme, REQUIRED_README_TEXT, "docs README")
    reject_all(doc, FORBIDDEN_DOC_TEXT, "local release verification doc")

    if doc.index("## Clone or refresh") > doc.index("## Runtime prerequisites"):
        raise SystemExit("runtime prerequisites should follow clone or refresh")
    if doc.index("## Runtime prerequisites") > doc.index("## Local syntax checks"):
        raise SystemExit("local syntax checks should follow runtime prerequisites")
    if doc.index("## Local syntax checks") > doc.index("## Required local contract checks"):
        raise SystemExit("contract checks should follow syntax checks")
    if doc.index("## Required local contract checks") > doc.index("## Static page preview"):
        raise SystemExit("static page preview should follow contract checks")
    if doc.index("## Static page preview") > doc.index("## Participant route check"):
        raise SystemExit("participant route check should follow static page preview")
    if doc.index("## Participant route check") > doc.index("## Operator route check"):
        raise SystemExit("operator route check should follow participant route check")
    if doc.index("## Operator route check") > doc.index("## GitHub Actions requirement"):
        raise SystemExit("GitHub Actions requirement should follow operator route check")
    if doc.index("## GitHub Actions requirement") > doc.index("## GitHub Pages requirement"):
        raise SystemExit("GitHub Pages requirement should follow GitHub Actions requirement")
    if doc.index("## GitHub Pages requirement") > doc.index("## Soft release versus public release"):
        raise SystemExit("soft/public release rule should follow GitHub Pages requirement")
    if doc.index("## Soft release versus public release") > doc.index("## Release blockers"):
        raise SystemExit("release blockers should follow soft/public release rule")

    print("local release verification test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
