#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

REPLACEMENTS = {
    'href="./history/"': 'href="../../../history/"',
    'href="./comparisons/2026-W20/"': 'href="../"',
    'href="../data/public-results.json"': 'href="../../../../data/public-results.json"',
}


def normalize_index(index_path: Path) -> int:
    text = index_path.read_text(encoding="utf-8")
    changed = 0
    for before, after in REPLACEMENTS.items():
        count = text.count(before)
        if count:
            text = text.replace(before, after)
            changed += count
    index_path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", required=True, help="Path to rank-root index.html")
    args = parser.parse_args()
    index_path = Path(args.index)
    if not index_path.exists():
        raise SystemExit(f"missing index file: {index_path}")
    changed = normalize_index(index_path)
    print(f"normalized comparison rank links: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
