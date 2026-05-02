#!/usr/bin/env python3
"""Generate a Prompt Vote Lab blog report with OpenAI Responses API.

This script writes Markdown reports only. It never modifies lab/.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from openai import OpenAI


ROOT = Path(__file__).resolve().parents[1]


def read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else "unrecorded"


def build_input(args: argparse.Namespace) -> dict[str, str]:
    return {
        "week": args.week,
        "candidate_rank": args.candidate_rank,
        "issue_number": args.issue_number,
        "vote_count": args.vote_count,
        "no_change_baseline": args.no_change_baseline,
        "support_usd": args.support_usd,
        "selected_prompt": args.selected_prompt,
        "expected_result": args.expected_result,
        "implementation_pr": args.implementation_pr,
        "terminal_state": args.terminal_state,
        "safety_result": args.safety_result,
        "changed_files": args.changed_files,
        "reviewer_notes": args.reviewer_notes,
        "run_log": read_optional(ROOT / args.run_log_path) if args.run_log_path else "unrecorded",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", required=True)
    parser.add_argument("--candidate-rank", required=True)
    parser.add_argument("--issue-number", default="unrecorded")
    parser.add_argument("--vote-count", default="unrecorded")
    parser.add_argument("--no-change-baseline", default="20")
    parser.add_argument("--support-usd", default="0")
    parser.add_argument("--selected-prompt", default="unrecorded")
    parser.add_argument("--expected-result", default="unrecorded")
    parser.add_argument("--implementation-pr", default="unrecorded")
    parser.add_argument("--terminal-state", required=True, choices=["merged", "rejected", "unsafe", "failed", "no-change", "unrecorded"])
    parser.add_argument("--safety-result", default="unrecorded")
    parser.add_argument("--changed-files", default="unrecorded")
    parser.add_argument("--reviewer-notes", default="unrecorded")
    parser.add_argument("--run-log-path", default="")
    parser.add_argument("--model", default=os.getenv("EVALUATION_MODEL", "gpt-5"))
    parser.add_argument("--max-output-tokens", type=int, default=int(os.getenv("EVAL_MAX_OUTPUT_TOKENS", "6000")))
    parser.add_argument("--out-dir", default="docs/blog")
    parser.add_argument("--hn-out-dir", default="docs/hn-drafts")
    parser.add_argument("--write-hn-draft", action="store_true")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set", file=sys.stderr)
        return 2

    report_prompt = read_optional(ROOT / "prompts" / "blog-report-v1.0.md")
    hn_prompt = read_optional(ROOT / "prompts" / "hn-draft-v1.0.md")
    input_data = build_input(args)

    client = OpenAI()
    response = client.responses.create(
        model=args.model,
        input=[
            {
                "role": "developer",
                "content": report_prompt,
            },
            {
                "role": "user",
                "content": json.dumps(input_data, indent=2, ensure_ascii=False),
            },
        ],
        max_output_tokens=args.max_output_tokens,
    )

    out_dir = ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"{args.week}-rank-{args.candidate_rank}.md"
    report_path.write_text(response.output_text.rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {report_path.relative_to(ROOT)}")

    if args.write_hn_draft:
        hn_response = client.responses.create(
            model=args.model,
            input=[
                {
                    "role": "developer",
                    "content": hn_prompt,
                },
                {
                    "role": "user",
                    "content": "## Weekly report\n\n" + response.output_text + "\n\n## Recorded data\n\n" + json.dumps(input_data, indent=2, ensure_ascii=False),
                },
            ],
            max_output_tokens=min(args.max_output_tokens, 2500),
        )
        hn_out_dir = ROOT / args.hn_out_dir
        hn_out_dir.mkdir(parents=True, exist_ok=True)
        hn_path = hn_out_dir / f"{args.week}-rank-{args.candidate_rank}.md"
        hn_path.write_text(hn_response.output_text.rstrip() + "\n", encoding="utf-8")
        print(f"Wrote {hn_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
