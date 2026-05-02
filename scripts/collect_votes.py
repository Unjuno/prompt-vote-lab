#!/usr/bin/env python3
"""Collect prompt proposal votes from GitHub Issues.

This script uses GitHub's API through the GITHUB_TOKEN available in Actions.
It writes a markdown summary and a JSON artifact under .tmp/.

A virtual no-change baseline candidate is inserted every week so low-vote weeks
produce no implementation run by default.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen


@dataclass
class Candidate:
    rank: int
    issue_number: int
    title: str
    url: str
    vote_count: int
    body: str
    candidate_type: str


def github_get(url: str, token: str) -> Any:
    req = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "prompt-vote-lab-weekly-vote-runner",
        },
    )
    with urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))


def extract_section(body: str, heading: str) -> str:
    """Extract a GitHub issue-form section by heading text.

    GitHub issue forms render textarea labels as Markdown headings, usually
    `### Heading`, but older hand-written issues may use `## Heading`.
    """
    if not body:
        return ""
    pattern = re.compile(
        rf"^#{{2,6}}\s+{re.escape(heading)}\s*$\n(?P<content>.*?)(?=^#{{2,6}}\s+|\Z)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    if not match:
        return ""
    content = match.group("content").strip()
    return content.replace("_No response_", "").strip()


def extract_voted_prompt(body: str, fallback: str) -> str:
    if not body:
        return fallback
    for heading in ["Voted prompt", "Prompt", "Exact prompt"]:
        section = extract_section(body, heading)
        if section:
            return section
    return fallback


def collect(repo: str, token: str, no_change_baseline: int) -> list[Candidate]:
    query = quote(f"repo:{repo} is:issue is:open label:prompt-proposal")
    search_url = f"https://api.github.com/search/issues?q={query}&sort=reactions&order=desc&per_page=50"
    data = github_get(search_url, token)
    issues = data.get("items", [])

    candidates: list[Candidate] = [
        Candidate(
            rank=0,
            issue_number=0,
            title="[Baseline]: No change this week",
            url="",
            vote_count=no_change_baseline,
            body="No implementation run this week. The prompt game must beat the weekly no-change baseline.",
            candidate_type="no-change-baseline",
        )
    ]

    for item in issues:
        reactions = item.get("reactions") or {}
        plus_one = int(reactions.get("+1") or 0)
        candidates.append(
            Candidate(
                rank=0,
                issue_number=int(item["number"]),
                title=str(item.get("title") or "unrecorded"),
                url=str(item.get("html_url") or ""),
                vote_count=plus_one,
                body=extract_voted_prompt(str(item.get("body") or ""), str(item.get("title") or "unrecorded")),
                candidate_type="prompt-proposal",
            )
        )

    candidates.sort(key=lambda c: (-c.vote_count, c.issue_number))
    for index, candidate in enumerate(candidates, start=1):
        candidate.rank = index
    return candidates


def issue_cell(candidate: Candidate) -> str:
    if candidate.issue_number == 0:
        return "baseline"
    return f"[#{candidate.issue_number}]({candidate.url})"


def write_outputs(candidates: list[Candidate], week: str, out_dir: Path, no_change_baseline: int) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    top3 = candidates[:3]
    (out_dir / "weekly-candidates.json").write_text(
        json.dumps([asdict(c) for c in top3], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        f"# Weekly vote summary: {week}",
        "",
        "Votes are counted from 👍 reactions on open `prompt-proposal` issues.",
        f"A virtual no-change baseline candidate is inserted every week with {no_change_baseline} votes.",
        "If the baseline ranks first, no implementation run should be created.",
        "",
        "| Rank | Candidate | Type | 👍 votes | Title |",
        "|---:|---|---|---:|---|",
    ]
    for candidate in top3:
        lines.append(
            f"| {candidate.rank} | {issue_cell(candidate)} | {candidate.candidate_type} | {candidate.vote_count} | {candidate.title} |"
        )
    if not top3:
        lines.append("| unrecorded | unrecorded | unrecorded | unrecorded | No candidates found |")
    lines.append("")
    (out_dir / "weekly-vote-summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--week", required=True)
    parser.add_argument("--out-dir", default=".tmp")
    parser.add_argument("--no-change-baseline", type=int, default=20)
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 2

    if args.no_change_baseline < 0:
        print("no-change baseline must be non-negative", file=sys.stderr)
        return 2

    candidates = collect(args.repo, token, args.no_change_baseline)
    write_outputs(candidates, args.week, Path(args.out_dir), args.no_change_baseline)
    real_count = sum(1 for c in candidates if c.candidate_type == "prompt-proposal")
    print(f"Collected {real_count} prompt candidates plus no-change baseline={args.no_change_baseline}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
