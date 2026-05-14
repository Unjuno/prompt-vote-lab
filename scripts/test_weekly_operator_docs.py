#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "operator-runbook.md"
WEEKLY = ROOT / "docs" / "weekly-automation.md"
DRIFT = ROOT / "docs" / "canonical-status-drift-check.md"

RUNBOOK_REQUIRED_TEXT = [
    "# Operator runbook",
    "manual selected-prompt workflow smoke -> PASS",
    "weekly canonical selected-prompt canary -> run 25858202166 -> PASS",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true",
    "runner: codex-cli-selected-prompt-packet-container",
    "weekly-selected-prompt-diagnostics-7",
    "weekly-selected-prompt-public-bundles-7",
    "weekly-selected-prompt-uploaded-bundle-verification-7",
    "## Canonical weekly feature flag policy",
    "The legacy `scripts/openai_lab_run.py` path is non-canonical.",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "## Temporary canary variable policy",
    "PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0",
    "PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=20 or unset",
    "Never leave `PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0` after a canary.",
    "## Default-on release gate",
    "The complete release-gate checklist is owned by [Canonical status drift check](./canonical-status-drift-check.md).",
    "Operator stop rule before default-on:",
    "operator runbook feature-flag cleanup documented",
    "manual review remains required",
    "auto-merge remains disabled",
    "Expected canonical eligible result when the canonical feature flag is deliberately enabled:",
    "canonical evidence artifacts are missing for a canonical run",
    "OPENAI_API_KEY present before codex exec: no",
]

WEEKLY_REQUIRED_TEXT = [
    "# Weekly automation",
    "upload canonical weekly diagnostics and public evidence when the canonical feature flag is enabled",
    "reverify uploaded canonical public bundles",
    "## Canonical selected-prompt feature flag",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER",
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "scripts/run_codex_selected_prompt.sh",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "The legacy `scripts/openai_lab_run.py` path is non-canonical",
    "## Canonical weekly evidence artifacts",
    "weekly-selected-prompt-diagnostics-<run_number>",
    "weekly-selected-prompt-public-bundles-<run_number>",
    "weekly-selected-prompt-uploaded-bundle-verification-<run_number>",
    "public bundle verification: ok",
    "uploaded bundle verification: ok",
    "Gitleaks finding count: 0",
    "repo_root_mounted: false",
    "OPENAI_API_KEY present before codex exec: no",
    "## Temporary canary settings",
    "PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0",
    "PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=20 or unset",
    "Leaving `PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0` changes selection behavior",
    "Verified canonical weekly selected-prompt canary evidence:",
    "run: 25858202166",
    "selected Issue: #282",
    "summary PR: #283",
    "implementation PR: #284",
    "bounded lab diff: PASS",
    "auto-merge: disabled",
    "## Default-on release gate",
    "The complete release-gate checklist is owned by [Canonical status drift check](./canonical-status-drift-check.md).",
    "Weekly workflow stop rule before default-on:",
    "weekly feature-flag canary with eligible candidate: PASS",
    "weekly diagnostics artifact: present",
    "weekly public bundle artifact: present",
    "weekly uploaded bundle verification artifact: present",
    "bounded lab diff: PASS",
    "manual review remains required",
    "auto-merge remains disabled",
]

DRIFT_REQUIRED_TEXT = [
    "## Required release gate language",
    "manual selected-prompt smoke: PASS",
    "weekly feature-flag canary with eligible candidate: PASS",
    "weekly diagnostics artifact: present",
    "weekly public bundle artifact: present",
    "weekly uploaded bundle verification artifact: present",
    "bounded lab diff: PASS",
    "legacy fallback documented as non-canonical",
    "manual review remains required",
    "auto-merge remains disabled",
]

FORBIDDEN_TEXT = [
    "eligible prompt -> implementation-agent preflight -> implementation-agent run -> lab-only implementation PR\n```\n\n## Weekly operating loop",
    "implementation-agent PR generation still needs a live eligible-candidate E2E verification",
    "legacy `scripts/openai_lab_run.py` path is canonical",
    "auto-merge may be enabled",
    "PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0 is acceptable for normal scheduled operation",
]

RUNBOOK_RELEASE_GATE_FORBIDDEN_TEXT = [
    "Do not make the canonical weekly runner default-on until all of these are true:\n\n```text\nmanual selected-prompt smoke: PASS",
]

WEEKLY_RELEASE_GATE_FORBIDDEN_TEXT = [
    "Do not make the canonical selected-prompt runner the weekly default until all of these remain true:\n\n```text\nmanual selected-prompt smoke: PASS",
    "participant evidence guide published\noperator runbook feature-flag cleanup documented",
]


def require_all(text: str, required: list[str], label: str) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing {label} text: {missing}")


def reject_all(text: str, forbidden: list[str], label: str) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"Forbidden {label} text found: {found}")


def main() -> int:
    runbook = RUNBOOK.read_text(encoding="utf-8")
    weekly = WEEKLY.read_text(encoding="utf-8")
    drift = DRIFT.read_text(encoding="utf-8")

    require_all(runbook, RUNBOOK_REQUIRED_TEXT, "operator runbook")
    require_all(weekly, WEEKLY_REQUIRED_TEXT, "weekly automation doc")
    require_all(drift, DRIFT_REQUIRED_TEXT, "canonical status drift release gate")
    reject_all(runbook, FORBIDDEN_TEXT, "operator runbook")
    reject_all(weekly, FORBIDDEN_TEXT, "weekly automation doc")
    reject_all(runbook, RUNBOOK_RELEASE_GATE_FORBIDDEN_TEXT, "operator runbook release gate duplication")
    reject_all(weekly, WEEKLY_RELEASE_GATE_FORBIDDEN_TEXT, "weekly automation release gate duplication")

    if runbook.index("Canonical weekly feature flag policy") > runbook.index("Temporary canary variable policy"):
        raise SystemExit("runbook should define the feature flag before cleanup policy")

    if runbook.index("Temporary canary variable policy") > runbook.index("Default-on release gate"):
        raise SystemExit("runbook cleanup policy should precede the default-on gate")

    if weekly.index("Canonical selected-prompt feature flag") > weekly.index("Canonical weekly evidence artifacts"):
        raise SystemExit("weekly doc should define the feature flag before evidence artifacts")

    if weekly.index("Temporary canary settings") > weekly.index("Manual verification"):
        raise SystemExit("weekly doc should define canary cleanup before manual verification")

    if weekly.index("Merge policy") > weekly.index("Default-on release gate"):
        raise SystemExit("weekly merge policy should precede the default-on gate")

    print("weekly operator docs test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
