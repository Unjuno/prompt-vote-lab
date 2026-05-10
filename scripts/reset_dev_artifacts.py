#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TARGETS = [".tmp", "tmp"]

ALLOWED_CLEANUP_ROOTS = {
    ".tmp",
    "tmp",
}

PROTECTED_PATHS = {
    ".git",
    ".github",
    "README.md",
    "data",
    "data/public-results.json",
    "data/public-results.md",
    "data/support-unlocks",
    "docs",
    "lab",
    "lab/index.html",
    "lab/style.css",
    "lab/app.js",
    "lab/comparisons",
    "lab/history",
    "rules",
    "runs",
}


@dataclass(frozen=True)
class ResetPlanItem:
    path: str
    exists: bool
    kind: str
    action: str


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def to_posix_relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def resolve_under_root(root: Path, raw: str) -> Path:
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise SystemExit(f"Refusing path outside repository root: {raw}") from exc
    return candidate


def is_protected(rel: str) -> bool:
    normalized = rel.strip("/")
    if normalized in {"", "."}:
        return True
    for protected in PROTECTED_PATHS:
        if normalized == protected or normalized.startswith(protected + "/"):
            return True
    return False


def is_allowed_cleanup_target(rel: str) -> bool:
    normalized = rel.strip("/")
    return any(normalized == root or normalized.startswith(root + "/") for root in ALLOWED_CLEANUP_ROOTS)


def classify(path: Path) -> str:
    if path.is_dir():
        return "dir"
    if path.is_file():
        return "file"
    if path.is_symlink():
        return "symlink"
    return "missing"


def build_plan(root: Path, targets: list[str]) -> list[ResetPlanItem]:
    plan: list[ResetPlanItem] = []
    for target in targets:
        path = resolve_under_root(root, target)
        rel = to_posix_relative(root, path)
        if is_protected(rel):
            raise SystemExit(f"Refusing to reset protected path: {rel}")
        if not is_allowed_cleanup_target(rel):
            raise SystemExit(
                f"Refusing to reset non-dev-artifact path: {rel}. "
                "Allowed cleanup roots are .tmp/ and tmp/."
            )
        exists = path.exists() or path.is_symlink()
        kind = classify(path)
        action = "remove" if exists else "skip-missing"
        plan.append(ResetPlanItem(path=rel, exists=exists, kind=kind, action=action))
    return plan


def apply_plan(root: Path, plan: list[ResetPlanItem]) -> None:
    for item in plan:
        if not item.exists:
            continue
        path = resolve_under_root(root, item.path)
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        else:
            raise SystemExit(f"Refusing unknown filesystem object: {item.path}")


def render_plan(plan: list[ResetPlanItem], as_json: bool) -> str:
    rows = [item.__dict__ for item in plan]
    if as_json:
        return json.dumps(rows, indent=2, sort_keys=True) + "\n"
    lines = []
    for item in plan:
        lines.append(f"{item.action}\t{item.kind}\t{item.path}")
    return "\n".join(lines) + ("\n" if lines else "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely remove local development artifacts.")
    parser.add_argument("--root", default=None, help="repository root; defaults to this script's repository")
    parser.add_argument("--target", action="append", default=None, help="cleanup target under .tmp/ or tmp/; repeatable")
    parser.add_argument("--apply", action="store_true", help="actually remove files; default is dry-run")
    parser.add_argument("--json", action="store_true", help="print reset plan as JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else repo_root_from_script()
    targets = args.target if args.target is not None else DEFAULT_TARGETS
    plan = build_plan(root, targets)
    print(render_plan(plan, args.json), end="")
    if args.apply:
        apply_plan(root, plan)
    else:
        print("dry-run only; pass --apply to remove listed dev artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
