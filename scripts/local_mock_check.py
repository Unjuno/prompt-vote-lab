#!/usr/bin/env python3
"""Run a local mock implementation check in a temporary copy.

This script verifies the mock implementation path without modifying the working tree
and without calling any external model API.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def copy_repo() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="pvl-local-mock-"))
    ignore = shutil.ignore_patterns(".git", ".tmp", "node_modules", "__pycache__")
    for item in ROOT.iterdir():
        if item.name in {".git", ".tmp", "node_modules", "__pycache__"}:
            continue
        dest = tmp / item.name
        if item.is_dir():
            shutil.copytree(item, dest, ignore=ignore)
        else:
            shutil.copy2(item, dest)
    return tmp


def main() -> int:
    repo = copy_repo()
    try:
        run(["git", "init"], repo)
        run(["git", "config", "user.name", "local-mock"], repo)
        run(["git", "config", "user.email", "local-mock@example.invalid"], repo)
        run(["git", "add", "."], repo)
        run(["git", "commit", "-m", "baseline"], repo)

        run([
            "python", "scripts/mock_lab_run.py",
            "--week", "week-local-mock",
            "--candidate-rank", "1",
            "--issue-number", "0",
            "--voted-prompt", "Mock: local workflow plumbing check.",
            "--vote-count", "21",
            "--run-reason", "mock-run",
        ], repo)

        run(["bash", "scripts/safety-check.sh", "HEAD", "HEAD"], repo)
        run(["bash", "scripts/static-site-check.sh"], repo)

        changed = subprocess.check_output(["git", "diff", "--name-only"], cwd=repo, text=True).splitlines()
        expected = {"lab/index.html", "lab/style.css", "lab/app.js"}
        actual = set(changed)
        print("Changed files:", sorted(actual))
        if actual != expected:
            raise SystemExit(f"Unexpected changed files: {sorted(actual)}")

        print("Local mock check passed.")
        return 0
    finally:
        shutil.rmtree(repo, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
