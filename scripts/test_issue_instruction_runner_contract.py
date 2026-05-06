#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_codex_issue_instruction_canary.sh"
WORKFLOW = ROOT / ".github" / "workflows" / "codex-fixed-issue-instruction-canary-run.yml"

REQUIRED_RUNNER_TEXT = [
    "python scripts/create_codex_issue_instruction_packet.py",
    "ISSUE_JSON_PATH",
    "-v \"$task:/task:ro\"",
    "-v \"$work:/work:rw\"",
    "-v \"$runtime:/codex-runtime:rw\"",
    "-v \"$diag:/diagnostics:rw\"",
    "OPENAI_API_KEY present before login: yes",
    "OPENAI_API_KEY present before codex exec: no",
    "unset OPENAI_API_KEY",
    "task-write-test-exit-code.txt",
    "policy-denied-access.txt",
    "task-file-hashes.json",
    "task-selected-issue.json",
    "task-raw-issue-body.md",
    "task-instruction-brief.md",
    "task-static-ui-v1.0.md",
    "task-agent-run-policy-v1.0.md",
    "--skip-git-repo-check",
    "first-canary-009",
]

REQUIRED_WORKFLOW_TEXT = [
    "name: Codex Fixed Issue Instruction Canary Run",
    "issue_number:",
    "issues: read",
    "CODEX_MODEL: gpt-5.4-nano",
    "RUN_WEEK: first-canary-009",
    "gh issue view \"$ISSUE_NUMBER\"",
    "--json number,title,body,url,author,createdAt",
    "bash scripts/run_codex_issue_instruction_canary.sh",
    "--canary-id first-canary-009",
    "--runner-mode codex-cli-fixed-issue-instruction-packet-container",
    "--sandbox-mode docker-workdir-plus-readonly-issue-instruction-packet",
    "codex-fixed-issue-instruction-canary-diagnostics-",
    "codex-fixed-issue-instruction-canary-public-log-",
    "--retry-policy none",
    "--fallback-policy none",
    "--auto-merge-policy disabled",
]

FORBIDDEN_RUNNER_TEXT = [
    "-v \"$task:/task:rw\"",
    "cat " + "$" + "OPENAI_API_KEY",
    "echo " + "$" + "OPENAI_API_KEY",
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
    runner_text = RUNNER.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")

    require_all(runner_text, REQUIRED_RUNNER_TEXT, "runner")
    reject_all(runner_text, FORBIDDEN_RUNNER_TEXT, "runner")
    require_all(workflow_text, REQUIRED_WORKFLOW_TEXT, "workflow")

    if runner_text.index("codex login --with-api-key") > runner_text.index("unset OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is unset before login, not after login")
    if runner_text.index("unset OPENAI_API_KEY") > runner_text.index("codex exec"):
        raise SystemExit("OPENAI_API_KEY is not unset before codex exec")

    print("fixed Issue instruction runner contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
