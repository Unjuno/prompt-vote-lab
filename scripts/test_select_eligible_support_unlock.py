#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "select_eligible.py"


def main() -> int:
    candidates = [
        {"rank": 1, "issue_number": 101, "vote_count": 25, "candidate_type": "prompt-proposal", "title": "rank 1", "body": "rank 1"},
        {"rank": 2, "issue_number": 102, "vote_count": 12, "candidate_type": "prompt-proposal", "title": "rank 2", "body": "rank 2"},
        {"rank": 3, "issue_number": 103, "vote_count": 8, "candidate_type": "prompt-proposal", "title": "rank 3", "body": "rank 3"},
        {"rank": 4, "issue_number": 0, "vote_count": 20, "candidate_type": "no-change-baseline", "title": "baseline", "body": "baseline"},
    ]
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "data" / "support-unlocks").mkdir(parents=True)
        (tmp_path / "data" / "support-unlocks" / "2026-W20.json").write_text(
            json.dumps({"support_total_usd": 10, "rank_2_unlocked": True, "rank_3_unlocked": True}),
            encoding="utf-8",
        )
        input_path = tmp_path / "candidates.json"
        out_path = tmp_path / "eligible.json"
        meta_path = tmp_path / "meta.json"
        flag_path = tmp_path / "flag.txt"
        input_path.write_text(json.dumps(candidates), encoding="utf-8")
        subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--candidates",
                str(input_path),
                "--support-usd",
                "0",
                "--week",
                "week-2026-W20",
                "--out",
                str(out_path),
                "--flag",
                str(flag_path),
                "--meta",
                str(meta_path),
            ],
            cwd=tmp_path,
            check=True,
        )
        eligible = json.loads(out_path.read_text(encoding="utf-8"))
        meta = json.loads(meta_path.read_text(encoding="utf-8"))

    ranks = [item["rank"] for item in eligible]
    if ranks != [1, 2, 3]:
        raise SystemExit(f"expected ranks 1,2,3 from support unlock file, got {ranks}")
    if meta["support_usd"] != 10:
        raise SystemExit(f"expected support_usd 10, got {meta['support_usd']}")
    print("eligible selector support unlock test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
