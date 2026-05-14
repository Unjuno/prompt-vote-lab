#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "repository-5s-and-language-policy.md"

SCANNED_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".yml",
    ".yaml",
}

EXCLUDED_PREFIXES = {
    ".git/",
    "data/",
    "lab/comparisons/",
    "lab/history/",
    "runs/",
}

# Maintainer-authored files should not contain CJK or common kana/hangul scripts.
# Generated public evidence and raw external prompt evidence are excluded above.
NON_ENGLISH_SCRIPT_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uac00-\ud7af]")

POLICY_REQUIRED_TEXT = [
    "# Repository 5S and language policy",
    "The repository language for maintainer-authored content is English.",
    "Sort",
    "Set in order",
    "Shine",
    "Standardize",
    "Sustain",
    "Protected evidence includes:",
    "raw external evidence",
    "quoted user-provided prompt text",
    "machine-generated public result snapshots",
    "Non-English source text should not be added to maintainer-authored docs, scripts, workflows, rules, or lab UI files.",
    "repository language policy test",
    "Cleanup PR checklist",
    "canonical selected-prompt path: scripts/run_codex_selected_prompt.sh",
    "legacy non-canonical fallback: scripts/openai_lab_run.py",
]


def is_scanned(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    if path.suffix not in SCANNED_SUFFIXES:
        return False
    if path.name.startswith(".") and path.suffix == "":
        return False
    return True


def iter_scanned_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and is_scanned(path))


def main() -> int:
    policy = POLICY.read_text(encoding="utf-8")
    missing = [item for item in POLICY_REQUIRED_TEXT if item not in policy]
    if missing:
        raise SystemExit(f"Missing repository language policy text: {missing}")

    offenders: list[str] = []
    for path in iter_scanned_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if NON_ENGLISH_SCRIPT_RE.search(line):
                rel = path.relative_to(ROOT).as_posix()
                offenders.append(f"{rel}:{line_number}: {line.strip()[:120]}")
                break

    if offenders:
        raise SystemExit("Non-English script characters found in maintainer-authored files:\n" + "\n".join(offenders))

    print("repository language policy test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
