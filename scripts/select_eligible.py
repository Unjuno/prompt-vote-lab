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
from copy import deepcopy
from pathlib import Path
from typing import Any


NORMAL_RUN = "normal-weekly-run"
SUPPORT_RUN = "support-unlocked-run"
BASELINE_TYPE = "no-change-baseline"
PROMPT_TYPE = "prompt-proposal"


def parse_support_usd(value: str | int | float) -> float:
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


def select_eligible(candidates: list[dict[str, Any]], support_usd: str | int | float) -> list[dict[str, Any]]:
    support = parse_support_usd(support_usd)
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


def write_outputs(eligible: list[dict[str, Any]], out: Path, flag: Path, meta: Path, candidates: list[dict[str, Any]]) -> None:
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
    parser.add_argument("--out", default=".tmp/eligible-candidates.json")
    parser.add_argument("--flag", default=".tmp/has-eligible.txt")
    parser.add_argument("--meta", default=".tmp/selection-meta.json")
    args = parser.parse_args()

    candidates = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
    if not isinstance(candidates, list):
        raise SystemExit("candidates JSON must be a list")
    eligible = select_eligible(candidates, args.support_usd)
    write_outputs(eligible, Path(args.out), Path(args.flag), Path(args.meta), candidates)
    print(json.dumps({"eligible": eligible, "baseline_won": baseline_won(candidates)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
