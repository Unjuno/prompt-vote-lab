#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "codex-comparison-issue-run.yml"

REQUIRED_TEXT = [
    "name: Codex Comparison Issue Run",
    "workflow_dispatch:",
    "issue_comment:",
    "types: [created]",
    "push:",
    "pull_request:",
    "branches:",
    "- main",
    "paths:",
    "run-requests/comparison/*.json",
    "week_id:",
    "base_sha:",
    "issue_number:",
    "candidate_rank:",
    "vote_count:",
    "startsWith(github.event.comment.body, '/run-comparison ')",
    "github.event_name == 'push'",
    "github.event_name == 'pull_request'",
    "github.event.pull_request.head.repo.full_name == github.repository",
    "Checkout workflow source",
    "Resolve comparison inputs",
    "COMMENT_BODY: ${{ github.event.comment.body }}",
    "COMMENT_ISSUE_NUMBER: ${{ github.event.issue.number }}",
    "PUSH_BEFORE: ${{ github.event.before }}",
    "PUSH_SHA: ${{ github.sha }}",
    "PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}",
    "PR_HEAD_SHA: ${{ github.event.pull_request.head.sha }}",
    "week|base|rank|votes",
    "missing comparison command keys",
    "git', 'diff', '--name-only', before, after, '--', 'run-requests/comparison/*.json'",
    "git', 'diff', '--name-only', base, head, '--', 'run-requests/comparison/*.json'",
    "exactly one comparison request JSON is required",
    "missing comparison request keys",
    "week_id",
    "base_sha",
    "issue_number",
    "candidate_rank",
    "vote_count",
    "RUN_WEEK=",
    "BASE_SHA=",
    "ISSUE_NUMBER=",
    "CANDIDATE_RANK=",
    "VOTE_COUNT=",
    "OUTPUT_ROOT=",
    "Checkout fixed comparison base",
    "git fetch origin \"$BASE_SHA\"",
    "git checkout \"$BASE_SHA\"",
    "CODEX_MODEL: gpt-5.4-nano",
    "candidate_rank must be 1, 2, or 3",
    "issue_number must be a positive integer",
    "week_id contains unsupported characters",
    "Fetch Issue and run safety gate",
    "gh issue view \"$ISSUE_NUMBER\"",
    "python scripts/scan_issue_safety.py",
    "bash scripts/apply_issue_safety_feedback.sh",
    "python scripts/check_issue_execution_gate.py",
    "Run existing fixed-Issue runner",
    "scripts/run_codex_issue_instruction_canary.sh",
    "Move root lab result into comparison output root",
    "cp lab/index.html \"$OUTPUT_ROOT/index.html\"",
    "cp lab/style.css \"$OUTPUT_ROOT/style.css\"",
    "cp lab/app.js \"$OUTPUT_ROOT/app.js\"",
    "git checkout -- lab/index.html lab/style.css lab/app.js",
    "Validate comparison output scope",
    "\"$OUTPUT_ROOT/index.html\"|\"$OUTPUT_ROOT/style.css\"|\"$OUTPUT_ROOT/app.js\"",
    "bash scripts/safety-check.sh \"$BASE_SHA\" HEAD",
    "bash scripts/static-site-check.sh",
    "Upload comparison diagnostics",
    "Commit comparison output and create PR",
    "Fixed comparison base:",
    "Output root:",
    "Auto-merge: disabled",
    "Manual review is required. Do not auto-merge.",
]

FORBIDDEN_TEXT = [
    "git add lab/index.html lab/style.css lab/app.js",
    "gh pr merge",
    "enable_auto_merge",
    "schedule:",
    "bash scripts/safety-check.sh origin/main HEAD",
]


def require_all(text: str, required: list[str]) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing comparison workflow text: {missing}")


def reject_all(text: str, forbidden: list[str]) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"Forbidden comparison workflow text found: {found}")


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    require_all(text, REQUIRED_TEXT)
    reject_all(text, FORBIDDEN_TEXT)

    if text.index("workflow_dispatch:") > text.index("issue_comment:"):
        raise SystemExit("workflow_dispatch should appear before issue_comment")
    if text.index("issue_comment:") > text.index("push:"):
        raise SystemExit("issue_comment should appear before request-file push trigger")
    if text.index("push:") > text.index("pull_request:"):
        raise SystemExit("push trigger should appear before request-file pull_request trigger")
    if text.index("Resolve comparison inputs") > text.index("Checkout fixed comparison base"):
        raise SystemExit("Inputs must be resolved before fixed-base checkout")
    if text.index("Checkout fixed comparison base") > text.index("Fetch Issue and run safety gate"):
        raise SystemExit("Fixed base must be checked out before fetching the Issue")
    if text.index("Fetch Issue and run safety gate") > text.index("Run existing fixed-Issue runner"):
        raise SystemExit("Issue safety gate must run before the model runner")
    if text.index("Run existing fixed-Issue runner") > text.index("Move root lab result into comparison output root"):
        raise SystemExit("Runner must execute before rank-root copy")
    if text.index("Move root lab result into comparison output root") > text.index("Validate comparison output scope"):
        raise SystemExit("Output must be moved before validation")
    if text.index("Validate comparison output scope") > text.index("Commit comparison output and create PR"):
        raise SystemExit("Validation must run before PR creation")

    print("comparison Issue run workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
