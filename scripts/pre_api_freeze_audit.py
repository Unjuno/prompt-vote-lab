#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/pre-api-freeze.md",
    "docs/current-features.md",
    "docs/canary-policy.md",
    "docs/canary-report-template.md",
    "docs/stop-rules.md",
    "formal/Selection.lean",
    "lean-toolchain",
    "scripts/select_eligible.py",
    "scripts/preflight_implementation_agent.py",
]

def main() -> int:
    failures = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            failures.append(f"missing required file: {rel}")

    if failures:
        for f in failures:
            print("ERROR:", f)
        return 1

    print("pre-API freeze audit passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
