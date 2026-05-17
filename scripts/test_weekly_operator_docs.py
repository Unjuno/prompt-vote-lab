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
    "canonical weekly default-on release -> approved",
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true",
    "runner: codex-cli-selected-prompt-packet-container",
    "weekly-selected-prompt-diagnostics-7",
    "weekly-selected-prompt-public-bundles-7",
    "weekly-selected-prompt-uploaded-bundle-verification-7",
    "## Canonical weekly default policy",
    "The legacy `scripts/openai_lab_run.py` path is non-canonical.",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true",
    "For ordinary `week-*` runs, `PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false` alone must not spend a legacy API/SDK attempt.",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "## Temporary override policy",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true or unset",
    "PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN unset",
    "Never leave `PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true` after a diagnostic run.",
    "PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0",
    "PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=20 or unset",
    "Never leave `PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0` after a canary.",
    "Never leave `PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false` unintentionally after a diagnostic run.",
    "## Default-on release status",
    "The complete release-gate checklist is owned by [Canonical status drift check](./canonical-status-drift-check.md).",
    "Operator release result:",
    "operator runbook feature-flag cleanup documented",
    "manual review remains required",
    "auto-merge remains disabled",
    "weekly canonical default-on release: approved",
    "Expected canonical eligible result under the default runner:",
    "Expected legacy diagnostic result only when both overrides are intentionally set:",
    "legacy API/SDK runner refused",
    "## Output cap status",
    "The old API-era `MAX_OUTPUT_TOKENS` value is not an active canonical Codex runner control.",
    "output_token_cap_enforced: false",
    "## Legacy fallback removal gate",
    "Do not remove `scripts/openai_lab_run.py` during ordinary cleanup.",
    "A future legacy fallback removal PR may be opened only after the explicit legacy fallback removal gate in [Workflow family map](./workflow-family-map.md) passes.",
    "ordinary default-on weekly no-eligible run observed",
    "vote summary PR created",
    "implementation PR: none for the no-eligible run",
    "no implementation-agent attempt made for the no-eligible run",
    "no Codex/API call made for the no-eligible run",
    "legacy API/SDK runner not reached for the no-eligible run",
    "eligible canonical run has selected-prompt canary evidence or a next natural eligible-run observation plan",
    "canonical evidence artifacts remain verified",
    "manual review remains required",
    "auto-merge remains disabled",
    "rollback plan exists",
    "maintainer explicitly approves removal",
    "If any item is missing, keep the legacy fallback present, non-canonical, and gated.",
    "canonical evidence artifacts are missing for a canonical run",
    "OPENAI_API_KEY present before codex exec: no",
]

WEEKLY_REQUIRED_TEXT = [
    "# Weekly automation",
    "upload canonical weekly diagnostics and public evidence for canonical runs",
    "reverify uploaded canonical public bundles",
    "## Canonical selected-prompt default",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER",
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true",
    "scripts/run_codex_selected_prompt.sh",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "The legacy `scripts/openai_lab_run.py` path is non-canonical",
    "When the variable is explicitly set to `false`, `Weekly Auto Run` can reach the legacy fallback path for emergency rollback or controlled diagnosis only.",
    "That feature flag alone must not silently authorize a legacy API/SDK attempt.",
    "PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true",
    "Leaving `PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true` is not acceptable for normal scheduled operation.",
    "## Canonical weekly evidence artifacts",
    "weekly-selected-prompt-diagnostics-<run_number>",
    "weekly-selected-prompt-public-bundles-<run_number>",
    "weekly-selected-prompt-uploaded-bundle-verification-<run_number>",
    "public bundle verification: ok",
    "uploaded bundle verification: ok",
    "Gitleaks finding count: 0",
    "repo_root_mounted: false",
    "OPENAI_API_KEY present before codex exec: no",
    "## Override and rollback settings",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true or unset",
    "PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN unset",
    "PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0",
    "PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=20 or unset",
    "Leaving `PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0` changes selection behavior",
    "may reach the legacy fallback only through an explicit rollback override plus `PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true`",
    "Verified canonical weekly selected-prompt canary evidence:",
    "run: 25858202166",
    "selected Issue: #282",
    "summary PR: #283",
    "implementation PR: #284",
    "bounded lab diff: PASS",
    "auto-merge: disabled",
    "## Default-on release status",
    "The complete release-gate checklist is owned by [Canonical status drift check](./canonical-status-drift-check.md).",
    "Weekly workflow default-on release result:",
    "weekly feature-flag canary with eligible candidate: PASS",
    "weekly diagnostics artifact: present",
    "weekly public bundle artifact: present",
    "weekly uploaded bundle verification artifact: present",
    "bounded lab diff: PASS",
    "manual review remains required",
    "auto-merge remains disabled",
    "weekly canonical default-on release: approved",
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
    "operator runbook feature-flag cleanup documented",
    "manual review remains required",
    "auto-merge remains disabled",
    "weekly canonical default-on release: approved",
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
]

FORBIDDEN_TEXT = [
    "eligible prompt -> implementation-agent preflight -> implementation-agent run -> lab-only implementation PR\n```\n\n## Weekly operating loop",
    "implementation-agent PR generation still needs a live eligible-candidate E2E verification",
    "legacy `scripts/openai_lab_run.py` path is canonical",
    "auto-merge may be enabled",
    "PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0 is acceptable for normal scheduled operation",
    "Still not default-on",
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "MAX_OUTPUT_TOKENS remains at the current configured limit until the system is complete.",
    "safe to delete legacy fallback now",
    "legacy fallback removal is approved",
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
    reject_all(drift, FORBIDDEN_TEXT, "canonical status drift doc")
    reject_all(runbook, RUNBOOK_RELEASE_GATE_FORBIDDEN_TEXT, "operator runbook release gate duplication")
    reject_all(weekly, WEEKLY_RELEASE_GATE_FORBIDDEN_TEXT, "weekly automation release gate duplication")

    if runbook.index("Canonical weekly default policy") > runbook.index("Temporary override policy"):
        raise SystemExit("runbook should define the default policy before override policy")

    if runbook.index("Temporary override policy") > runbook.index("Default-on release status"):
        raise SystemExit("runbook override policy should precede the default-on release status")

    if runbook.index("Output cap status") > runbook.index("Legacy fallback removal gate"):
        raise SystemExit("runbook legacy fallback removal gate should follow output cap status")

    if runbook.index("Legacy fallback removal gate") > runbook.index("Reset and cleanup policy"):
        raise SystemExit("runbook cleanup policy should follow legacy fallback removal gate")

    if weekly.index("Canonical selected-prompt default") > weekly.index("Canonical weekly evidence artifacts"):
        raise SystemExit("weekly doc should define the default before evidence artifacts")

    if weekly.index("Override and rollback settings") > weekly.index("Manual verification"):
        raise SystemExit("weekly doc should define rollback cleanup before manual verification")

    if weekly.index("Merge policy") > weekly.index("Default-on release status"):
        raise SystemExit("weekly merge policy should precede the default-on release status")

    print("weekly operator docs test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())