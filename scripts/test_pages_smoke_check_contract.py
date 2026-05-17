#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "pages-smoke-check.py"
WORKFLOW = ROOT / ".github" / "workflows" / "pages-smoke-check.yml"
INDEX = ROOT / "index.html"
LAB_INDEX = ROOT / "lab" / "index.html"

REQUIRED_SCRIPT_TEXT = [
    "ROOT_EXPECTED_TEXT",
    "LAB_EXPECTED_TEXT",
    "20-vote baseline",
    "require_all(base + \"/\", ROOT_EXPECTED_TEXT)",
    "require_all(base + \"/lab/\", LAB_EXPECTED_TEXT)",
]

REQUIRED_WORKFLOW_TEXT = [
    "name: GitHub Pages Smoke Check",
    "python scripts/pages-smoke-check.py --base-url \"https://unjuno.github.io/prompt-vote-lab\"",
]

FORBIDDEN_TEXT = [
    "20 virtual votes",
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
    workflow = WORKFLOW.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    lab_index = LAB_INDEX.read_text(encoding="utf-8")

    require_all(script, REQUIRED_SCRIPT_TEXT, "pages smoke script")
    require_all(workflow, REQUIRED_WORKFLOW_TEXT, "pages smoke workflow")
    require_all(index, ["Prompt Vote Lab", "20-vote baseline"], "root landing page")
    require_all(lab_index, ["Prompt Vote Lab"], "lab page")

    reject_all(script, FORBIDDEN_TEXT, "pages smoke script")
    reject_all(workflow, FORBIDDEN_TEXT, "pages smoke workflow")
    reject_all(index, FORBIDDEN_TEXT, "root landing page")

    print("pages smoke check contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
