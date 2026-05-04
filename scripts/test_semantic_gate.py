#!/usr/bin/env python3
"""Smoke tests for scripts/semantic_gate.py.

No network calls. No model calls.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "semantic_gate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("semantic_gate", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load semantic_gate.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["semantic_gate"] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    sg = load_module()

    prompt = "Add a small visible canary panel explaining the first bounded implementation agent test."
    good_diff = """
+<section class="canary-panel">
+  <h2>First bounded implementation agent test</h2>
+  <p>This visible canary panel explains the first run.</p>
+</section>
"""
    good = sg.evaluate(prompt, good_diff, 0.20, True)
    if good.decision != "SEMANTIC_CONTINUE_ALLOWED":
        raise SystemExit(f"expected good diff to pass, got {good!r}")

    unrelated_diff = """
+<section class="weather-widget">
+  <h2>Forecast</h2>
+  <p>Rain and temperature chart.</p>
+</section>
"""
    bad = sg.evaluate(prompt, unrelated_diff, 0.20, True)
    if bad.decision != "STOP":
        raise SystemExit(f"expected unrelated diff to stop, got {bad!r}")

    empty = sg.evaluate(prompt, "", 0.20, True)
    if empty.decision != "STOP":
        raise SystemExit("empty diff must stop")

    print("semantic_gate smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
