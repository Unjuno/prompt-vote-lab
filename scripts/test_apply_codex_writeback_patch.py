#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "apply_codex_writeback_patch.py"


def load_module():
    spec = importlib.util.spec_from_file_location("apply_codex_writeback_patch", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load apply_codex_writeback_patch module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expect_raises(fn, needle: str) -> None:
    try:
        fn()
    except Exception as exc:
        assert needle in str(exc), str(exc)
        return
    raise AssertionError(f"expected exception containing {needle!r}")


def main() -> int:
    module = load_module()

    raw = """Here is the patch:\n```diff\ndiff --git a/lab/index.html b/lab/index.html\n--- a/lab/index.html\n+++ b/lab/index.html\n@@ -1,1 +1,1 @@\n-old\n+new\n```\n"""
    patch = module.extract_patch(raw)
    assert patch.startswith("diff --git a/lab/index.html b/lab/index.html")
    module.validate_patch_paths(patch)
    module.validate_patch_content(patch)

    forbidden_path_patch = """diff --git a/README.md b/README.md\n--- a/README.md\n+++ b/README.md\n@@ -1,1 +1,1 @@\n-old\n+new\n"""
    expect_raises(lambda: module.validate_patch_paths(forbidden_path_patch), "forbidden path")

    delete_allowed_file_patch = """diff --git a/lab/index.html b/lab/index.html\n--- a/lab/index.html\n+++ /dev/null\n@@ -1,1 +0,0 @@\n-old\n"""
    expect_raises(lambda: module.validate_patch_paths(delete_allowed_file_patch), "Creating or deleting")

    forbidden_content_patch = """diff --git a/lab/app.js b/lab/app.js\n--- a/lab/app.js\n+++ b/lab/app.js\n@@ -1,1 +1,1 @@\n-old\n+fetch('/x')\n"""
    expect_raises(lambda: module.validate_patch_content(forbidden_content_patch), "Forbidden patch content")

    no_diff = "not a patch"
    expect_raises(lambda: module.extract_patch(no_diff), "No unified diff")

    print("codex writeback patch applier test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
