#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT_DOC = ROOT / "docs" / "first-canary-prompt.md"
OUT_DIR = ROOT / ".tmp"

START = "## Fixed prompt"
FENCE = "```text"


def extract_fixed_prompt(text: str) -> str:
    section_start = text.find(START)
    if section_start < 0:
        raise SystemExit("Fixed prompt section not found")

    fence_start = text.find(FENCE, section_start)
    if fence_start < 0:
        raise SystemExit("Fixed prompt opening fence not found")

    content_start = fence_start + len(FENCE)
    fence_end = text.find("```", content_start)
    if fence_end < 0:
        raise SystemExit("Fixed prompt closing fence not found")

    prompt = text[content_start:fence_end].strip()
    if not prompt:
        raise SystemExit("Fixed prompt is empty")
    return prompt


def main() -> int:
    prompt = extract_fixed_prompt(PROMPT_DOC.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    candidate = {
        "candidate_type": "prompt-proposal",
        "rank": 1,
        "issue_number": 0,
        "vote_count": 0,
        "run_reason": "normal-weekly-run",
        "body": prompt,
    }

    (OUT_DIR / "first-canary-prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    (OUT_DIR / "eligible-candidates.json").write_text(
        json.dumps([candidate], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "has-eligible.txt").write_text("true", encoding="utf-8")
    (OUT_DIR / "selection-meta.json").write_text(
        json.dumps(
            {
                "first_canary": True,
                "fixed_prompt_source": "docs/first-canary-prompt.md",
                "eligible_count": 1,
                "eligible_ranks": [1],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"first_canary": True, "prompt_chars": len(prompt)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
