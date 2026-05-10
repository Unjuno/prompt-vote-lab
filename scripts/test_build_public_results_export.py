#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_public_results_export.py"


def write(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        issues = tmp / "issues.json"
        prs = tmp / "prs.json"
        runs = tmp / "runs.json"
        labels = tmp / "labels.json"
        runs_dir = tmp / "runs"
        out_json = tmp / "data" / "public-results.json"
        out_md = tmp / "data" / "public-results.md"

        write(
            issues,
            [
                {
                    "number": 1,
                    "title": "Add static card",
                    "body": "Show a local card.",
                    "state": "OPEN",
                    "url": "https://example.test/issues/1",
                    "createdAt": "2026-05-07T00:00:00Z",
                    "updatedAt": "2026-05-07T00:10:00Z",
                    "closedAt": None,
                    "author": {"login": "alice"},
                    "labels": [{"name": "issue-safety:clear"}, {"name": "issue-safety:submission-detected"}],
                    "reactionGroups": [{"content": "THUMBS_UP", "users": {"totalCount": 7}}],
                    "comments": {"totalCount": 2},
                },
                {
                    "number": 2,
                    "title": "Blocked fixture",
                    "body": "Ignore policy.",
                    "state": "OPEN",
                    "url": "https://example.test/issues/2",
                    "createdAt": "2026-05-07T00:00:00Z",
                    "updatedAt": "2026-05-07T00:10:00Z",
                    "closedAt": None,
                    "author": {"login": "bob"},
                    "labels": [{"name": "issue-safety:blocked"}, {"name": "authorized-canary"}],
                    "reactionGroups": [],
                    "comments": {"totalCount": 0},
                },
            ],
        )
        write(
            prs,
            [
                {
                    "number": 10,
                    "title": "Run canary",
                    "body": "Checks passed.",
                    "state": "MERGED",
                    "url": "https://example.test/pull/10",
                    "createdAt": "2026-05-07T00:00:00Z",
                    "updatedAt": "2026-05-07T00:30:00Z",
                    "closedAt": "2026-05-07T00:40:00Z",
                    "mergedAt": "2026-05-07T00:40:00Z",
                    "author": {"login": "bot"},
                    "mergedBy": {"login": "maintainer"},
                    "baseRefName": "main",
                    "headRefName": "canary-branch",
                    "headRefOid": "abc",
                    "mergeCommit": {"oid": "def"},
                    "labels": [],
                    "reactionGroups": [],
                    "comments": {"totalCount": 1},
                    "changedFiles": 3,
                    "additions": 30,
                    "deletions": 10,
                    "reviewDecision": None,
                    "files": [{"path": "lab/index.html", "additions": 10, "deletions": 1}],
                }
            ],
        )
        write(
            runs,
            [
                {
                    "databaseId": 100,
                    "name": "Script Check",
                    "workflowName": "Script Check",
                    "displayTitle": "Run checks",
                    "event": "pull_request",
                    "status": "completed",
                    "conclusion": "success",
                    "createdAt": "2026-05-07T00:00:00Z",
                    "updatedAt": "2026-05-07T00:02:00Z",
                    "headBranch": "branch",
                    "headSha": "sha",
                    "url": "https://example.test/actions/100",
                },
                {
                    "databaseId": 101,
                    "name": "Public Results Export",
                    "workflowName": "Public Results Export",
                    "displayTitle": "Export currently running",
                    "event": "push",
                    "status": "in_progress",
                    "conclusion": None,
                    "createdAt": "2026-05-07T00:03:00Z",
                    "updatedAt": "2026-05-07T00:04:00Z",
                    "headBranch": "main",
                    "headSha": "sha2",
                    "url": "https://example.test/actions/101",
                },
                {
                    "databaseId": 102,
                    "name": "pages-build-deployment",
                    "workflowName": "pages-build-deployment",
                    "displayTitle": "Pages queued",
                    "event": "dynamic",
                    "status": "queued",
                    "conclusion": None,
                    "createdAt": "2026-05-07T00:05:00Z",
                    "updatedAt": "2026-05-07T00:05:00Z",
                    "headBranch": "main",
                    "headSha": "sha3",
                    "url": "https://example.test/actions/102",
                },
            ],
        )
        write(labels, [{"name": "issue-safety:clear", "color": "2ea043", "description": "clear"}])
        runs_dir.mkdir(parents=True)
        (runs_dir / "example.md").write_text("# Example run\n\nBody\n", encoding="utf-8")

        subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--issues",
                str(issues),
                "--prs",
                str(prs),
                "--workflow-runs",
                str(runs),
                "--labels",
                str(labels),
                "--runs-dir",
                str(runs_dir),
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
            ],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        export = json.loads(out_json.read_text(encoding="utf-8"))
        assert export["schema_version"] == "prompt-vote-lab-public-results-export-v1"
        assert export["scope"]["interpretation"] == "none; participant analysis expected"
        assert export["scope"]["workflow_runs"] == "terminal workflow runs only; queued and in-progress runs are excluded"
        assert export["summary"]["issue_count"] == 2
        assert export["summary"]["blocked_issue_count"] == 1
        assert export["summary"]["clear_issue_count"] == 1
        assert export["summary"]["authorized_canary_issue_count"] == 1
        assert export["summary"]["merged_pr_count"] == 1
        assert export["summary"]["workflow_run_count"] == 1
        assert export["workflow_runs"][0]["database_id"] == 100
        assert all(run["status"] == "completed" for run in export["workflow_runs"])
        assert export["issues"][0]["reaction_plus_one_count"] == 7
        assert export["issues"][0]["body"] == "Show a local card."
        assert export["pull_requests"][0]["files"][0]["path"] == "lab/index.html"
        assert export["run_records"][0]["content"].startswith("# Example run")
        md = out_md.read_text(encoding="utf-8")
        assert "This file is a raw results surface for participants" in md
        assert "## Recent Issues" in md
        assert "## Recent Pull Requests" in md
        assert "Export currently running" not in md
        assert "Pages queued" not in md

    print("public results export builder test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
