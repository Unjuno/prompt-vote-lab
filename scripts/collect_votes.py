#!/usr/bin/env python3
"""Collect prompt proposal votes from GitHub Issues.

This script uses GitHub's API through the GITHUB_TOKEN available in Actions.
It writes a markdown summary and a JSON artifact under .tmp/.
"""

from __future__ import annotations

import argparse
import json
import os
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


def extract_voted_prompt(body: str, fallback: str) -> str:
    if not body:
        return fallback
    marker = "## Voted prompt"
    if marker not in body:
        return fallback
    after = body.split(marker, 1)[1].strip()
    if "## " in after:
        after = after.split("## ", 1)[0].strip()
    return after or fallback


def collect(repo: str, token: str) -> list[Candidate]:
    query = quote(f"repo:{repo} is:issue is:open label:prompt-proposal")
    search_url = f"https://api.github.com/search/issues?q={query}&sort=reactions&order=desc&per_page=50"
    data = github_get(search_url, token)
    issues = data.get("items", [])

    candidates: list[Candidate] = []
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
            )
        )

    candidates.sort(key=lambda c: (-c.vote_count, c.issue_number))
    for index, candidate in enumerate(candidates, start=1):
        candidate.rank = index
    return candidates


def write_outputs(candidates: list[Candidate], week: str, out_dir: Path) -> None:
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
        "",
        "| Rank | Issue | 👍 votes | Title |",
        "|---:|---:|---:|---|",
    ]
    for candidate in top3:
        lines.append(
            f"| {candidate.rank} | [#{candidate.issue_number}]({candidate.url}) | {candidate.vote_count} | {candidate.title} |"
        )
    if not top3:
        lines.append("| unrecorded | unrecorded | unrecorded | No candidates found |")
    lines.append("")
    (out_dir / "weekly-vote-summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--week", required=True)
    parser.add_argument("--out-dir", default=".tmp")
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 2

    candidates = collect(args.repo, token)
    write_outputs(candidates, args.week, Path(args.out_dir))
    print(f"Collected {len(candidates)} prompt candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
