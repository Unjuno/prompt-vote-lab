#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "codex-selected-prompt-run.yml"

REQUIRED_TEXT = [
    "name: Codex Selected Prompt Run",
    "workflow_dispatch:",
    "prompt_body:",
    "issue_number:",
    "issue_title:",
    "issue_url:",
    "candidate_rank:",
    "vote_count:",
    "selection_policy:",
    "contents: read",
    "concurrency:",
    "codex-selected-prompt-run",
    "OPENAI_API_KEY:",
    "scripts/run_codex_selected_prompt.sh",
    "--prompt-body",
    "--candidate-rank",
    "--vote-count",
    "--selection-policy",
    "scripts/safety-check.sh",
    "scripts/static-site-check.sh",
    "scripts/collect_canary_diagnostics.py",
    "scripts/build_public_agent_run_bundle.py",
    "scripts/enrich_public_agent_run_bundle.py",
    "scripts/verify_public_agent_run_bundle.py",
    "scripts/run_gitleaks_public_bundle_scan.sh",
    "actions/upload-artifact@v4",
    "actions/download-artifact@v4",
    "scripts/write_public_run_log.py",
    "codex-selected-prompt-public-bundle",
    "codex-selected-prompt-diagnostics",
    "codex-selected-prompt-public-log",
    "runner codex-cli-selected-prompt-packet-container",
    "fallback-policy none",
    "auto-merge-policy disabled",
]

FORBIDDEN_TEXT = [
    "pull_request:",
    "schedule:",
    "contents: write",
    "pull-requests: write",
    "issues: write",
    "gh pr create",
    "gh pr merge",
    "git push",
    "git commit",
    "workflow_run:",
]


def require_all(text: str, required: list[str]) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing selected prompt workflow text: {missing}")


def reject_all(text: str, forbidden: list[str]) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"Forbidden selected prompt workflow text found: {found}")


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    require_all(text, REQUIRED_TEXT)
    reject_all(text, FORBIDDEN_TEXT)

    if text.index("scripts/run_codex_selected_prompt.sh") > text.index("scripts/safety-check.sh"):
        raise SystemExit("safety check should run after the selected prompt runner")

    if text.index("scripts/build_public_agent_run_bundle.py") > text.index("scripts/enrich_public_agent_run_bundle.py"):
        raise SystemExit("bundle enrichment should run after bundle build")

    if text.index("scripts/enrich_public_agent_run_bundle.py") > text.index("scripts/verify_public_agent_run_bundle.py"):
        raise SystemExit("bundle verification should run after enrichment")

    if text.index("actions/upload-artifact@v4") > text.index("actions/download-artifact@v4"):
        raise SystemExit("artifact download should happen after upload")

    print("selected prompt workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
