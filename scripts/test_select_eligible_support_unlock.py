#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "select_eligible.py"
SUPPORT_POLICY = ROOT / "docs" / "support-policy.md"

REQUIRED_SUPPORT_POLICY_TEXT = [
    "Additional comparison runs can only happen after the weekly candidate set has passed the baseline rule.",
    "Current implementation rule:",
    "If the no-change baseline ranks first, no implementation candidates are eligible.",
    "If a real prompt ranks first, the weekly candidate set has passed the baseline rule.",
    "Rank 1 is then eligible for the normal weekly implementation run.",
    "If weekly support is at least 5 USD, rank 2 is eligible as a support-unlocked comparison run.",
    "If weekly support is at least 10 USD, rank 3 is eligible as a support-unlocked comparison run.",
    "Rank 2 and rank 3 do not independently need to exceed 20 votes after the candidate set has passed the baseline rule.",
    "no-change baseline: 20 votes",
    "rank 1 prompt: 25 votes",
    "rank 2 prompt: 12 votes",
    "rank 3 prompt: 8 votes",
    "eligible implementation ranks: 1, 2, 3",
    "rank 1 prompt: 18 votes",
    "eligible implementation ranks: none",
    "Support unlocks additional comparison runs only after the prompt candidate set beats the no-change baseline.",
]

FORBIDDEN_SUPPORT_POLICY_TEXT = [
    "Rank 2 and rank 3 must independently exceed 20 votes",
    "Support overrides the no-change baseline",
    "Support buys an implementation run when the baseline wins",
]


def run_selector(candidates: list[dict[str, object]], support_file_total: int | float) -> tuple[list[dict[str, object]], dict[str, object]]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "data" / "support-unlocks").mkdir(parents=True)
        (tmp_path / "data" / "support-unlocks" / "2026-W20.json").write_text(
            json.dumps({"support_total_usd": support_file_total, "rank_2_unlocked": support_file_total >= 5, "rank_3_unlocked": support_file_total >= 10}),
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
    return eligible, meta


def require_policy_text() -> None:
    text = SUPPORT_POLICY.read_text(encoding="utf-8")
    missing = [item for item in REQUIRED_SUPPORT_POLICY_TEXT if item not in text]
    if missing:
        raise SystemExit(f"Missing support policy text: {missing}")
    forbidden = [item for item in FORBIDDEN_SUPPORT_POLICY_TEXT if item.lower() in text.lower()]
    if forbidden:
        raise SystemExit(f"Forbidden support policy text found: {forbidden}")


def main() -> int:
    require_policy_text()

    baseline_loses = [
        {"rank": 1, "issue_number": 101, "vote_count": 25, "candidate_type": "prompt-proposal", "title": "rank 1", "body": "rank 1"},
        {"rank": 2, "issue_number": 102, "vote_count": 12, "candidate_type": "prompt-proposal", "title": "rank 2", "body": "rank 2"},
        {"rank": 3, "issue_number": 103, "vote_count": 8, "candidate_type": "prompt-proposal", "title": "rank 3", "body": "rank 3"},
        {"rank": 4, "issue_number": 0, "vote_count": 20, "candidate_type": "no-change-baseline", "title": "baseline", "body": "baseline"},
    ]
    eligible, meta = run_selector(baseline_loses, support_file_total=10)
    ranks = [item["rank"] for item in eligible]
    if ranks != [1, 2, 3]:
        raise SystemExit(f"expected ranks 1,2,3 from support unlock file after baseline loses, got {ranks}")
    if meta["support_usd"] != 10:
        raise SystemExit(f"expected support_usd 10, got {meta['support_usd']}")
    if meta["baseline_won"] is not False:
        raise SystemExit(f"expected baseline_won false when rank 1 is a prompt, got {meta['baseline_won']}")

    baseline_wins = [
        {"rank": 1, "issue_number": 0, "vote_count": 20, "candidate_type": "no-change-baseline", "title": "baseline", "body": "baseline"},
        {"rank": 2, "issue_number": 201, "vote_count": 18, "candidate_type": "prompt-proposal", "title": "rank 1 prompt", "body": "rank 1 prompt"},
        {"rank": 3, "issue_number": 202, "vote_count": 12, "candidate_type": "prompt-proposal", "title": "rank 2 prompt", "body": "rank 2 prompt"},
        {"rank": 4, "issue_number": 203, "vote_count": 8, "candidate_type": "prompt-proposal", "title": "rank 3 prompt", "body": "rank 3 prompt"},
    ]
    eligible, meta = run_selector(baseline_wins, support_file_total=10)
    if eligible:
        raise SystemExit(f"expected no eligible ranks when baseline wins, got {eligible}")
    if meta["baseline_won"] is not True:
        raise SystemExit(f"expected baseline_won true when no-change baseline ranks first, got {meta['baseline_won']}")
    if meta["eligible_count"] != 0:
        raise SystemExit(f"expected eligible_count 0 when baseline wins, got {meta['eligible_count']}")

    print("eligible selector support unlock test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
