#!/usr/bin/env python3
"""Write a terminal run report without calling an LLM.

This is a deterministic fallback report generator used before the evaluation model workflow exists.
"""

from __future__ import annotations

import argparse
from pathlib import Path


CLASSIFICATIONS = {
    "merged": "Hit",
    "rejected": "Rejected",
    "unsafe": "Unsafe",
    "failed": "Rejected",
    "no-change": "Underbuild",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", required=True)
    parser.add_argument("--candidate-rank", required=True)
    parser.add_argument("--issue-number", required=True)
    parser.add_argument("--vote-count", default="unrecorded")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--pr", default="unrecorded")
    parser.add_argument("--state", required=True, choices=sorted(CLASSIFICATIONS))
    parser.add_argument("--safety", default="unrecorded")
    parser.add_argument("--changed-files", default="unrecorded")
    parser.add_argument("--notes", default="unrecorded")
    args = parser.parse_args()

    classification = CLASSIFICATIONS[args.state]
    out_dir = Path("docs/reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{args.week}-rank-{args.candidate_rank}.md"

    content = f"""# {args.week} rank {args.candidate_rank} report

## Summary

- Week: {args.week}
- Rank: {args.candidate_rank}
- Issue: #{args.issue_number}
- Votes: {args.vote_count}
- PR: {args.pr}
- Terminal state: {args.state}
- Safety check: {args.safety}
- Expectation-gap classification: {classification}

## Selected prompt

{args.prompt}

## Changed files

{args.changed_files}

## Notes

{args.notes}

## Interpretation

This report was generated deterministically from recorded workflow inputs.
It does not use an evaluation model.
Missing facts are recorded as `unrecorded`.
"""
    path.write_text(content, encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
