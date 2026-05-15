#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUPPORT_WORKFLOW = ROOT / ".github" / "workflows" / "support-unlock-export.yml"
WEEKLY_WORKFLOW = ROOT / ".github" / "workflows" / "weekly-auto-run.yml"
SCRIPT_CHECK = ROOT / ".github" / "workflows" / "script-check.yml"

FORBIDDEN_RUN_TEXT = [
    "${{ inputs.week_id }}",
    "${{ inputs.since }}",
    "${{ inputs.until }}",
]


def require(text: str, required: list[str], label: str) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"{label}: missing required text: {missing}")


def reject(text: str, forbidden: list[str], label: str) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"{label}: forbidden text found: {found}")


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
        raise SystemExit(f"Unsafe support workflow input interpolation inside run blocks: {sorted(set(found))}")


def main() -> int:
    support = SUPPORT_WORKFLOW.read_text(encoding="utf-8")
    weekly = WEEKLY_WORKFLOW.read_text(encoding="utf-8")
    script_check = SCRIPT_CHECK.read_text(encoding="utf-8")

    require(
        support,
        [
            "name: Support Unlock Export",
            "schedule:",
            "workflow_dispatch:",
            "week_id:",
            "since:",
            "until:",
            "previous UTC ISO week",
            "target = current - timedelta(days=7)",
            "INPUT_WEEK_ID: ${{ inputs.week_id }}",
            "INPUT_SINCE: ${{ inputs.since }}",
            "INPUT_UNTIL: ${{ inputs.until }}",
            "os.environ.get(\"INPUT_WEEK_ID\", \"\").strip()",
            "os.environ.get(\"INPUT_SINCE\", \"\").strip()",
            "os.environ.get(\"INPUT_UNTIL\", \"\").strip()",
            "SPONSORS_GRAPHQL_TOKEN",
            "scripts/fetch_support_activities.py",
            "scripts/build_support_unlocks.py",
            "Validate public support unlock output",
            "python scripts/test_unlock_export_public.py",
            "data/support-unlocks",
            "git add data/support-unlocks/",
        ],
        "support workflow",
    )
    reject(
        support,
        [
            "OPENAI_API_KEY",
            "codex exec",
            "gh pr merge",
            "lab/index.html",
            "lab/style.css",
            "lab/app.js",
        ],
        "support workflow",
    )
    reject_inputs_in_run_blocks(support)

    require(
        weekly,
        [
            "Resolve automated support unlocks",
            "scripts/resolve_support_unlock.py",
            "SUPPORT_UNLOCK_WEEK",
            "SUPPORT_UNLOCK_FILE",
            "RANK_2_UNLOCKED",
            "RANK_3_UNLOCKED",
            "--week \"$RUN_WEEK\"",
            "--require",
        ],
        "weekly workflow",
    )

    require(
        script_check,
        [
            "Run support unlock builder test",
            "python scripts/test_build_support_unlocks.py",
            "Run support unlock resolver test",
            "python scripts/test_resolve_support_unlock.py",
            "Run eligible selector support unlock test",
            "python scripts/test_select_eligible_support_unlock.py",
            "Run support unlock workflow contract test",
            "python scripts/test_support_unlock_workflow_contract.py",
            "python scripts/test_unlock_export_public.py",
        ],
        "script check",
    )

    if support.index("Resolve support window") > support.index("Fetch support activity"):
        raise SystemExit("support window must resolve before support activity fetch")

    if support.index("Validate public support unlock output") > support.index("Commit support unlocks"):
        raise SystemExit("public support unlock output must be validated before commit")

    print("support unlock workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())