#!/usr/bin/env python3
"""Select eligible Prompt Vote Lab implementation candidates.

Selection rule:
- If the no-change baseline ranks first, no implementation candidates are eligible.
- If the baseline does not rank first, rank 1 real prompt is eligible.
- Rank 2 real prompt is eligible only when support_usd >= 5.
- Rank 3 real prompt is eligible only when support_usd >= 10.
- The no-change baseline itself is never eligible.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from copy import deepcopy
from pathlib import Path
from typing import Any


NORMAL_RUN = "normal-weekly-run"
SUPPORT_RUN = "support-unlocked-run"
BASELINE_TYPE = "no-change-baseline"
PROMPT_TYPE = "prompt-proposal"
SUPPORT_UNLOCK_DIR = Path("data/support-unlocks")


def normalize_week_id(value: str) -> str:
    text = value.strip()
    return text[5:] if text.startswith("week-") else text


def support_from_unlock_file(week: str | None) -> float | None:
    if not week:
        return None
    path = SUPPORT_UNLOCK_DIR / f"{normalize_week_id(week)}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    support = float(data.get("support_total_usd") or 0)
    if not math.isfinite(support) or support < 0:
        raise ValueError(f"support unlock file has invalid support_total_usd: {path}")
    return support


def parse_support_usd(value: str | int | float, week: str | None = None) -> float:
    override = support_from_unlock_file(week)
    if override is not None:
        return override
    support = float(value or 0)
    if not math.isfinite(support) or support < 0:
        raise ValueError("support_usd must be a finite non-negative number")
    return support


def rank_of(candidate: dict[str, Any]) -> int:
    try:
        rank = int(candidate.get("rank"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"candidate has invalid rank: {candidate!r}") from exc
    if rank < 1:
        raise ValueError(f"candidate rank must be >= 1: {candidate!r}")
    return rank


def baseline_won(candidates: list[dict[str, Any]]) -> bool:
    return any(
        candidate.get("candidate_type") == BASELINE_TYPE and rank_of(candidate) == 1
        for candidate in candidates
    )


def select_eligible(candidates: list[dict[str, Any]], support_usd: str | int | float, week: str | None = None) -> list[dict[str, Any]]:
    support = parse_support_usd(support_usd, week=week)
    if baseline_won(candidates):
        return []

    eligible: list[dict[str, Any]] = []
    for original in candidates:
        if original.get("candidate_type") == BASELINE_TYPE:
            continue
        if original.get("candidate_type") != PROMPT_TYPE:
            continue

        candidate = deepcopy(original)
        rank = rank_of(candidate)
        if rank == 1:
            candidate["run_reason"] = NORMAL_RUN
            eligible.append(candidate)
        elif rank == 2 and support >= 5:
            candidate["run_reason"] = SUPPORT_RUN
            eligible.append(candidate)
        elif rank == 3 and support >= 10:
            candidate["run_reason"] = SUPPORT_RUN
            eligible.append(candidate)
    return eligible


def write_outputs(eligible: list[dict[str, Any]], out: Path, flag: Path, meta: Path, candidates: list[dict[str, Any]], support_usd: float) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    flag.parent.mkdir(parents=True, exist_ok=True)
    meta.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(eligible, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    flag.write_text("true" if eligible else "false", encoding="utf-8")
    meta.write_text(
        json.dumps(
            {
                "baseline_won": baseline_won(candidates),
                "eligible_count": len(eligible),
                "eligible_ranks": [candidate.get("rank") for candidate in eligible],
                "support_usd": support_usd,
                "support_source": "support-unlock-file" if os.getenv("RUN_WEEK") and support_from_unlock_file(os.getenv("RUN_WEEK")) is not None else "workflow-input",
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", default=".tmp/weekly-candidates.json")
    parser.add_argument("--support-usd", default="0")
    parser.add_argument("--week", default=os.getenv("RUN_WEEK", ""))
    parser.add_argument("--out", default=".tmp/eligible-candidates.json")
    parser.add_argument("--flag", default=".tmp/has-eligible.txt")
    parser.add_argument("--meta", default=".tmp/selection-meta.json")
    args = parser.parse_args()

    candidates = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
    if not isinstance(candidates, list):
        raise SystemExit("candidates JSON must be a list")
    support = parse_support_usd(args.support_usd, week=args.week)
    eligible = select_eligible(candidates, support, week=args.week)
    write_outputs(eligible, Path(args.out), Path(args.flag), Path(args.meta), candidates, support)
    print(json.dumps({"eligible": eligible, "baseline_won": baseline_won(candidates), "support_usd": support}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
