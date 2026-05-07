#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "prompt-vote-lab-weekly-issue-finalizer-v1"
OUTCOME_PREFIX = "outcome:"
WEEK_PREFIX = "week:"
PROTECTED_LABELS = {
    "carryover",
    "future-candidate",
    "discussion",
    "bug",
    "admin",
    "do-not-close",
    "pinned",
}
COMPLETED_OUTCOMES = {
    "outcome:implemented",
    "outcome:archived-fixture",
}
NOT_PLANNED_OUTCOMES = {
    "outcome:not-selected",
    "outcome:blocked",
    "outcome:rejected-after-run",
}
ALLOWED_OUTCOMES = COMPLETED_OUTCOMES | NOT_PLANNED_OUTCOMES


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8") or json.dumps(fallback))
    except json.JSONDecodeError:
        return fallback


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def labels_from_issue(issue: dict[str, Any]) -> list[str]:
    labels = issue.get("labels") or []
    out: list[str] = []
    for label in labels:
        if isinstance(label, dict):
            name = str(label.get("name") or "").strip()
        else:
            name = str(label).strip()
        if name:
            out.append(name)
    return sorted(set(out))


def issue_number(issue: dict[str, Any]) -> int:
    return int(issue.get("number") or issue.get("issue_number") or 0)


def issue_title(issue: dict[str, Any]) -> str:
    return str(issue.get("title") or "").strip()


def issue_url(issue: dict[str, Any]) -> str:
    return str(issue.get("url") or issue.get("html_url") or "").strip()


def public_results_issue_numbers(public_results: dict[str, Any]) -> set[int]:
    out: set[int] = set()
    for issue in public_results.get("issues") or []:
        try:
            out.add(int(issue.get("number") or issue.get("issue_number") or 0))
        except (TypeError, ValueError):
            continue
    return out


def public_results_generated_at(public_results: dict[str, Any]) -> str | None:
    value = public_results.get("generated_at")
    return str(value) if value else None


def choose_close_reason(outcome_label: str) -> str:
    if outcome_label in COMPLETED_OUTCOMES:
        return "completed"
    if outcome_label in NOT_PLANNED_OUTCOMES:
        return "not_planned"
    raise ValueError(f"Unsupported outcome label: {outcome_label}")


def issue_decision(
    issue: dict[str, Any],
    *,
    week_id: str,
    public_issue_numbers: set[int],
    require_public_results_membership: bool,
) -> dict[str, Any]:
    number = issue_number(issue)
    labels = labels_from_issue(issue)
    label_set = set(labels)
    week_labels = sorted(label for label in labels if label.startswith(WEEK_PREFIX))
    outcome_labels = sorted(label for label in labels if label.startswith(OUTCOME_PREFIX))
    protected = sorted(label_set & PROTECTED_LABELS)

    skip_reasons: list[str] = []
    if not number:
        skip_reasons.append("missing_issue_number")
    if f"week:{week_id}" not in label_set:
        skip_reasons.append("missing_matching_week_label")
    if len(week_labels) != 1:
        skip_reasons.append("expected_exactly_one_week_label")
    if len(outcome_labels) != 1:
        skip_reasons.append("expected_exactly_one_outcome_label")
    if outcome_labels and outcome_labels[0] not in ALLOWED_OUTCOMES:
        skip_reasons.append("unsupported_outcome_label")
    if protected:
        skip_reasons.append("protected_label_present")
    if require_public_results_membership and number not in public_issue_numbers:
        skip_reasons.append("missing_from_public_results_snapshot")

    if skip_reasons:
        return {
            "number": number,
            "title": issue_title(issue),
            "url": issue_url(issue),
            "labels": labels,
            "action": "skip",
            "skip_reasons": skip_reasons,
            "week_labels": week_labels,
            "outcome_labels": outcome_labels,
            "protected_labels": protected,
        }

    outcome = outcome_labels[0]
    close_reason = choose_close_reason(outcome)
    return {
        "number": number,
        "title": issue_title(issue),
        "url": issue_url(issue),
        "labels": labels,
        "action": "close",
        "week_id": week_id,
        "outcome": outcome,
        "close_reason": close_reason,
        "comment_file": f"comments/{number}.md",
    }


def render_close_comment(item: dict[str, Any], *, public_results_path: str, run_record_hint: str, generated_at: str | None) -> str:
    lines = [
        "<!-- prompt-vote-lab:weekly-issue-finalizer:v1 -->",
        "## Weekly experiment cycle complete",
        "",
        "This Issue is being closed automatically because the weekly experiment cycle has been recorded.",
        "",
        "```text",
        f"week: {item['week_id']}",
        f"outcome: {item['outcome']}",
        f"close_reason: {item['close_reason']}",
        f"public_results: {public_results_path}",
        f"public_results_generated_at: {generated_at or 'unknown'}",
        "```",
        "",
        "The Issue is not deleted. It remains visible through its original URL and GitHub closed-Issue search.",
        "",
        "Evidence locations:",
        "",
        f"- Public results snapshot: `{public_results_path}`",
    ]
    if run_record_hint:
        lines.append(f"- Run record hint: `{run_record_hint}`")
    lines.extend(
        [
            "- This Issue thread contains the finalizer comment and all prior discussion.",
            "",
            "Reason for automatic close:",
            "",
            "```text",
            "Only Issues with both week:* and outcome:* labels are eligible for automatic close.",
            "Issues with carryover, future-candidate, discussion, bug, admin, do-not-close, or pinned labels are skipped.",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Weekly Issue Finalizer plan",
        "",
        f"Generated at: `{plan['generated_at']}`",
        f"Week: `{plan['week_id']}`",
        f"Dry run: `{plan['dry_run']}`",
        f"Require public results membership: `{plan['require_public_results_membership']}`",
        "",
        "## Summary",
        "",
        "| metric | value |",
        "| --- | --- |",
        f"| close_count | {plan['summary']['close_count']} |",
        f"| skip_count | {plan['summary']['skip_count']} |",
        "",
        "## Issues to close",
        "",
        "| # | outcome | reason | title |",
        "| --- | --- | --- | --- |",
    ]
    for item in plan["to_close"]:
        lines.append(f"| {item['number']} | {item['outcome']} | {item['close_reason']} | {item['title']} |")
    lines.extend(["", "## Skipped Issues", "", "| # | reasons | title |", "| --- | --- | --- |"])
    for item in plan["skipped"]:
        lines.append(f"| {item['number']} | {', '.join(item['skip_reasons'])} | {item['title']} |")
    lines.append("")
    return "\n".join(lines)


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    issues_raw = read_json(Path(args.issues_json), [])
    if isinstance(issues_raw, dict):
        issues = issues_raw.get("issues") or issues_raw.get("items") or []
    else:
        issues = issues_raw
    if not isinstance(issues, list):
        raise ValueError("issues_json must contain a list or an object with issues/items")

    public_results = read_json(Path(args.public_results), {})
    public_numbers = public_results_issue_numbers(public_results)
    generated_at = public_results_generated_at(public_results)

    results = [
        issue_decision(
            issue,
            week_id=args.week_id,
            public_issue_numbers=public_numbers,
            require_public_results_membership=args.require_public_results_membership,
        )
        for issue in issues
    ]
    to_close = [item for item in results if item["action"] == "close"]
    skipped = [item for item in results if item["action"] == "skip"]

    plan = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "week_id": args.week_id,
        "dry_run": args.dry_run,
        "public_results_path": args.public_results,
        "public_results_generated_at": generated_at,
        "require_public_results_membership": args.require_public_results_membership,
        "summary": {
            "close_count": len(to_close),
            "skip_count": len(skipped),
        },
        "to_close": to_close,
        "skipped": skipped,
    }
    return plan


def write_outputs(plan: dict[str, Any], args: argparse.Namespace) -> None:
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    comments_dir = Path(args.comments_dir)
    write_text(out_json, json.dumps(plan, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    write_text(out_md, render_markdown(plan))
    comments_dir.mkdir(parents=True, exist_ok=True)
    for item in plan["to_close"]:
        comment = render_close_comment(
            item,
            public_results_path=args.public_results,
            run_record_hint=args.run_record_hint,
            generated_at=plan.get("public_results_generated_at"),
        )
        write_text(comments_dir / f"{item['number']}.md", comment)


def valid_week_id(value: str) -> str:
    if not re.fullmatch(r"\d{4}-W\d{2}|initial|test-week", value):
        raise argparse.ArgumentTypeError("week_id must look like YYYY-Www, initial, or test-week")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issues-json", required=True)
    parser.add_argument("--public-results", default="data/public-results.json")
    parser.add_argument("--week-id", required=True, type=valid_week_id)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    parser.add_argument("--comments-dir", required=True)
    parser.add_argument("--run-record-hint", default="runs/")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--require-public-results-membership", action="store_true")
    args = parser.parse_args()

    plan = build_plan(args)
    write_outputs(plan, args)
    print(json.dumps(plan["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
