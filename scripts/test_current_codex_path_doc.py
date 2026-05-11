#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "current-codex-implementation-path.md"

REQUIRED_TEXT = [
    "The canonical production implementation path for Prompt Vote Lab is now:",
    "Docker-mounted workdir-only + Codex CLI",
    "runner_family: codex-cli-container-agent",
    "runner: codex-cli-policy-enforced-agent-container",
    "runner: codex-cli-selected-prompt-task-packet-container",
    "runner: codex-cli-fixed-issue-instruction-packet-container",
    "model: gpt-5.4-nano",
    "attempts_per_candidate: 1",
    "retry_policy: none",
    "fallback_policy: none",
    "auto_merge_policy: disabled",
    "sandbox_mode: docker-mounted-workdir-only",
    "sandbox_mode: docker-workdir-plus-readonly-task-packet",
    "sandbox_mode: docker-workdir-plus-readonly-issue-instruction-packet",
    "container_work_root: /work",
    "container_runtime_root: /codex-runtime",
    "repo_root_mounted: false",
    "final_writable_files: lab/index.html, lab/style.css, lab/app.js",
    "manual_review: required",
    "The Python SDK / Responses API full-file JSON path is not the canonical production implementation path.",
    "first-canary-005: offline context + JSON full-file replacement -> PASS, now non-canonical",
    "Use this concrete canary workflow to verify the basic canonical boundary:",
    "Codex Policy Agent Canary Run",
    "Do not count `First Canary Run` / Python SDK / Responses API output as the canonical production implementation-agent verification.",
    "Prompt instructions are still used, but they are not treated as enforcement.",
    "Do not merge or report a run as canonical implementation E2E merely because the API/JSON path produced a small valid lab diff.",
]

FORBIDDEN_TEXT = [
    "The current stable production-oriented implementation path remains:",
    "Use `first-canary-005` style execution for routine production-oriented implementation runs.",
    "Use this for routine production-oriented implementation:",
    "008 is not yet the default production-oriented implementation path",
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
