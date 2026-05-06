#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ALLOWED_FILES = {
    "lab/index.html",
    "lab/style.css",
    "lab/app.js",
}

MAX_FILE_BYTES = 200_000


def extract_json(raw: str) -> dict[str, Any]:
    text = raw.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end < start:
            raise ValueError("No JSON object found in Codex output")
        text = text[start : end + 1]

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON output: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return data


def validate_payload(data: dict[str, Any]) -> list[tuple[str, str]]:
    files = data.get("files")
    if not isinstance(files, list) or not files:
        raise ValueError("JSON must contain a non-empty files list")

    seen: set[str] = set()
    updates: list[tuple[str, str]] = []
    for item in files:
        if not isinstance(item, dict):
            raise ValueError("Each files item must be an object")
        path = item.get("path")
        content = item.get("content")
        if not isinstance(path, str) or path not in ALLOWED_FILES:
            raise ValueError(f"Forbidden or invalid path: {path!r}")
        if path in seen:
            raise ValueError(f"Duplicate path: {path}")
        seen.add(path)
        if not isinstance(content, str):
            raise ValueError(f"Content for {path} must be a string")
        if not content.strip():
            raise ValueError(f"Content for {path} must not be empty")
        if len(content.encode("utf-8")) > MAX_FILE_BYTES:
            raise ValueError(f"Content for {path} exceeds max size")
        if not Path(path).exists():
            raise ValueError(f"Target file does not exist: {path}")
        updates.append((path, content))

    return updates


def apply_updates(updates: list[tuple[str, str]]) -> list[str]:
    changed: list[str] = []
    for path, content in updates:
        target = Path(path)
        old = target.read_text(encoding="utf-8")
        if old != content:
            target.write_text(content, encoding="utf-8")
            changed.append(path)
    if not changed:
        raise ValueError("JSON payload produced no file changes")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and apply Codex offline JSON output.")
    parser.add_argument("--input", required=True, help="Path to Codex last-message text")
    parser.add_argument("--json-out", default=".tmp/codex-offline-output.json")
    args = parser.parse_args()

    raw = Path(args.input).read_text(encoding="utf-8", errors="replace")
    data = extract_json(raw)
    updates = validate_payload(data)

    json_out = Path(args.json_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    changed = apply_updates(updates)
    print("Applied Codex offline JSON output:")
    for path in changed:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
