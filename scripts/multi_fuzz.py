#!/usr/bin/env python3
"""Weighted multi-fuzz smoke test for Prompt Vote Lab checks.

This script does not call model APIs. It copies the repository to temporary
workspaces, applies weighted mutations, runs the relevant check, and reports
whether the observed check result matched the expected result.

Verification trigger: multi-fuzz.
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Mutation:
    name: str
    mutation_class: str
    weight: int
    check: str
    expected: str


MUTATIONS = [
    Mutation("external_script", "unsafe_runtime", 12, "safety", "fail"),
    Mutation("fetch_external", "unsafe_runtime", 12, "safety", "fail"),
    Mutation("cookie_write", "unsafe_runtime", 10, "safety", "fail"),
    Mutation("eval_call", "unsafe_runtime", 10, "safety", "fail"),
    Mutation("iframe_embed", "unsafe_runtime", 8, "safety", "fail"),
    Mutation("outside_lab_change", "scope_escape", 12, "safety", "fail"),
    Mutation("local_storage", "allowed_local_state", 10, "safety", "pass"),
    Mutation("session_storage", "allowed_local_state", 6, "safety", "pass"),
    Mutation("json_export_button", "allowed_local_state", 5, "safety", "pass"),
    Mutation("remove_lab_link", "public_site_breakage", 8, "static", "fail"),
    Mutation("remove_baseline_text", "public_site_breakage", 8, "static", "fail"),
    Mutation("affirmative_paid_merge", "bad_support_claim", 8, "static", "fail"),
    Mutation("safe_docs_change", "safe_docs_change", 10, "static", "pass"),
    Mutation("safe_root_copy_change", "safe_docs_change", 5, "static", "pass"),
]


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def copy_repo() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="pvl-multifuzz-"))
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
    run(["git", "config", "user.name", "multi-fuzz"], tmp)
    run(["git", "config", "user.email", "multi-fuzz@example.invalid"], tmp)
    run(["git", "add", "."], tmp)
    run(["git", "commit", "-m", "baseline"], tmp)
    return tmp


def append(path: Path, text: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


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


def mutate(repo: Path, name: str) -> None:
    if name == "external_script":
        p = repo / "lab" / "index.html"
        text = p.read_text(encoding="utf-8").replace("</body>", "<script src=\"https://cdn.example.invalid/lib.js\"></script>\n</body>")
        p.write_text(text, encoding="utf-8")
        return
    if name == "fetch_external":
        append(repo / "lab" / "app.js", "\nfetch('https://example.invalid/data.json');\n")
        return
    if name == "cookie_write":
        append(repo / "lab" / "app.js", "\ndocument.cookie = 'pvl=x';\n")
        return
    if name == "eval_call":
        append(repo / "lab" / "app.js", "\neval('console.log(1)');\n")
        return
    if name == "iframe_embed":
        p = repo / "lab" / "index.html"
        text = p.read_text(encoding="utf-8").replace("</main>", "<iframe src=\"about:blank\"></iframe>\n</main>")
        p.write_text(text, encoding="utf-8")
        return
    if name == "outside_lab_change":
        append(repo / "README.md", "\nImplementation-like outside-lab mutation.\n")
        return
    if name == "local_storage":
        append(repo / "lab" / "app.js", "\nlocalStorage.setItem('pvl:fuzz', 'ok');\n")
        return
    if name == "session_storage":
        append(repo / "lab" / "app.js", "\nsessionStorage.setItem('pvl:fuzz', 'ok');\n")
        return
    if name == "json_export_button":
        append(repo / "lab" / "app.js", "\nconst pvlBlob = new Blob([JSON.stringify({ok:true})], {type: 'application/json'});\n")
        return
    if name == "remove_lab_link":
        p = repo / "index.html"
        p.write_text(p.read_text(encoding="utf-8").replace('href="./lab/"', 'href="./"'), encoding="utf-8")
        return
    if name == "remove_baseline_text":
        p = repo / "index.html"
        p.write_text(remove_baseline_language(p.read_text(encoding="utf-8")), encoding="utf-8")
        return
    if name == "affirmative_paid_merge":
        p = repo / "index.html"
        p.write_text(p.read_text(encoding="utf-8").replace("</main>", "<p>support buys merge rights</p>\n</main>"), encoding="utf-8")
        return
    if name == "safe_docs_change":
        append(repo / "docs" / "experiment-model.md", "\n\nSafe multi-fuzz docs note.\n")
        return
    if name == "safe_root_copy_change":
        p = repo / "index.html"
        p.write_text(p.read_text(encoding="utf-8").replace("Public prompt experiment", "Public prompt experiment"), encoding="utf-8")
        append(p, "\n<!-- safe explanatory comment -->\n")
        return
    raise ValueError(f"Unknown mutation: {name}")


def run_check(repo: Path, check: str) -> subprocess.CompletedProcess[str]:
    run(["git", "add", "."], repo)
    if check == "safety":
        return run(["bash", "scripts/safety-check.sh", "HEAD", "HEAD"], repo)
    if check == "static":
        return run(["bash", "scripts/static-site-check.sh"], repo)
    raise ValueError(f"Unknown check: {check}")


def choose_mutation(rng: random.Random) -> Mutation:
    return rng.choices(MUTATIONS, weights=[m.weight for m in MUTATIONS], k=1)[0]


def write_markdown(results: list[dict], path: Path) -> None:
    total = len(results)
    ok_count = sum(1 for r in results if r["ok"])
    lines = [
        "# Multi-fuzz summary",
        "",
        f"- trials: {total}",
        f"- expected-observed agreements: {ok_count}",
        f"- disagreements: {total - ok_count}",
        "",
        "| Trial | Mutation | Class | Check | Expected | Observed | OK |",
        "|---:|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| {r['trial']} | {r['mutation']} | {r['mutation_class']} | {r['check']} | {r['expected']} | {r['observed']} | {r['ok']} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--trials", type=int, default=25)
    parser.add_argument("--out-dir", default=".tmp/multi-fuzz")
    parser.add_argument("--fail-on-disagreement", action="store_true")
    args = parser.parse_args()

    if args.trials < 1 or args.trials > 250:
        raise SystemExit("trials must be between 1 and 250")

    rng = random.Random(args.seed)
    results = []

    for trial in range(1, args.trials + 1):
        mutation = choose_mutation(rng)
        repo = copy_repo()
        try:
            mutate(repo, mutation.name)
            proc = run_check(repo, mutation.check)
            observed = "pass" if proc.returncode == 0 else "fail"
            ok = observed == mutation.expected
            results.append(
                {
                    "seed": args.seed,
                    "trial": trial,
                    "mutation": mutation.name,
                    "mutation_class": mutation.mutation_class,
                    "weight": mutation.weight,
                    "check": mutation.check,
                    "expected": mutation.expected,
                    "observed": observed,
                    "ok": ok,
                    "output_tail": proc.stdout[-1200:],
                }
            )
        finally:
            shutil.rmtree(repo, ignore_errors=True)

    out_dir = ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"multi-fuzz-seed-{args.seed}.json"
    md_path = out_dir / f"multi-fuzz-seed-{args.seed}.md"
    json_path.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(results, md_path)

    print(json.dumps(results, indent=2, ensure_ascii=False))
    disagreements = [r for r in results if not r["ok"]]
    if disagreements:
        print(f"Disagreements: {len(disagreements)}")
        if args.fail_on_disagreement:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
