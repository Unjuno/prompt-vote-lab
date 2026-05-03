#!/usr/bin/env python3
"""Smoke test for the weekly auto no-eligible selection case.

Verification trigger: no-eligible selector guard.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "select_eligible.py"


def load_module():
    spec = importlib.util.spec_from_file_location("select_eligible", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load select_eligible.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["select_eligible"] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    sel = load_module()
    candidates = [
        {"rank": 1, "issue_number": 0, "vote_count": 20, "candidate_type": "no-change-baseline", "title": "baseline", "body": "baseline"},
        {"rank": 2, "issue_number": 101, "vote_count": 9, "candidate_type": "prompt-proposal", "title": "prompt", "body": "prompt"},
        {"rank": 3, "issue_number": 102, "vote_count": 5, "candidate_type": "prompt-proposal", "title": "prompt", "body": "prompt"},
    ]
    eligible = sel.select_eligible(candidates, 10)
    if eligible != []:
        raise SystemExit(f"expected empty eligible list, got {eligible!r}")
    if sel.baseline_won(candidates) is not True:
        raise SystemExit("expected baseline_won true")
    print("weekly auto no-eligible selector test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
