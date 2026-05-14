#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "usable-experiment-ops.md"
README = ROOT / "README.md"
DOCS_README = ROOT / "docs" / "README.md"
MODEL_POLICY = ROOT / "rules" / "model-policy-v1.1.md"
RUN_RECORD = ROOT / "runs" / "first-canary-009-authorized-canary-issue-170-success.md"

REQUIRED_DOC_TEXT = [
    "Prompt Vote Lab is currently usable as a manual canary experiment system.",
    "Issue safety scan",
    "optional manual rescan",
    "fixed-Issue 009 runtime scan",
    "execution gate",
    "Codex implementation PR",
    "manual review",
    "runs/ record",
    "issue-safety:clear",
    "issue-safety:blocked",
    "authorized-canary",
    "Rank 1, rank 2, and rank 3 must use the same implementation model policy",
    "model-policy-v1.1: gpt-5.4-nano",
    "auto-merge",
]

REQUIRED_README_TEXT = [
    "model-policy-v1.1: gpt-5.4-nano",
    "docs/usable-experiment-ops.md",
    "automatic merge: no",
]

REQUIRED_DOCS_README_TEXT = [
    "Usable experiment operations",
    "model-policy-v1.1.md",
    "Manual canary experiments and comparison operations remain available through [Usable experiment operations](./usable-experiment-ops.md).",
]

REQUIRED_MODEL_POLICY_TEXT = [
    "# model-policy-v1.1",
    "gpt-5.4-nano",
    "first-canary-009",
    "Do not directly compare prompt results across v1.0 and v1.1",
]

REQUIRED_RUN_RECORD_TEXT = [
    "Issue: #170",
    "PR: #173",
    "Merge commit: c60f3ca3e01c9a90f632c5f30a4e643a47be2bf8",
    "authorized-canary",
    "policy_override",
    "file_scope_escalation",
    "network_behavior",
    "cookie_or_tracking",
    "dynamic_code_execution",
    "manual squash merge",
]


def require_text(path: Path, required: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing required text in {path}: {missing}")


def main() -> int:
    require_text(DOC, REQUIRED_DOC_TEXT)
    require_text(README, REQUIRED_README_TEXT)
    require_text(DOCS_README, REQUIRED_DOCS_README_TEXT)
    require_text(MODEL_POLICY, REQUIRED_MODEL_POLICY_TEXT)
    require_text(RUN_RECORD, REQUIRED_RUN_RECORD_TEXT)
    print("usable experiment ops doc test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
