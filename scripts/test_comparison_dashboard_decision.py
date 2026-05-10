#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_comparison_dashboard.py"


def main() -> int:
    data = {
        "generated_at": "2026-05-10T00:00:00+00:00",
        "issues": [
            {
                "number": 195,
                "title": "[Prompt][Rank 2]: Evidence map",
                "url": "https://example.test/issues/195",
                "state": "OPEN",
                "labels": [
                    "week:2026-W20",
                    "prompt-proposal",
                    "normal-candidate",
                    "issue-safety:clear",
                ],
                "reaction_plus_one_count": 0,
                "safety": {
                    "clear": True,
                    "blocked": False,
                    "review": False,
                    "runtime_detected": True,
                },
                "body": "## Comparison metadata\n\n- Intended comparison rank: 2",
            }
        ],
        "pull_requests": [
            {
                "number": 214,
                "title": "Rank 2 implementation",
                "url": "https://example.test/pulls/214",
                "state": "MERGED",
                "body": "- Issue: #195\n- Rank: 2\n- Votes: 0",
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
            [
                sys.executable,
                str(SCRIPT),
                "--public-results",
                str(source),
                "--week-id",
                "2026-W20",
                "--out-dir",
                str(out_dir),
            ],
            cwd=ROOT,
            check=True,
        )
        html = (out_dir / "index.html").read_text(encoding="utf-8")

    if "PR #214" not in html or "MERGED" not in html:
        raise SystemExit("fixture PR was not rendered as merged")
    if "<div><dt>Decision</dt><dd>implemented</dd></div>" not in html:
        raise SystemExit("merged implementation PR should imply implemented decision")
    if "pending" in html:
        raise SystemExit("merged implementation PR must not remain pending")

    print("comparison dashboard decision test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
