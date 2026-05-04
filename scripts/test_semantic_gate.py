#!/usr/bin/env python3
# CI trigger change

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "semantic_gate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("semantic_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["semantic_gate"] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    sg = load_module()
    result = sg.evaluate("canary panel", "canary panel visible", 0.2, False)
    if result.decision not in ("SEMANTIC_CONTINUE_ALLOWED", "STOP"):
        raise SystemExit("invalid")
    print("ok")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
