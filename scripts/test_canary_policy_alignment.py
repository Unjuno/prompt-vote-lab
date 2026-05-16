#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_MODEL = "gpt-5.4-nano"

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
        "historical guardrail record",
        "legacy API/SDK runner: present, non-canonical",
        f"model: {ACTIVE_MODEL}",
        "one agent attempt",
        "one model",
        "no retry",
        "no fallback",
        "SDK max_retries: 0",
        "API call limit per candidate: 1",
        "legacy max output tokens: 5000",
        "output_token_cap_enforced: false",
        "lab/ only",
        "manual review before merge",
        "automatic merge",
        "workflow attempts to auto-merge",
        "not the release gate for the current canonical weekly selected-prompt runner",
    ],
    "docs/canary-policy.md": [
        "# Legacy API canary policy",
        "legacy API/SDK path",
        f"model: {ACTIVE_MODEL}",
        "attempts per candidate: 1",
        "SDK max_retries: 0",
        "fallback model: none",
        "legacy max_output_tokens: 5000",
        "output_token_cap_enforced: false",
        "automatic merge: no",
        "max continuation runs per candidate: 1",
        "must not be cited as proof that the active canonical weekly path uses the API/SDK runner",
    ],
    "scripts/preflight_implementation_agent.py": [
        f"ALLOWED_MODELS = {{\"{ACTIVE_MODEL}\"}}",
        "if sdk_max_retries != 0",
        "api_call_limit != 1",
        "output_token_cap_enforced",
        "legacy_max_output_tokens_input_present",
    ],
    "scripts/openai_lab_run.py": [
        "OpenAI(api_key=api_key, max_retries=0, timeout=120.0)",
        "MAX_OUTPUT_TOKENS_LIMIT = 5000",
        "os.getenv(\"MAX_OUTPUT_TOKENS\", \"5000\")",
        "if args.max_output_tokens > MAX_OUTPUT_TOKENS_LIMIT",
        ACTIVE_MODEL,
    ],
    "scripts/create_first_canary_candidate.py": [
        "docs/first-canary-prompt.md",
        "Fixed prompt",
        "eligible-candidates.json",
        "first_canary",
        "fixed_prompt_source",
    ],
    ".github/workflows/weekly-auto-run.yml": [
        f"AUTO_IMPLEMENTATION_MODEL: \"{ACTIVE_MODEL}\"",
        f"IMPLEMENTATION_MODEL: {ACTIVE_MODEL}",
        "MAX_OUTPUT_TOKENS: \"5000\"",
        "SDK_MAX_RETRIES: \"0\"",
        "--api-call-limit-per-candidate 1",
        "gh pr create",
    ],
    ".github/workflows/first-canary-run.yml": [
        "name: Legacy First API Canary Run",
        "confirm_legacy_api_canary",
        "RUN_LEGACY_API_CANARY",
        "LEGACY_API_CANARY_CONFIRMATION",
        "Confirm legacy API canary intent",
        "This is a legacy non-canonical API/SDK canary workflow.",
        "Use the canonical selected-prompt runner for normal weekly operation.",
        "workflow_dispatch",
        f"IMPLEMENTATION_MODEL: {ACTIVE_MODEL}",
        "MAX_OUTPUT_TOKENS: \"5000\"",
        "SDK_MAX_RETRIES: \"0\"",
        "RUN_WEEK: first-canary-001",
        "python scripts/create_first_canary_candidate.py",
        "python scripts/preflight_implementation_agent.py",
        "--api-call-limit-per-candidate 1",
        "python scripts/openai_lab_run.py",
        "bash scripts/safety-check.sh origin/main HEAD",
        "bash scripts/static-site-check.sh",
        "Forbidden first-canary changed file",
        "Canonical selected-prompt runner: \\`false\\`",
        "Legacy runner: \\`true\\`",
        "gh pr create",
        "Manual review is required. Do not auto-merge.",
    ],
}

FORBIDDEN = {
    "docs/pre-api-freeze.md": [
        "fallback model: gpt-5",
        "automatic merge: yes",
        "SDK max_retries: 1",
        "API call limit per candidate: 2",
        "max output tokens: 12000",
    ],
    "docs/canary-policy.md": [
        "fallback model: gpt-5",
        "automatic merge: yes",
        "SDK max_retries: 1",
        "attempts per candidate: 2",
        "max_output_tokens: 12000",
    ],
    "scripts/preflight_implementation_agent.py": [
        "ALLOWED_MODELS = {\"gpt-5\"}",
        "ALLOWED_MODELS = {\"gpt-5-mini\"}",
        "ALLOWED_MODELS = {\"gpt-5-nano\"}",
        "sdk_max_retries != 1",
        "api_call_limit != 2",
        "MAX_OUTPUT_TOKENS_LIMIT = 5000",
        "MAX_OUTPUT_TOKENS_LIMIT = 12000",
    ],
    "scripts/openai_lab_run.py": [
        "os.getenv(\"IMPLEMENTATION_MODEL\", \"gpt-5-nano\")",
        "MAX_OUTPUT_TOKENS_LIMIT = 12000",
        "os.getenv(\"MAX_OUTPUT_TOKENS\", \"12000\")",
        "args.max_output_tokens > 12000",
        "max_output_tokens above 12000",
        "max_retries=1",
        "max_retries=2",
    ],
    ".github/workflows/weekly-auto-run.yml": [
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5\"",
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5-mini\"",
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5-nano\"",
        "MAX_OUTPUT_TOKENS: \"12000\"",
        "SDK_MAX_RETRIES: \"1\"",
        "SDK_MAX_RETRIES: \"2\"",
        "enable-auto-merge",
        "gh pr merge --auto",
    ],
    ".github/workflows/first-canary-run.yml": [
        "IMPLEMENTATION_MODEL: gpt-5-nano",
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5\"",
        "AUTO_IMPLEMENTATION_MODEL: \"gpt-5-mini\"",
        "MAX_OUTPUT_TOKENS: \"12000\"",
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