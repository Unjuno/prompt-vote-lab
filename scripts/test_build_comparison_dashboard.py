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
                "number": 183,
                "title": "Old Rank 1 non-prompt candidate",
                "url": "https://example.test/issues/183",
                "state": "CLOSED",
                "labels": ["week:2026-W20", "normal-candidate", "issue-safety:clear"],
                "reaction_plus_one_count": 0,
                "safety": {"clear": True, "blocked": False, "review": False, "runtime_detected": True},
                "body": "## Comparison metadata\n\n- Intended comparison rank: 1",
            },
            {
                "number": 191,
                "title": "Preferred Rank 1 candidate",
                "url": "https://example.test/issues/191",
                "state": "CLOSED",
                "labels": ["week:2026-W20", "prompt-proposal", "normal-candidate", "issue-safety:clear"],
                "reaction_plus_one_count": 0,
                "safety": {"clear": True, "blocked": False, "review": False, "runtime_detected": True},
                "body": "## Comparison metadata\n\n- Intended comparison rank: 1",
            },
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
                "number": 184,
                "title": "Older merged rank 1 output",
                "url": "https://example.test/pulls/184",
                "state": "MERGED",
                "body": "- Issue: #183\n- Rank: 1\n- Votes: 0",
                "files": [{"path": "lab/comparisons/2026-W20/rank-1/old.html"}],
            },
            {
                "number": 192,
                "title": "Preferred merged rank 1 output",
                "url": "https://example.test/pulls/192",
                "state": "MERGED",
                "body": "- Issue: #191\n- Rank: 1\n- Votes: 0",
                "files": [
                    {"path": "lab/index.html"},
                    {"path": "lab/style.css"},
                    {"path": "lab/app.js"},
                ],
            },
            {
                "number": 256,
                "title": "Later script-only maintenance PR for same issue",
                "url": "https://example.test/pulls/256",
                "state": "MERGED",
                "body": "- Issue: #191\n- Rank: 1\n- Votes: 0",
                "files": [{"path": "scripts/build_history_page.py"}],
            },
            {
                "number": 199,
                "title": "Closed stale comparison output",
                "url": "https://example.test/pulls/199",
                "state": "CLOSED",
                "body": "- Issue: #195\n- Rank: 2\n- Votes: 4",
                "files": [{"path": "lab/comparisons/2026-W20/rank-2/stale.html"}],
            },
            {
                "number": 201,
                "title": "Merged comparison output",
                "url": "https://example.test/pulls/201",
                "state": "MERGED",
                "body": "- Issue: #195\n- Rank: 2\n- Votes: 4",
                "files": [{"path": "lab/comparisons/2026-W20/rank-2/index.html"}],
            },
            {
                "number": 216,
                "title": "Superseded closed rank 3 output",
                "url": "https://example.test/pulls/216",
                "state": "CLOSED",
                "body": "- Issue: #196\n- Rank: 3\n- Votes: 2",
                "files": [{"path": "lab/comparisons/2026-W20/rank-3/index.html"}],
            },
            {
                "number": 224,
                "title": "Merged rank 3 output",
                "url": "https://example.test/pulls/224",
                "state": "MERGED",
                "body": "- Issue: #196\n- Rank: 3\n- Votes: 2",
                "files": [{"path": "lab/comparisons/2026-W20/rank-3/index.html"}],
            },
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
        "Rank 1",
        "Rank 2",
        "Rank 3",
        "Issue #191",
        "Issue #195",
        "Issue #196",
        "PR #192",
        "PR #201",
        "PR #224",
        "MERGED",
        "Live output",
        "Open rank 1 output",
        "Open rank 2 output",
        "./rank-1/",
        "./rank-2/",
        "lab/comparisons/2026-W20/rank-1/",
        "lab/comparisons/2026-W20/rank-2/",
        "Implementation PR changed files",
        "Live output snapshot files",
        "lab/index.html",
        "lab/style.css",
        "lab/app.js",
        "lab/comparisons/2026-W20/rank-1/index.html",
        "lab/comparisons/2026-W20/rank-1/style.css",
        "lab/comparisons/2026-W20/rank-1/app.js",
        "lab/comparisons/2026-W20/rank-2/index.html",
        "lab/comparisons/2026-W20/rank-2/style.css",
        "lab/comparisons/2026-W20/rank-2/app.js",
        "lab/comparisons/2026-W20/rank-3/index.html",
        "lab/comparisons/2026-W20/rank-3/style.css",
        "lab/comparisons/2026-W20/rank-3/app.js",
        "https://github.com/Unjuno/prompt-vote-lab/blob/main/runs/2026-W20-rank-2-issue-195.md",
        "runs/2026-W20-rank-2-issue-195.md",
        "participant evidence comprehension",
        "data/public-results.json",
        "connect-src 'none'",
    ]
    missing = [item for item in required if item not in html]
    if missing:
        raise AssertionError(f"dashboard missing expected text: {missing}")

    forbidden = [
        "<h3>Changed files</h3>",
        "Old Rank 1 non-prompt candidate",
        "Issue #183",
        "PR #184",
        "old.html",
        "PR #199",
        "stale.html",
        "PR #216",
        "PR #256",
        "scripts/build_history_page.py",
    ]
    found = [item for item in forbidden if item in html]
    if found:
        raise AssertionError(f"dashboard leaked forbidden text: {found}")

    if html.count('<p class="rank-eyebrow">Rank 1</p>') != 1:
        raise AssertionError("dashboard should render exactly one Rank 1 card")

    if html.count("Implementation PR changed files") != 3:
        raise AssertionError("dashboard should label PR changed files on each rank card")

    if html.count("Live output snapshot files") != 3:
        raise AssertionError("dashboard should label live output snapshot files on each rank card")

    if "rank-grid" not in css or "rank-card" not in css:
        raise AssertionError("dashboard CSS should define rank grid/cards")


def main() -> int:
    test_dashboard_builder()
    print("comparison dashboard builder test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())