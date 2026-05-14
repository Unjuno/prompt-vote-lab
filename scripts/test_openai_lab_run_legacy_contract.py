#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "openai_lab_run.py"
CURRENT_PATH_DOC = ROOT / "docs" / "current-codex-implementation-path.md"
WORKFLOW_MAP = ROOT / "docs" / "workflow-family-map.md"

REQUIRED_SCRIPT_TEXT = [
    "Legacy non-canonical Prompt Vote Lab implementation-agent fallback.",
    "This script is not the canonical selected-prompt evidence path.",
    "scripts/run_codex_selected_prompt.sh",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "LEGACY_RUNNER_CLASSIFICATION = \"legacy-non-canonical-fallback\"",
    "CANONICAL_SELECTED_PROMPT_RUNNER = \"codex-cli-selected-prompt-packet-container\"",
    "This is the legacy non-canonical fallback runner, not the canonical selected-prompt Docker/Codex path.",
    "runner_classification: {LEGACY_RUNNER_CLASSIFICATION}",
    "canonical_selected_prompt_runner: false",
    "canonical_runner_name: {CANONICAL_SELECTED_PROMPT_RUNNER}",
    "- runner_classification: `{LEGACY_RUNNER_CLASSIFICATION}`",
    "- canonical_selected_prompt_runner: false",
    "- canonical_runner_name: `{CANONICAL_SELECTED_PROMPT_RUNNER}`",
    "no automatic merge",
]

FORBIDDEN_SCRIPT_TEXT = [
    "This script is the canonical selected-prompt evidence path.",
    "canonical_selected_prompt_runner: true",
    "LEGACY_RUNNER_CLASSIFICATION = \"canonical\"",
    "auto merge",
    "automatic merge enabled",
]

REQUIRED_DOC_TEXT = [
    "scripts/openai_lab_run.py",
    "non-canonical",
    "fallback",
    "codex-cli-selected-prompt-packet-container",
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
    script = SCRIPT.read_text(encoding="utf-8")
    current_path_doc = CURRENT_PATH_DOC.read_text(encoding="utf-8")
    workflow_map = WORKFLOW_MAP.read_text(encoding="utf-8")
    docs_text = current_path_doc + "\n" + workflow_map

    require_all(script, REQUIRED_SCRIPT_TEXT, "openai_lab_run legacy contract")
    reject_all(script, FORBIDDEN_SCRIPT_TEXT, "openai_lab_run legacy contract")
    require_all(docs_text, REQUIRED_DOC_TEXT, "legacy fallback docs")

    if script.index("Legacy non-canonical") > script.index("from __future__ import annotations"):
        raise SystemExit("legacy classification should appear in the module docstring before imports")

    if script.index("LEGACY_RUNNER_CLASSIFICATION") > script.index("SCHEMA ="):
        raise SystemExit("runner classification constants should appear before schema definition")

    if script.index("runner_classification: {LEGACY_RUNNER_CLASSIFICATION}") > script.index("## Selected prompt"):
        raise SystemExit("runner classification should appear in prompt metadata before the selected prompt")

    print("OpenAI lab runner legacy contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
