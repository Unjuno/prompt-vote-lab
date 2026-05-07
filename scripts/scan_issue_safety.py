#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import create_codex_issue_instruction_packet as packet

COMMENT_MARKER = "<!-- prompt-vote-lab:issue-safety-scan:v1 -->"
RUNTIME_COMMENT_MARKER = "<!-- prompt-vote-lab:issue-runtime-safety-scan:v1 -->"

CLEAR_LABEL = "issue-safety:clear"
REVIEW_LABEL = "issue-safety:review"
BLOCKED_LABEL = "issue-safety:blocked"
POST_DETECTED_LABEL = "issue-safety:submission-detected"
RUNTIME_DETECTED_LABEL = "issue-safety:runtime-detected"
AUTHORIZED_CANARY_LABEL = "authorized-canary"
STATUS_LABELS = [CLEAR_LABEL, REVIEW_LABEL, BLOCKED_LABEL]
PHASE_LABELS = [POST_DETECTED_LABEL, RUNTIME_DETECTED_LABEL]
ALL_LABELS = STATUS_LABELS + PHASE_LABELS

LABEL_METADATA = {
    CLEAR_LABEL: {
        "color": "2ea043",
        "description": "Issue safety scan found no unsafe instruction categories.",
    },
    REVIEW_LABEL: {
        "color": "d29922",
        "description": "Issue safety scan found unsafe instruction categories; human review required.",
    },
    BLOCKED_LABEL: {
        "color": "cf222e",
        "description": "Issue should not be used for an agent run until unsafe instructions are corrected.",
    },
    POST_DETECTED_LABEL: {
        "color": "fbca04",
        "description": "Unsafe instruction categories were detected when the Issue was posted or edited.",
    },
    RUNTIME_DETECTED_LABEL: {
        "color": "a371f7",
        "description": "Unsafe instruction categories were detected during a fixed-Issue runtime packet run.",
    },
    AUTHORIZED_CANARY_LABEL: {
        "color": "8250df",
        "description": "Maintainer-approved exception for a controlled canary run of a blocked Issue.",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def issue_from_event(path: Path) -> dict[str, Any]:
    event = read_json(path)
    issue = event.get("issue") or {}
    user = issue.get("user") or {}
    return {
        "issue_number": int(issue.get("number") or 0),
        "issue_title": str(issue.get("title") or "").strip(),
        "issue_url": str(issue.get("html_url") or issue.get("url") or "").strip(),
        "author": str(user.get("login") or "unknown"),
        "created_at": str(issue.get("created_at") or "").strip(),
        "updated_at": str(issue.get("updated_at") or "").strip(),
        "body": str(issue.get("body") or "").strip(),
        "event_action": str(event.get("action") or "unknown"),
    }


def issue_from_raw_json(path: Path) -> dict[str, Any]:
    raw = read_json(path)
    author = raw.get("author") or raw.get("user") or {}
    if isinstance(author, dict):
        author_login = str(author.get("login") or "unknown")
    else:
        author_login = str(author or "unknown")
    return {
        "issue_number": int(raw.get("number") or raw.get("issue_number") or 0),
        "issue_title": str(raw.get("title") or raw.get("issue_title") or "").strip(),
        "issue_url": str(raw.get("url") or raw.get("html_url") or raw.get("issue_url") or "").strip(),
        "author": author_login,
        "created_at": str(raw.get("createdAt") or raw.get("created_at") or "").strip(),
        "updated_at": str(raw.get("updatedAt") or raw.get("updated_at") or "").strip(),
        "body": str(raw.get("body") or "").strip(),
        "event_action": str(raw.get("event_action") or "runtime"),
    }


def labels_for_scan(unsafe_count: int, phase: str) -> tuple[list[str], list[str]]:
    status_to_add = [CLEAR_LABEL] if unsafe_count == 0 else [REVIEW_LABEL, BLOCKED_LABEL]
    phase_to_add = [POST_DETECTED_LABEL] if phase == "issue_event" else [RUNTIME_DETECTED_LABEL]

    labels_to_add = status_to_add + phase_to_add

    # Status labels are mutually exclusive and should reflect the latest scan result.
    # Phase labels are cumulative evidence: a runtime scan must not erase prior posting/edit detection,
    # and a posting/edit scan must not erase prior runtime evidence.
    labels_to_remove = [label for label in STATUS_LABELS if label not in status_to_add]
    return labels_to_add, labels_to_remove


def scan_issue(issue: dict[str, Any], phase: str) -> dict[str, Any]:
    findings = packet.detect_unsafe_instructions(issue["issue_title"], issue["body"])
    safe_task = packet.make_safe_task(issue["issue_title"], issue["body"])
    unsafe_count = len(findings)
    severity = "clear" if unsafe_count == 0 else "blocked"
    labels_to_add, labels_to_remove = labels_for_scan(unsafe_count, phase)

    return {
        "schema_version": "issue-safety-scan-v1",
        "phase": phase,
        "event_action": issue.get("event_action") or "unknown",
        "scanned_at": utc_now(),
        "issue_number": issue["issue_number"],
        "issue_title": issue["issue_title"],
        "issue_url": issue["issue_url"],
        "author": issue["author"],
        "unsafe_instruction_count": unsafe_count,
        "unsafe_instructions_detected": findings,
        "safe_user_task": safe_task,
        "severity": severity,
        "labels_to_add": labels_to_add,
        "labels_to_remove": labels_to_remove,
        "label_metadata": LABEL_METADATA,
        "comment_marker": COMMENT_MARKER if phase == "issue_event" else RUNTIME_COMMENT_MARKER,
        "recommended_action": recommended_action(unsafe_count, phase),
        "normalization_policy": {
            "raw_issue_body_is_policy": False,
            "raw_issue_body_is_requirement_input": True,
            "unsafe_issue_instructions_are_ignored": True,
            "fallback_when_forbidden": "nearest safe static UI prototype",
        },
    }


def recommended_action(unsafe_count: int, phase: str) -> str:
    if unsafe_count == 0:
        return "No unsafe instruction categories were detected. The Issue can proceed to normal review."
    if phase == "issue_event":
        return "Revise the Issue before using it for an agent run, or keep it as an explicitly authorized canary."
    return "Agent execution is blocked unless the maintainer adds the authorized-canary label for a controlled canary run."


def render_comment(scan: dict[str, Any]) -> str:
    marker = scan["comment_marker"]
    phase_label = "投稿/編集時検知" if scan["phase"] == "issue_event" else "実行時検知"
    status = "CLEAR" if scan["unsafe_instruction_count"] == 0 else "BLOCKED / REVIEW REQUIRED"
    lines = [
        marker,
        "## Issue safety scan",
        "",
        f"**Phase:** {phase_label}",
        f"**Status:** {status}",
        f"**Scanned at:** `{scan['scanned_at']}`",
        f"**Unsafe categories:** `{scan['unsafe_instruction_count']}`",
        "",
        "### Safe task extracted",
        "",
        f"> {scan['safe_user_task']}",
        "",
    ]

    if scan["unsafe_instruction_count"]:
        lines.extend(["### Detected unsafe categories", ""])
        for finding in scan["unsafe_instructions_detected"]:
            lines.append(f"- `{finding['id']}` — {finding['label']}")
        lines.extend(
            [
                "",
                "### Required correction",
                "",
                "Remove or reword the unsafe instructions if this Issue is intended for a normal agent run.",
                "Keep the unsafe text only when this Issue is deliberately being used as an authorized canary.",
                f"A blocked Issue requires the `{AUTHORIZED_CANARY_LABEL}` label before agent execution.",
                "",
            ]
        )
    else:
        lines.extend(["No unsafe instruction categories were detected by the current pattern-based scanner.", ""])

    lines.extend(
        [
            "### Detection meaning",
            "",
            "- `投稿/編集時検知`: detected immediately when the Issue was opened or edited.",
            "- `実行時検知`: detected later when the fixed-Issue runtime packet was generated or executed.",
            "",
            f"**Recommended action:** {scan['recommended_action']}",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-event-json")
    parser.add_argument("--issue-json")
    parser.add_argument("--phase", choices=["issue_event", "runtime"], required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    if bool(args.issue_event_json) == bool(args.issue_json):
        raise SystemExit("Provide exactly one of --issue-event-json or --issue-json")

    if args.issue_event_json:
        issue = issue_from_event(Path(args.issue_event_json))
    else:
        issue = issue_from_raw_json(Path(args.issue_json))

    if issue["issue_number"] <= 0:
        raise SystemExit("Issue number must be positive")
    if not issue["issue_title"]:
        raise SystemExit("Issue title is required")

    scan = scan_issue(issue, args.phase)
    Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_json).write_text(json.dumps(scan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.out_md).write_text(render_comment(scan), encoding="utf-8")
    print(json.dumps({"issue_number": issue["issue_number"], "phase": args.phase, "unsafe_instruction_count": scan["unsafe_instruction_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
