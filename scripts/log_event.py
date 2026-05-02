#!/usr/bin/env python3
"""Append Prompt Vote Lab JSONL events.

This script is intentionally dependency-free. It writes one JSON object per line
and avoids secrets by accepting only explicit non-secret values.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_OUT = ".tmp/events.jsonl"


def parse_payload(raw: str) -> dict[str, Any]:
    if not raw:
        return {}
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise SystemExit("payload_json must decode to an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--event-type", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--week", default="")
    parser.add_argument("--candidate-rank", default="")
    parser.add_argument("--issue-number", default="")
    parser.add_argument("--pr-number", default="")
    parser.add_argument("--model", default="")
    parser.add_argument("--api-call-count", default="")
    parser.add_argument("--sdk-max-retries", default="")
    parser.add_argument("--payload-json", default="{}")
    args = parser.parse_args()

    payload = parse_payload(args.payload_json)
    event = {
        "schema_version": "event-logging-v1.0",
        "event_type": args.event_type,
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": args.source,
        "status": args.status,
        "week": args.week,
        "candidate_rank": args.candidate_rank,
        "issue_number": args.issue_number,
        "pr_number": args.pr_number,
        "workflow": os.getenv("GITHUB_WORKFLOW", ""),
        "run_id": os.getenv("GITHUB_RUN_ID", ""),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT", ""),
        "commit_sha": os.getenv("GITHUB_SHA", ""),
        "branch": os.getenv("GITHUB_REF_NAME", ""),
        "model": args.model,
        "api_call_count": args.api_call_count,
        "sdk_max_retries": args.sdk_max_retries,
        "payload": payload,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Logged {args.event_type} to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
