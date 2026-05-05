#!/usr/bin/env python3
"""Write redacted public run logs for Prompt Vote Lab.

This script is API-free and deterministic. It intentionally records public
experiment evidence without storing raw model output, raw stderr, or secrets.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {"started", "passed", "failed", "skipped"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--model", default="unrecorded")
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--run-number", default="unrecorded")
    parser.add_argument("--week", default="unrecorded")
    parser.add_argument("--candidate-rank", default="unrecorded")
    parser.add_argument("--issue-number", default="unrecorded")
    parser.add_argument("--vote-count", default="unrecorded")
    parser.add_argument("--base-sha", default="unrecorded")
    parser.add_argument("--branch", default="unrecorded")
    parser.add_argument("--attempt-count", default="1")
    parser.add_argument("--retry-policy", default="none")
    parser.add_argument("--fallback-policy", default="none")
    parser.add_argument("--auto-merge-policy", default="disabled")
    parser.add_argument("--status", required=True, choices=sorted(ALLOWED_STATUSES))
    parser.add_argument("--failure-step", default="none")
    parser.add_argument("--failure-type", default="none")
    parser.add_argument("--error-summary", default="none")
    parser.add_argument("--changed-files", default="")
    parser.add_argument("--checks", default="{}")
    args = parser.parse_args()

    changed_files = [item for item in args.changed_files.split(",") if item]
    try:
        checks: dict[str, Any] = json.loads(args.checks)
    except json.JSONDecodeError:
        checks = {"parse_error": "checks was not valid JSON"}

    data = {
        "schema": "prompt-vote-lab-public-run-log-v1",
        "provider": args.provider,
        "runner": args.runner,
        "model": args.model,
        "workflow": args.workflow,
        "run_number": args.run_number,
        "week": args.week,
        "candidate_rank": args.candidate_rank,
        "issue_number": args.issue_number,
        "vote_count": args.vote_count,
        "base_sha": args.base_sha,
        "branch": args.branch,
        "attempt_count": args.attempt_count,
        "retry_policy": args.retry_policy,
        "fallback_policy": args.fallback_policy,
        "auto_merge_policy": args.auto_merge_policy,
        "status": args.status,
        "failure_step": args.failure_step,
        "failure_type": args.failure_type,
        "error_summary": args.error_summary[:500],
        "changed_files": changed_files,
        "checks": checks,
        "redaction": {
            "raw_stderr": "not published",
            "raw_model_output": "not published",
            "raw_codex_jsonl": "not published",
            "secrets": "not published",
        },
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
