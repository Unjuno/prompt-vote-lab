#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_history_page.py"


def test_history_builder() -> None:
    data = {
        "generated_at": "2026-05-08T00:00:00+00:00",
        "issues": [
            {
                "number": 195,
                "title": "[Prompt][Rank 2]: Add an evidence map",
                "url": "https://example.test/issues/195",
                "state": "OPEN",
                "labels": ["week:2026-W20", "prompt-proposal", "normal-candidate", "issue-safety:clear", "issue-safety:submission-detected"],
                "safety": {"clear": True, "blocked": False, "review": False, "runtime_detected": True},
                "body": "## Comparison metadata\n\n- Intended comparison rank: 2",
            },
            {
                "number": 196,
                "title": "[Prompt][Rank 3]: Add a decision card",
                "url": "https://example.test/issues/196",
                "state": "OPEN",
                "labels": ["week:2026-W20", "prompt-proposal", "normal-candidate", "issue-safety:review"],
                "safety": {"clear": False, "blocked": False, "review": True, "runtime_detected": False},
                "body": "## Comparison metadata\n\n- Intended comparison rank: 3",
            },
            {
                "number": 191,
                "title": "[Prompt]: Add a static reviewer orientation panel",
                "url": "https://example.test/issues/191",
                "state": "CLOSED",
                "labels": ["week:2026-W19", "prompt-proposal", "normal-candidate", "issue-safety:clear", "issue-safety:runtime-detected", "outcome:implemented"],
                "safety": {"clear": True, "blocked": False, "review": False, "runtime_detected": True},
                "body": "normal candidate without embedded rank metadata",
            },
        ],
        "pull_requests": [
            {
                "number": 179,
                "title": "Run Codex fixed Issue instruction canary",
                "url": "https://example.test/pulls/179",
                "state": "MERGED",
                "body": "- Issue: #191\n- Rank: 1\n- Votes: 0",
                "files": [
                    {"path": "lab/index.html"},
                    {"path": "lab/style.css"},
                    {"path": "lab/app.js"},
                ],
            }
        ],
    }
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        source = tmp_path / "public-results.json"
        runs_dir = tmp_path / "runs"
        out_dir = tmp_path / "lab" / "history"
        source.write_text(json.dumps(data), encoding="utf-8")
        runs_dir.mkdir()
        (runs_dir / "week-2026-W21-vote-summary.md").write_text(
            "# Weekly vote summary: week-2026-W21\n\nbaseline_won: true\neligible_count: 0\n",
            encoding="utf-8",
        )
        subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--public-results",
                str(source),
                "--runs-dir",
                str(runs_dir),
                "--out-dir",
                str(out_dir),
            ],
            check=True,
            cwd=ROOT,
        )
        html = (out_dir / "index.html").read_text(encoding="utf-8")
        css = (out_dir / "style.css").read_text(encoding="utf-8")
        baseline_html = (tmp_path / "lab" / "weeks" / "2026-W21" / "index.html").read_text(encoding="utf-8")

    required = [
        "Prompt Vote Lab history",
        "2026-W21",
        "2026-W20",
        "2026-W19",
        "Candidate state flow",
        "submission safety scan",
        "comparison run",
        "finalizer close",
        "live rank output pages remain the source of truth",
        "Open weekly comparison",
        "Open weekly summary",
        "../weeks/2026-W21/",
        "../comparisons/2026-W20/",
        "../comparisons/2026-W19/",
        "<dt>Adopted</dt><dd>no change</dd>",
        "<dt>Adopted</dt><dd>rank 1</dd>",
        "Generated from <code>data/public-results.json</code>",
        "connect-src 'none'",
    ]
    missing = [item for item in required if item not in html]
    if missing:
        raise AssertionError(f"history page missing expected text: {missing}")

    baseline_required = [
        "2026-W21 no-change summary",
        "The no-change baseline won this week.",
        "No prompt beat the 20-vote baseline",
        "No implementation-agent attempt was created.",
        "<dt>Baseline votes</dt><dd>20</dd>",
        "<dt>Adopted</dt><dd>no change</dd>",
        "../../../runs/week-2026-W21-vote-summary.md",
        "Back to history",
        "../../history/",
        "connect-src 'none'",
    ]
    missing_baseline = [item for item in baseline_required if item not in baseline_html]
    if missing_baseline:
        raise AssertionError(f"baseline week page missing expected text: {missing_baseline}")

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
    found = [item for item in forbidden if item in html or item in baseline_html]
    if found:
        raise AssertionError(f"history page leaked forbidden text: {found}")

    if "week-grid" not in css or "week-card" not in css:
        raise AssertionError("history CSS should define week grid/cards")


def main() -> int:
    test_history_builder()
    print("history page builder test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
