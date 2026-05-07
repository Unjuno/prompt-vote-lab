#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "issue-safety-scan.yml"

REQUIRED_TEXT = [
    "name: Issue Safety Scan",
    "issues:",
    "- opened",
    "- edited",
    "- reopened",
    "workflow_dispatch:",
    "issue_number:",
    "contents: read",
    "issues: write",
    "ISSUE_NUMBER:",
    "gh issue view \"$ISSUE_NUMBER\"",
    "--json number,title,body,url,author,createdAt,updatedAt",
    "python scripts/scan_issue_safety.py",
    "--phase issue_event",
    "bash scripts/apply_issue_safety_feedback.sh",
    "issue-safety-scan-${{ env.ISSUE_NUMBER }}-${{ github.run_number }}",
]

FORBIDDEN_TEXT = [
    "contents: write",
    "pull-requests: write",
    "OPENAI_API_KEY",
    "bash scripts/run_codex_issue_instruction_canary.sh",
]


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    missing = [item for item in REQUIRED_TEXT if item not in text]
    if missing:
        raise SystemExit(f"Missing Issue Safety Scan workflow contract text: {missing}")
    found = [item for item in FORBIDDEN_TEXT if item in text]
    if found:
        raise SystemExit(f"Forbidden Issue Safety Scan workflow text found: {found}")
    print("Issue safety workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
