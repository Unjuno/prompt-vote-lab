#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def normalize_week_id(value: str) -> str:
    text = value.strip()
    return text[5:] if text.startswith("week-") else text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", required=True)
    parser.add_argument("--dir", default="data/support-unlocks")
    parser.add_argument("--out", default=".tmp/support-unlock-env.txt")
    parser.add_argument("--require", action="store_true", help="fail when the weekly support unlock file is missing")
    args = parser.parse_args()

    week_id = normalize_week_id(args.week)
    path = Path(args.dir) / f"{week_id}.json"
    support_total_usd = 0.0
    rank_2 = False
    rank_3 = False

    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        support_total_usd = float(data.get("support_total_usd") or 0)
        rank_2 = bool(data.get("rank_2_unlocked"))
        rank_3 = bool(data.get("rank_3_unlocked"))
    elif args.require:
        raise SystemExit(
            f"Missing required support unlock file: {path}. "
            "Run Support Unlock Export before Weekly Auto Run."
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "SUPPORT_UNLOCK_WEEK=" + week_id + "\n"
        + "SUPPORT_UNLOCK_FILE=" + str(path) + "\n"
        + "SUPPORT_USD=" + str(support_total_usd) + "\n"
        + "RANK_2_UNLOCKED=" + ("true" if rank_2 else "false") + "\n"
        + "RANK_3_UNLOCKED=" + ("true" if rank_3 else "false") + "\n",
        encoding="utf-8",
    )
    print(f"support_unlock_week={week_id}")
    print(f"support_unlock_file={path}")
    print(f"support_usd={support_total_usd}")
    print(f"rank_2_unlocked={rank_2}")
    print(f"rank_3_unlocked={rank_3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
