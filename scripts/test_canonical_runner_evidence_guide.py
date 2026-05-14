#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "canonical-runner-evidence-guide.md"
DOCS_INDEX = ROOT / "docs" / "README.md"

GUIDE_REQUIRED_TEXT = [
    "# Canonical runner evidence guide",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "weekly-selected-prompt-diagnostics-<run_number>",
    "weekly-selected-prompt-public-bundles-<run_number>",
    "weekly-selected-prompt-uploaded-bundle-verification-<run_number>",
    "weekly-selected-prompt-diagnostics-7",
    "weekly-selected-prompt-public-bundles-7",
    "weekly-selected-prompt-uploaded-bundle-verification-7",
    "/work:rw",
    "/task:ro",
    "/codex-runtime:rw",
    "repo_root_mounted: false",
    "OPENAI_API_KEY present before codex exec: no",
    "changed files subset of lab/index.html, lab/style.css, lab/app.js",
    "forbidden changed files: none",
    "lab/index.html",
    "lab/style.css",
    "lab/app.js",
    "public bundle verification: ok",
    "uploaded bundle verification: ok",
    "Gitleaks finding count: 0",
    "The legacy `scripts/openai_lab_run.py` path may still exist as a migration fallback.",
    "It is non-canonical.",
    "workflow run: 25858202166",
    "selected Issue: #282",
    "summary PR: #283",
    "implementation PR: #284",
    "manual selected-prompt smoke: PASS",
    "weekly feature-flag canary with eligible candidate: PASS",
    "participant evidence guide published",
    "manual review remains required",
    "auto-merge remains disabled",
    "It does not automatically prove:",
    "The run should be merged.",
]

GUIDE_FORBIDDEN_TEXT = [
    "A run is canonical merely because it produced a small valid lab diff.",
    "The legacy `scripts/openai_lab_run.py` path satisfies the selected-prompt canonical runner requirement.",
    "auto-merge may be enabled",
    "public bundle verification is optional",
    "uploaded bundle verification is optional",
]

INDEX_REQUIRED_TEXT = [
    "This README is a navigation entry point, not a release-gate source of truth.",
    "[Canonical runner evidence guide](./canonical-runner-evidence-guide.md)",
    "Runner: codex-cli-selected-prompt-packet-container",
    "Canonical selected-prompt runner: true",
    "The legacy `scripts/openai_lab_run.py` path is non-canonical",
    "current status contract -> docs/canonical-status-drift-check.md",
    "weekly workflow operation -> docs/weekly-automation.md",
    "canonical evidence decision rule -> docs/canonical-runner-evidence-guide.md",
]

INDEX_FORBIDDEN_TEXT = [
    "Weekly Auto Run -> run 25858202166",
    "artifacts present: diagnostics, public bundle, uploaded bundle verification",
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
    guide = GUIDE.read_text(encoding="utf-8")
    index = DOCS_INDEX.read_text(encoding="utf-8")
    require_all(guide, GUIDE_REQUIRED_TEXT, "canonical runner evidence guide")
    reject_all(guide, GUIDE_FORBIDDEN_TEXT, "canonical runner evidence guide")
    require_all(index, INDEX_REQUIRED_TEXT, "docs index")
    reject_all(index, INDEX_FORBIDDEN_TEXT, "docs index detailed canary evidence")

    if guide.index("What to inspect first") > guide.index("Expected artifacts"):
        raise SystemExit("inspection order should be described before artifact names")

    if guide.index("Expected artifacts") > guide.index("What each artifact proves"):
        raise SystemExit("artifact names should appear before artifact interpretation")

    if guide.index("Non-canonical fallback") > guide.index("Verified weekly canary"):
        raise SystemExit("legacy fallback warning should appear before the canary example")

    if guide.index("Verified weekly canary") > guide.index("Release readiness rule"):
        raise SystemExit("release readiness should follow the verified canary example")

    print("canonical runner evidence guide test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
