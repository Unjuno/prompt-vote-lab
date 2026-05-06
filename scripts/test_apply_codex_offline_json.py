#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "apply_codex_offline_json.py"


def load_module():
    spec = importlib.util.spec_from_file_location("apply_codex_offline_json", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load apply_codex_offline_json module")
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

    raw = 'prefix ```json\n{"files":[{"path":"lab/index.html","content":"<main>ok</main>"}]}\n``` suffix'
    data = module.extract_json(raw)
    assert data["files"][0]["path"] == "lab/index.html"

    module.validate_payload({"files": [{"path": "lab/index.html", "content": "ok"}]})
    module.validate_payload({"files": [{"path": "lab/style.css", "content": "body{}"}]})
    module.validate_payload({"files": [{"path": "lab/app.js", "content": "console.log('ok')"}]})

    expect_raises(lambda: module.extract_json("not json"), "No JSON object")
    expect_raises(lambda: module.validate_payload({}), "non-empty files list")
    expect_raises(lambda: module.validate_payload({"files": [{"path": "README.md", "content": "ok"}]}), "Forbidden")
    expect_raises(lambda: module.validate_payload({"files": [{"path": "lab/index.html", "content": ""}]}), "must not be empty")
    expect_raises(lambda: module.validate_payload({"files": [{"path": "lab/index.html", "content": "ok"}, {"path": "lab/index.html", "content": "ok2"}]}), "Duplicate")

    print("offline JSON applier test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
