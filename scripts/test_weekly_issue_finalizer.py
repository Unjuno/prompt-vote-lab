#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "weekly_issue_finalizer.py"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        issues = tmp / "issues.json"
        public_results = tmp / "public-results.json"
        out_json = tmp / "plan.json"
        out_md = tmp / "plan.md"
        comments_dir = tmp / "comments"

        write_json(
            issues,
            [
                {
                    "number": 177,
                    "title": "Implemented clear Issue",
                    "url": "https://example.test/issues/177",
                    "labels": [
                        {"name": "week:2026-W19"},
                        {"name": "outcome:implemented"},
                        {"name": "issue-safety:clear"},
                    ],
                },
                {
                    "number": 170,
                    "title": "Archived fixture",
                    "url": "https://example.test/issues/170",
                    "labels": [
                        {"name": "week:2026-W19"},
                        {"name": "outcome:archived-fixture"},
                        {"name": "authorized-canary"},
                    ],
                },
                {
                    "number": 164,
                    "title": "Missing outcome must stay open",
                    "url": "https://example.test/issues/164",
                    "labels": [
                        {"name": "week:2026-W19"},
                        {"name": "hostile-test"},
                    ],
                },
                {
                    "number": 3,
                    "title": "Carryover must stay open",
                    "url": "https://example.test/issues/3",
                    "labels": [
                        {"name": "week:2026-W19"},
                        {"name": "outcome:not-selected"},
                        {"name": "carryover"},
                    ],
                },
                {
                    "number": 2,
                    "title": "Wrong week must stay open",
                    "url": "https://example.test/issues/2",
                    "labels": [
                        {"name": "week:2026-W20"},
                        {"name": "outcome:not-selected"},
                    ],
                },
                {
                    "number": 1,
                    "title": "Missing from public results must stay open when required",
                    "url": "https://example.test/issues/1",
                    "labels": [
                        {"name": "week:2026-W19"},
                        {"name": "outcome:not-selected"},
                    ],
                },
            ],
        )
        write_json(
            public_results,
            {
                "generated_at": "2026-05-07T14:11:36+00:00",
                "issues": [
                    {"number": 177, "title": "Implemented clear Issue"},
                    {"number": 170, "title": "Archived fixture"},
                    {"number": 164, "title": "Missing outcome must stay open"},
                    {"number": 3, "title": "Carryover must stay open"},
                    {"number": 2, "title": "Wrong week must stay open"},
                ],
            },
        )

        subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--issues-json",
                str(issues),
                "--public-results",
                str(public_results),
                "--week-id",
                "2026-W19",
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
                "--comments-dir",
                str(comments_dir),
                "--run-record-hint",
                "runs/first-canary-009-clear-issue-177-success.md",
                "--dry-run",
                "--require-public-results-membership",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        plan = json.loads(out_json.read_text(encoding="utf-8"))
        assert plan["schema_version"] == "prompt-vote-lab-weekly-issue-finalizer-v1"
        assert plan["dry_run"] is True
        assert plan["summary"]["close_count"] == 2
        assert plan["summary"]["skip_count"] == 4

        close_by_number = {item["number"]: item for item in plan["to_close"]}
        assert set(close_by_number) == {177, 170}
        assert close_by_number[177]["close_reason"] == "completed"
        assert close_by_number[170]["close_reason"] == "completed"

        skip_by_number = {item["number"]: item for item in plan["skipped"]}
        assert "expected_exactly_one_outcome_label" in skip_by_number[164]["skip_reasons"]
        assert "protected_label_present" in skip_by_number[3]["skip_reasons"]
        assert "missing_matching_week_label" in skip_by_number[2]["skip_reasons"]
        assert "missing_from_public_results_snapshot" in skip_by_number[1]["skip_reasons"]

        comment_177 = (comments_dir / "177.md").read_text(encoding="utf-8")
        assert "<!-- prompt-vote-lab:weekly-issue-finalizer:v1 -->" in comment_177
        assert "week: 2026-W19" in comment_177
        assert "outcome: outcome:implemented" in comment_177
        assert "close_reason: completed" in comment_177
        assert "The Issue is not deleted" in comment_177
        assert "Public results snapshot" in comment_177
        assert "runs/first-canary-009-clear-issue-177-success.md" in comment_177

        assert not (comments_dir / "164.md").exists()
        md = out_md.read_text(encoding="utf-8")
        assert "Weekly Issue Finalizer plan" in md
        assert "Implemented clear Issue" in md
        assert "Missing outcome must stay open" in md

    print("weekly issue finalizer test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
