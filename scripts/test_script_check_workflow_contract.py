#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "script-check.yml"

REQUIRED_TEXT = [
    "name: Script Check",
    "pull_request:",
    "paths:",
    "lab/comparisons/**",
    "runs/**",
    "workflow_dispatch:",
    "contents: read",
    "Run actionlint",
    "raven-actions/actionlint@v2",
    "Run comparison dashboard builder test",
    "python scripts/test_build_comparison_dashboard.py",
    "Run comparison dashboard decision test",
    "python scripts/test_comparison_dashboard_decision.py",
    "Run generated comparison dashboard test",
    "python scripts/test_generated_comparison_dashboards.py",
    "Run public results export workflow contract test",
    "python scripts/test_public_results_export_workflow_contract.py",
    "Run script-check workflow contract test",
    "python scripts/test_script_check_workflow_contract.py",
    "Run public agent run bundle verifier test",
    "python scripts/test_verify_public_agent_run_bundle.py",
    "Run policy agent public bundle contract test",
    "python scripts/test_policy_agent_public_bundle_contract.py",
    "Run lab PR scope guard self-test",
    "bash scripts/test-lab-pr-scope.sh",
]

FORBIDDEN_TEXT = [
    "contents: write",
    "pull-requests: write",
    "issues: write",
    "secrets.OPENAI",
    "OPENAI_API_KEY",
    "codex exec",
    "gh pr merge",
]


def require_all(text: str, required: list[str]) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing script-check workflow text: {missing}")


def reject_all(text: str, forbidden: list[str]) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise SystemExit(f"Forbidden script-check workflow text found: {found}")


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    require_all(text, REQUIRED_TEXT)
    reject_all(text, FORBIDDEN_TEXT)

    if text.index("Checkout") > text.index("Run actionlint"):
        raise SystemExit("actionlint should run after checkout")

    if text.index("Run actionlint") > text.index("Setup Node"):
        raise SystemExit("actionlint should run before language-specific script checks")

    if text.index("lab/comparisons/**") > text.index("runs/**"):
        raise SystemExit("runs/** should be tracked near generated/evidence paths")

    if text.index("Run public agent run bundle enrichment test") > text.index("Run public agent run bundle verifier test"):
        raise SystemExit("Public bundle verifier test should run after enrichment test")

    if text.index("Run public agent run bundle verifier test") > text.index("Run policy agent public bundle contract test"):
        raise SystemExit("Policy agent public bundle contract test should run after verifier test")

    if text.index("Run comparison dashboard builder test") > text.index("Run comparison dashboard decision test"):
        raise SystemExit("Comparison dashboard decision test should run after the builder test")

    if text.index("Run comparison dashboard decision test") > text.index("Run generated comparison dashboard test"):
        raise SystemExit("Generated comparison dashboard test should run after the decision test")

    if text.index("Run generated comparison dashboard test") > text.index("Run weekly Issue finalizer test"):
        raise SystemExit("Generated dashboard test should run before later weekly finalizer tests")

    print("script-check workflow contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
