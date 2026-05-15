#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "weekly-issue-finalizer.yml"
DOC = ROOT / "docs" / "issue-lifecycle.md"
SCRIPT = ROOT / "scripts" / "weekly_issue_finalizer.py"

FORBIDDEN_RUN_TEXT = [
    "${{ inputs.week_id }}",
    "${{ inputs.run_record_hint }}",
    "${{ inputs.dry_run }}",
    "${{ inputs.require_public_results_membership }}",
]

REQUIRED_WORKFLOW_TEXT = [
    "name: Weekly Issue Finalizer",
    "workflow_dispatch:",
    "dry_run:",
    "default: \"true\"",
    "require_public_results_membership:",
    "issues: write",
    "contents: read",
    "WEEK_ID: ${{ inputs.week_id }}",
    "DRY_RUN: ${{ inputs.dry_run }}",
    "REQUIRE_PUBLIC_RESULTS_MEMBERSHIP: ${{ inputs.require_public_results_membership }}",
    "RUN_RECORD_HINT: ${{ inputs.run_record_hint }}",
    "gh issue list",
    "--label \"week:${WEEK_ID}\"",
    "python scripts/weekly_issue_finalizer.py",
    "--public-results data/public-results.json",
    "--week-id \"$WEEK_ID\"",
    "--run-record-hint \"$RUN_RECORD_HINT\"",
    "--require-public-results-membership",
    "Upload finalizer plan artifact",
    "Comment and close eligible Issues",
    "if: ${{ inputs.dry_run != 'true' }}",
    "gh issue comment",
    "gh issue close",
    "gh_reason = reason.replace('_', ' ')",
    "--reason {shlex.quote(gh_reason)}",
]

FORBIDDEN_WORKFLOW_TEXT = [
    "schedule:",
    "gh issue list \\\n            --repo \"$GITHUB_REPOSITORY\" \\\n            --state open \\\n            --limit 200",
    "OPENAI_API_KEY",
    "codex exec",
]

REQUIRED_SCRIPT_TEXT = [
    "PROTECTED_LABELS",
    "carryover",
    "future-candidate",
    "do-not-close",
    "pinned",
    "expected_exactly_one_week_label",
    "expected_exactly_one_outcome_label",
    "missing_from_public_results_snapshot",
    "The Issue is not deleted.",
    "Only Issues with both week:* and outcome:* labels are eligible",
]

REQUIRED_DOC_TEXT = [
    "Issue lifecycle",
    "closed, not deleted",
    "week:*",
    "outcome:*",
    "Public Results Export",
    "comment before close",
    "carryover",
    "do-not-close",
]


def require_all(text: str, required: list[str], label: str) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing {label}: {missing}")


def reject_all(text: str, forbidden: list[str], label: str) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"Forbidden {label}: {found}")


def run_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "run: |":
            indent = len(line) - len(line.lstrip())
            block: list[str] = []
            i += 1
            while i < len(lines):
                child = lines[i]
                if child.strip() and len(child) - len(child.lstrip()) <= indent:
                    break
                block.append(child)
                i += 1
            blocks.append("\n".join(block))
            continue
        i += 1
    return blocks


def reject_inputs_in_run_blocks(text: str) -> None:
    found: list[str] = []
    for block in run_blocks(text):
        for item in FORBIDDEN_RUN_TEXT:
            if item in block:
                found.append(item)
    if found:
        raise SystemExit(f"Unsafe weekly issue finalizer input interpolation inside run blocks: {sorted(set(found))}")


def main() -> int:
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    script_text = SCRIPT.read_text(encoding="utf-8")
    doc_text = DOC.read_text(encoding="utf-8")

    require_all(workflow_text, REQUIRED_WORKFLOW_TEXT, "workflow text")
    reject_all(workflow_text, FORBIDDEN_WORKFLOW_TEXT, "workflow text")
    reject_inputs_in_run_blocks(workflow_text)
    require_all(script_text, REQUIRED_SCRIPT_TEXT, "script text")
    require_all(doc_text, REQUIRED_DOC_TEXT, "doc text")

    if workflow_text.index("Build finalizer plan") > workflow_text.index("Comment and close eligible Issues"):
        raise SystemExit("Finalizer plan must be built before close step")
    if workflow_text.index("Upload finalizer plan artifact") > workflow_text.index("Comment and close eligible Issues"):
        raise SystemExit("Plan artifact must be uploaded before close step")

    print("weekly issue finalizer workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())