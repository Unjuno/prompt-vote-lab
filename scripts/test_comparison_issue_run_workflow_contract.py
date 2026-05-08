#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "codex-comparison-issue-run.yml"

REQUIRED_TEXT = [
    "name: Codex Comparison Issue Run",
    "workflow_dispatch:",
    "week_id:",
    "base_sha:",
    "issue_number:",
    "candidate_rank:",
    "vote_count:",
    "ref: ${{ inputs.base_sha }}",
    "CODEX_MODEL: gpt-5.4-nano",
    "OUTPUT_ROOT: lab/comparisons/${{ inputs.week_id }}/rank-${{ inputs.candidate_rank }}",
    "codex-comparison-${{ inputs.week_id }}-rank-${{ inputs.candidate_rank }}",
    "candidate_rank must be 1, 2, or 3",
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
    "bash scripts/safety-check.sh origin/main HEAD",
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

    if text.index("Validate comparison inputs") > text.index("Fetch Issue and run safety gate"):
        raise SystemExit("Inputs must be validated before fetching the Issue")
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
