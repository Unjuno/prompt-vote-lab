#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPARISONS_DIR = ROOT / "lab" / "comparisons"

RANK_CARD_RE = re.compile(r'<p class="rank-eyebrow">Rank ([123])</p>')
RANK_TITLE_ID_RE = re.compile(r'id="(rank-[123]-title)"')

REQUIRED_TEXT = [
    "Prompt Vote Lab comparison:",
    "Comparison dashboard · generated from public results",
    "GitHub Issues, PRs, commits, public bundles, run records, and live rank output pages remain the source of truth",
    "default-src 'self'",
    "connect-src 'none'",
    "frame-src 'none'",
    "object-src 'none'",
    "base-uri 'none'",
    "form-action 'none'",
]

RANK_REQUIRED_TEXT = [
    "Live output",
]

EMPTY_DASHBOARD_TEXT = "No comparison rows found for this week."

FORBIDDEN_TEXT = [
    "OPENAI_API_KEY",
    "codex login",
    "container stderr",
    "raw stderr",
    "document.cookie",
    "eval(",
    "<iframe",
    "https://example.com/ping",
]


def _comparison_indexes() -> list[Path]:
    if not COMPARISONS_DIR.exists():
        return []
    return sorted(
        path
        for path in COMPARISONS_DIR.glob("*/index.html")
        if path.parent.name and not path.parent.name.startswith(".")
    )


def _require_unique(values: list[str], label: str, path: Path) -> None:
    duplicates = sorted({item for item in values if values.count(item) > 1})
    if duplicates:
        rel = path.relative_to(ROOT)
        raise AssertionError(f"{rel}: duplicate {label}: {duplicates}")


def test_dashboard(path: Path) -> None:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")

    missing = [item for item in REQUIRED_TEXT if item not in text]
    if missing:
        raise AssertionError(f"{rel}: missing required text: {missing}")

    forbidden = [item for item in FORBIDDEN_TEXT if item in text]
    if forbidden:
        raise AssertionError(f"{rel}: forbidden text found: {forbidden}")

    ranks = RANK_CARD_RE.findall(text)
    if not ranks:
        if EMPTY_DASHBOARD_TEXT not in text:
            raise AssertionError(f"{rel}: no rank cards found and missing empty-dashboard message")
        return

    missing_rank_text = [item for item in RANK_REQUIRED_TEXT if item not in text]
    if missing_rank_text:
        raise AssertionError(f"{rel}: missing rank-only required text: {missing_rank_text}")

    _require_unique(ranks, "rank cards", path)

    title_ids = RANK_TITLE_ID_RE.findall(text)
    _require_unique(title_ids, "rank title ids", path)

    for rank in ranks:
        expected_root = f"lab/comparisons/{path.parent.name}/rank-{rank}/"
        if expected_root not in text:
            raise AssertionError(f"{rel}: missing output root for rank {rank}: {expected_root}")

        expected_label = f"Open rank {rank} output"
        if expected_label not in text:
            raise AssertionError(f"{rel}: missing live output label for rank {rank}: {expected_label}")

        expected_href = f'href="./rank-{rank}/"'
        if expected_href not in text:
            raise AssertionError(f"{rel}: missing live output href for rank {rank}: {expected_href}")

    if '<section class="rank-grid" aria-label="Comparison candidates">' not in text:
        raise AssertionError(f"{rel}: missing rank-grid section")


def main() -> int:
    indexes = _comparison_indexes()
    if not indexes:
        raise SystemExit("No generated comparison dashboards found")

    for path in indexes:
        test_dashboard(path)

    print(f"generated comparison dashboard test passed: {len(indexes)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
