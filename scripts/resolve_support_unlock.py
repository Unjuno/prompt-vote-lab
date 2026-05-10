#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path


def normalize_week_id(value: str) -> str:
    text = value.strip()
    return text[5:] if text.startswith("week-") else text


def previous_utc_iso_week_id(now: datetime | None = None) -> str:
    current = now or datetime.now(timezone.utc)
    target = current - timedelta(days=7)
    iso = target.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def support_unlock_path(directory: Path, week_id: str) -> Path:
    return directory / f"{week_id}.json"


def resolve_week_and_path(directory: Path, requested_week: str, require: bool) -> tuple[str, Path]:
    requested_id = normalize_week_id(requested_week)
    requested_path = support_unlock_path(directory, requested_id)

    is_scheduled_github_run = os.getenv("GITHUB_EVENT_NAME") == "schedule"
    if require and is_scheduled_github_run:
        previous_id = previous_utc_iso_week_id()
        previous_path = support_unlock_path(directory, previous_id)
        if previous_path.exists():
            return previous_id, previous_path
        raise SystemExit(
            f"Missing required support unlock file for scheduled previous week: {previous_path}. "
            "Run Support Unlock Export before Weekly Auto Run."
        )

    if requested_path.exists():
        return requested_id, requested_path

    if require:
        raise SystemExit(
            f"Missing required support unlock file: {requested_path}. "
            "Run Support Unlock Export before Weekly Auto Run."
        )
    return requested_id, requested_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", required=True)
    parser.add_argument("--dir", default="data/support-unlocks")
    parser.add_argument("--out", default=".tmp/support-unlock-env.txt")
    parser.add_argument("--require", action="store_true", help="fail when the weekly support unlock file is missing")
    args = parser.parse_args()

    directory = Path(args.dir)
    week_id, path = resolve_week_and_path(directory, args.week, args.require)
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
        "RUN_WEEK=week-" + week_id + "\n"
        + "SUPPORT_UNLOCK_WEEK=" + week_id + "\n"
        + "SUPPORT_UNLOCK_FILE=" + str(path) + "\n"
        + "SUPPORT_USD=" + str(support_total_usd) + "\n"
        + "RANK_2_UNLOCKED=" + ("true" if rank_2 else "false") + "\n"
        + "RANK_3_UNLOCKED=" + ("true" if rank_3 else "false") + "\n",
        encoding="utf-8",
    )
    print(f"run_week=week-{week_id}")
    print(f"support_unlock_week={week_id}")
    print(f"support_unlock_file={path}")
    print(f"support_usd={support_total_usd}")
    print(f"rank_2_unlocked={rank_2}")
    print(f"rank_3_unlocked={rank_3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
