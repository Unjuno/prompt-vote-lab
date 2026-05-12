#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "codex-policy-agent-canary-run.yml"
BUNDLE = ROOT / "scripts" / "build_public_agent_run_bundle.py"
ENRICH = ROOT / "scripts" / "enrich_public_agent_run_bundle.py"
VERIFY = ROOT / "scripts" / "verify_public_agent_run_bundle.py"
GITLEAKS = ROOT / "scripts" / "run_gitleaks_public_bundle_scan.sh"
DOC = ROOT / "docs" / "public-agent-run-bundle.md"

REQUIRED_WORKFLOW_TEXT = [
    "name: Codex Policy Agent Canary Run",
    "bash scripts/run_codex_policy_agent_canary.sh",
    "python scripts/collect_canary_diagnostics.py",
    "Build redacted public agent run bundle",
    "python scripts/build_public_agent_run_bundle.py",
    "Enrich public agent run bundle with sanitized logs and reasoning traces",
    "python scripts/enrich_public_agent_run_bundle.py",
    "Verify public agent run bundle contents",
    "python scripts/verify_public_agent_run_bundle.py",
    "--report .tmp/public-agent-run-bundle-verification.json",
    "public-agent-run-bundle-verification.json",
    "Scan public agent run bundle with Gitleaks",
    "bash scripts/run_gitleaks_public_bundle_scan.sh",
    "--report .tmp/public-agent-run-bundle-gitleaks.json",
    "public-agent-run-bundle-gitleaks.json",
    "public-agent-run-bundle-gitleaks-findings.json",
    "Download uploaded public agent run bundle",
    "actions/download-artifact@v4",
    "path: .tmp/public-agent-run-bundle-uploaded",
    "Verify uploaded public agent run bundle contents",
    "--bundle-dir .tmp/public-agent-run-bundle-uploaded",
    "--report .tmp/public-agent-run-bundle-uploaded-verification.json",
    "public-agent-run-bundle-uploaded-verification.json",
    "Scan uploaded public agent run bundle with Gitleaks",
    "--report .tmp/public-agent-run-bundle-uploaded-gitleaks.json",
    "public-agent-run-bundle-uploaded-gitleaks.json",
    "public-agent-run-bundle-uploaded-gitleaks-findings.json",
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
    "Sanitized exposed reasoning / CoT-like trace directory:",
    "reasoning-traces/",
    "Public bundle Gitleaks report:",
    "Uploaded public bundle verification report:",
    "Uploaded public bundle Gitleaks report:",
    "If the run artifact exposes reasoning / CoT-like trace text, it is part of the public lab evidence after sanitizer replacement.",
    "Public artifacts are redacted, sanitized, indexed, verified for required structure, scanned for secret-like strings, and include exposed reasoning traces when present.",
    "uploaded artifact Gitleaks scan analysis",
]

REQUIRED_BUNDLE_TEXT = [
    '\"policy-agent-container-exit-code.txt\"',
    '\"policy-agent-diff-name-only.txt\"',
    '\"policy-agent-diff.patch\"',
    '\"policy-agent-copied-files.txt\"',
    '\"policy-agent-container-stdout.txt\"',
    '\"policy-agent-container-stderr.txt\"',
    '\"policy-container-mounts.txt\"',
    'line_list(diag / \"policy-agent-diff-name-only.txt\")',
]

REQUIRED_ENRICH_TEXT = [
    "SANITIZED_PUBLIC_FILES",
    "REASONING_TRACE_FILES",
    '\"codex-events.jsonl\"',
    '\"codex-last-message.txt\"',
    '\"codex-stderr.txt\"',
    '\"codex-stdout.txt\"',
    '\"policy-agent-container-stdout.txt\"',
    '\"policy-agent-container-stderr.txt\"',
    '\"npm-install-codex.txt\"',
    '\"policy-container-mounts.txt\"',
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

REQUIRED_VERIFY_TEXT = [
    "REQUIRED_ROOT_FILES",
    "REQUIRED_DIRS",
    "observation-summary.md",
    "observation-summary.json",
    "reasoning-traces",
    "sanitized",
    "FORBIDDEN_PUBLIC_PATTERNS",
    "verify_public_agent_run_bundle",
    "public agent run bundle verification passed",
]

REQUIRED_GITLEAKS_TEXT = [
    "scan_scope",
    "public-agent-run-bundle-only",
    "repo_wide_scan",
    "False",
    "ghcr.io/gitleaks/gitleaks:v8.30.1",
    "--no-git",
    "--redact",
    "--report-format=json",
    "public bundle Gitleaks scan passed",
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
    verify = VERIFY.read_text(encoding="utf-8")
    gitleaks = GITLEAKS.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")

    require_all(workflow, REQUIRED_WORKFLOW_TEXT, "policy agent workflow")
    reject_all(workflow, FORBIDDEN_WORKFLOW_TEXT, "policy agent workflow")
    require_all(bundle, REQUIRED_BUNDLE_TEXT, "public bundle builder")
    require_all(enrich, REQUIRED_ENRICH_TEXT, "public bundle enrichment script")
    require_all(verify, REQUIRED_VERIFY_TEXT, "public bundle verifier")
    require_all(gitleaks, REQUIRED_GITLEAKS_TEXT, "public bundle Gitleaks scanner")
    require_all(doc, REQUIRED_DOC_TEXT, "public agent run bundle doc")
    reject_all(doc, FORBIDDEN_DOC_TEXT, "public agent run bundle doc")

    if workflow.index("Collect diagnostics artifact") > workflow.index("Build redacted public agent run bundle"):
        raise SystemExit("public bundle must be built after diagnostics collection")
    if workflow.index("Build redacted public agent run bundle") > workflow.index("Enrich public agent run bundle with sanitized logs and reasoning traces"):
        raise SystemExit("public bundle must be enriched after bundle build")
    if workflow.index("Enrich public agent run bundle with sanitized logs and reasoning traces") > workflow.index("Verify public agent run bundle contents"):
        raise SystemExit("public bundle must be verified after enrichment")
    if workflow.index("Verify public agent run bundle contents") > workflow.index("Scan public agent run bundle with Gitleaks"):
        raise SystemExit("public bundle must be scanned after pre-upload verification")
    if workflow.index("Scan public agent run bundle with Gitleaks") > workflow.index("Upload redacted public agent run bundle"):
        raise SystemExit("public bundle upload must occur after pre-upload Gitleaks scan")
    if workflow.index("Upload redacted public agent run bundle") > workflow.index("Download uploaded public agent run bundle"):
        raise SystemExit("uploaded public bundle must be downloaded after upload")
    if workflow.index("Download uploaded public agent run bundle") > workflow.index("Verify uploaded public agent run bundle contents"):
        raise SystemExit("uploaded public bundle must be verified after download")
    if workflow.index("Verify uploaded public agent run bundle contents") > workflow.index("Scan uploaded public agent run bundle with Gitleaks"):
        raise SystemExit("uploaded public bundle must be scanned after uploaded verification")
    if workflow.index("Scan uploaded public agent run bundle with Gitleaks") > workflow.index("Upload diagnostics artifact"):
        raise SystemExit("diagnostics upload must include uploaded bundle Gitleaks report")

    print("policy agent public bundle contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
