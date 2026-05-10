#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", required=True)
    parser.add_argument("--dir", default="data/support-unlocks")
    parser.add_argument("--out", default=".tmp/support-unlock-env.txt")
    args = parser.parse_args()

    path = Path(args.dir) / f"{args.week}.json"
    support_total_usd = 0.0
    rank_2 = False
    rank_3 = False

    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        support_total_usd = float(data.get("support_total_usd") or 0)
        rank_2 = bool(data.get("rank_2_unlocked"))
        rank_3 = bool(data.get("rank_3_unlocked"))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "SUPPORT_USD=" + str(support_total_usd) + "\n"
        + "RANK_2_UNLOCKED=" + ("true" if rank_2 else "false") + "\n"
        + "RANK_3_UNLOCKED=" + ("true" if rank_3 else "false") + "\n",
        encoding="utf-8",
    )
    print(f"support_usd={support_total_usd}")
    print(f"rank_2_unlocked={rank_2}")
    print(f"rank_3_unlocked={rank_3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
