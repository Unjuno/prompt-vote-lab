#!/usr/bin/env python3
"""Mechanical semantic gate for automatic PARTIAL continuation.

No network calls. No model calls.

This gate is intentionally conservative. It checks whether the changed diff has
basic lexical overlap with the original prompt before allowing automatic
continuation after a PARTIAL result.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


STOPWORDS = {
    "a", "an", "and", "are", "as", "be", "by", "for", "from", "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "with",
    "add", "make", "keep", "change", "update", "show", "use", "page", "lab", "static", "local", "only",
}

CANARY_TERMS = {
    "canary", "panel", "visible", "bounded", "implementation", "agent", "test", "explain", "first", "run",
}


@dataclass
class SemanticGateResult:
    decision: str
    prompt_terms: list[str]
    diff_terms: list[str]
    intersection: list[str]
    jaccard: float
    reasons: list[str]


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text.lower())
    return {word for word in words if word not in STOPWORDS}


def git_diff(base_ref: str, head_ref: str) -> str:
    return subprocess.check_output(["git", "diff", "--unified=0", base_ref, head_ref, "--", "lab/"], text=True)


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def evaluate(prompt: str, diff_text: str, min_jaccard: float, require_canary_term: bool) -> SemanticGateResult:
    prompt_terms = tokenize(prompt)
    diff_terms = tokenize(diff_text)
    score = jaccard(prompt_terms, diff_terms)
    reasons: list[str] = []

    if not prompt_terms:
        reasons.append("prompt has no usable terms")
    if not diff_terms:
        reasons.append("diff has no usable terms")
    if score < min_jaccard:
        reasons.append(f"jaccard too low: {score:.3f} < {min_jaccard:.3f}")
    if require_canary_term and not (diff_terms & CANARY_TERMS):
        reasons.append("diff does not contain any required canary term")

    return SemanticGateResult(
        decision="SEMANTIC_CONTINUE_ALLOWED" if not reasons else "STOP",
        prompt_terms=sorted(prompt_terms),
        diff_terms=sorted(diff_terms),
        intersection=sorted(prompt_terms & diff_terms),
        jaccard=round(score, 6),
        reasons=reasons,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="")
    parser.add_argument("--prompt-file", default="")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--min-jaccard", type=float, default=0.20)
    parser.add_argument("--require-canary-term", action="store_true")
    parser.add_argument("--out", default=".tmp/semantic-gate.json")
    args = parser.parse_args()

    prompt = args.prompt
    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    diff_text = git_diff(args.base, args.head)
    result = evaluate(prompt, diff_text, args.min_jaccard, args.require_canary_term)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    return 0 if result.decision == "SEMANTIC_CONTINUE_ALLOWED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
