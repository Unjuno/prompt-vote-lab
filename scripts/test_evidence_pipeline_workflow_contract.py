#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "evidence-pipeline-dry-run.yml"

FORBIDDEN_RUN_TEXT = [
    "${{ github.event.inputs.week_id",
    "${{ github.event.inputs.snapshot_at",
    "${{ github.event.inputs.site_url",
    "${{ github.event.inputs.source",
    "${{ inputs.week_id",
    "${{ inputs.snapshot_at",
    "${{ inputs.site_url",
    "${{ inputs.source",
]

REQUIRED_TEXT = [
    "name: Evidence Pipeline Dry Run",
    "workflow_dispatch:",
    "week_id:",
    "snapshot_at:",
    "site_url:",
    "source:",
    "contents: read",
    "issues: read",
    "INPUT_WEEK_ID: ${{ inputs.week_id }}",
    "INPUT_SNAPSHOT_AT: ${{ inputs.snapshot_at }}",
    "INPUT_SITE_URL: ${{ inputs.site_url }}",
    "INPUT_SOURCE: ${{ inputs.source }}",
    "WEEK_ID=\"${INPUT_WEEK_ID:-dry-run-001}\"",
    "SOURCE=\"${INPUT_SOURCE:-fixture}\"",
    "SNAPSHOT_AT_INPUT=\"${INPUT_SNAPSHOT_AT:-}\"",
    "SITE_URL=\"${INPUT_SITE_URL:-https://unjuno.github.io/prompt-vote-lab/}\"",
    "node scripts/create-weekly-snapshot.mjs",
    "node scripts/create-snapshot-summary.mjs",
    "node scripts/create-public-briefing.mjs",
    "node scripts/create-hn-draft.mjs",
    "node scripts/validate-evidence-artifact.mjs",
    "Upload evidence pipeline dry-run artifact",
]

FORBIDDEN_TEXT = [
    "contents: write",
    "pull-requests: write",
    "OPENAI_API_KEY",
    "codex exec",
    "gh pr create",
    "gh pr merge",
    "git commit",
    "git push",
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
        raise SystemExit(f"Unsafe evidence pipeline input interpolation inside run blocks: {sorted(set(found))}")


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    require_all(text, REQUIRED_TEXT, "evidence pipeline workflow")
    reject_all(text, FORBIDDEN_TEXT, "evidence pipeline workflow")
    reject_inputs_in_run_blocks(text)

    if text.index("Generate snapshot and run log") > text.index("Generate summary from generated snapshots"):
        raise SystemExit("snapshot generation must precede summary generation")
    if text.index("Generate summary from generated snapshots") > text.index("Generate public briefing"):
        raise SystemExit("summary generation must precede public briefing generation")
    if text.index("Generate public briefing") > text.index("Generate HN draft from generated snapshot"):
        raise SystemExit("public briefing should precede HN draft generation")
    if text.index("Verify dry-run outputs") > text.index("Upload evidence pipeline dry-run artifact"):
        raise SystemExit("dry-run outputs must be verified before artifact upload")

    print("evidence pipeline workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
