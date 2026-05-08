#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "public-results-export.yml"
DOC = ROOT / "docs" / "public-results-export.md"
DATA_JSON = ROOT / "data" / "public-results.json"
DATA_MD = ROOT / "data" / "public-results.md"

REQUIRED_WORKFLOW_TEXT = [
    "name: Public Results Export",
    "workflow_dispatch:",
    "push:",
    "branches:",
    "- main",
    "paths-ignore:",
    "data/public-results.json",
    "data/public-results.md",
    "lab/comparisons/**",
    "lab/history/**",
    "schedule:",
    "contents: write",
    "issues: read",
    "pull-requests: read",
    "actions: read",
    "gh api graphql",
    "gh run list",
    "gh label list",
    "python scripts/build_public_results_export.py",
    "Build comparison dashboards",
    "scripts/build_comparison_dashboard.py",
    "Build history page",
    "scripts/build_history_page.py",
    "--out-dir lab/history",
    "lab/comparisons",
    "git add data/public-results.json data/public-results.md lab/comparisons lab/history",
    "public-results-export-${{ github.run_number }}",
]

FORBIDDEN_WORKFLOW_TEXT = [
    "OPENAI_API_KEY",
    "secrets.OPENAI",
    "run_codex_issue_instruction_canary",
    "codex exec",
    "gh pr merge",
    "raw diagnostics",
]

REQUIRED_DOC_TEXT = [
    "This export is intentionally descriptive, not interpretive.",
    "It does not score prompts",
    "Issues",
    "Pull Requests",
    "workflow run metadata",
    "API keys",
    "raw Actions logs",
    "prompt-vote-lab-public-results-export-v1",
]

REQUIRED_DATA_TEXT = [
    "prompt-vote-lab-public-results-export-v1",
    "public GitHub repository data only",
    "none; participant analysis expected",
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
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    doc_text = DOC.read_text(encoding="utf-8")
    data_json_text = DATA_JSON.read_text(encoding="utf-8")
    data_md_text = DATA_MD.read_text(encoding="utf-8")

    require_all(workflow_text, REQUIRED_WORKFLOW_TEXT, "public results workflow")
    reject_all(workflow_text, FORBIDDEN_WORKFLOW_TEXT, "public results workflow")
    require_all(doc_text, REQUIRED_DOC_TEXT, "public results doc")
    require_all(data_json_text, REQUIRED_DATA_TEXT, "public results json")
    require_all(data_md_text, ["raw results surface", "See `public-results.json`"], "public results markdown")

    if workflow_text.index("workflow_dispatch:") > workflow_text.index("push:"):
        raise SystemExit("workflow_dispatch should remain before push trigger for readability")
    if workflow_text.index("push:") > workflow_text.index("schedule:"):
        raise SystemExit("push trigger should appear before schedule trigger")
    if workflow_text.index("Build public results export") > workflow_text.index("Build comparison dashboards"):
        raise SystemExit("Comparison dashboards must be built after public results export")
    if workflow_text.index("Build comparison dashboards") > workflow_text.index("Build history page"):
        raise SystemExit("History page must be built after comparison dashboards")
    if workflow_text.index("Build history page") > workflow_text.index("Upload public results artifact"):
        raise SystemExit("History page must be built before artifact upload")
    if workflow_text.index("Upload public results artifact") > workflow_text.index("Commit public results snapshot"):
        raise SystemExit("Artifacts should be uploaded before the commit step")

    print("public results export workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
