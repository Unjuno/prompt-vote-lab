#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "extract_pr_metadata.py"


def run_extract(body: str, labels: list[str]) -> dict[str, object]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        body_file = tmp_path / "body.md"
        out_file = tmp_path / "out.json"
        body_file.write_text(body, encoding="utf-8")
        labels_json = json.dumps([{"name": label} for label in labels])
        subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--body-file",
                str(body_file),
                "--labels-json",
                labels_json,
                "--out",
                str(out_file),
            ],
            check=True,
            cwd=ROOT,
        )
        return json.loads(out_file.read_text(encoding="utf-8"))


def test_ordinary_maintenance_pr_remains_unrecorded() -> None:
    data = run_extract(
        """## Summary

Tightens release readiness guardrails.

## Changed files

- docs/current-features.md
""",
        [],
    )
    assert data["week"] == "unrecorded"
    assert data["candidate_rank"] == "unrecorded"
    assert data["issue_number"] == "unrecorded"
    assert data["vote_count"] == "unrecorded"
    assert data["selected_prompt"] == "unrecorded"
    assert data["terminal_state"] == "unrecorded"


def test_run_pr_metadata_is_extracted() -> None:
    data = run_extract(
        """Implements the selected ranked prompt candidate with the fixed implementation agent.

## Candidate

- Week: week-2026-W19
- Rank: 1
- Issue: #12
- Votes: 24
- Run reason: normal-weekly-run

## Selected prompt

Add a compact run-history section to /lab/.

## Implementation summary

Changed lab/index.html only.
""",
        ["pvl:merged"],
    )
    assert data["week"] == "week-2026-W19"
    assert data["candidate_rank"] == "1"
    assert data["issue_number"] == "12"
    assert data["vote_count"] == "24"
    assert data["run_reason"] == "normal-weekly-run"
    assert data["selected_prompt"] == "Add a compact run-history section to /lab/."
    assert data["terminal_state"] == "merged"


def main() -> int:
    test_ordinary_maintenance_pr_remains_unrecorded()
    test_run_pr_metadata_is_extracted()
    print("extract PR metadata tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
