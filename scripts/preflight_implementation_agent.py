#!/usr/bin/env python3
"""Preflight checks before a paid implementation-agent run.

This script does not call any model API.
It validates local run configuration before the workflow is allowed to install
API dependencies or invoke the implementation backend.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
from typing import Any


ALLOWED_MODELS = {"gpt-5-nano"}
MAX_OUTPUT_TOKENS_LIMIT = 12000
REQUIRED_RUN_REASONS = {"normal-weekly-run", "support-unlocked-run"}


def load_candidates(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("eligible candidates must be a JSON list")
    return data


def parse_int(value: str, name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise SystemExit(f"{name} must be an integer") from exc
    return parsed


def validate_env_secret(eligible_count: int) -> None:
    has_secret = bool(
        os.getenv("OPENAI_API_KEY_")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("OPENAI_IMPLEMENTATION_API_KEY")
    )
    if eligible_count > 0 and not has_secret:
        raise SystemExit("eligible candidates exist, but no implementation-agent secret is configured")
    if eligible_count == 0:
        print("No eligible candidates. Secret is not required.")


def validate_candidate(candidate: dict[str, Any]) -> None:
    candidate_type = candidate.get("candidate_type")
    if candidate_type != "prompt-proposal":
        raise SystemExit(f"eligible candidate must be prompt-proposal, got {candidate_type!r}")
    rank = parse_int(str(candidate.get("rank")), "rank")
    if rank not in {1, 2, 3}:
        raise SystemExit(f"eligible rank must be 1, 2, or 3, got {rank}")
    reason = candidate.get("run_reason")
    if reason not in REQUIRED_RUN_REASONS:
        raise SystemExit(f"unexpected run_reason: {reason!r}")
    if rank == 1 and reason != "normal-weekly-run":
        raise SystemExit("rank 1 must use normal-weekly-run")
    if rank in {2, 3} and reason != "support-unlocked-run":
        raise SystemExit(f"rank {rank} must use support-unlocked-run")
    body = str(candidate.get("body") or "").strip()
    if not body:
        raise SystemExit(f"eligible rank {rank} has empty prompt body")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eligible", default=".tmp/eligible-candidates.json")
    parser.add_argument("--model", default=os.getenv("IMPLEMENTATION_MODEL", "gpt-5-nano"))
    parser.add_argument("--max-output-tokens", default=os.getenv("MAX_OUTPUT_TOKENS", "12000"))
    parser.add_argument("--sdk-max-retries", default=os.getenv("SDK_MAX_RETRIES", "0"))
    parser.add_argument("--api-call-limit-per-candidate", default="1")
    args = parser.parse_args()

    candidates = load_candidates(Path(args.eligible))
    if len(candidates) > 3:
        raise SystemExit("at most three eligible candidates are allowed")

    model = args.model.strip()
    if model not in ALLOWED_MODELS:
        raise SystemExit(f"implementation model {model!r} is not allowed")

    max_output_tokens = parse_int(str(args.max_output_tokens), "max_output_tokens")
    if max_output_tokens < 1 or max_output_tokens > MAX_OUTPUT_TOKENS_LIMIT:
        raise SystemExit(f"max_output_tokens must be between 1 and {MAX_OUTPUT_TOKENS_LIMIT}")

    sdk_max_retries = parse_int(str(args.sdk_max_retries), "sdk_max_retries")
    if sdk_max_retries != 0:
        raise SystemExit("sdk_max_retries must be 0")

    api_call_limit = parse_int(str(args.api_call_limit_per_candidate), "api_call_limit_per_candidate")
    if api_call_limit != 1:
        raise SystemExit("api_call_limit_per_candidate must be 1")

    seen_ranks: set[int] = set()
    for candidate in candidates:
        validate_candidate(candidate)
        rank = int(candidate["rank"])
        if rank in seen_ranks:
            raise SystemExit(f"duplicate eligible rank: {rank}")
        seen_ranks.add(rank)

    validate_env_secret(len(candidates))

    summary = {
        "eligible_count": len(candidates),
        "eligible_ranks": sorted(seen_ranks),
        "model": model,
        "max_output_tokens": max_output_tokens,
        "sdk_max_retries": sdk_max_retries,
        "api_call_limit_per_candidate": api_call_limit,
        "api_call_performed": False,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
