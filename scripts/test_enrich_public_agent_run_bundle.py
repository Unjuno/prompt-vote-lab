#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "enrich_public_agent_run_bundle.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        diag = tmp / "diag"
        bundle = tmp / "bundle"
        diag.mkdir()
        bundle.mkdir()
        (bundle / "raw").mkdir()

        write_json(
            bundle / "index.json",
            {
                "schema_version": "prompt-vote-lab-public-agent-run-bundle-v1",
                "run_id": "fixture-run",
                "issue_number": "12",
                "pr_number": "34",
                "policy": {"primary_artifact": "redacted raw files"},
                "quick_index": {"codex_event_lines": 2},
                "included_files": [],
                "omitted_files": [],
            },
        )
        write(bundle / "README.md", "# Public agent run bundle\n")

        write_json(
            diag / "policy-allowed-paths.json",
            {
                "repo_root_mounted": False,
                "container_work_root": "/work",
                "container_runtime_root": "/codex-runtime",
                "final_copyback_paths": ["lab/index.html", "lab/style.css", "lab/app.js"],
            },
        )
        write_json(diag / "check-results.json", {"changed_files": ["lab/index.html"], "forbidden_changed_files": []})
        write_json(
            diag / "file-hashes-before.json",
            {"lab/index.html": {"sha256": "old-index", "size_bytes": 10}, "lab/style.css": {"sha256": "old-css", "size_bytes": 20}},
        )
        write_json(
            diag / "file-hashes-after.json",
            {"lab/index.html": {"sha256": "new-index", "size_bytes": 30}, "lab/style.css": {"sha256": "old-css", "size_bytes": 20}},
        )
        write(diag / "container-visible-files-before.txt", "/work/lab/index.html\n/work/lab/style.css\n/work/lab/app.js\n")
        write(diag / "container-visible-files-after.txt", "/work/lab/index.html\n/work/lab/style.css\n/work/lab/app.js\n")
        write(diag / "task-visible-files-container.txt", "/task/execution-policy.md\n/task/instruction-brief.md\n")
        write(diag / "policy-agent-copied-files.txt", "lab/index.html\n")
        write(diag / "policy-denied-access.txt", "/repo/private-file.txt\n")
        write(
            diag / "policy-agent-diff.patch",
            "diff --git a/lab/index.html b/lab/index.html\n--- a/lab/index.html\n+++ b/lab/index.html\n@@ -1 +1,2 @@\n-old\n+new\n+line\n",
        )
        write(diag / "codex-last-message.txt", "I changed lab/index.html and did not touch app.js. token sk-FAKEFAKEFAKEFAKE should redact.\n")
        write(diag / "codex-stderr.txt", "stderr path /home/runner/work/prompt-vote-lab/prompt-vote-lab and key sk-FAKEFAKEFAKEFAKEFAKEFAKEFAKE\n")
        write(diag / "policy-agent-container-stderr.txt", "container stderr from /tmp/pvl-secret\n")
        write(diag / "npm-install-codex.txt", "npm installed in /github/workspace with GH_TOKEN=ghp_FAKEFAKEFAKEFAKEFAKE\n")
        write(diag / "policy-container-mounts.txt", "/home/runner/work/prompt-vote-lab/prompt-vote-lab/.tmp/work /work rw\n")

        subprocess.run(
            [sys.executable, str(SCRIPT), "--diagnostics-dir", str(diag), "--bundle-dir", str(bundle)],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        index = json.loads((bundle / "index.json").read_text(encoding="utf-8"))
        assert index["policy"]["sanitized_diagnostic_logs_included"] is True
        assert index["policy"]["sanitizer_guarantee"] == "best_effort_pattern_redaction"
        assert index["observation_summary"]["json"] == "observation-summary.json"
        assert index["observation_summary"]["markdown"] == "observation-summary.md"

        sanitized_stderr = (bundle / "sanitized" / "codex-stderr.txt").read_text(encoding="utf-8")
        assert "sk-FAKE" not in sanitized_stderr
        assert "/home/runner/work" not in sanitized_stderr
        assert "[REDACTED_SECRET]" in sanitized_stderr
        assert "[REDACTED_RUNNER_WORKDIR]" in sanitized_stderr

        npm_log = (bundle / "sanitized" / "npm-install-codex.txt").read_text(encoding="utf-8")
        assert "ghp_FAKE" not in npm_log
        assert "/github/workspace" not in npm_log
        assert "[REDACTED_SECRET]" in npm_log
        assert "[REDACTED_GITHUB_WORKSPACE]" in npm_log

        summary = json.loads((bundle / "observation-summary.json").read_text(encoding="utf-8"))
        assert summary["schema_version"] == "prompt-vote-lab-agent-observation-summary-v1"
        assert summary["path_model"]["repo_root_mounted"] is False
        assert summary["path_model"]["work_root"] == "/work"
        assert summary["path_model"]["task_root"] == "/task"
        assert summary["path_model"]["task_mount_mode"] == "read-only"
        assert summary["agent_observation"]["denied_access_paths"] == ["/repo/private-file.txt"]
        assert "sk-FAKE" not in summary["agent_observation"]["agent_final_action_summary"]
        assert "[REDACTED_SECRET]" in summary["agent_observation"]["agent_final_action_summary"]
        assert summary["limits"]["raw_private_reasoning_collected"] is False
        assert summary["limits"]["exact_read_order_observed"] is False

        by_file = {item["file"]: item for item in summary["file_activity"]}
        assert by_file["lab/index.html"]["changed"] is True
        assert by_file["lab/index.html"]["copied_back"] is True
        assert by_file["lab/index.html"]["additions"] == 2
        assert by_file["lab/index.html"]["deletions"] == 1
        assert by_file["lab/style.css"]["changed"] is False

        md = (bundle / "observation-summary.md").read_text(encoding="utf-8")
        assert "Agent observation summary" in md
        assert "Sanitized logs" in md
        assert "Exact file read order is not guaranteed" in md

        readme = (bundle / "README.md").read_text(encoding="utf-8")
        assert "Agent observation summary" in readme
        assert "Sanitized diagnostic logs" in readme

    print("public agent run bundle enrichment test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
