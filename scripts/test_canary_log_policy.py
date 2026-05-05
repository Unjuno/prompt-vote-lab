#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "canary-log-policy.md"

REQUIRED_LINES = [
    "Collect thick internal artifacts.",
    "Publish only redacted durable summaries.",
    "Never publish secrets, raw environment dumps, or raw private chain-of-thought.",
    "codex-events.jsonl",
    "codex-last-message.txt",
    "codex-stderr.txt",
    "codex-stdout.txt",
    "git-status-before.txt",
    "git-status-after.txt",
    "git-diff-name-only.txt",
    "git-diff-stat.txt",
    "git-diff.patch",
    "file-hashes-before.json",
    "file-hashes-after.json",
    "check-results.json",
    "failure-summary.json",
    "artifact-manifest.json",
    "tool error excerpts",
    "sandbox errors",
    "command exit codes",
    "API keys",
    "repository secrets",
    "raw environment variables",
    "raw private chain-of-thought",
    "auth_failure",
    "sandbox_failure",
    "invalid_json",
    "forbidden_changed_file",
    "static_site_check_failure",
    "Prompt-design game loop",
]


def main() -> int:
    text = POLICY.read_text(encoding="utf-8")
    missing = [line for line in REQUIRED_LINES if line not in text]
    if missing:
        raise SystemExit("Missing canary log policy lines: " + ", ".join(missing))
    print("canary log policy test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
