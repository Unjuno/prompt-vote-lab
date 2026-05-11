#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reset_dev_artifacts.py"


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        tmp_dir = root / ".tmp"
        tmp_dir.mkdir()
        (tmp_dir / "artifact.txt").write_text("temporary\n", encoding="utf-8")
        tmp2 = root / "tmp"
        tmp2.mkdir()
        (tmp2 / "scratch.json").write_text("{}\n", encoding="utf-8")
        protected_paths = [
            root / "data" / "public-results.json",
            root / "data" / "support-unlocks" / "2026-W19.json",
            root / "runs" / "week-2026-W19-vote-summary.md",
            root / "lab" / "comparisons" / "2026-W20" / "index.html",
            root / "lab" / "history" / "index.html",
        ]
        for path in protected_paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("protected\n", encoding="utf-8")

        dry = run(["--root", str(root)], ROOT)
        if dry.returncode != 0:
            raise SystemExit(dry.stdout + dry.stderr)
        if "dry-run only" not in dry.stdout:
            raise SystemExit("dry run notice missing")
        if not (tmp_dir / "artifact.txt").exists():
            raise SystemExit("dry run removed .tmp artifact")
        if not (tmp2 / "scratch.json").exists():
            raise SystemExit("dry run removed tmp artifact")

        for target in [
            "data",
            "data/public-results.json",
            "data/support-unlocks/2026-W19.json",
            "runs/week-2026-W19-vote-summary.md",
            "lab/comparisons/2026-W20/index.html",
            "lab/history/index.html",
            "docs",
            "rules",
            "README.md",
        ]:
            result = run(["--root", str(root), "--target", target], ROOT)
            if result.returncode == 0:
                raise SystemExit(f"protected target unexpectedly allowed: {target}")
            if "Refusing" not in (result.stdout + result.stderr):
                raise SystemExit(f"protected target did not emit refusal: {target}")

        outside = run(["--root", str(root), "--target", "../outside"], ROOT)
        if outside.returncode == 0:
            raise SystemExit("outside path unexpectedly allowed")

        non_dev = root / "scratch"
        non_dev.mkdir()
        denied = run(["--root", str(root), "--target", "scratch"], ROOT)
        if denied.returncode == 0:
            raise SystemExit("non-dev artifact path unexpectedly allowed")

        applied = run(["--root", str(root), "--apply"], ROOT)
        if applied.returncode != 0:
            raise SystemExit(applied.stdout + applied.stderr)
        if tmp_dir.exists() or tmp2.exists():
            raise SystemExit("apply did not remove default dev artifact directories")
        for path in protected_paths:
            if not path.exists():
                raise SystemExit(f"protected path was removed: {path}")

    print("reset dev artifacts test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
