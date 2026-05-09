#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


def infer_week_id(index_path: Path) -> str:
    parts = index_path.as_posix().split("/")
    try:
        comparisons_index = parts.index("comparisons")
        return parts[comparisons_index + 1]
    except (ValueError, IndexError) as exc:
        raise SystemExit("week id is required when index path is not under lab/comparisons/<week_id>/rank-*/index.html") from exc


def build_link_replacements(week_id: str) -> dict[str, str]:
    return {
        'href="./history/"': 'href="../../../history/"',
        f'href="./comparisons/{week_id}/"': 'href="../"',
        'href="../data/public-results.json"': 'href="../../../../data/public-results.json"',
    }


def normalize_text(text: str, week_id: str, issue_number: str, candidate_rank: str) -> tuple[str, int]:
    changed = 0
    for before, after in build_link_replacements(week_id).items():
        count = text.count(before)
        if count:
            text = text.replace(before, after)
            changed += count
    if issue_number:
        text, count = re.subn(r"Issue #\d+", f"Issue #{issue_number}", text)
        changed += count
    if candidate_rank:
        text, count = re.subn(r"Candidate #\d+", f"Candidate #{candidate_rank}", text)
        changed += count
    return text, changed


def normalize_file(path: Path, week_id: str, issue_number: str, candidate_rank: str) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    text, changed = normalize_text(text, week_id, issue_number, candidate_rank)
    path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", required=True, help="Path to rank-root index.html")
    parser.add_argument("--week-id", default="", help="Week id such as 2026-W20. Inferred from path when omitted.")
    parser.add_argument("--issue-number", default="", help="Selected Issue number to stamp into copied rank artifacts.")
    parser.add_argument("--candidate-rank", default="", help="Candidate rank to stamp into copied rank artifacts.")
    args = parser.parse_args()

    index_path = Path(args.index)
    if not index_path.exists():
        raise SystemExit(f"missing index file: {index_path}")
    week_id = args.week_id or infer_week_id(index_path)
    rank_root = index_path.parent
    changed = normalize_file(index_path, week_id, args.issue_number, args.candidate_rank)
    changed += normalize_file(rank_root / "app.js", week_id, args.issue_number, args.candidate_rank)
    print(f"normalized comparison rank artifact: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
