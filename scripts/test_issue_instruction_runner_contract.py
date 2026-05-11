#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_codex_issue_instruction_canary.sh"
WORKFLOW = ROOT / ".github" / "workflows" / "codex-fixed-issue-instruction-canary-run.yml"

REQUIRED_RUNNER_TEXT = [
    "python scripts/create_codex_issue_instruction_packet.py",
    "ISSUE_JSON_PATH",
    "-v \"$task:/task:ro\"",
    "-v \"$work:/work:rw\"",
    "-v \"$runtime:/codex-runtime:rw\"",
    "-v \"$diag:/diagnostics:rw\"",
    "OPENAI_API_KEY present before login: yes",
    "OPENAI_API_KEY present before codex exec: no",
    "unset OPENAI_API_KEY",
    "task-write-test-exit-code.txt",
    "policy-denied-access.txt",
    "task-file-hashes.json",
    "task-selected-issue.json",
    "task-raw-issue-body.md",
    "task-issue-safety-analysis.json",
    "task-instruction-brief.md",
    "task-static-ui-v1.0.md",
    "task-agent-run-policy-v1.0.md",
    "/task/issue-safety-analysis.json",
    "Use /task/issue-safety-analysis.json as the repository-generated unsafe-instruction classification.",
    "--skip-git-repo-check",
    "first-canary-009",
]

REQUIRED_WORKFLOW_TEXT = [
    "name: Codex Fixed Issue Instruction Canary Run",
    "issue_number:",
    "candidate_rank:",
    "vote_count:",
    "Candidate rank within the comparison set. Use 1 for normal weekly winner, 2/3 for comparison runs.",
    "Vote count recorded for this candidate at selection time.",
    "CANDIDATE_RANK: ${{ inputs.candidate_rank }}",
    "VOTE_COUNT: ${{ inputs.vote_count }}",
    "candidate_rank must be 1, 2, or 3",
    "vote_count must be a non-negative integer",
    "issues: write",
    "CODEX_MODEL: gpt-5.4-nano",
    "RUN_WEEK: first-canary-009",
    "gh issue view \"$ISSUE_NUMBER\"",
    "--json number,title,body,url,author,createdAt,labels",
    "python scripts/scan_issue_safety.py",
    "--phase runtime",
    "bash scripts/apply_issue_safety_feedback.sh",
    "python scripts/check_issue_execution_gate.py",
    "--scan-json .tmp/issue-safety-runtime/scan.json",
    "--issue-json .tmp/issue-source/selected-issue.raw.json",
    "issue execution gate passed before Codex execution",
    "codex-fixed-issue-execution-gate-",
    "runtime Issue safety scan completed before task packet execution",
    "bash scripts/run_codex_issue_instruction_canary.sh",
    "--canary-id first-canary-009",
    "--runner-mode codex-cli-fixed-issue-instruction-packet-container",
    "--sandbox-mode docker-workdir-plus-readonly-issue-instruction-packet",
    "python scripts/build_public_agent_run_bundle.py",
    "python scripts/enrich_public_agent_run_bundle.py",
    "python scripts/verify_public_agent_run_bundle.py",
    "--report .tmp/public-agent-run-bundle-verification.json",
    "public-agent-run-bundle-verification.json",
    "--diagnostics-dir .tmp/canary-diagnostics",
    "--bundle-dir .tmp/public-agent-run-bundle",
    "--out-dir .tmp/public-agent-run-bundle",
    "codex-fixed-issue-public-agent-run-bundle-",
    "redacted public agent run bundle",
    "allowlisted raw evidence files",
    "sanitized diagnostic logs",
    "reasoning-traces/",
    "observation-summary.md",
    "observation-summary.json",
    "codex-fixed-issue-instruction-canary-diagnostics-",
    "codex-fixed-issue-instruction-canary-public-log-",
    "codex-fixed-issue-runtime-safety-scan-",
    "--candidate-rank \"$CANDIDATE_RANK\"",
    "--vote-count \"$VOTE_COUNT\"",
    "- Rank: $CANDIDATE_RANK",
    "- Votes: $VOTE_COUNT",
    "--retry-policy none",
    "--fallback-policy none",
    "--auto-merge-policy disabled",
]

FORBIDDEN_RUNNER_TEXT = [
    "-v \"$task:/task:rw\"",
    "cat " + "$" + "OPENAI_API_KEY",
    "echo " + "$" + "OPENAI_API_KEY",
]

FORBIDDEN_WORKFLOW_TEXT = [
    "--candidate-rank 1",
    "--vote-count 0",
    "- Rank: 1",
    "- Votes: 0",
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
    runner_text = RUNNER.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")

    require_all(runner_text, REQUIRED_RUNNER_TEXT, "runner")
    reject_all(runner_text, FORBIDDEN_RUNNER_TEXT, "runner")
    require_all(workflow_text, REQUIRED_WORKFLOW_TEXT, "workflow")
    reject_all(workflow_text, FORBIDDEN_WORKFLOW_TEXT, "workflow")

    if workflow_text.index("Validate dispatch inputs") > workflow_text.index("Capture diagnostics baseline"):
        raise SystemExit("Dispatch inputs must be validated before diagnostics baseline")
    if workflow_text.index("Check Issue execution gate") > workflow_text.index("Run Codex fixed Issue instruction packet once"):
        raise SystemExit("Issue execution gate must run before Codex execution")
    if workflow_text.index("Collect diagnostics artifact") > workflow_text.index("Build redacted public agent run bundle"):
        raise SystemExit("Public agent run bundle must be built after diagnostics are collected")
    if workflow_text.index("Build redacted public agent run bundle") > workflow_text.index("Enrich public agent run bundle with sanitized logs and reasoning traces"):
        raise SystemExit("Public agent run bundle must be enriched after it is built")
    if workflow_text.index("Enrich public agent run bundle with sanitized logs and reasoning traces") > workflow_text.index("Verify public agent run bundle contents"):
        raise SystemExit("Public agent run bundle must be verified after enrichment")
    if workflow_text.index("Verify public agent run bundle contents") > workflow_text.index("Upload redacted public agent run bundle"):
        raise SystemExit("Public agent run bundle upload must happen after verification")
    if runner_text.index("codex login --with-api-key") > runner_text.index("unset OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is unset before login, not after login")
    if runner_text.index("unset OPENAI_API_KEY") > runner_text.index("codex exec"):
        raise SystemExit("OPENAI_API_KEY is not unset before codex exec")

    print("fixed Issue instruction runner contract test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
