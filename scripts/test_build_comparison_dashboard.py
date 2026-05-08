#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_comparison_dashboard.py"


def test_dashboard_builder() -> None:
    data = {
        "generated_at": "2026-05-08T00:00:00+00:00",
        "issues": [
            {
                "number": 195,
                "title": "[Prompt][Rank 2]: Add an evidence map",
                "url": "https://example.test/issues/195",
                "state": "OPEN",
                "labels": ["week:2026-W20", "prompt-proposal", "normal-candidate", "issue-safety:clear", "issue-safety:submission-detected"],
                "reaction_plus_one_count": 4,
                "safety": {"clear": True, "blocked": False, "review": False, "runtime_detected": True},
                "body": "## Comparison metadata\n\n- Intended comparison rank: 2",
            },
            {
                "number": 196,
                "title": "[Prompt][Rank 3]: Add a decision card",
                "url": "https://example.test/issues/196",
                "state": "OPEN",
                "labels": ["week:2026-W20", "prompt-proposal", "normal-candidate", "issue-safety:clear", "issue-safety:submission-detected"],
                "reaction_plus_one_count": 2,
                "safety": {"clear": True, "blocked": False, "review": False, "runtime_detected": False},
                "body": "## Comparison metadata\n\n- Intended comparison rank: 3",
            },
        ],
        "pull_requests": [
            {
                "number": 201,
                "title": "Run Codex fixed Issue instruction canary",
                "url": "https://example.test/pulls/201",
                "state": "OPEN",
                "body": "- Issue: #195\n- Rank: 2\n- Votes: 4",
                "files": [{"path": "lab/comparisons/2026-W20/rank-2/index.html"}],
            }
        ],
    }
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        source = tmp_path / "public-results.json"
        out_dir = tmp_path / "out"
        source.write_text(json.dumps(data), encoding="utf-8")
        subprocess.run(
            [sys.executable, str(SCRIPT), "--public-results", str(source), "--week-id", "2026-W20", "--out-dir", str(out_dir)],
            check=True,
            cwd=ROOT,
        )
        html = (out_dir / "index.html").read_text(encoding="utf-8")
        css = (out_dir / "style.css").read_text(encoding="utf-8")

    required = [
        "Prompt Vote Lab comparison: 2026-W20",
        "Rank 2",
        "Rank 3",
        "Issue #195",
        "Issue #196",
        "PR #201",
        "lab/comparisons/2026-W20/rank-2/",
        "runs/2026-W20-rank-2-issue-195.md",
        "participant evidence comprehension",
        "data/public-results.json",
        "connect-src &#x27;none&#x27;",
    ]
    missing = [item for item in required if item not in html]
    if missing:
        raise AssertionError(f"dashboard missing expected text: {missing}")

    forbidden = [
        "OPENAI_API_KEY",
        "codex login",
        "container stderr",
        "raw stderr",
        "document.cookie",
        "eval(",
        "<iframe",
        "https://example.com/ping",
    ]
    found = [item for item in forbidden if item in html]
    if found:
        raise AssertionError(f"dashboard leaked forbidden text: {found}")

    if "rank-grid" not in css or "rank-card" not in css:
        raise AssertionError("dashboard CSS should define rank grid/cards")


def main() -> int:
    test_dashboard_builder()
    print("comparison dashboard builder test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
