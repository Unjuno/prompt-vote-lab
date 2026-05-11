#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

REQUIRED_ROOT_FILES = [
    "index.json",
    "README.md",
    "observation-summary.md",
    "observation-summary.json",
]

REQUIRED_DIRS = [
    "raw",
    "sanitized",
    "reasoning-traces",
]

FORBIDDEN_PUBLIC_PATTERNS = [
    ("openai_key", re.compile(r"sk-[A-Za-z0-9_\-]{12,}")),
    ("github_classic_token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{12,}")),
    ("github_fine_grained_token", re.compile(r"github_pat_[A-Za-z0-9_]{12,}")),
    ("authorization_bearer", re.compile(r"(?i)authorization:\s*bearer\s+[A-Za-z0-9_.\-]+")),
    ("openai_env_assignment", re.compile(r"(?i)OPENAI_API_KEY\s*[:=]\s*[^\s]+")),
    ("github_token_env_assignment", re.compile(r"(?i)GITHUB_TOKEN\s*[:=]\s*[^\s]+")),
    ("gh_token_env_assignment", re.compile(r"(?i)GH_TOKEN\s*[:=]\s*[^\s]+")),
]

EXPECTED_REDACTION_MARKERS = [
    "[REDACTED_SECRET]",
    "[REDACTED_RUNNER_WORKDIR]",
    "[REDACTED_RUNNER_TEMP]",
    "[REDACTED_TMP_PATH]",
    "[REDACTED_GITHUB_WORKSPACE]",
]

EXPECTED_OBSERVATION_SCHEMA = "prompt-vote-lab-agent-observation-summary-v1"
EXPECTED_BUNDLE_SCHEMA = "prompt-vote-lab-public-agent-run-bundle-v1"


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {path}: {exc}") from exc


def text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        files.append(path)
    return files


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def assert_file(path: Path, errors: list[str], label: str) -> None:
    if not path.exists() or not path.is_file():
        add_error(errors, f"Missing required file: {label}")
    elif path.stat().st_size <= 0:
        add_error(errors, f"Required file is empty: {label}")


def assert_dir(path: Path, errors: list[str], label: str) -> None:
    if not path.exists() or not path.is_dir():
        add_error(errors, f"Missing required directory: {label}")


def verify_index(bundle: Path, errors: list[str]) -> dict[str, Any]:
    index = read_json(bundle / "index.json")
    if index.get("schema_version") != EXPECTED_BUNDLE_SCHEMA:
        add_error(errors, f"Unexpected index schema_version: {index.get('schema_version')}")
    policy = index.get("policy") if isinstance(index.get("policy"), dict) else {}
    if policy.get("sanitized_diagnostic_logs_included") is not True:
        add_error(errors, "index.policy.sanitized_diagnostic_logs_included must be true")
    if policy.get("sanitized_reasoning_traces_included") is not True:
        add_error(errors, "index.policy.sanitized_reasoning_traces_included must be true")
    observation = index.get("observation_summary") if isinstance(index.get("observation_summary"), dict) else {}
    if observation.get("json") != "observation-summary.json":
        add_error(errors, "index.observation_summary.json must point to observation-summary.json")
    if observation.get("markdown") != "observation-summary.md":
        add_error(errors, "index.observation_summary.markdown must point to observation-summary.md")
    if "reasoning_trace_files" not in index:
        add_error(errors, "index.reasoning_trace_files is required")
    if not isinstance(index.get("sanitized_files"), list):
        add_error(errors, "index.sanitized_files must be a list")
    return index


def verify_observation_summary(bundle: Path, errors: list[str]) -> dict[str, Any]:
    summary = read_json(bundle / "observation-summary.json")
    if summary.get("schema_version") != EXPECTED_OBSERVATION_SCHEMA:
        add_error(errors, f"Unexpected observation summary schema_version: {summary.get('schema_version')}")

    reasoning = summary.get("reasoning_trace") if isinstance(summary.get("reasoning_trace"), dict) else {}
    if reasoning.get("sanitized") is not True:
        add_error(errors, "observation.reasoning_trace.sanitized must be true")
    if reasoning.get("published_directory") != "reasoning-traces/":
        add_error(errors, "observation.reasoning_trace.published_directory must be reasoning-traces/")
    if reasoning.get("used_for_behavior_evaluation") is not True:
        add_error(errors, "observation.reasoning_trace.used_for_behavior_evaluation must be true")
    if reasoning.get("unexposed_provider_private_cot_published") is not False:
        add_error(errors, "observation.reasoning_trace.unexposed_provider_private_cot_published must be false")
    if not isinstance(reasoning.get("files"), list):
        add_error(errors, "observation.reasoning_trace.files must be a list")

    hypotheses = summary.get("reasoning_effect_hypotheses")
    if not isinstance(hypotheses, list) or not hypotheses:
        add_error(errors, "observation.reasoning_effect_hypotheses must be a non-empty list")

    file_activity = summary.get("file_activity")
    if not isinstance(file_activity, list):
        add_error(errors, "observation.file_activity must be a list")

    sanitized_logs = summary.get("sanitized_logs")
    if not isinstance(sanitized_logs, list):
        add_error(errors, "observation.sanitized_logs must be a list")

    return summary


def verify_dirs_have_content(bundle: Path, errors: list[str]) -> None:
    for directory in REQUIRED_DIRS:
        path = bundle / directory
        assert_dir(path, errors, directory)
        if path.exists() and path.is_dir() and not any(item.is_file() for item in path.rglob("*")):
            add_error(errors, f"Required directory has no files: {directory}")


def verify_markdown(bundle: Path, errors: list[str]) -> None:
    readme = (bundle / "README.md").read_text(encoding="utf-8", errors="replace")
    observation = (bundle / "observation-summary.md").read_text(encoding="utf-8", errors="replace")
    required_readme = [
        "Agent observation summary",
        "sanitized/",
        "reasoning-traces/",
    ]
    required_observation = [
        "Agent observation summary",
        "Reasoning / CoT-like trace evidence",
        "Reasoning effect hypotheses",
        "Sanitized logs",
        "Evidence limits",
    ]
    for item in required_readme:
        if item not in readme:
            add_error(errors, f"README.md missing text: {item}")
    for item in required_observation:
        if item not in observation:
            add_error(errors, f"observation-summary.md missing text: {item}")


def verify_no_forbidden_public_patterns(bundle: Path, errors: list[str]) -> None:
    for path in text_files(bundle):
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in FORBIDDEN_PUBLIC_PATTERNS:
            if pattern.search(text):
                add_error(errors, f"Forbidden public pattern {name} found in {rel(path, bundle)}")


def verify_marker_accounting(bundle: Path, errors: list[str]) -> None:
    public_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in text_files(bundle))
    if "[REDACTED" in public_text:
        if not any(marker in public_text for marker in EXPECTED_REDACTION_MARKERS):
            add_error(errors, "Unknown redaction marker family found")


def verify_public_agent_run_bundle(bundle: Path) -> dict[str, Any]:
    errors: list[str] = []
    if not bundle.exists() or not bundle.is_dir():
        raise SystemExit(f"Bundle directory not found: {bundle}")

    for name in REQUIRED_ROOT_FILES:
        assert_file(bundle / name, errors, name)
    verify_dirs_have_content(bundle, errors)

    if not errors:
        verify_index(bundle, errors)
        verify_observation_summary(bundle, errors)
        verify_markdown(bundle, errors)
        verify_no_forbidden_public_patterns(bundle, errors)
        verify_marker_accounting(bundle, errors)

    result = {
        "bundle": str(bundle),
        "ok": not errors,
        "errors": errors,
        "checked_root_files": REQUIRED_ROOT_FILES,
        "checked_directories": REQUIRED_DIRS,
        "forbidden_pattern_count": len(FORBIDDEN_PUBLIC_PATTERNS),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle-dir", required=True)
    parser.add_argument("--report", default="")
    args = parser.parse_args()

    result = verify_public_agent_run_bundle(Path(args.bundle_dir))
    if args.report:
        report = Path(args.report)
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("public agent run bundle verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
