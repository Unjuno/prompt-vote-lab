#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def infer_week_id(index_path: Path) -> str:
    parts = index_path.as_posix().split("/")
    try:
        comparisons_index = parts.index("comparisons")
        return parts[comparisons_index + 1]
    except (ValueError, IndexError) as exc:
        raise SystemExit("week id is required when index path is not under lab/comparisons/<week_id>/rank-*/index.html") from exc


def build_replacements(week_id: str) -> dict[str, str]:
    return {
        'href="./history/"': 'href="../../../history/"',
        f'href="./comparisons/{week_id}/"': 'href="../"',
        'href="../data/public-results.json"': 'href="../../../../data/public-results.json"',
    }


def normalize_index(index_path: Path, week_id: str) -> int:
    text = index_path.read_text(encoding="utf-8")
    changed = 0
    for before, after in build_replacements(week_id).items():
        count = text.count(before)
        if count:
            text = text.replace(before, after)
            changed += count
    index_path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", required=True, help="Path to rank-root index.html")
    parser.add_argument("--week-id", default="", help="Week id such as 2026-W20. Inferred from path when omitted.")
    args = parser.parse_args()
    index_path = Path(args.index)
    if not index_path.exists():
        raise SystemExit(f"missing index file: {index_path}")
    week_id = args.week_id or infer_week_id(index_path)
    changed = normalize_index(index_path, week_id)
    print(f"normalized comparison rank links: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
