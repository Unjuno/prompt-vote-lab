#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "resolve_support_unlock.py"


def run_embedded_resolver(base: Path, event_name: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["GITHUB_EVENT_NAME"] = event_name
    env["PYTHONPATH"] = str(ROOT)
    code = """
from pathlib import Path
from scripts import resolve_support_unlock as r
base = Path(r'{base}')
unlock_dir = base / 'support-unlocks'
r.previous_utc_iso_week_id = lambda now=None: '2026-W20'
week_id, path = r.resolve_week_and_path(unlock_dir, 'week-2026-W21', True)
assert week_id == '2026-W20', week_id
assert path.name == '2026-W20.json', path
print('{event_name} previous-week fallback passed')
""".format(base=str(base), event_name=event_name)
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


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
                "week-2026-W20",
                "--dir",
                str(unlock_dir),
                "--out",
                str(out),
                "--require",
            ],
            cwd=ROOT,
            check=True,
        )
        text = out.read_text(encoding="utf-8")

        scheduled_result = run_embedded_resolver(base, "schedule")
        manual_result = run_embedded_resolver(base, "workflow_dispatch")

        missing_result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--week",
                "week-2026-W21",
                "--dir",
                str(unlock_dir),
                "--out",
                str(base / "missing-env.txt"),
                "--require",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    required = [
        "RUN_WEEK=week-2026-W20",
        "SUPPORT_UNLOCK_WEEK=2026-W20",
        "SUPPORT_UNLOCK_FILE=",
        "SUPPORT_USD=10.0",
        "RANK_2_UNLOCKED=true",
        "RANK_3_UNLOCKED=true",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"missing resolver output: {missing}")

    for label, result in (("scheduled", scheduled_result), ("manual", manual_result)):
        if result.returncode != 0:
            raise SystemExit(
                f"{label} previous-week fallback failed\n"
                + result.stdout
                + result.stderr
            )

    if missing_result.returncode == 0:
        raise SystemExit("--require should fail when the weekly support unlock file is missing outside schedule/manual workflow runs")
    if "Missing required support unlock file" not in (missing_result.stdout + missing_result.stderr):
        raise SystemExit("missing required support unlock failure message was not emitted")

    print("support unlock resolver test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
