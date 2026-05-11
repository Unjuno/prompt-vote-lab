#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "codex-policy-agent-canary-run.yml"
BUNDLE = ROOT / "scripts" / "build_public_agent_run_bundle.py"
DOC = ROOT / "docs" / "public-agent-run-bundle.md"

REQUIRED_WORKFLOW_TEXT = [
    "name: Codex Policy Agent Canary Run",
    "bash scripts/run_codex_policy_agent_canary.sh",
    "python scripts/collect_canary_diagnostics.py",
    "Build redacted public agent run bundle",
    "python scripts/build_public_agent_run_bundle.py",
    "--diagnostics-dir .tmp/canary-diagnostics",
    "--out-dir .tmp/public-agent-run-bundle",
    "codex-policy-agent-canary-public-bundle-",
    "Upload redacted public agent run bundle",
    "codex-policy-agent-canary-diagnostics-",
    "codex-policy-agent-canary-public-log-",
    "Redacted public agent run bundle artifact",
    "Public artifacts are redacted and allowlisted.",
]

REQUIRED_BUNDLE_TEXT = [
    '"policy-agent-container-exit-code.txt"',
    '"policy-agent-diff-name-only.txt"',
    '"policy-agent-diff.patch"',
    '"policy-agent-copied-files.txt"',
    '"policy-agent-container-stdout.txt"',
    '"policy-agent-container-stderr.txt"',
    '"policy-container-mounts.txt"',
    'line_list(diag / "policy-agent-diff-name-only.txt")',
]

REQUIRED_DOC_TEXT = [
    "policy-agent-container-exit-code.txt",
    "policy-agent-diff-name-only.txt",
    "policy-agent-diff.patch",
    "policy-agent-copied-files.txt",
    "codex-policy-agent-canary-public-bundle-",
    "policy-agent-container-stdout.txt",
    "policy-agent-container-stderr.txt",
]

FORBIDDEN_WORKFLOW_TEXT = [
    "cat .tmp/canary-diagnostics/codex-stderr.txt",
    "Upload raw public agent run bundle",
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
    workflow = WORKFLOW.read_text(encoding="utf-8")
    bundle = BUNDLE.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")

    require_all(workflow, REQUIRED_WORKFLOW_TEXT, "policy agent workflow")
    reject_all(workflow, FORBIDDEN_WORKFLOW_TEXT, "policy agent workflow")
    require_all(bundle, REQUIRED_BUNDLE_TEXT, "public bundle builder")
    require_all(doc, REQUIRED_DOC_TEXT, "public agent run bundle doc")

    if workflow.index("Collect diagnostics artifact") > workflow.index("Build redacted public agent run bundle"):
        raise SystemExit("public bundle must be built after diagnostics collection")
    if workflow.index("Build redacted public agent run bundle") > workflow.index("Upload redacted public agent run bundle"):
        raise SystemExit("public bundle upload must occur after public bundle build")
    if workflow.index("Upload redacted public agent run bundle") > workflow.index("Upload diagnostics artifact"):
        raise SystemExit("public bundle should be uploaded before internal diagnostics artifact")

    print("policy agent public bundle contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
