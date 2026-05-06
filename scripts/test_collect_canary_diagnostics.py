#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "collect_canary_diagnostics.py"


def load_module():
    spec = importlib.util.spec_from_file_location("collect_canary_diagnostics", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load collect_canary_diagnostics module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()

    required = set(module.EXPECTED_INTERNAL_ARTIFACTS)
    for name in [
        "codex-events.jsonl",
        "codex-last-message.txt",
        "codex-stderr.txt",
        "codex-stdout.txt",
        "git-status-before.txt",
        "git-status-after.txt",
        "git-diff-name-only.txt",
        "git-diff-stat.txt",
        "git-diff.patch",
        "file-hashes-before.json",
        "file-hashes-after.json",
        "check-results.json",
        "failure-summary.json",
        "artifact-manifest.json",
    ]:
        assert name in required, name

    assert module.parse_name_only("lab/index.html\n\nlab/style.css\n") == [
        "lab/index.html",
        "lab/style.css",
    ]

    assert module.normalize_status(" success ") == "success"
    assert module.normalize_status("FAILURE") == "failure"

    assert module.classify_failure([], module.DEFAULT_ALLOWED_FILES, "bwrap failed", "") == "sandbox_failure"
    assert module.classify_failure([], module.DEFAULT_ALLOWED_FILES, "401 Unauthorized", "") == "auth_failure"
    assert module.classify_failure([], module.DEFAULT_ALLOWED_FILES, "", "") == "no_changes"
    assert module.classify_failure(["README.md"], module.DEFAULT_ALLOWED_FILES, "", "") == "forbidden_changed_file"

    # Successful runs must not retain a failure classifier such as auth_failure
    # merely because Codex stderr mentions authentication during a successful login.
    status = "success"
    failure_type = "none" if module.normalize_status(status) == "success" else module.classify_failure(
        ["lab/index.html"], module.DEFAULT_ALLOWED_FILES, "authentication", ""
    )
    assert failure_type == "none"

    print("canary diagnostics collector test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
