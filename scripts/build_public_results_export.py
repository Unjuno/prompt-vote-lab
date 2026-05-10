#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "prompt-vote-lab-public-results-export-v1"
TERMINAL_WORKFLOW_STATUSES = {"completed"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8") or json.dumps(fallback))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def connection_nodes(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        nodes = value.get("nodes")
        if isinstance(nodes, list):
            return nodes
    return []


def reaction_count(item: dict[str, Any], content: str) -> int:
    for group in item.get("reactionGroups") or []:
        if str(group.get("content") or "").upper() == content.upper():
            return int(group.get("users", {}).get("totalCount") or 0)
    return 0


def compact_labels(item: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for label in connection_nodes(item.get("labels")):
        if isinstance(label, dict):
            name = str(label.get("name") or "").strip()
        else:
            name = str(label).strip()
        if name:
            out.append(name)
    return sorted(set(out))


def compact_author(item: dict[str, Any]) -> str:
    author = item.get("author") or {}
    if isinstance(author, dict):
        return str(author.get("login") or "unknown")
    return str(author or "unknown")


def comment_count(item: dict[str, Any]) -> int | None:
    comments = item.get("comments")
    if isinstance(comments, dict):
        return int(comments.get("totalCount") or 0)
    if comments is None:
        return None
    return int(comments)


def normalize_issue(issue: dict[str, Any]) -> dict[str, Any]:
    labels = compact_labels(issue)
    body = str(issue.get("body") or "")
    return {
        "number": issue.get("number"),
        "title": issue.get("title"),
        "state": issue.get("state"),
        "url": issue.get("url"),
        "author": compact_author(issue),
        "created_at": issue.get("createdAt"),
        "updated_at": issue.get("updatedAt"),
        "closed_at": issue.get("closedAt"),
        "labels": labels,
        "reaction_plus_one_count": reaction_count(issue, "THUMBS_UP"),
        "reaction_minus_one_count": reaction_count(issue, "THUMBS_DOWN"),
        "comment_count": comment_count(issue),
        "body": body,
        "body_length": len(body),
        "safety": {
            "clear": "issue-safety:clear" in labels,
            "review": "issue-safety:review" in labels,
            "blocked": "issue-safety:blocked" in labels,
            "submission_detected": "issue-safety:submission-detected" in labels,
            "runtime_detected": "issue-safety:runtime-detected" in labels,
            "authorized_canary": "authorized-canary" in labels,
        },
    }


def normalize_pr(pr: dict[str, Any]) -> dict[str, Any]:
    labels = compact_labels(pr)
    body = str(pr.get("body") or "")
    compact_files = []
    for file in connection_nodes(pr.get("files")):
        if isinstance(file, dict):
            compact_files.append(
                {
                    "path": file.get("path"),
                    "additions": file.get("additions"),
                    "deletions": file.get("deletions"),
                }
            )
    return {
        "number": pr.get("number"),
        "title": pr.get("title"),
        "state": pr.get("state"),
        "url": pr.get("url"),
        "author": compact_author(pr),
        "created_at": pr.get("createdAt"),
        "updated_at": pr.get("updatedAt"),
        "closed_at": pr.get("closedAt"),
        "merged_at": pr.get("mergedAt"),
        "merged_by": compact_author({"author": pr.get("mergedBy")}) if pr.get("mergedBy") else None,
        "base_ref_name": pr.get("baseRefName"),
        "head_ref_name": pr.get("headRefName"),
        "head_ref_oid": pr.get("headRefOid"),
        "merge_commit_oid": (pr.get("mergeCommit") or {}).get("oid") if isinstance(pr.get("mergeCommit"), dict) else None,
        "labels": labels,
        "changed_files": pr.get("changedFiles"),
        "additions": pr.get("additions"),
        "deletions": pr.get("deletions"),
        "review_decision": pr.get("reviewDecision"),
        "comment_count": comment_count(pr),
        "reaction_plus_one_count": reaction_count(pr, "THUMBS_UP"),
        "files": compact_files,
        "body": body,
        "body_length": len(body),
    }


def is_terminal_workflow_run(run: dict[str, Any]) -> bool:
    return str(run.get("status") or "").lower() in TERMINAL_WORKFLOW_STATUSES


def normalize_run(run: dict[str, Any]) -> dict[str, Any] | None:
    if not is_terminal_workflow_run(run):
        return None
    return {
        "database_id": run.get("databaseId"),
        "name": run.get("name"),
        "workflow_name": run.get("workflowName"),
        "display_title": run.get("displayTitle"),
        "event": run.get("event"),
        "status": run.get("status"),
        "conclusion": run.get("conclusion"),
        "created_at": run.get("createdAt"),
        "updated_at": run.get("updatedAt"),
        "head_branch": run.get("headBranch"),
        "head_sha": run.get("headSha"),
        "url": run.get("url"),
    }


def normalize_runs(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for run in runs:
        item = normalize_run(run)
        if item is not None:
            normalized.append(item)
    return normalized


def run_records(runs_dir: Path) -> list[dict[str, Any]]:
    records = []
    if not runs_dir.exists():
        return records
    for path in sorted(runs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        records.append(
            {
                "path": str(path),
                "title": text.splitlines()[0].lstrip("# ").strip() if text.splitlines() else path.name,
                "size_bytes": path.stat().st_size,
                "content": text,
            }
        )
    return records


def summarize(issues: list[dict[str, Any]], prs: list[dict[str, Any]], runs: list[dict[str, Any]], records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "issue_count": len(issues),
        "open_issue_count": sum(1 for issue in issues if issue.get("state") == "OPEN"),
        "blocked_issue_count": sum(1 for issue in issues if issue.get("safety", {}).get("blocked")),
        "clear_issue_count": sum(1 for issue in issues if issue.get("safety", {}).get("clear")),
        "authorized_canary_issue_count": sum(1 for issue in issues if issue.get("safety", {}).get("authorized_canary")),
        "pr_count": len(prs),
        "open_pr_count": sum(1 for pr in prs if pr.get("state") == "OPEN"),
        "merged_pr_count": sum(1 for pr in prs if pr.get("merged_at")),
        "workflow_run_count": len(runs),
        "run_record_count": len(records),
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines) + "\n"


def render_md(export: dict[str, Any]) -> str:
    summary = export["summary"]
    issues = export["issues"][:30]
    prs = export["pull_requests"][:30]
    runs = export["workflow_runs"][:30]
    lines = [
        "# Prompt Vote Lab public results export",
        "",
        f"Generated at: `{export['generated_at']}`",
        "",
        "This file is a raw results surface for participants. It does not score prompts or recommend improvements.",
        "",
        "## Summary",
        "",
        markdown_table(
            ["metric", "value"],
            [[key, value] for key, value in summary.items()],
        ),
        "## Recent Issues",
        "",
        markdown_table(
            ["#", "state", "+1", "labels", "title"],
            [[i.get("number"), i.get("state"), i.get("reaction_plus_one_count"), ", ".join(i.get("labels") or []), i.get("title")] for i in issues],
        ),
        "## Recent Pull Requests",
        "",
        markdown_table(
            ["#", "state", "changed", "+/-", "title"],
            [[p.get("number"), p.get("state"), p.get("changed_files"), f"{p.get('additions')}/{p.get('deletions')}", p.get("title")] for p in prs],
        ),
        "## Recent Workflow Runs",
        "",
        markdown_table(
            ["id", "workflow", "event", "status", "conclusion", "title"],
            [[r.get("database_id"), r.get("workflow_name"), r.get("event"), r.get("status"), r.get("conclusion"), r.get("display_title")] for r in runs],
        ),
        "## Raw JSON",
        "",
        "See `public-results.json` in the same export artifact or committed data snapshot.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issues", required=True)
    parser.add_argument("--prs", required=True)
    parser.add_argument("--workflow-runs", required=True)
    parser.add_argument("--labels", required=True)
    parser.add_argument("--runs-dir", default="runs")
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    issues = [normalize_issue(item) for item in read_json(Path(args.issues), [])]
    prs = [normalize_pr(item) for item in read_json(Path(args.prs), [])]
    workflow_runs = normalize_runs(read_json(Path(args.workflow_runs), []))
    labels = read_json(Path(args.labels), [])
    records = run_records(Path(args.runs_dir))

    export = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "scope": {
            "privacy": "public GitHub repository data only",
            "interpretation": "none; participant analysis expected",
            "secrets": "not collected",
            "raw_actions_logs": "not collected",
            "workflow_runs": "terminal workflow runs only; queued and in-progress runs are excluded",
        },
        "summary": summarize(issues, prs, workflow_runs, records),
        "issues": issues,
        "pull_requests": prs,
        "workflow_runs": workflow_runs,
        "labels": labels,
        "run_records": records,
    }

    write_json(Path(args.out_json), export)
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text(render_md(export), encoding="utf-8")
    print(args.out_json)
    print(args.out_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
