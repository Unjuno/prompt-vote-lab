#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "prompt.yml"

REQUIRED_TEXT = [
    "name: Prompt Proposal",
    "description: Propose a safe prompt for a constrained lab run",
    "title: \"[Prompt]: \"",
    "labels: [\"prompt-proposal\"]",
    "Goal",
    "Requested visible change",
    "Expected result",
    "Acceptance checks",
    "Allowed scope",
    "Disallowed scope confirmation",
    "Optional context",
    "week:<week_id>",
    "normal-candidate",
    "carryover",
    "outcome:*",
    "static HTML/CSS/vanilla JS",
    "lab/index.html",
    "lab/style.css",
    "lab/app.js",
    "Browser-local UI state is optional",
    "does not store credentials, tokens, secrets, tracking identifiers, or cookies",
    "does not require backend services, login, payment, database changes, external APIs, external scripts, or network calls",
    "does not require cookies, credential handling, secrets, analytics, tracking, iframes, or dynamic code execution",
    "does not request changes to workflows, rules, docs, run records, repository policy, branches, commits, pull requests, or merge behavior",
]

FORBIDDEN_TEXT = [
    "authorized-canary",
    "issue-safety:clear",
    "issue-safety:blocked",
    "outcome:implemented",
    "outcome:blocked",
]


def require_all(text: str, required: list[str]) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing prompt issue template text: {missing}")


def reject_all(text: str, forbidden: list[str]) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"Forbidden prompt issue template text: {found}")


def main() -> int:
    text = TEMPLATE.read_text(encoding="utf-8")
    require_all(text, REQUIRED_TEXT)
    reject_all(text, FORBIDDEN_TEXT)

    if text.count("required: true") < 8:
        raise SystemExit("Prompt template should require the core fields and hard scope confirmations")
    if text.index("Goal") > text.index("Requested visible change"):
        raise SystemExit("Goal should appear before Requested visible change")
    if text.index("Allowed scope") > text.index("Disallowed scope confirmation"):
        raise SystemExit("Allowed scope should appear before disallowed scope confirmation")

    print("prompt issue template contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
