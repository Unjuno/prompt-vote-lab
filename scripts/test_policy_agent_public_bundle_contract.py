#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "codex-policy-agent-canary-run.yml"
BUNDLE = ROOT / "scripts" / "build_public_agent_run_bundle.py"
ENRICH = ROOT / "scripts" / "enrich_public_agent_run_bundle.py"
DOC = ROOT / "docs" / "public-agent-run-bundle.md"

REQUIRED_WORKFLOW_TEXT = [
    "name: Codex Policy Agent Canary Run",
    "bash scripts/run_codex_policy_agent_canary.sh",
    "python scripts/collect_canary_diagnostics.py",
    "Build redacted public agent run bundle",
    "python scripts/build_public_agent_run_bundle.py",
    "Enrich public agent run bundle with sanitized logs",
    "python scripts/enrich_public_agent_run_bundle.py",
    "--diagnostics-dir .tmp/canary-diagnostics",
    "--bundle-dir .tmp/public-agent-run-bundle",
    "--out-dir .tmp/public-agent-run-bundle",
    "codex-policy-agent-canary-public-bundle-",
    "Upload redacted public agent run bundle",
    "codex-policy-agent-canary-diagnostics-",
    "codex-policy-agent-canary-public-log-",
    "Observation summary files:",
    "observation-summary.md",
    "observation-summary.json",
    "Sanitized diagnostic logs directory:",
    "sanitized/",
    "Public artifacts are redacted, sanitized, and indexed for participant review.",
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

REQUIRED_ENRICH_TEXT = [
    "SANITIZED_PUBLIC_FILES",
    "REASONING_TRACE_FILES",
    '"codex-events.jsonl"',
    '"codex-last-message.txt"',
    '"codex-stderr.txt"',
    '"codex-stdout.txt"',
    '"policy-agent-container-stdout.txt"',
    '"policy-agent-container-stderr.txt"',
    '"npm-install-codex.txt"',
    '"policy-container-mounts.txt"',
    "reasoning-traces/",
    "copy_reasoning_trace_files",
    "reasoning_trace_files",
    "reasoning_effect_hypotheses",
    "exposed_reasoning_trace_published",
    "unexposed_provider_private_cot_available",
    "unexposed_provider_private_cot_published",
    "observation-summary.json",
    "observation-summary.md",
    "[REDACTED_SECRET]",
    "[REDACTED_RUNNER_WORKDIR]",
    "exact_read_order_observed",
]

REQUIRED_DOC_TEXT = [
    "redacted raw evidence",
    "sanitized diagnostic logs",
    "sanitized reasoning / CoT-like trace artifacts",
    "sanitized/codex-stderr.txt",
    "sanitized/policy-agent-container-stderr.txt",
    "sanitized/npm-install-codex.txt",
    "reasoning-traces/codex-events.jsonl",
    "reasoning-traces/codex-last-message.txt",
    "reasoning-traces/codex-stdout.txt",
    "reasoning-traces/codex-stderr.txt",
    "This is not a proxy-only policy. Exposed reasoning / CoT-like traces are evaluation targets.",
    "unexposed_provider_private_cot_available = unknown",
    "unexposed_provider_private_cot_published = false",
    "reasoning-to-behavior hypotheses",
    "observation-summary.md",
    "observation-summary.json",
    "[REDACTED_SECRET]",
    "[REDACTED_RUNNER_WORKDIR]",
    "Sanitization is a best-effort publication guard.",
]

FORBIDDEN_WORKFLOW_TEXT = [
    "cat .tmp/canary-diagnostics/codex-stderr.txt",
    "Upload raw public agent run bundle",
]

FORBIDDEN_DOC_TEXT = [
    "raw private chain-of-thought",
    "CoTそのものではなく",
    "Only proxy behavior is evaluated",
    "Reasoning traces are not evaluation targets",
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
    enrich = ENRICH.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")

    require_all(workflow, REQUIRED_WORKFLOW_TEXT, "policy agent workflow")
    reject_all(workflow, FORBIDDEN_WORKFLOW_TEXT, "policy agent workflow")
    require_all(bundle, REQUIRED_BUNDLE_TEXT, "public bundle builder")
    require_all(enrich, REQUIRED_ENRICH_TEXT, "public bundle enrichment script")
    require_all(doc, REQUIRED_DOC_TEXT, "public agent run bundle doc")
    reject_all(doc, FORBIDDEN_DOC_TEXT, "public agent run bundle doc")

    if workflow.index("Collect diagnostics artifact") > workflow.index("Build redacted public agent run bundle"):
        raise SystemExit("public bundle must be built after diagnostics collection")
    if workflow.index("Build redacted public agent run bundle") > workflow.index("Enrich public agent run bundle with sanitized logs"):
        raise SystemExit("public bundle must be enriched after bundle build")
    if workflow.index("Enrich public agent run bundle with sanitized logs") > workflow.index("Upload redacted public agent run bundle"):
        raise SystemExit("public bundle upload must occur after enrichment")
    if workflow.index("Upload redacted public agent run bundle") > workflow.index("Upload diagnostics artifact"):
        raise SystemExit("public bundle should be uploaded before internal diagnostics artifact")

    print("policy agent public bundle contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
