#!/usr/bin/env python3
"""Mechanical gate for PARTIAL continuation decisions.

No network calls. No model calls.

The gate decides whether a PARTIAL implementation result is small and safe
enough to be considered for a separate continuation run.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path


ALLOWED_FILES = {"lab/index.html", "lab/style.css", "lab/app.js"}
FORBIDDEN_PATTERNS = [
    re.compile(r"<script[^>]+src=['\"]https?://", re.I),
    re.compile(r"\bfetch\s*\(", re.I),
    re.compile(r"\bXMLHttpRequest\b", re.I),
    re.compile(r"\bWebSocket\b", re.I),
    re.compile(r"\bEventSource\b", re.I),
    re.compile(r"\beval\s*\(", re.I),
    re.compile(r"document\.cookie", re.I),
    re.compile(r"navigator\.sendBeacon", re.I),
    re.compile(r"new Function\s*\([^)]*(user|input|textarea|location|hash|search|params|localStorage|sessionStorage|indexedDB|imported|json|body|prompt|innerText|textContent|value)", re.I),
]


@dataclass
class GateResult:
    decision: str
    changed_files: list[str]
    total_added: int
    total_deleted: int
    max_file_delta: int
    reasons: list[str]


def run_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], text=True)


def changed_files(base_ref: str, head_ref: str) -> list[str]:
    output = run_git(["diff", "--name-only", base_ref, head_ref])
    return [line.strip() for line in output.splitlines() if line.strip()]


def numstat(base_ref: str, head_ref: str) -> tuple[int, int, int]:
    output = run_git(["diff", "--numstat", base_ref, head_ref])
    total_added = 0
    total_deleted = 0
    max_file_delta = 0
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added_s, deleted_s, _path = parts[:3]
        added = int(added_s) if added_s.isdigit() else 0
        deleted = int(deleted_s) if deleted_s.isdigit() else 0
        total_added += added
        total_deleted += deleted
        max_file_delta = max(max_file_delta, added + deleted)
    return total_added, total_deleted, max_file_delta


def file_at_ref(ref: str, path: str) -> str:
    try:
        return run_git(["show", f"{ref}:{path}"])
    except subprocess.CalledProcessError:
        return ""


def forbidden_hits(head_ref: str, files: list[str]) -> list[str]:
    hits: list[str] = []
    for path in files:
        if path not in ALLOWED_FILES:
            continue
        text = file_at_ref(head_ref, path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                hits.append(f"{path}: {pattern.pattern}")
    return hits


def evaluate(base_ref: str, head_ref: str, max_total_delta: int, max_file_delta_limit: int) -> GateResult:
    files = changed_files(base_ref, head_ref)
    added, deleted, max_delta = numstat(base_ref, head_ref)
    total_delta = added + deleted
    reasons: list[str] = []

    if not files:
        reasons.append("no files changed")
    outside = [path for path in files if path not in ALLOWED_FILES]
    if outside:
        reasons.append(f"changes outside lab allowlist: {outside}")
    if len(files) > len(ALLOWED_FILES):
        reasons.append(f"too many changed files: {len(files)}")
    if total_delta > max_total_delta:
        reasons.append(f"total diff too large: {total_delta} > {max_total_delta}")
    if max_delta > max_file_delta_limit:
        reasons.append(f"single-file diff too large: {max_delta} > {max_file_delta_limit}")
    hits = forbidden_hits(head_ref, files)
    if hits:
        reasons.append(f"forbidden runtime patterns: {hits}")

    return GateResult(
        decision="CONTINUE_ALLOWED" if not reasons else "STOP",
        changed_files=files,
        total_added=added,
        total_deleted=deleted,
        max_file_delta=max_delta,
        reasons=reasons,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--max-total-delta", type=int, default=220)
    parser.add_argument("--max-file-delta", type=int, default=140)
    parser.add_argument("--out", default=".tmp/continuation-gate.json")
    args = parser.parse_args()

    result = evaluate(args.base, args.head, args.max_total_delta, args.max_file_delta)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    return 0 if result.decision == "CONTINUE_ALLOWED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
