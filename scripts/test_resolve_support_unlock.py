#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "resolve_support_unlock.py"


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        unlock_dir = base / "support-unlocks"
        unlock_dir.mkdir()
        (unlock_dir / "2026-W20.json").write_text(
            json.dumps(
                {
                    "support_total_usd": 10,
                    "rank_2_unlocked": True,
                    "rank_3_unlocked": True,
                }
            ),
            encoding="utf-8",
        )
        out = base / "env.txt"
        subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--week",
                "2026-W20",
                "--dir",
                str(unlock_dir),
                "--out",
                str(out),
            ],
            cwd=ROOT,
            check=True,
        )
        text = out.read_text(encoding="utf-8")

    required = ["SUPPORT_USD=10.0", "RANK_2_UNLOCKED=true", "RANK_3_UNLOCKED=true"]
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"missing resolver output: {missing}")

    print("support unlock resolver test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
