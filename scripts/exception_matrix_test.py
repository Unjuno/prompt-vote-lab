#!/usr/bin/env python3
"""Run local exception-matrix checks for Prompt Vote Lab.

This script mutates a temporary copy of the repository and verifies that safety
and static-site checks fail or pass as expected. It does not call any model API.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Case:
    name: str
    expected: str
    check: str
    mutation: str


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def copy_repo() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="pvl-exception-"))
    ignore = shutil.ignore_patterns(".git", ".tmp", "node_modules", "__pycache__")
    for item in ROOT.iterdir():
        if item.name in {".git", ".tmp", "node_modules", "__pycache__"}:
            continue
        dest = tmp / item.name
        if item.is_dir():
            shutil.copytree(item, dest, ignore=ignore)
        else:
            shutil.copy2(item, dest)
    run(["git", "init"], tmp)
    run(["git", "config", "user.name", "exception-test"], tmp)
    run(["git", "config", "user.email", "exception-test@example.invalid"], tmp)
    run(["git", "add", "."], tmp)
    run(["git", "commit", "-m", "baseline"], tmp)
    return tmp


def remove_baseline_language(html: str) -> str:
    replacements = [
        ("20-vote gate", "baseline gate"),
        ("20 virtual votes", "baseline votes"),
        ("virtual votes baseline", "baseline marker"),
        ("20", "twenty"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    return html


def mutate(repo: Path, mutation: str) -> None:
    if mutation == "outside_lab_change":
        (repo / "README.md").write_text((repo / "README.md").read_text(encoding="utf-8") + "\nunsafe outside lab mutation\n", encoding="utf-8")
        return
    if mutation == "external_script":
        html = (repo / "lab/index.html").read_text(encoding="utf-8")
        html = html.replace("</body>", "<script src=\"https://cdn.example.invalid/x.js\"></script>\n</body>")
        (repo / "lab/index.html").write_text(html, encoding="utf-8")
        return
    if mutation == "fetch_call":
        js = (repo / "lab/app.js").read_text(encoding="utf-8")
        js += "\nfetch('https://example.invalid/data.json');\n"
        (repo / "lab/app.js").write_text(js, encoding="utf-8")
        return
    if mutation == "cookie_use":
        js = (repo / "lab/app.js").read_text(encoding="utf-8")
        js += "\ndocument.cookie = 'x=y';\n"
        (repo / "lab/app.js").write_text(js, encoding="utf-8")
        return
    if mutation == "local_storage":
        js = (repo / "lab/app.js").read_text(encoding="utf-8")
        js += "\nlocalStorage.setItem('pvl:test', 'ok');\n"
        (repo / "lab/app.js").write_text(js, encoding="utf-8")
        return
    if mutation == "indexed_db":
        js = (repo / "lab/app.js").read_text(encoding="utf-8")
        js += "\nconst pvlDbOpenRequest = indexedDB.open('pvl-local-test', 1);\n"
        (repo / "lab/app.js").write_text(js, encoding="utf-8")
        return
    if mutation == "fixed_new_function":
        js = (repo / "lab/app.js").read_text(encoding="utf-8")
        js += "\nconst pvlScore = new Function('votes', 'baseline', 'return Math.max(0, votes - baseline);');\n"
        (repo / "lab/app.js").write_text(js, encoding="utf-8")
        return
    if mutation == "dynamic_new_function":
        js = (repo / "lab/app.js").read_text(encoding="utf-8")
        js += "\nconst userText = document.querySelector('textarea')?.value || '';\nconst pvlUnsafe = new Function(userText);\n"
        (repo / "lab/app.js").write_text(js, encoding="utf-8")
        return
    if mutation == "remove_lab_link":
        html = (repo / "index.html").read_text(encoding="utf-8")
        html = html.replace('href="./lab/"', 'href="./"')
        (repo / "index.html").write_text(html, encoding="utf-8")
        return
    if mutation == "remove_baseline_text":
        html = (repo / "index.html").read_text(encoding="utf-8")
        (repo / "index.html").write_text(remove_baseline_language(html), encoding="utf-8")
        return
    if mutation == "affirmative_paid_merge":
        html = (repo / "index.html").read_text(encoding="utf-8")
        html = html.replace("</main>", "<p>support buys merge rights</p>\n</main>")
        (repo / "index.html").write_text(html, encoding="utf-8")
        return
    if mutation == "safe_docs_only":
        (repo / "docs" / "experiment-model.md").write_text((repo / "docs" / "experiment-model.md").read_text(encoding="utf-8") + "\n\nSafe docs-only note.\n", encoding="utf-8")
        return
    raise ValueError(f"unknown mutation: {mutation}")


def run_check(repo: Path, check: str) -> subprocess.CompletedProcess[str]:
    run(["git", "add", "."], repo)
    if check == "safety":
        return run(["bash", "scripts/safety-check.sh", "HEAD", "HEAD"], repo)
    if check == "static":
        return run(["bash", "scripts/static-site-check.sh"], repo)
    raise ValueError(f"unknown check: {check}")


def write_markdown(results: list[dict], path: Path) -> None:
    total = len(results)
    ok_count = sum(1 for r in results if r["ok"])
    lines = [
        "# Exception matrix summary",
        "",
        f"- cases: {total}",
        f"- expected-observed agreements: {ok_count}",
        f"- disagreements: {total - ok_count}",
        "",
        "| Case | Check | Expected | Actual | OK |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r['name']} | {r['check']} | {r['expected']} | {r['actual']} | {r['ok']} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default=".tmp/exception-matrix")
    args = parser.parse_args()

    cases = [
        Case("safety_blocks_outside_lab", "fail", "safety", "outside_lab_change"),
        Case("safety_blocks_external_script", "fail", "safety", "external_script"),
        Case("safety_blocks_fetch", "fail", "safety", "fetch_call"),
        Case("safety_blocks_cookie", "fail", "safety", "cookie_use"),
        Case("safety_allows_local_storage", "pass", "safety", "local_storage"),
        Case("safety_allows_indexed_db", "pass", "safety", "indexed_db"),
        Case("safety_allows_fixed_new_function", "pass", "safety", "fixed_new_function"),
        Case("safety_blocks_dynamic_new_function", "fail", "safety", "dynamic_new_function"),
        Case("static_blocks_missing_lab_link", "fail", "static", "remove_lab_link"),
        Case("static_blocks_missing_baseline_text", "fail", "static", "remove_baseline_text"),
        Case("static_blocks_affirmative_paid_merge", "fail", "static", "affirmative_paid_merge"),
        Case("static_allows_safe_docs_only", "pass", "static", "safe_docs_only"),
    ]

    results = []
    for case in cases:
        repo = copy_repo()
        try:
            mutate(repo, case.mutation)
            proc = run_check(repo, case.check)
            actual = "pass" if proc.returncode == 0 else "fail"
            ok = actual == case.expected
            results.append({
                "name": case.name,
                "expected": case.expected,
                "actual": actual,
                "check": case.check,
                "mutation": case.mutation,
                "ok": ok,
                "output_tail": proc.stdout[-1200:],
            })
        finally:
            shutil.rmtree(repo, ignore_errors=True)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "exception-matrix.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(results, out_dir / "exception-matrix.md")

    print(json.dumps(results, indent=2, ensure_ascii=False))
    failures = [r for r in results if not r["ok"]]
    if failures:
        print("Exception matrix failures detected", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
