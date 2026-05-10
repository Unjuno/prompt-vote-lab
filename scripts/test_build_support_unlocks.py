#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_support_unlocks.py"
FIXTURE = ROOT / "tests" / "fixtures" / "support-activities-w20.json"

FORBIDDEN_PUBLIC_TEXT = [
    "private-sponsor-one",
    "private-sponsor-two",
    "ignored-cancel",
    "ignored-old",
    "ignored-recurring",
    "sponsor\"",
    "login\"",
    "email\"",
]


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp) / "support-unlocks"
        subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input",
                str(FIXTURE),
                "--week-id",
                "2026-W20",
                "--since",
                "2026-05-04T00:00:00Z",
                "--until",
                "2026-05-11T00:00:00Z",
                "--out-dir",
                str(out_dir),
            ],
            cwd=ROOT,
            check=True,
        )
        output_path = out_dir / "2026-W20.json"
        text = output_path.read_text(encoding="utf-8")
        data = json.loads(text)

    if data["support_total_cents"] != 1000:
        raise SystemExit(f"expected 1000 cents, got {data['support_total_cents']}")
    if data["support_total_usd"] != 10:
        raise SystemExit(f"expected 10 USD, got {data['support_total_usd']}")
    if data["counted_event_count"] != 2:
        raise SystemExit(f"expected 2 counted events, got {data['counted_event_count']}")
    if data["ignored_event_count"] != 3:
        raise SystemExit(f"expected 3 ignored events, got {data['ignored_event_count']}")
    if data["rank_2_unlocked"] is not True:
        raise SystemExit("rank 2 should be unlocked at 5 USD")
    if data["rank_3_unlocked"] is not True:
        raise SystemExit("rank 3 should be unlocked at 10 USD")
    if data["privacy"]["sponsor_identity_included"] is not False:
        raise SystemExit("public support unlock output must not include sponsor identity")

    leaked = [item for item in FORBIDDEN_PUBLIC_TEXT if item in text]
    if leaked:
        raise SystemExit(f"public support unlock output leaked private fields: {leaked}")

    print("support unlock builder test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
