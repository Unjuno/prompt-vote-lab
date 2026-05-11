#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_public_agent_run_bundle.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def make_valid_bundle(bundle: Path) -> None:
    write_json(
        bundle / "index.json",
        {
            "schema_version": "prompt-vote-lab-public-agent-run-bundle-v1",
            "run_id": "fixture-run",
            "issue_number": "0",
            "pr_number": None,
            "policy": {
                "sanitized_diagnostic_logs_included": True,
                "sanitized_reasoning_traces_included": True,
                "sanitizer_guarantee": "best_effort_pattern_redaction",
            },
            "observation_summary": {
                "json": "observation-summary.json",
                "markdown": "observation-summary.md",
                "schema_version": "prompt-vote-lab-agent-observation-summary-v1",
            },
            "reasoning_trace_files": [
                {
                    "name": "codex-events.jsonl",
                    "included": True,
                    "path": "reasoning-traces/codex-events.jsonl",
                    "redactions": [],
                }
            ],
            "sanitized_files": [
                {
                    "name": "codex-stderr.txt",
                    "included": True,
                    "path": "sanitized/codex-stderr.txt",
                    "redactions": [{"kind": "openai_key", "count": 1}],
                }
            ],
            "included_files": [],
            "omitted_files": [],
        },
    )
    write(
        bundle / "README.md",
        "# Public agent run bundle\n\n## Agent observation summary\n\nSee sanitized/ and reasoning-traces/.\n",
    )
    write(
        bundle / "observation-summary.md",
        "# Agent observation summary\n\n"
        "## Reasoning / CoT-like trace evidence\n\n"
        "## Reasoning effect hypotheses\n\n"
        "## Sanitized logs\n\n"
        "## Evidence limits\n",
    )
    write_json(
        bundle / "observation-summary.json",
        {
            "schema_version": "prompt-vote-lab-agent-observation-summary-v1",
            "reasoning_trace": {
                "available": True,
                "public_trace_available": True,
                "sanitized": True,
                "published_directory": "reasoning-traces/",
                "used_for_behavior_evaluation": True,
                "exposed_reasoning_trace_published": True,
                "unexposed_provider_private_cot_available": "unknown",
                "unexposed_provider_private_cot_published": False,
                "files": [
                    {
                        "name": "codex-events.jsonl",
                        "included": True,
                        "path": "reasoning-traces/codex-events.jsonl",
                        "redactions": [],
                    }
                ],
            },
            "reasoning_effect_hypotheses": [
                {
                    "hypothesis": "fixture",
                    "confidence": "low",
                    "participant_prompt_adjustment": "inspect traces",
                }
            ],
            "file_activity": [],
            "sanitized_logs": [
                {
                    "name": "codex-stderr.txt",
                    "included": True,
                    "path": "sanitized/codex-stderr.txt",
                    "redactions": [{"kind": "openai_key", "count": 1}],
                }
            ],
        },
    )
    write(bundle / "raw" / "codex-events.jsonl", '{"type":"event"}\n')
    write(bundle / "sanitized" / "codex-stderr.txt", "OPENAI_API_KEY=[REDACTED_SECRET]\n")
    write(bundle / "reasoning-traces" / "codex-events.jsonl", '{"type":"reasoning","message":"inspect visible copy"}\n')


def run_verify(bundle: Path, report: Path | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(SCRIPT), "--bundle-dir", str(bundle)]
    if report:
        cmd += ["--report", str(report)]
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        valid = tmp / "valid"
        make_valid_bundle(valid)
        report = tmp / "report.json"
        ok = run_verify(valid, report)
        assert ok.returncode == 0, ok.stdout + ok.stderr
        result = json.loads(report.read_text(encoding="utf-8"))
        assert result["ok"] is True
        assert "raw" in result["checked_directories"]
        assert "sanitized" in result["checked_directories"]
        assert "reasoning-traces" in result["checked_directories"]

        missing = tmp / "missing"
        make_valid_bundle(missing)
        (missing / "reasoning-traces" / "codex-events.jsonl").unlink()
        bad_missing = run_verify(missing)
        assert bad_missing.returncode == 1
        assert "Required directory has no files: reasoning-traces" in bad_missing.stdout

        leaked = tmp / "leaked"
        make_valid_bundle(leaked)
        write(leaked / "sanitized" / "codex-stderr.txt", "leaked sk-FAKEFAKEFAKEFAKEFAKE\n")
        bad_secret = run_verify(leaked)
        assert bad_secret.returncode == 1
        assert "Forbidden public pattern openai_key" in bad_secret.stdout

        broken_summary = tmp / "broken-summary"
        make_valid_bundle(broken_summary)
        summary = json.loads((broken_summary / "observation-summary.json").read_text(encoding="utf-8"))
        summary["reasoning_trace"]["published_directory"] = "traces/"
        write_json(broken_summary / "observation-summary.json", summary)
        bad_summary = run_verify(broken_summary)
        assert bad_summary.returncode == 1
        assert "published_directory must be reasoning-traces/" in bad_summary.stdout

    print("public agent run bundle verifier test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
