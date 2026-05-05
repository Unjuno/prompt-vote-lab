#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "write_public_run_log.py"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="pvl-public-log-") as tmp_name:
        out = Path(tmp_name) / "public-run-log.json"
        subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--out",
                str(out),
                "--provider",
                "openai-codex",
                "--runner",
                "codex-cli",
                "--model",
                "gpt-5.1-codex",
                "--workflow",
                "Codex First Canary Run",
                "--run-number",
                "1",
                "--week",
                "first-canary-001",
                "--candidate-rank",
                "1",
                "--issue-number",
                "0",
                "--vote-count",
                "0",
                "--base-sha",
                "abc123",
                "--branch",
                "codex-first-canary-001-1",
                "--attempt-count",
                "1",
                "--retry-policy",
                "none",
                "--fallback-policy",
                "none",
                "--auto-merge-policy",
                "disabled",
                "--status",
                "failed",
                "--failure-step",
                "Run Codex once",
                "--failure-type",
                "workflow_failure",
                "--error-summary",
                "redacted error summary",
                "--changed-files",
                "lab/index.html,lab/style.css",
                "--checks",
                '{"safety-check":"not-run"}',
            ],
            check=True,
            cwd=ROOT,
        )
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["schema"] == "prompt-vote-lab-public-run-log-v1"
        assert data["provider"] == "openai-codex"
        assert data["runner"] == "codex-cli"
        assert data["status"] == "failed"
        assert data["changed_files"] == ["lab/index.html", "lab/style.css"]
        assert data["checks"]["safety-check"] == "not-run"
        assert data["redaction"]["raw_stderr"] == "not published"
        assert data["redaction"]["raw_model_output"] == "not published"
        assert data["redaction"]["raw_codex_jsonl"] == "not published"

    print("public run log writer test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
