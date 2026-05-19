#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "repository-cleanup-inventory.md"
README = ROOT / "docs" / "README.md"
POLICY = ROOT / "docs" / "repository-5s-and-language-policy.md"

REMOVED_LEGACY_LAUNCH_FILES = [
    ROOT / ".github" / "workflows" / "first-canary-run.yml",
    ROOT / "scripts" / "create_first_canary_candidate.py",
]

REQUIRED_DOC_TEXT = [
    "# Repository cleanup inventory",
    "It is intentionally conservative.",
    "No file should be deleted only because it looks old.",
    "Protected evidence",
    "Canonical active",
    "Legacy script",
    "Historical archive evidence",
    "Generated snapshot",
    "Retired legacy launch scaffolding",
    "Cleanup candidate",
    "Not-yet-removable",
    "They should not be deleted in cleanup PRs:",
    "scripts/run_codex_selected_prompt.sh",
    ".github/workflows/codex-selected-prompt-run.yml",
    "scripts/openai_lab_run.py",
    "Keep until a separate legacy-removal gate explicitly removes it",
    "Weekly Auto Run no longer has a legacy API/SDK branch.",
    "Do not reintroduce a weekly legacy override during cleanup.",
    "## Retired legacy first API canary workflow",
    ".github/workflows/first-canary-run.yml",
    "scripts/create_first_canary_candidate.py",
    "protected evidence removed: no",
    "generated snapshots touched: no",
    "run records touched: no",
    "protected evidence check: PASS",
    "canonical/legacy check: not canonical, not active weekly path",
    "generated snapshot check: untouched",
    "rollback path: restore from git history only through explicit rollback PR",
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
    "Legacy script removal gate in `docs/workflow-family-map.md` passes and a separate PR updates docs/tests",
    "Protected evidence check:",
    "Canonical/legacy check:",
    "Generated snapshot check:",
    "Removal gate:",
    "Rollback path:",
    "Keep scripts/openai_lab_run.py labeled as non-canonical manual diagnostic / historical fallback.",
    "Avoid deleting protected evidence, generated snapshots, run records, or fallback code without a separate removal gate.",
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
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true",
]


def require_all(text: str, required: list[str], label: str) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing {label} text: {missing}")


def reject_all(text: str, forbidden: list[str], label: str) -> None:
    found = [item for item in forbidden if item.lower() in text.lower()]
    if found:
        raise SystemExit(f"Forbidden {label} text found: {found}")


def require_removed_legacy_launch_files() -> None:
    existing = [str(path.relative_to(ROOT)) for path in REMOVED_LEGACY_LAUNCH_FILES if path.exists()]
    if existing:
        raise SystemExit(f"Retired legacy launch files still exist: {existing}")


def main() -> int:
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    policy = POLICY.read_text(encoding="utf-8")

    require_all(doc, REQUIRED_DOC_TEXT, "repository cleanup inventory")
    reject_all(doc, FORBIDDEN_DOC_TEXT, "repository cleanup inventory")
    require_all(readme, REQUIRED_README_TEXT, "docs README")
    require_all(policy, REQUIRED_POLICY_TEXT, "repository 5S policy")
    require_removed_legacy_launch_files()

    if doc.index("## Protected evidence") > doc.index("## Canonical active surfaces"):
        raise SystemExit("protected evidence should be listed before active surfaces")
    if doc.index("## Canonical active surfaces") > doc.index("## Legacy script surfaces"):
        raise SystemExit("legacy script should follow canonical active surfaces")
    if doc.index("## Legacy script surfaces") > doc.index("## Retired legacy first API canary workflow"):
        raise SystemExit("retired legacy workflow should follow legacy script surfaces")
    if doc.index("## Retired legacy first API canary workflow") > doc.index("## Historical archive evidence"):
        raise SystemExit("historical archive evidence should follow retired legacy workflow")
    if doc.index("## Cleanup candidates") > doc.index("## Not-yet-removable items"):
        raise SystemExit("not-yet-removable items should follow cleanup candidates")

    print("repository cleanup inventory test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
