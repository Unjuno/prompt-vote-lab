#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "current-codex-implementation-path.md"

REQUIRED_TEXT = [
    "first-canary-005: offline context + JSON full-file replacement",
    "first-canary-007: policy-enforced agent container",
    "runner: codex-cli-offline-json-writeback",
    "runner: codex-cli-policy-enforced-agent-container",
    "model: gpt-5.4-nano",
    "attempts_per_candidate: 1",
    "retry_policy: none",
    "fallback_policy: none",
    "auto_merge_policy: disabled",
    "sandbox_mode: read-only-empty-context",
    "sandbox_mode: docker-mounted-workdir-only",
    "writeback_mode: validated JSON full-file replacement",
    "repo_root_mounted: false",
    "lab/index.html",
    "lab/style.css",
    "lab/app.js",
    "manual_review: required",
    "Prompt instructions are still used, but they are not treated as enforcement.",
    "first-canary-006: isolated three-file agent-observed direct edit -> PASS",
    "first-canary-007: Docker-mounted workdir-only policy agent -> PASS",
    "007 may be promoted from candidate to standard agent path after at least 2 consecutive successful full 007 runs",
    "Do not give Codex a repository working tree if the intended protocol is purely mediated output.",
]


def main() -> int:
    text = DOC.read_text(encoding="utf-8")
    missing = [item for item in REQUIRED_TEXT if item not in text]
    if missing:
        raise SystemExit("Missing current Codex path doc text: " + ", ".join(missing))
    print("current Codex implementation path doc test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
