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
    "ordinary default-on weekly no-eligible observation -> PR #333 -> PASS",
    "canonical weekly fixed-on release -> approved",
    "manual review remains required",
    "auto-merge remains disabled",
    "weekly default status: canonical selected-prompt runner fixed-on",
    "weekly feature flag override: removed",
    "weekly legacy override: removed from Weekly Auto Run",
    "runner: codex-cli-selected-prompt-packet-container",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "## Weekly runner policy",
    "Weekly Auto Run` no longer has a legacy API/SDK branch.",
    "Do not reintroduce a weekly legacy override during cleanup.",
    "## Legacy script status",
    "Do not remove `scripts/openai_lab_run.py` during ordinary cleanup.",
    "status: non-canonical manual diagnostic / historical fallback",
    "weekly reachability: none",
    "canonical evidence status: invalid",
    "Expected no-eligible result:",
    "implementation-agent attempt: none",
    "Expected canonical eligible result:",
    "weekly-selected-prompt-diagnostics-<run_number> artifact is present",
    "weekly-selected-prompt-public-bundles-<run_number> artifact is present",
    "weekly-selected-prompt-uploaded-bundle-verification-<run_number> artifact is present",
    "## Output cap status",
    "The old API-era `MAX_OUTPUT_TOKENS` value is not an active canonical Codex runner control.",
    "output_token_cap_enforced: false",
    "## Cleanup boundary",
    "Do not delete public evidence casually.",
    "A later PR may remove the legacy script only after the explicit removal gate in [Workflow family map](./workflow-family-map.md) passes.",
    "OPENAI_API_KEY present before codex exec: no",
]

WEEKLY_REQUIRED_TEXT = [
    "# Weekly automation",
    "upload canonical weekly diagnostics and public evidence",
    "reverify uploaded canonical public bundles",
    "## Canonical weekly runner status",
    "weekly default status: canonical selected-prompt runner fixed-on",
    "weekly feature flag override: removed",
    "weekly legacy override: removed from Weekly Auto Run",
    "Weekly Auto Run no longer has a legacy API/SDK branch.",
    "scripts/run_codex_selected_prompt.sh",
    "runner: codex-cli-selected-prompt-packet-container",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "## Legacy script status",
    "scripts/openai_lab_run.py: non-canonical manual diagnostic / historical fallback",
    "weekly reachability: none",
    "canonical evidence status: invalid",
    "## Canonical weekly evidence artifacts",
    "weekly-selected-prompt-diagnostics-<run_number>",
    "weekly-selected-prompt-public-bundles-<run_number>",
    "weekly-selected-prompt-uploaded-bundle-verification-<run_number>",
    "public bundle verification: ok",
    "uploaded bundle verification: ok",
    "Gitleaks finding count: 0",
    "repo_root_mounted: false",
    "OPENAI_API_KEY present before codex exec: no",
    "## Observed no-eligible production evidence",
    "ordinary default-on weekly no-eligible observation: PASS",
    "support unlock file: data/support-unlocks/2026-W20.json",
    "vote summary PR: #333",
    "merged run record: runs/week-2026-W20-vote-summary.md",
    "implementation-agent attempt: none",
    "## Default-on release status",
    "The complete release-gate checklist is owned by [Canonical status drift check](./canonical-status-drift-check.md).",
    "weekly canonical fixed-on release: approved",
    "## Cleanup boundary",
    "Do not delete public evidence casually.",
]

DRIFT_REQUIRED_TEXT = [
    "## Required release gate language",
    "manual selected-prompt smoke: PASS",
    "weekly selected-prompt canary with eligible candidate: PASS",
    "weekly diagnostics artifact: present",
    "weekly public bundle artifact: present",
    "weekly uploaded bundle verification artifact: present",
    "bounded lab diff: PASS",
    "ordinary default-on weekly no-eligible observation: PASS",
    "legacy script documented as non-canonical manual diagnostic / historical fallback",
    "obsolete Legacy First API Canary Run workflow retired",
    "manual review remains required",
    "auto-merge remains disabled",
    "weekly canonical fixed-on release: approved",
    "## Required legacy fallback removal gate",
    "The legacy fallback removal gate is a deletion-prevention gate, not a deletion approval by itself.",
    "ordinary default-on weekly no-eligible run observed",
    "vote summary PR created",
    "no implementation-agent attempt made for no-eligible run",
    "no Codex/API call made for no-eligible run",
    "weekly legacy branch absent from Weekly Auto Run",
    "eligible canonical run has selected-prompt canary evidence or a next natural eligible-run observation plan",
    "canonical evidence artifacts remain verified",
    "rollback plan exists",
    "public docs no longer cite legacy script as an active weekly requirement",
    "maintainer explicitly approves removal",
]

FORBIDDEN_TEXT = [
    "legacy `scripts/openai_lab_run.py` path is canonical",
    "auto-merge may be enabled",
    "Still not default-on",
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true",
    "PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false",
    "PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true",
    "safe to delete legacy fallback now",
    "legacy fallback removal is approved",
    "weekly feature-flag canary",
    "operator runbook feature-flag cleanup documented",
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

    if runbook.index("Weekly runner policy") > runbook.index("Legacy script status"):
        raise SystemExit("runbook should define weekly runner policy before legacy script status")

    if runbook.index("Legacy script status") > runbook.index("Manual weekly run verification"):
        raise SystemExit("runbook should define legacy script status before manual verification")

    if runbook.index("Output cap status") > runbook.index("Cleanup boundary"):
        raise SystemExit("runbook cleanup boundary should follow output cap status")

    if weekly.index("Canonical weekly runner status") > weekly.index("Legacy script status"):
        raise SystemExit("weekly doc should define canonical runner status before legacy script status")

    if weekly.index("Canonical weekly evidence artifacts") > weekly.index("Observed no-eligible production evidence"):
        raise SystemExit("weekly doc should define evidence artifacts before observed no-eligible evidence")

    if weekly.index("Default-on release status") > weekly.index("Manual weekly run verification"):
        raise SystemExit("weekly manual verification should follow release status")

    print("weekly operator docs test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
