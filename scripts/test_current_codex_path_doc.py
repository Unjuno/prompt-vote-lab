#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "current-codex-implementation-path.md"

REQUIRED_TEXT = [
    "The canonical production implementation path for Prompt Vote Lab is:",
    "Docker-mounted workdir-only + Codex CLI + selected-prompt task packet",
    "runner_family: codex-cli-container-agent",
    "runner: codex-cli-selected-prompt-packet-container",
    "model: gpt-5.4-nano",
    "attempts_per_candidate: 1",
    "retry_policy: none",
    "fallback_policy: none",
    "auto_merge_policy: disabled",
    "sandbox_mode: docker-workdir-plus-readonly-selected-prompt-packet",
    "repo_root_mounted: false",
    "final_writable_files: lab/index.html, lab/style.css, lab/app.js",
    "manual_review: required",
    "weekly default status: canonical selected-prompt runner fixed-on",
    "weekly feature flag override: removed",
    "weekly legacy override: removed from Weekly Auto Run",
    "Weekly Auto Run no longer has a legacy branch.",
    "scripts/run_codex_selected_prompt.sh",
    "prompt_transport: --prompt-file",
    "summary_pr: #283",
    "implementation_pr: #284",
    "selected_issue: #282",
    "weekly-selected-prompt-diagnostics-7",
    "weekly-selected-prompt-public-bundles-7",
    "weekly-selected-prompt-uploaded-bundle-verification-7",
    "support unlock file: data/support-unlocks/2026-W20.json",
    "vote summary PR: #333",
    "merged run record: runs/week-2026-W20-vote-summary.md",
    "implementation-agent attempt: none",
    "## Non-canonical legacy script",
    "scripts/openai_lab_run.py",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "removed workflow: .github/workflows/first-canary-run.yml",
    "removed helper: scripts/create_first_canary_candidate.py",
]

FORBIDDEN_TEXT = [
    "default-off feature flag",
    "still contains a non-canonical branch",
]


def main() -> int:
    text = DOC.read_text(encoding="utf-8")
    missing = [item for item in REQUIRED_TEXT if item not in text]
    if missing:
        raise SystemExit("Missing current Codex path doc text: " + ", ".join(missing))
    forbidden = [item for item in FORBIDDEN_TEXT if item in text]
    if forbidden:
        raise SystemExit("Forbidden outdated current Codex path doc text: " + ", ".join(forbidden))
    print("current Codex implementation path doc test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
