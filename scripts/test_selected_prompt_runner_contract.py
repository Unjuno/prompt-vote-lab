#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_codex_selected_prompt.sh"

REQUIRED_TEXT = [
    "Usage: scripts/run_codex_selected_prompt.sh",
    "--prompt-body",
    "--prompt-file",
    "--issue-number",
    "--issue-title",
    "--issue-url",
    "--candidate-rank",
    "--vote-count",
    "--selection-policy",
    "python scripts/create_codex_task_packet.py",
    "-v \"$work:/work:rw\"",
    "-v \"$task:/task:ro\"",
    "-v \"$runtime:/codex-runtime:rw\"",
    "container_task_mount_mode",
    "read-only",
    "repo_root_mounted",
    "false",
    "codex login --with-api-key",
    "unset OPENAI_API_KEY",
    "codex exec --cd /work --skip-git-repo-check",
    "selected-prompt-diff.patch",
    "selected-prompt-copied-files.txt",
]

FORBIDDEN_TEXT = [
    "-v \"$root:/work:rw\"",
    "-v \"$task:/task:rw\"",
    "git commit",
    "gh pr create",
    "gh pr merge",
]


def require_all(text: str, required: list[str]) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing selected-prompt runner text: {missing}")


def reject_all(text: str, forbidden: list[str]) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"Forbidden selected-prompt runner text found: {found}")


def main() -> int:
    text = RUNNER.read_text(encoding="utf-8")
    require_all(text, REQUIRED_TEXT)
    reject_all(text, FORBIDDEN_TEXT)

    if text.index("python scripts/create_codex_task_packet.py") > text.index("docker run --rm"):
        raise SystemExit("task packet must be generated before Docker execution")

    if text.index("unset OPENAI_API_KEY") > text.index("codex exec"):
        raise SystemExit("OPENAI_API_KEY must be unset before codex exec")

    print("selected prompt runner contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
