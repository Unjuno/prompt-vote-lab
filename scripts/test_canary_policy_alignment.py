#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "formal/Canary.lean": [
        "scope := Scope.labOnly",
        "attempts := 1",
        "sdkMaxRetries := 0",
        "apiCallsPerCandidate := 1",
        "fallbackModel := false",
        "autoMerge := false",
        "externalPublishing := false",
        "safe_canary_scope_lab_only",
        "safe_canary_one_attempt",
        "safe_canary_no_sdk_retry",
        "safe_canary_one_api_call",
        "safe_canary_no_fallback",
        "safe_canary_no_auto_merge",
        "safe_canary_no_external_publishing",
    ],
    "docs/pre-api-freeze.md": [
        "model: gpt-5-nano",
        "one agent attempt",
        "one model",
        "no retry",
        "no fallback",
        "SDK max_retries: 0",
        "API call limit per candidate: 1",
        "lab/ only",
        "manual review before merge",
        "automatic merge",
        "workflow attempts to auto-merge",
    ],
    "docs/canary-policy.md": [
        "model: gpt-5-nano",
        "attempts per candidate: 1",
        "SDK max_retries: 0",
        "fallback model: none",
        "automatic merge: no",
        "max continuation runs per candidate: 1",
    ],
    "scripts/preflight_implementation_agent.py": [
        "ALLOWED_MODELS = {\"gpt-5-nano\"}",
        "if sdk_max_retries != 0",
        "api_call_limit != 1",
        "MAX_OUTPUT_TOKENS_LIMIT = 12000",
    ],
    ".github/workflows/weekly-auto-run.yml": [
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5-nano\"",
        "SDK_MAX_RETRIES: \"0\"",
        "--api-call-limit-per-candidate 1",
        "gh pr create",
    ],
}

FORBIDDEN = {
    "docs/pre-api-freeze.md": [
        "fallback model: gpt-5",
        "automatic merge: yes",
        "SDK max_retries: 1",
        "API call limit per candidate: 2",
    ],
    "docs/canary-policy.md": [
        "fallback model: gpt-5",
        "automatic merge: yes",
        "SDK max_retries: 1",
        "attempts per candidate: 2",
    ],
    "scripts/preflight_implementation_agent.py": [
        "ALLOWED_MODELS = {\"gpt-5\"}",
        "ALLOWED_MODELS = {\"gpt-5-mini\"}",
        "sdk_max_retries != 1",
        "api_call_limit != 2",
    ],
    ".github/workflows/weekly-auto-run.yml": [
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5\"",
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5-mini\"",
        "SDK_MAX_RETRIES: \"1\"",
        "SDK_MAX_RETRIES: \"2\"",
        "enable-auto-merge",
        "gh pr merge --auto",
    ],
}


def main() -> int:
    failures: list[str] = []

    for rel, needles in REQUIRED.items():
        text = read(rel, failures)
        for needle in needles:
            if needle not in text:
                failures.append(f"{rel}: missing required canary policy text: {needle}")

    for rel, needles in FORBIDDEN.items():
        text = read(rel, failures)
        for needle in needles:
            if needle in text:
                failures.append(f"{rel}: forbidden canary policy text present: {needle}")

    if failures:
        for failure in failures:
            print("ERROR:", failure)
        return 1

    print("canary policy alignment passed")
    return 0


def read(rel: str, failures: list[str]) -> str:
    path = ROOT / rel
    if not path.is_file():
        failures.append(f"missing file: {rel}")
        return ""
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
