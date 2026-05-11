#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "prompt-vote-lab-public-agent-run-bundle-v1"

# Primary policy: publish raw evidence where safe, not model-written summaries.
# Files not listed here are omitted by default.
PUBLIC_RAW_ALLOWLIST = [
    "codex-events.jsonl",
    "codex-last-message.txt",
    "codex-exit-code.txt",
    "policy-agent-container-exit-code.txt",
    "policy-agent-diff-name-only.txt",
    "policy-agent-diff.patch",
    "policy-agent-copied-files.txt",
    "issue-instruction-container-exit-code.txt",
    "issue-instruction-diff-name-only.txt",
    "issue-instruction-diff.patch",
    "issue-instruction-copied-files.txt",
    "git-diff-name-only.txt",
    "git-diff-stat.txt",
    "git-diff.patch",
    "check-results.json",
    "failure-summary.json",
    "artifact-manifest.json",
    "file-hashes-before.json",
    "file-hashes-after.json",
    "credential-presence-check.txt",
    "policy-allowed-paths.json",
    "policy-denied-access.txt",
    "task-write-test-exit-code.txt",
    "issue-execution-gate.json",
    "issue-execution-gate.md",
    "runtime-issue-safety-scan.json",
    "runtime-issue-safety-comment.md",
    "source-issue.raw.json",
    "task-run-manifest.json",
    "task-allowed-files.json",
    "task-execution-policy.md",
    "task-selected-issue.json",
    "task-raw-issue-body.md",
    "task-issue-safety-analysis.json",
    "task-instruction-brief.md",
    "task-selected-prompt.md",
    "task-static-ui-v1.0.md",
    "task-agent-run-policy-v1.0.md",
    "task-file-hashes.json",
    "task-visible-files.txt",
    "task-visible-files-container.txt",
    "task-visible-files-container-after.txt",
    "container-visible-files-before.txt",
    "container-visible-files-after.txt",
]

# Files that can contain login flows, package manager noise, full mount paths, stderr details, or environment details.
# They remain internal diagnostics unless a later review explicitly promotes them.
PUBLIC_RAW_DENYLIST = [
    "codex-login-stdout.txt",
    "codex-login-stderr.txt",
    "codex-stderr.txt",
    "codex-stdout.txt",
    "policy-agent-container-stdout.txt",
    "policy-agent-container-stderr.txt",
    "issue-instruction-container-stdout.txt",
    "issue-instruction-container-stderr.txt",
    "npm-install-codex.txt",
    "npm-install-codex-stderr.txt",
    "policy-container-mounts.txt",
    "container-runtime-files-after.txt",
    "container-runtime-dirs-before.txt",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(OPENAI_API_KEY\s*[:=]\s*)[^\s]+"),
    re.compile(r"(?i)(GITHUB_TOKEN\s*[:=]\s*)[^\s]+"),
    re.compile(r"(?i)(GH_TOKEN\s*[:=]\s*)[^\s]+"),
    re.compile(r"(?i)(authorization:\s*bearer\s+)[A-Za-z0-9_.\-]+"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return sha256_bytes(path.read_bytes())


def redact_text(text: str) -> tuple[str, list[str]]:
    redactions: list[str] = []
    out = text
    for index, pattern in enumerate(SECRET_PATTERNS, start=1):
        new, count = pattern.subn(lambda match: f"{match.group(1) if match.groups() else ''}[REDACTED_SECRET]", out)
        if count:
            redactions.append(f"pattern_{index}:{count}")
        out = new
    return out, redactions


def copy_redacted(source: Path, dest: Path) -> dict[str, Any]:
    raw = source.read_bytes()
    raw_sha = sha256_bytes(raw)
    try:
        text = raw.decode("utf-8")
        redacted_text, redactions = redact_text(text)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(redacted_text, encoding="utf-8")
        public_sha = sha256_file(dest)
        return {
            "name": source.name,
            "included": True,
            "encoding": "utf-8",
            "source_size_bytes": len(raw),
            "public_size_bytes": dest.stat().st_size,
            "source_sha256": raw_sha,
            "public_sha256": public_sha,
            "redactions": redactions,
        }
    except UnicodeDecodeError:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        return {
            "name": source.name,
            "included": True,
            "encoding": "binary",
            "source_size_bytes": len(raw),
            "public_size_bytes": dest.stat().st_size,
            "source_sha256": raw_sha,
            "public_sha256": sha256_file(dest),
            "redactions": [],
        }


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace") or json.dumps(fallback))
    except json.JSONDecodeError:
        return fallback


def event_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())


def line_list(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]


def build_bundle(diag: Path, out_dir: Path, run_id: str, issue_number: str, pr_number: str) -> dict[str, Any]:
    raw_dir = out_dir / "raw"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)

    manifest_entries: list[dict[str, Any]] = []
    for name in PUBLIC_RAW_ALLOWLIST:
        source = diag / name
        if not source.exists() or not source.is_file():
            manifest_entries.append({"name": name, "included": False, "reason": "not_found"})
            continue
        manifest_entries.append(copy_redacted(source, raw_dir / name))

    omitted = []
    for path in sorted(diag.iterdir()) if diag.exists() else []:
        if not path.is_file():
            continue
        if path.name in PUBLIC_RAW_ALLOWLIST:
            continue
        reason = "denylisted" if path.name in PUBLIC_RAW_DENYLIST else "not_allowlisted"
        omitted.append(
            {
                "name": path.name,
                "reason": reason,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

    check_results = read_json(diag / "check-results.json", {})
    safety = read_json(diag / "task-issue-safety-analysis.json", {})
    gate = read_json(diag / "issue-execution-gate.json", {})
    failure_summary = read_json(diag / "failure-summary.json", {})

    index = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_id": run_id,
        "issue_number": issue_number or None,
        "pr_number": pr_number or None,
        "policy": {
            "primary_artifact": "redacted raw files",
            "summary_is_not_primary_evidence": True,
            "raw_actions_logs_included": False,
            "secrets_included": False,
            "denylisted_files_omitted": PUBLIC_RAW_DENYLIST,
        },
        "quick_index": {
            "codex_event_lines": event_count(diag / "codex-events.jsonl"),
            "changed_files": check_results.get("changed_files") or line_list(diag / "policy-agent-diff-name-only.txt") or line_list(diag / "issue-instruction-diff-name-only.txt"),
            "forbidden_changed_files": check_results.get("forbidden_changed_files"),
            "unsafe_instruction_count": safety.get("unsafe_instruction_count"),
            "unsafe_categories": [item.get("id") for item in safety.get("unsafe_instructions_detected", []) if isinstance(item, dict)],
            "execution_allowed": gate.get("execution_allowed"),
            "failure_type": failure_summary.get("failure_type"),
        },
        "included_files": manifest_entries,
        "omitted_files": omitted,
    }
    (out_dir / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "README.md").write_text(render_readme(index), encoding="utf-8")
    return index


def render_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines)


def render_readme(index: dict[str, Any]) -> str:
    quick = index["quick_index"]
    included = [entry for entry in index["included_files"] if entry.get("included")]
    omitted = index["omitted_files"]
    return "\n".join(
        [
            "# Public agent run bundle",
            "",
            "This bundle exposes redacted raw evidence for participant analysis.",
            "It does not replace raw evidence with model-written interpretation.",
            "",
            "## Quick index",
            "",
            render_table(
                ["field", "value"],
                [
                    ["run_id", index.get("run_id")],
                    ["issue_number", index.get("issue_number")],
                    ["pr_number", index.get("pr_number")],
                    ["codex_event_lines", quick.get("codex_event_lines")],
                    ["changed_files", ", ".join(quick.get("changed_files") or [])],
                    ["forbidden_changed_files", ", ".join(quick.get("forbidden_changed_files") or [])],
                    ["unsafe_instruction_count", quick.get("unsafe_instruction_count")],
                    ["unsafe_categories", ", ".join(quick.get("unsafe_categories") or [])],
                    ["execution_allowed", quick.get("execution_allowed")],
                    ["failure_type", quick.get("failure_type")],
                ],
            ),
            "",
            "## Included raw files",
            "",
            render_table(
                ["file", "size", "redactions"],
                [[entry.get("name"), entry.get("public_size_bytes"), ", ".join(entry.get("redactions") or [])] for entry in included],
            ),
            "",
            "## Omitted diagnostic files",
            "",
            render_table(
                ["file", "reason"],
                [[entry.get("name"), entry.get("reason")] for entry in omitted],
            ),
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostics-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--run-id", default="unknown")
    parser.add_argument("--issue-number", default="")
    parser.add_argument("--pr-number", default="")
    args = parser.parse_args()
    build_bundle(Path(args.diagnostics_dir), Path(args.out_dir), args.run_id, args.issue_number, args.pr_number)
    print(args.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
