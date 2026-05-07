#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "weekly-issue-finalizer.yml"
DOC = ROOT / "docs" / "issue-lifecycle.md"
SCRIPT = ROOT / "scripts" / "weekly_issue_finalizer.py"

REQUIRED_WORKFLOW_TEXT = [
    "name: Weekly Issue Finalizer",
    "workflow_dispatch:",
    "dry_run:",
    "default: \"true\"",
    "require_public_results_membership:",
    "issues: write",
    "contents: read",
    "gh issue list",
    "--label \"week:${WEEK_ID}\"",
    "python scripts/weekly_issue_finalizer.py",
    "--public-results data/public-results.json",
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


def main() -> int:
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    script_text = SCRIPT.read_text(encoding="utf-8")
    doc_text = DOC.read_text(encoding="utf-8")

    require_all(workflow_text, REQUIRED_WORKFLOW_TEXT, "workflow text")
    reject_all(workflow_text, FORBIDDEN_WORKFLOW_TEXT, "workflow text")
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
