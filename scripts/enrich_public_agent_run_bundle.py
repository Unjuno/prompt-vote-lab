#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OBSERVATION_SCHEMA_VERSION = "prompt-vote-lab-agent-observation-summary-v1"

SANITIZED_PUBLIC_FILES = [
    "codex-login-stdout.txt",
    "codex-login-stderr.txt",
    "codex-stderr.txt",
    "codex-stdout.txt",
    "policy-agent-container-stdout.txt",
    "policy-agent-container-stderr.txt",
    "issue-instruction-container-stdout.txt",
    "issue-instruction-container-stderr.txt",
    "npm-install-codex.txt",
    "npm-install-codex-stderr.txt",
    "policy-container-mounts.txt",
    "container-runtime-files-after.txt",
    "container-runtime-dirs-before.txt",
]

SECRET_PATTERNS = [
    ("openai_key", re.compile(r"sk-[A-Za-z0-9_\-]{12,}")),
    ("github_classic_token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{12,}")),
    ("github_fine_grained_token", re.compile(r"github_pat_[A-Za-z0-9_]{12,}")),
    ("authorization_bearer", re.compile(r"(?i)(authorization:\s*bearer\s+)[A-Za-z0-9_.\-]+")),
    ("openai_env_assignment", re.compile(r"(?i)(OPENAI_API_KEY\s*[:=]\s*)[^\s]+")),
    ("github_token_env_assignment", re.compile(r"(?i)(GITHUB_TOKEN\s*[:=]\s*)[^\s]+")),
    ("gh_token_env_assignment", re.compile(r"(?i)(GH_TOKEN\s*[:=]\s*)[^\s]+")),
]

PATH_PATTERNS = [
    ("runner_workdir", re.compile(r"/home/runner/work/[^\s:'\"]+")),
    ("runner_temp", re.compile(r"/home/runner/[^\s:'\"]+")),
    ("tmp_path", re.compile(r"/tmp/[^\s:'\"]+")),
    ("github_workspace", re.compile(r"/github/workspace[^\s:'\"]*")),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace") or json.dumps(fallback))
    except json.JSONDecodeError:
        return fallback


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def line_list(path: Path) -> list[str]:
    return [line.strip() for line in read_text(path).splitlines() if line.strip()]


def redact_for_public(text: str) -> tuple[str, list[dict[str, Any]]]:
    out = text
    redactions: list[dict[str, Any]] = []

    for name, pattern in SECRET_PATTERNS:
        if name.endswith("_assignment") or name == "authorization_bearer":
            out, count = pattern.subn(lambda match: f"{match.group(1)}[REDACTED_SECRET]", out)
        else:
            out, count = pattern.subn("[REDACTED_SECRET]", out)
        if count:
            redactions.append({"kind": name, "count": count})

    for name, pattern in PATH_PATTERNS:
        out, count = pattern.subn(f"[REDACTED_{name.upper()}]", out)
        if count:
            redactions.append({"kind": name, "count": count})

    return out, redactions


def copy_sanitized_files(diag: Path, bundle: Path) -> list[dict[str, Any]]:
    out_dir = bundle / "sanitized"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, Any]] = []
    for name in SANITIZED_PUBLIC_FILES:
        source = diag / name
        if not source.exists() or not source.is_file():
            manifest.append({"name": name, "included": False, "reason": "not_found"})
            continue
        raw = read_text(source)
        sanitized, redactions = redact_for_public(raw)
        dest = out_dir / name
        dest.write_text(sanitized, encoding="utf-8")
        manifest.append(
            {
                "name": name,
                "included": True,
                "path": f"sanitized/{name}",
                "source_size_bytes": source.stat().st_size,
                "public_size_bytes": dest.stat().st_size,
                "redactions": redactions,
                "quarantined": False,
            }
        )
    return manifest


def patch_stats(patch: str) -> dict[str, dict[str, int]]:
    stats: dict[str, dict[str, int]] = {}
    current: str | None = None
    for line in patch.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            current = parts[-1][2:] if len(parts) >= 4 and parts[-1].startswith("b/") else None
            if current:
                stats.setdefault(current, {"additions": 0, "deletions": 0})
            continue
        if not current:
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            stats[current]["additions"] += 1
        elif line.startswith("-"):
            stats[current]["deletions"] += 1
    return stats


def first_existing(diag: Path, names: list[str]) -> Path | None:
    for name in names:
        p = diag / name
        if p.exists():
            return p
    return None


def build_observation_summary(diag: Path, bundle: Path, sanitized_manifest: list[dict[str, Any]]) -> dict[str, Any]:
    index = read_json(bundle / "index.json", {})
    policy = read_json(diag / "policy-allowed-paths.json", {})
    check_results = read_json(diag / "check-results.json", {})
    before_hashes = read_json(diag / "file-hashes-before.json", {})
    after_hashes = read_json(diag / "file-hashes-after.json", {})

    changed_files = check_results.get("changed_files") or line_list(diag / "policy-agent-diff-name-only.txt") or line_list(diag / "issue-instruction-diff-name-only.txt") or line_list(diag / "git-diff-name-only.txt")
    copied_files = line_list(diag / "policy-agent-copied-files.txt") or line_list(diag / "issue-instruction-copied-files.txt")
    visible_before = line_list(diag / "container-visible-files-before.txt")
    visible_after = line_list(diag / "container-visible-files-after.txt")
    task_visible = line_list(diag / "task-visible-files-container.txt") or line_list(diag / "task-visible-files.txt")
    denied_access = line_list(diag / "policy-denied-access.txt")

    patch_path = first_existing(diag, ["policy-agent-diff.patch", "issue-instruction-diff.patch", "git-diff.patch"])
    stats = patch_stats(read_text(patch_path)) if patch_path else {}
    final_paths = policy.get("final_copyback_paths") or ["lab/index.html", "lab/style.css", "lab/app.js"]
    normalized_final_paths = [str(path).removeprefix("/work/") for path in final_paths]

    file_set = sorted(set(normalized_final_paths) | set(changed_files) | set(copied_files))
    file_activity = []
    for name in file_set:
        container_path = name if name.startswith("/work/") else f"/work/{name}"
        before = before_hashes.get(name, {}) if isinstance(before_hashes, dict) else {}
        after = after_hashes.get(name, {}) if isinstance(after_hashes, dict) else {}
        file_activity.append(
            {
                "file": name,
                "container_path": container_path,
                "visible_before": container_path in visible_before or name in visible_before,
                "visible_after": container_path in visible_after or name in visible_after,
                "changed": name in changed_files,
                "copied_back": name in copied_files,
                "additions": stats.get(name, {}).get("additions", 0),
                "deletions": stats.get(name, {}).get("deletions", 0),
                "sha256_before": before.get("sha256") if isinstance(before, dict) else None,
                "sha256_after": after.get("sha256") if isinstance(after, dict) else None,
                "size_before_bytes": before.get("size_bytes") if isinstance(before, dict) else None,
                "size_after_bytes": after.get("size_bytes") if isinstance(after, dict) else None,
            }
        )

    final_summary, final_summary_redactions = redact_for_public(read_text(diag / "codex-last-message.txt"))
    return {
        "schema_version": OBSERVATION_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "run_id": index.get("run_id"),
        "issue_number": index.get("issue_number"),
        "pr_number": index.get("pr_number"),
        "path_model": {
            "repo_root_mounted": policy.get("repo_root_mounted"),
            "work_root": policy.get("container_work_root") or "/work",
            "task_root": "/task" if task_visible else None,
            "task_mount_mode": "read-only" if task_visible else None,
            "runtime_root": policy.get("container_runtime_root") or "/codex-runtime",
            "final_copyback_paths": normalized_final_paths,
        },
        "agent_observation": {
            "visible_files_before": visible_before,
            "visible_files_after": visible_after,
            "task_visible_files": task_visible,
            "denied_access_paths": denied_access,
            "codex_event_lines": index.get("quick_index", {}).get("codex_event_lines"),
            "agent_final_action_summary": final_summary[:4000],
            "agent_final_action_summary_redactions": final_summary_redactions,
        },
        "file_activity": file_activity,
        "sanitized_logs": sanitized_manifest,
        "limits": {
            "exact_read_order_observed": False,
            "exact_read_order_reason": "This summary records visible files, changed files, copied files, diffs, hashes, and event counts. Exact file read sequence is not guaranteed unless the Codex event schema exposes it and is reviewed separately.",
            "raw_private_reasoning_collected": False,
            "raw_private_reasoning_policy": "Raw private chain-of-thought is not collected or published. The public record uses final action summary plus objective artifacts.",
            "sanitizer_guarantee": "Best-effort pattern redaction before publication. A public leak must still be treated as an incident and rotated if a real token is found.",
        },
    }


def render_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines)


def render_observation_md(summary: dict[str, Any]) -> str:
    path_model = summary["path_model"]
    agent = summary["agent_observation"]
    files = summary["file_activity"]
    sanitized = summary["sanitized_logs"]
    return "\n".join(
        [
            "# Agent observation summary",
            "",
            "This is a participant-facing observation index. It describes visible files, changed files, copied files, sanitized logs, and the agent final action summary.",
            "It is not raw private reasoning.",
            "",
            "## Path model",
            "",
            render_table(
                ["field", "value"],
                [
                    ["repo_root_mounted", path_model.get("repo_root_mounted")],
                    ["work_root", path_model.get("work_root")],
                    ["task_root", path_model.get("task_root")],
                    ["task_mount_mode", path_model.get("task_mount_mode")],
                    ["runtime_root", path_model.get("runtime_root")],
                    ["final_copyback_paths", ", ".join(path_model.get("final_copyback_paths") or [])],
                ],
            ),
            "",
            "## File activity",
            "",
            render_table(
                ["file", "visible_before", "visible_after", "changed", "copied_back", "+", "-"],
                [[item.get("file"), item.get("visible_before"), item.get("visible_after"), item.get("changed"), item.get("copied_back"), item.get("additions"), item.get("deletions")] for item in files],
            ),
            "",
            "## Sanitized logs",
            "",
            render_table(
                ["file", "included", "redactions"],
                [[item.get("name"), item.get("included"), ", ".join(f"{r.get('kind')}:{r.get('count')}" for r in item.get("redactions", []))] for item in sanitized],
            ),
            "",
            "## Agent final action summary",
            "",
            agent.get("agent_final_action_summary") or "No final action summary captured.",
            "",
            "## Evidence limits",
            "",
            "- Exact file read order is not guaranteed by this summary.",
            "- Raw private chain-of-thought is not collected or published.",
            "- Sanitization is best-effort. Real token discovery still requires rotation.",
            "- Use raw/codex-events.jsonl and sanitized/* logs for deeper inspection.",
            "",
        ]
    )


def append_readme(bundle: Path) -> None:
    readme = bundle / "README.md"
    existing = read_text(readme)
    addition = "\n".join(
        [
            "",
            "## Agent observation summary",
            "",
            "Start with `observation-summary.md` to see:",
            "",
            "```text",
            "path model",
            "file activity",
            "sanitized logs",
            "agent final action summary",
            "evidence limits",
            "```",
            "",
            "Use `observation-summary.json` for machine-readable analysis.",
            "Sanitized diagnostic logs are under `sanitized/`.",
            "",
        ]
    )
    readme.write_text(existing + addition, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostics-dir", required=True)
    parser.add_argument("--bundle-dir", required=True)
    args = parser.parse_args()

    diag = Path(args.diagnostics_dir)
    bundle = Path(args.bundle_dir)
    if not bundle.exists():
        raise SystemExit(f"bundle dir not found: {bundle}")

    sanitized_manifest = copy_sanitized_files(diag, bundle)
    summary = build_observation_summary(diag, bundle, sanitized_manifest)
    write_json(bundle / "observation-summary.json", summary)
    (bundle / "observation-summary.md").write_text(render_observation_md(summary), encoding="utf-8")

    index_path = bundle / "index.json"
    index = read_json(index_path, {})
    index["sanitized_files"] = sanitized_manifest
    index["observation_summary"] = {
        "json": "observation-summary.json",
        "markdown": "observation-summary.md",
        "schema_version": OBSERVATION_SCHEMA_VERSION,
    }
    policy = index.setdefault("policy", {})
    policy["sanitized_diagnostic_logs_included"] = True
    policy["sanitizer_guarantee"] = "best_effort_pattern_redaction"
    write_json(index_path, index)
    append_readme(bundle)
    print(str(bundle))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
