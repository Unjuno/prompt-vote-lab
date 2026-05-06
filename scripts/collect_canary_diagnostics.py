#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

DEFAULT_ALLOWED_FILES = [
    "lab/index.html",
    "lab/style.css",
    "lab/app.js",
]

EXPECTED_INTERNAL_ARTIFACTS = [
    "codex-events.jsonl",
    "codex-last-message.txt",
    "codex-stderr.txt",
    "codex-stdout.txt",
    "git-status-before.txt",
    "git-status-after.txt",
    "git-diff-name-only.txt",
    "git-diff-stat.txt",
    "git-diff.patch",
    "file-hashes-before.json",
    "file-hashes-after.json",
    "check-results.json",
    "failure-summary.json",
    "artifact-manifest.json",
]


def run_git(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_hashes(files: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name in files:
        path = Path(name)
        result[name] = {
            "exists": path.exists(),
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size if path.exists() and path.is_file() else None,
        }
    return result


def parse_name_only(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def classify_failure(changed_files: list[str], allowed_files: list[str], codex_stderr: str, codex_events: str) -> str:
    combined = "\n".join([codex_stderr, codex_events]).lower()
    if "unauthorized" in combined or "authentication" in combined:
        return "auth_failure"
    if "model" in combined and ("not found" in combined or "access" in combined):
        return "model_access_failure"
    if "bwrap" in combined or "sandbox" in combined:
        return "sandbox_failure"
    if not changed_files:
        return "no_changes"
    forbidden = [path for path in changed_files if path not in allowed_files]
    if forbidden:
        return "forbidden_changed_file"
    return "unknown_failure"


def normalize_status(status: str) -> str:
    return status.strip().lower()


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect canary diagnostics artifacts.")
    parser.add_argument("--out-dir", default=".tmp/canary-diagnostics")
    parser.add_argument("--canary-id", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--runner-mode", required=True)
    parser.add_argument("--sandbox-mode", required=True)
    parser.add_argument("--status", default="unknown")
    parser.add_argument("--failure-step", default="unknown")
    parser.add_argument("--allowed-file", action="append", default=[])
    parser.add_argument("--codex-events", default=".tmp/codex-events.jsonl")
    parser.add_argument("--codex-last-message", default=".tmp/codex-last-message.txt")
    parser.add_argument("--codex-stderr", default=".tmp/codex-stderr.txt")
    parser.add_argument("--codex-stdout", default=".tmp/codex-stdout.txt")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    allowed_files = args.allowed_file or DEFAULT_ALLOWED_FILES

    rc, status_after, status_err = run_git(["status", "--porcelain"])
    write_text(out_dir / "git-status-after.txt", status_after + (status_err if status_err else ""))

    rc, name_only, name_err = run_git(["diff", "--name-only", "--"])
    write_text(out_dir / "git-diff-name-only.txt", name_only + (name_err if name_err else ""))

    rc, diff_stat, stat_err = run_git(["diff", "--stat", "--"])
    write_text(out_dir / "git-diff-stat.txt", diff_stat + (stat_err if stat_err else ""))

    rc, diff_patch, patch_err = run_git(["diff", "--", *allowed_files])
    write_text(out_dir / "git-diff.patch", diff_patch + (patch_err if patch_err else ""))

    hashes_after = collect_hashes(allowed_files)
    write_text(out_dir / "file-hashes-after.json", json.dumps(hashes_after, indent=2, sort_keys=True) + "\n")

    codex_events_path = Path(args.codex_events)
    codex_last_path = Path(args.codex_last_message)
    codex_stderr_path = Path(args.codex_stderr)
    codex_stdout_path = Path(args.codex_stdout)

    for source, dest in [
        (codex_events_path, out_dir / "codex-events.jsonl"),
        (codex_last_path, out_dir / "codex-last-message.txt"),
        (codex_stderr_path, out_dir / "codex-stderr.txt"),
        (codex_stdout_path, out_dir / "codex-stdout.txt"),
    ]:
        if source.exists():
            dest.write_bytes(source.read_bytes())
        else:
            write_text(dest, "")

    if not (out_dir / "git-status-before.txt").exists():
        write_text(out_dir / "git-status-before.txt", "not captured\n")
    if not (out_dir / "file-hashes-before.json").exists():
        write_text(out_dir / "file-hashes-before.json", "{}\n")

    changed_files = parse_name_only(name_only)
    codex_stderr = (out_dir / "codex-stderr.txt").read_text(encoding="utf-8", errors="replace")
    codex_events = (out_dir / "codex-events.jsonl").read_text(encoding="utf-8", errors="replace")
    normalized_status = normalize_status(args.status)
    if normalized_status == "success":
        failure_type = "none"
    else:
        failure_type = classify_failure(changed_files, allowed_files, codex_stderr, codex_events)

    check_results = {
        "changed_files": changed_files,
        "allowed_files": allowed_files,
        "forbidden_changed_files": [path for path in changed_files if path not in allowed_files],
        "has_changes": bool(changed_files),
    }
    write_text(out_dir / "check-results.json", json.dumps(check_results, indent=2, sort_keys=True) + "\n")

    failure_summary = {
        "canary_id": args.canary_id,
        "status": args.status,
        "failure_step": args.failure_step,
        "failure_type": failure_type,
        "model": args.model,
        "runner_mode": args.runner_mode,
        "sandbox_mode": args.sandbox_mode,
        "changed_files": changed_files,
    }
    write_text(out_dir / "failure-summary.json", json.dumps(failure_summary, indent=2, sort_keys=True) + "\n")

    manifest = []
    for name in EXPECTED_INTERNAL_ARTIFACTS:
        path = out_dir / name
        manifest.append(
            {
                "name": name,
                "exists": path.exists(),
                "size_bytes": path.stat().st_size if path.exists() else None,
                "sha256": sha256_file(path),
            }
        )
    write_text(out_dir / "artifact-manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    print(f"Collected canary diagnostics in {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
