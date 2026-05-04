#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        shutil.copytree(
            ROOT,
            repo,
            ignore=shutil.ignore_patterns(".git", "tmp", ".DS_Store"),
        )
        workflow = repo / ".github" / "workflows" / "evidence-pipeline-dry-run.yml"
        text = workflow.read_text(encoding="utf-8")
        changed = "\n".join(
            line for line in text.splitlines()
            if "validate-evidence-artifact.mjs" not in line
        ) + "\n"
        workflow.write_text(changed, encoding="utf-8")

        result = subprocess.run(
            ["python", "scripts/pre_api_freeze_audit.py"],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        output = f"{result.stdout}\n{result.stderr}"
        print(output)
        if result.returncode == 0:
            raise SystemExit("expected audit to reject missing dry-run validator call")
        if "validate-evidence-artifact.mjs" not in output:
            raise SystemExit("expected audit output to mention validate-evidence-artifact.mjs")

    print("dry-run validator audit self-test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
