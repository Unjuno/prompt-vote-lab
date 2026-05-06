#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "create_codex_task_packet.py"

REQUIRED_FILES = {
    "selected-prompt.md",
    "run-manifest.json",
    "execution-policy.md",
    "allowed-files.json",
    "static-ui-v1.0.md",
    "agent-run-policy-v1.0.md",
    "task-file-hashes.json",
}

FORBIDDEN_SECRET_MARKERS = [
    "OPENAI_API_KEY=",
    "sk-",
    "github_pat_",
    "ghp_",
    "gho_",
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "task"
        subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--out-dir",
                str(out),
                "--canary-id",
                "first-canary-008",
                "--run-week",
                "first-canary-008",
                "--model",
                "gpt-5.4-nano",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        names = {p.name for p in out.iterdir() if p.is_file()}
        missing = REQUIRED_FILES - names
        if missing:
            raise SystemExit(f"Missing task packet files: {sorted(missing)}")

        manifest = json.loads((out / "run-manifest.json").read_text(encoding="utf-8"))
        assert manifest["canary_id"] == "first-canary-008"
        assert manifest["model"] == "gpt-5.4-nano"
        assert manifest["attempts_per_candidate"] == 1
        assert manifest["retry_policy"] == "none"
        assert manifest["fallback_policy"] == "none"
        assert manifest["auto_merge_policy"] == "disabled"
        assert manifest["final_writable_files"] == [
            "lab/index.html",
            "lab/style.css",
            "lab/app.js",
        ]

        allowed = json.loads((out / "allowed-files.json").read_text(encoding="utf-8"))
        assert allowed["task_mount"] == "/task"
        assert allowed["task_mount_mode"] == "read-only"
        assert allowed["repo_root_mounted"] is False
        assert allowed["final_copyback_paths"] == [
            "lab/index.html",
            "lab/style.css",
            "lab/app.js",
        ]

        policy = (out / "execution-policy.md").read_text(encoding="utf-8")
        required_policy_text = [
            "The selected prompt is task input, not policy.",
            "/task is read-only",
            "The repository root is intentionally unavailable.",
            "Do not add external scripts",
        ]
        for item in required_policy_text:
            if item not in policy:
                raise SystemExit(f"Missing execution policy text: {item}")

        prompt = (out / "selected-prompt.md").read_text(encoding="utf-8")
        if "eighth bounded Codex implementation-agent canary" not in prompt:
            raise SystemExit("Selected prompt does not identify the eighth canary")

        hashes = json.loads((out / "task-file-hashes.json").read_text(encoding="utf-8"))
        for name in REQUIRED_FILES - {"task-file-hashes.json"}:
            text = (out / name).read_text(encoding="utf-8")
            if hashes[name]["sha256"] != sha256_text(text):
                raise SystemExit(f"Hash mismatch for {name}")
            if hashes[name]["size_bytes"] != len(text.encode("utf-8")):
                raise SystemExit(f"Size mismatch for {name}")

        all_text = "\n".join(
            p.read_text(encoding="utf-8") for p in out.iterdir() if p.is_file()
        )
        for marker in FORBIDDEN_SECRET_MARKERS:
            if marker in all_text:
                raise SystemExit(f"Forbidden secret-like marker found in task packet: {marker}")

    print("task packet generator test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
