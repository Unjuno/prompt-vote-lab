#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ALLOWED_FILES = {
    "lab/index.html",
    "lab/style.css",
    "lab/app.js",
}

FORBIDDEN_PATCH_PATTERNS = [
    re.compile(r"^\+.*<script[^>]+src=", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\+.*\beval\s*\(", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\+.*\bnew\s+Function\s*\(", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\+.*\bfetch\s*\(", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\+.*\bXMLHttpRequest\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\+.*\blocalStorage\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\+.*\bsessionStorage\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\+.*\bdocument\.cookie\b", re.IGNORECASE | re.MULTILINE),
]


def extract_patch(raw: str) -> str:
    text = raw.strip()
    fenced = re.search(r"```(?:diff|patch)?\s*(.*?)\s*```", text, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()

    start = text.find("diff --git ")
    if start == -1:
        raise ValueError("No unified diff found in Codex output")
    patch = text[start:].strip() + "\n"
    if "@@" not in patch:
        raise ValueError("Patch has no hunk header")
    return patch


def normalize_patch_path(path: str) -> str:
    path = path.strip()
    if path == "/dev/null":
        return path
    if path.startswith("a/") or path.startswith("b/"):
        path = path[2:]
    return path


def validate_patch_paths(patch: str) -> None:
    touched: set[str] = set()
    for line in patch.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) < 4:
                raise ValueError(f"Malformed diff header: {line}")
            paths = [normalize_patch_path(parts[2]), normalize_patch_path(parts[3])]
        elif line.startswith("--- ") or line.startswith("+++ "):
            paths = [normalize_patch_path(line.split(maxsplit=1)[1])]
        else:
            continue

        for path in paths:
            if path == "/dev/null":
                raise ValueError("Creating or deleting files is not allowed")
            if path not in ALLOWED_FILES:
                raise ValueError(f"Patch touches forbidden path: {path}")
            touched.add(path)

    if not touched:
        raise ValueError("Patch touches no files")


def validate_patch_content(patch: str) -> None:
    for pattern in FORBIDDEN_PATCH_PATTERNS:
        if pattern.search(patch):
            raise ValueError(f"Forbidden patch content matched: {pattern.pattern}")


def run_git_apply(patch_path: Path) -> None:
    check = subprocess.run(
        ["git", "apply", "--check", "--whitespace=nowarn", str(patch_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check.returncode != 0:
        raise RuntimeError("git apply --check failed:\n" + check.stdout + check.stderr)

    apply = subprocess.run(
        ["git", "apply", "--whitespace=nowarn", str(patch_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if apply.returncode != 0:
        raise RuntimeError("git apply failed:\n" + apply.stdout + apply.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and apply a Codex unified diff writeback patch.")
    parser.add_argument("--input", required=True, help="Path to Codex last-message text")
    parser.add_argument("--patch-out", default=".tmp/codex-writeback.patch")
    args = parser.parse_args()

    raw = Path(args.input).read_text(encoding="utf-8", errors="replace")
    patch = extract_patch(raw)
    validate_patch_paths(patch)
    validate_patch_content(patch)

    patch_out = Path(args.patch_out)
    patch_out.parent.mkdir(parents=True, exist_ok=True)
    patch_out.write_text(patch, encoding="utf-8")
    run_git_apply(patch_out)

    print(f"Applied Codex writeback patch: {patch_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
