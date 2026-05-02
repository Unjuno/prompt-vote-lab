#!/usr/bin/env python3
"""Extract Prompt Vote Lab metadata from a PR body and labels."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FIELD_RE = re.compile(r"^-\s*(Week|Rank|Issue|Votes|Run reason):\s*(.+?)\s*$", re.MULTILINE)


def clean_issue(value: str) -> str:
    return value.strip().lstrip("#") or "unrecorded"


def terminal_state(labels: list[str]) -> str:
    mapping = {
        "pvl:merged": "merged",
        "pvl:rejected": "rejected",
        "pvl:unsafe": "unsafe",
        "pvl:failed": "failed",
        "pvl:no-change": "no-change",
    }
    found = [mapping[label] for label in labels if label in mapping]
    if len(found) == 1:
        return found[0]
    if len(found) > 1:
        return "failed"
    return "unrecorded"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--body-file", required=True)
    parser.add_argument("--labels-json", required=True)
    parser.add_argument("--out", default=".tmp/pr-metadata.json")
    args = parser.parse_args()

    body = Path(args.body_file).read_text(encoding="utf-8")
    labels = json.loads(args.labels_json)
    if labels and isinstance(labels[0], dict):
        labels = [str(item.get("name", "")) for item in labels]

    values = {"week": "unrecorded", "candidate_rank": "unrecorded", "issue_number": "unrecorded", "vote_count": "unrecorded", "run_reason": "unrecorded"}
    for key, value in FIELD_RE.findall(body):
        normalized = key.lower().replace(" ", "_")
        if normalized == "rank":
            normalized = "candidate_rank"
        elif normalized == "issue":
            normalized = "issue_number"
            value = clean_issue(value)
        elif normalized == "votes":
            normalized = "vote_count"
        values[normalized] = value.strip()

    selected_prompt = "unrecorded"
    marker = "## Selected prompt"
    if marker in body:
        after = body.split(marker, 1)[1].strip()
        if "## " in after:
            after = after.split("## ", 1)[0].strip()
        selected_prompt = after or "unrecorded"

    values["selected_prompt"] = selected_prompt
    values["terminal_state"] = terminal_state(labels)
    values["labels"] = labels

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(values, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
