#!/usr/bin/env python3
"""Run a constrained Prompt Vote Lab implementation-agent attempt.

This script currently uses the OpenAI Responses API as the backend for the
implementation agent, but the public experiment concept is an agent run:

Prompt → 20-vote gate → agent PR → inherited lab state

This script intentionally writes only:
- lab/index.html
- lab/style.css
- lab/app.js

Agent-run policy:
- one bounded implementation-agent attempt per candidate per workflow run
- SDK retries disabled
- no automatic fallback
- no automatic merge
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from openai import OpenAI


ROOT = Path(__file__).resolve().parents[1]
LAB_FILES = {
    "index_html": ROOT / "lab" / "index.html",
    "style_css": ROOT / "lab" / "style.css",
    "app_js": ROOT / "lab" / "app.js",
}

MAX_PROMPT_CHARS = int(os.getenv("MAX_IMPLEMENTATION_PROMPT_CHARS", "120000"))
MAX_OUTPUT_TOKENS_LIMIT = 5000


SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "index_html": {"type": "string"},
        "style_css": {"type": "string"},
        "app_js": {"type": "string"},
        "final_message": {"type": "string"},
        "ignored_unsupported_parts": {"type": "string"},
        "manual_test_steps": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "index_html",
        "style_css",
        "app_js",
        "final_message",
        "ignored_unsupported_parts",
        "manual_test_steps",
    ],
}


def resolve_openai_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY_") or os.getenv("OPENAI_API_KEY")
    if not key:
        print("Implementation-agent backend secret is not set.", file=sys.stderr)
        raise SystemExit(2)
    return key


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else "unrecorded"


def enforce_prompt_budget(prompt: str) -> None:
    if len(prompt) > MAX_PROMPT_CHARS:
        raise SystemExit(
            f"Implementation prompt is too large: {len(prompt)} chars > {MAX_PROMPT_CHARS}. "
            "Refusing to start the implementation-agent attempt."
        )


def build_prompt(args: argparse.Namespace) -> str:
    rules = []
    for rel in [
        "rules/static-ui-v1.0.md",
        "rules/agent-run-policy-v1.0.md",
        "rules/model-policy-v1.1.md",
        "rules/merge-policy-v1.0.md",
        "rules/operational-decisions-v1.1.md",
        "rules/no-external-resources-v1.0.md",
        "rules/local-data-store-v1.0.md",
        "rules/single-shot-api-v1.0.md",
    ]:
        rules.append(f"# {rel}\n\n{read_optional(ROOT / rel)}")

    lab_snapshot = []
    for name, path in LAB_FILES.items():
        lab_snapshot.append(f"# {path.relative_to(ROOT)}\n\n```\n{read(path)}\n```")

    prompt = "\n\n".join(
        [
            "You are the implementation agent for Prompt Vote Lab.",
            "Modify exactly these three lab files and return their full replacement contents as JSON.",
            "Do not create additional files. Do not use network calls, external scripts, forms, login, payment, cookies, eval, or trackers.",
            "Controlled new Function(...) is allowed only when the function body is fixed by repository code and not assembled from user input, URL data, localStorage, sessionStorage, IndexedDB, imported JSON, GitHub Issue text, or any external source.",
            "Preserve the static-only GitHub Pages design. Prefer small, readable changes.",
            "The experiment intentionally keeps complexity inside three files.",
            "This is one bounded implementation-agent attempt. Do not ask for a hidden retry or another pass.",
            "The current lab files are the inherited lab state from the main branch.",
            "## Run metadata",
            f"week: {args.week}",
            f"candidate_rank: {args.candidate_rank}",
            f"issue_number: {args.issue_number}",
            f"vote_count: {args.vote_count}",
            f"run_reason: {args.run_reason}",
            f"model: {args.model}",
            f"temperature_policy: {args.temperature_policy}",
            f"top_p_policy: {args.top_p_policy}",
            f"max_output_tokens: {args.max_output_tokens}",
            "## Selected prompt",
            args.voted_prompt,
            "## Active rules",
            "\n\n".join(rules),
            "## Current inherited lab files",
            "\n\n".join(lab_snapshot),
            "## Output requirement",
            "Return valid structured JSON only. Include full contents for index_html, style_css, and app_js.",
        ]
    )
    enforce_prompt_budget(prompt)
    return prompt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", required=True)
    parser.add_argument("--candidate-rank", required=True)
    parser.add_argument("--issue-number", required=True)
    parser.add_argument("--voted-prompt", required=True)
    parser.add_argument("--vote-count", default="unrecorded")
    parser.add_argument("--run-reason", default="normal-weekly-run")
    parser.add_argument("--model", default=os.getenv("IMPLEMENTATION_MODEL", "gpt-5.4-nano"))
    parser.add_argument("--max-output-tokens", type=int, default=int(os.getenv("MAX_OUTPUT_TOKENS", "5000")))
    parser.add_argument("--temperature-policy", default=os.getenv("TEMPERATURE_POLICY", "model-default"))
    parser.add_argument("--top-p-policy", default=os.getenv("TOP_P_POLICY", "model-default"))
    parser.add_argument("--summary-out", default=".tmp/implementation-summary.md")
    args = parser.parse_args()

    api_key = resolve_openai_api_key()

    if args.max_output_tokens > MAX_OUTPUT_TOKENS_LIMIT:
        print(
            f"max_output_tokens above {MAX_OUTPUT_TOKENS_LIMIT} is not allowed for implementation-agent attempts",
            file=sys.stderr,
        )
        return 2

    prompt = build_prompt(args)
    client = OpenAI(api_key=api_key, max_retries=0, timeout=120.0)

    response = client.responses.create(
        model=args.model,
        input=[
            {
                "role": "developer",
                "content": "You are a constrained code-generation worker. Return only the requested structured output. This is one bounded implementation-agent attempt.",
            },
            {"role": "user", "content": prompt},
        ],
        max_output_tokens=args.max_output_tokens,
        text={
            "format": {
                "type": "json_schema",
                "name": "prompt_vote_lab_files",
                "schema": SCHEMA,
                "strict": True,
            }
        },
    )

    try:
        data = json.loads(response.output_text)
    except json.JSONDecodeError as exc:
        print("Implementation agent did not return valid JSON", file=sys.stderr)
        print(response.output_text, file=sys.stderr)
        raise exc

    for key, path in LAB_FILES.items():
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Missing non-empty {key}")
        path.write_text(value.rstrip() + "\n", encoding="utf-8")

    summary_path = ROOT / args.summary_out
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary = [
        f"# Implementation-agent summary for {args.week} rank {args.candidate_rank}",
        "",
        f"- model: `{args.model}`",
        "- agent_attempts: 1",
        "- sdk_max_retries: 0",
        "- sdk_timeout_seconds: 120",
        f"- temperature_policy: {args.temperature_policy}",
        f"- top_p_policy: {args.top_p_policy}",
        f"- max_output_tokens: {args.max_output_tokens}",
        f"- prompt_chars: {len(prompt)}",
        f"- issue: #{args.issue_number}",
        f"- votes: {args.vote_count}",
        f"- run_reason: {args.run_reason}",
        "",
        "## Final message",
        "",
        str(data.get("final_message", "unrecorded")),
        "",
        "## Ignored unsupported parts",
        "",
        str(data.get("ignored_unsupported_parts", "unrecorded")),
        "",
        "## Manual test steps",
        "",
    ]
    for step in data.get("manual_test_steps", []):
        summary.append(f"- {step}")
    summary_path.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print(f"Wrote lab files using implementation model {args.model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
