#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_issue_execution_gate.py"


def run_gate(scan: dict[str, object], issue: dict[str, object]) -> tuple[int, dict[str, object], str]:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        scan_json = tmp / "scan.json"
        issue_json = tmp / "issue.json"
        out_json = tmp / "gate.json"
        out_md = tmp / "gate.md"
        scan_json.write_text(json.dumps(scan), encoding="utf-8")
        issue_json.write_text(json.dumps(issue), encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--scan-json",
                str(scan_json),
                "--issue-json",
                str(issue_json),
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode, json.loads(out_json.read_text(encoding="utf-8")), out_md.read_text(encoding="utf-8")


def test_clear_issue_allowed() -> None:
    rc, gate, md = run_gate(
        {
            "issue_number": 300,
            "issue_title": "Add local cards",
            "unsafe_instruction_count": 0,
            "severity": "clear",
        },
        {"number": 300, "title": "Add local cards", "labels": [{"name": "issue-safety:clear"}]},
    )
    assert rc == 0
    assert gate["execution_allowed"] is True
    assert gate["gate_required"] is False
    assert gate["reason"] == "Issue safety scan is clear."
    assert "Status: **PASS**" in md


def test_blocked_issue_stops_without_authorized_label() -> None:
    rc, gate, md = run_gate(
        {
            "issue_number": 301,
            "issue_title": "Unsafe request",
            "unsafe_instruction_count": 2,
            "severity": "blocked",
        },
        {"number": 301, "title": "Unsafe request", "labels": [{"name": "issue-safety:blocked"}]},
    )
    assert rc == 3
    assert gate["execution_allowed"] is False
    assert gate["gate_required"] is True
    assert gate["has_authorized_canary_label"] is False
    assert gate["required_exception_label"] == "authorized-canary"
    assert "Status: **STOP**" in md


def test_blocked_issue_allowed_with_authorized_label() -> None:
    rc, gate, md = run_gate(
        {
            "issue_number": 302,
            "issue_title": "Controlled canary request",
            "unsafe_instruction_count": 3,
            "severity": "blocked",
        },
        {
            "number": 302,
            "title": "Controlled canary request",
            "labels": [{"name": "issue-safety:blocked"}, {"name": "authorized-canary"}],
        },
    )
    assert rc == 0
    assert gate["execution_allowed"] is True
    assert gate["gate_required"] is True
    assert gate["has_authorized_canary_label"] is True
    assert gate["reason"] == "Issue allowed only because authorized-canary label is present."
    assert "Status: **PASS**" in md


def main() -> int:
    test_clear_issue_allowed()
    test_blocked_issue_stops_without_authorized_label()
    test_blocked_issue_allowed_with_authorized_label()
    print("Issue execution gate test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
