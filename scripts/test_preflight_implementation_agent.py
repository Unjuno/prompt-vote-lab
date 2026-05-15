#!/usr/bin/env python3
"""Smoke tests for scripts/preflight_implementation_agent.py.

No network calls. No model calls.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "preflight_implementation_agent.py"
ACTIVE_MODEL = "gpt-5.4-nano"


def run(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    for key in ["OPENAI_API_KEY_", "OPENAI_API_KEY", "OPENAI_IMPLEMENTATION_API_KEY"]:
        merged_env.pop(key, None)
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=merged_env,
    )


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="pvl-preflight-") as tmp_name:
        tmp = Path(tmp_name)
        empty = tmp / "empty.json"
        eligible = tmp / "eligible.json"
        bad_reason_fixture = tmp / "bad-reason.json"

        write_json(empty, [])
        write_json(
            eligible,
            [
                {
                    "rank": 1,
                    "issue_number": 101,
                    "candidate_type": "prompt-proposal",
                    "run_reason": "normal-weekly-run",
                    "body": "Add a small visible canary panel.",
                }
            ],
        )
        write_json(
            bad_reason_fixture,
            [
                {
                    "rank": 2,
                    "issue_number": 102,
                    "candidate_type": "prompt-proposal",
                    "run_reason": "normal-weekly-run",
                    "body": "Invalid rank reason.",
                }
            ],
        )

        no_eligible = run(["--eligible", str(empty), "--model", ACTIVE_MODEL])
        if no_eligible.returncode != 0:
            print(no_eligible.stdout)
            raise SystemExit("empty eligible list should pass without secret")
        if "output_token_cap_enforced" not in no_eligible.stdout:
            print(no_eligible.stdout)
            raise SystemExit("preflight summary should declare that no output token cap is enforced")

        needs_secret = run(["--eligible", str(eligible), "--model", ACTIVE_MODEL])
        if needs_secret.returncode == 0:
            raise SystemExit("eligible candidates without secret should fail")

        with_secret = run(
            ["--eligible", str(eligible), "--model", ACTIVE_MODEL],
            env={"OPENAI_API_KEY_": "test-secret-placeholder"},
        )
        if with_secret.returncode != 0:
            print(with_secret.stdout)
            raise SystemExit("eligible candidates with placeholder secret should pass preflight")
        if '"output_token_cap_enforced": false' not in with_secret.stdout:
            print(with_secret.stdout)
            raise SystemExit("preflight summary should record output_token_cap_enforced=false")

        wrong_model = run(
            ["--eligible", str(eligible), "--model", "not-allowed-model"],
            env={"OPENAI_API_KEY_": "test-secret-placeholder"},
        )
        if wrong_model.returncode == 0:
            raise SystemExit("wrong model should fail")

        retry_enabled = run(
            ["--eligible", str(eligible), "--model", ACTIVE_MODEL, "--sdk-max-retries", "1"],
            env={"OPENAI_API_KEY_": "test-secret-placeholder"},
        )
        if retry_enabled.returncode == 0:
            raise SystemExit("sdk retries should fail")

        bad_reason = run(
            ["--eligible", str(bad_reason_fixture), "--model", ACTIVE_MODEL],
            env={"OPENAI_API_KEY_": "test-secret-placeholder"},
        )
        if bad_reason.returncode == 0:
            raise SystemExit("rank 2 normal-weekly-run should fail")

    print("implementation preflight smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())