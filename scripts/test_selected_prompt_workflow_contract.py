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
    "INPUT_PROMPT_BODY: ${{ inputs.prompt_body }}",
    "INPUT_ISSUE_NUMBER: ${{ inputs.issue_number }}",
    "INPUT_ISSUE_TITLE: ${{ inputs.issue_title }}",
    "INPUT_ISSUE_URL: ${{ inputs.issue_url }}",
    "INPUT_CANDIDATE_RANK: ${{ inputs.candidate_rank }}",
    "INPUT_VOTE_COUNT: ${{ inputs.vote_count }}",
    "INPUT_SELECTION_POLICY: ${{ inputs.selection_policy }}",
    "OPENAI_API_KEY:",
    "scripts/run_codex_selected_prompt.sh",
    "--prompt-body \"$INPUT_PROMPT_BODY\"",
    "--issue-title \"$INPUT_ISSUE_TITLE\"",
    "--issue-url \"$INPUT_ISSUE_URL\"",
    "--candidate-rank \"$INPUT_CANDIDATE_RANK\"",
    "--vote-count \"$INPUT_VOTE_COUNT\"",
    "--selection-policy \"$INPUT_SELECTION_POLICY\"",
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

FORBIDDEN_RUN_TEXT = [
    "${{ inputs.prompt_body }}",
    "${{ inputs.issue_title }}",
    "${{ inputs.issue_url }}",
    "${{ inputs.issue_number }}",
    "${{ inputs.candidate_rank }}",
    "${{ inputs.vote_count }}",
    "${{ inputs.selection_policy }}",
]


def require_all(text: str, required: list[str]) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing selected prompt workflow text: {missing}")


def reject_all(text: str, forbidden: list[str]) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"Forbidden selected prompt workflow text found: {found}")


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
        raise SystemExit(f"Unsafe workflow input interpolation inside run blocks: {sorted(set(found))}")


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    require_all(text, REQUIRED_TEXT)
    reject_all(text, FORBIDDEN_TEXT)
    reject_inputs_in_run_blocks(text)

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
