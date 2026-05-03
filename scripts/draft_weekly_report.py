#!/usr/bin/env python3
"""Draft a Prompt Vote Lab weekly report without calling a model API.

The script intentionally uses explicit inputs and repository files only.
It writes a Markdown report draft under runs/<week>-report.md by default.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_GAPS = {
    "Hit",
    "Partial",
    "Misread",
    "Overbuild",
    "Underbuild",
    "Rule conflict",
    "Unsafe",
    "Rejected",
    "Unknown",
}
SAFE_WEEK_RE = re.compile(r"^[A-Za-z0-9._-]{1,80}$")


def validate_week(value: str) -> str:
    value = value.strip()
    if not SAFE_WEEK_RE.fullmatch(value):
        raise SystemExit("week must contain only letters, numbers, dots, underscores, and hyphens")
    return value


def resolve_repo_path(value: str) -> Path:
    rel = value.strip()
    if not rel:
        raise ValueError("empty path")
    path = (ROOT / rel).resolve()
    if ROOT.resolve() not in path.parents and path != ROOT.resolve():
        raise SystemExit(f"path escapes repository root: {rel}")
    return path


def read_optional(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return "unrecorded"


def normalize_gap(value: str) -> str:
    value = value.strip() or "Unknown"
    for allowed in ALLOWED_GAPS:
        if value.lower() == allowed.lower():
            return allowed
    return "Unknown"


def bullet_value(value: str) -> str:
    value = value.strip()
    return value if value else "unrecorded"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", required=True)
    parser.add_argument("--selected-prompt", default="unrecorded")
    parser.add_argument("--issue-number", default="unrecorded")
    parser.add_argument("--pr-number", default="unrecorded")
    parser.add_argument("--candidate-rank", default="unrecorded")
    parser.add_argument("--vote-count", default="unrecorded")
    parser.add_argument("--baseline-votes", default="20")
    parser.add_argument("--outcome", default="Unknown")
    parser.add_argument("--expectation-gap", default="Unknown")
    parser.add_argument("--run-reason", default="unrecorded")
    parser.add_argument("--vote-summary", default="")
    parser.add_argument("--implementation-summary", default="")
    parser.add_argument("--reputation-memory", default="")
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    week = validate_week(args.week)
    gap = normalize_gap(args.expectation_gap)

    if args.out:
        out_path = resolve_repo_path(args.out)
        if not str(out_path.relative_to(ROOT)).startswith("runs/"):
            raise SystemExit("report output must be under runs/")
    else:
        out_path = ROOT / f"runs/{week}-report.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    vote_summary_text = read_optional(resolve_repo_path(args.vote_summary)) if args.vote_summary else "unrecorded"
    implementation_summary_text = read_optional(resolve_repo_path(args.implementation_summary)) if args.implementation_summary else "unrecorded"
    reputation_memory = args.reputation_memory.strip() or "No automated trust rating is computed. Players should use this public outcome as qualitative memory for future votes."

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    lines = [
        f"# Weekly Prompt Game Report: {week}",
        "",
        "This is a model-free draft report generated from explicit workflow inputs and repository files.",
        "",
        "It is not an automatic final judgment and it does not compute automated trust ratings.",
        "",
        "## Round summary",
        "",
        f"- Week: {bullet_value(week)}",
        f"- Generated at: {now}",
        f"- No-change baseline: {bullet_value(args.baseline_votes)} virtual votes",
        f"- Selected candidate rank: {bullet_value(args.candidate_rank)}",
        f"- Selected candidate votes: {bullet_value(args.vote_count)}",
        f"- Run reason: {bullet_value(args.run_reason)}",
        "",
        "## Selected candidate",
        "",
        f"- Issue: #{bullet_value(args.issue_number)}",
        f"- Implementation PR: #{bullet_value(args.pr_number)}",
        "",
        "### Selected prompt",
        "",
        args.selected_prompt.strip() or "unrecorded",
        "",
        "## Outcome",
        "",
        f"- Outcome: {bullet_value(args.outcome)}",
        f"- Expectation gap: {gap}",
        "",
        "## Reputation memory",
        "",
        reputation_memory,
        "",
        "## Source material",
        "",
        "### Vote summary",
        "",
        vote_summary_text,
        "",
        "### Implementation summary",
        "",
        implementation_summary_text,
        "",
        "## Human review note",
        "",
        "This report is a draft. A maintainer should review the outcome label, expectation-gap label, and reputation-memory note before treating it as canonical game memory.",
        "",
    ]

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
