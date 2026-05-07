#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AUTHORIZED_CANARY_LABEL = "authorized-canary"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def label_names(issue: dict[str, Any]) -> list[str]:
    labels = issue.get("labels") or []
    names: list[str] = []
    for label in labels:
        if isinstance(label, dict):
            name = str(label.get("name") or "").strip()
        else:
            name = str(label).strip()
        if name:
            names.append(name)
    return names


def evaluate_gate(scan: dict[str, Any], issue: dict[str, Any]) -> dict[str, Any]:
    labels = sorted(set(label_names(issue)))
    unsafe_count = int(scan.get("unsafe_instruction_count") or 0)
    severity = str(scan.get("severity") or "clear")
    has_authorized_canary = AUTHORIZED_CANARY_LABEL in labels
    needs_gate = unsafe_count > 0 or severity == "blocked"
    execution_allowed = (not needs_gate) or has_authorized_canary
    if execution_allowed and needs_gate:
        reason = "Issue allowed only because authorized-canary label is present."
    elif execution_allowed:
        reason = "Issue safety scan is clear."
    else:
        reason = "Issue requires authorized-canary label before agent execution."

    return {
        "schema_version": "issue-execution-gate-v1",
        "checked_at": utc_now(),
        "issue_number": int(scan.get("issue_number") or issue.get("number") or 0),
        "issue_title": str(scan.get("issue_title") or issue.get("title") or ""),
        "unsafe_instruction_count": unsafe_count,
        "severity": severity,
        "labels": labels,
        "required_exception_label": AUTHORIZED_CANARY_LABEL,
        "has_authorized_canary_label": has_authorized_canary,
        "gate_required": needs_gate,
        "execution_allowed": execution_allowed,
        "reason": reason,
    }


def render_markdown(gate: dict[str, Any]) -> str:
    status = "PASS" if gate["execution_allowed"] else "STOP"
    lines = [
        "# Issue execution gate",
        "",
        f"Status: **{status}**",
        "",
        f"Issue: #{gate['issue_number']} {gate['issue_title']}",
        f"Unsafe categories: `{gate['unsafe_instruction_count']}`",
        f"Severity: `{gate['severity']}`",
        f"Required exception label: `{gate['required_exception_label']}`",
        f"Has exception label: `{str(gate['has_authorized_canary_label']).lower()}`",
        "",
        f"Reason: {gate['reason']}",
        "",
        "Labels:",
    ]
    if gate["labels"]:
        lines.extend(f"- `{name}`" for name in gate["labels"])
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan-json", required=True)
    parser.add_argument("--issue-json", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    scan = read_json(Path(args.scan_json))
    issue = read_json(Path(args.issue_json))
    gate = evaluate_gate(scan, issue)

    Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_json).write_text(json.dumps(gate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.out_md).write_text(render_markdown(gate), encoding="utf-8")
    print(json.dumps({"execution_allowed": gate["execution_allowed"], "reason": gate["reason"]}, sort_keys=True))
    return 0 if gate["execution_allowed"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
