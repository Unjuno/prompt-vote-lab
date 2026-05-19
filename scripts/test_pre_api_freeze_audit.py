#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    run_case("current repo passes", expect_pass=True, mutate=None)
    run_case("reject retry relaxation", expect_pass=False, mutate=mutate_retry_relaxation, expected="SDK_MAX_RETRIES")
    run_case("reject missing eligible guard", expect_pass=False, mutate=mutate_missing_guard, expected="step lacks eligible guard")
    run_case("reject missing artifact review boundary", expect_pass=False, mutate=mutate_review_boundary, expected="missing required text")
    run_case("reject missing required doc", expect_pass=False, mutate=mutate_missing_required_doc, expected="missing required file")
    print("pre-API freeze audit self-test passed")
    return 0


def run_case(name: str, expect_pass: bool, mutate, expected: str | None = None) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        shutil.copytree(
            ROOT,
            repo,
            ignore=shutil.ignore_patterns(".git", "tmp", ".DS_Store"),
        )
        if mutate is not None:
            mutate(repo)

        result = subprocess.run(
            ["python", "scripts/pre_api_freeze_audit.py"],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        output = f"{result.stdout}\n{result.stderr}"
        print(f"CASE {name}: status={result.returncode}")
        if output.strip():
            print(output)

        if expect_pass and result.returncode != 0:
            raise SystemExit(f"{name}: expected PASS but failed")
        if not expect_pass and result.returncode == 0:
            raise SystemExit(f"{name}: expected FAIL but passed")
        if expected and expected not in output:
            raise SystemExit(f"{name}: expected output to contain {expected!r}")


def mutate_retry_relaxation(repo: Path) -> None:
    path = repo / ".github/workflows/weekly-auto-run.yml"
    text = path.read_text(encoding="utf-8")
    text = text.replace('SDK_MAX_RETRIES: "0"', 'SDK_MAX_RETRIES: "1"', 1)
    path.write_text(text, encoding="utf-8")


def mutate_missing_guard(repo: Path) -> None:
    path = repo / ".github/workflows/weekly-auto-run.yml"
    text = path.read_text(encoding="utf-8")
    step = "      - name: Create implementation PRs for eligible candidates\n"
    start = text.find(step)
    if start < 0:
        raise SystemExit("test fixture could not find implementation step")
    next_step = text.find("\n      - name:", start + len(step))
    end = next_step if next_step >= 0 else len(text)
    block = text[start:end]
    lines = block.splitlines(keepends=True)
    filtered = [line for line in lines if not line.lstrip().startswith("if: ")]
    path.write_text(text[:start] + "".join(filtered) + text[end:], encoding="utf-8")


def mutate_review_boundary(repo: Path) -> None:
    path = repo / "docs/evidence-artifact-review.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("no voter login list appears", "generated files look plausible")
    path.write_text(text, encoding="utf-8")


def mutate_missing_required_doc(repo: Path) -> None:
    path = repo / "docs/weekly-ops-doctrine.md"
    path.unlink()


if __name__ == "__main__":
    raise SystemExit(main())