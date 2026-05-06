#!/usr/bin/env bash
set -euo pipefail

key_env_name="OPENAI_API_KEY"
if [ -z "${!key_env_name:-}" ]; then
  echo "Required API key environment variable is not configured."
  exit 1
fi

mkdir -p "${CODEX_HOME:-.codex-home}"
mkdir -p .tmp

printf '%s' "${!key_env_name}" | codex login --with-api-key

context_dir=".tmp/codex-offline-context"
rm -rf "$context_dir"
mkdir -p "$context_dir"

python - <<'PY'
from __future__ import annotations

from pathlib import Path

files = ["lab/index.html", "lab/style.css", "lab/app.js"]
parts = [
    "You are Codex running an offline-context Prompt Vote Lab writeback canary.",
    "",
    "Goal: add a small static canary panel explaining that this is the fifth bounded Codex implementation-agent canary.",
    "",
    "You do not have repository write access. Use only the file contents below as context.",
    "Return only a JSON object with this exact shape:",
    '{"files":[{"path":"lab/index.html","content":"FULL REPLACEMENT CONTENT"}]}',
    "",
    "Rules:",
    "- Return only JSON. No markdown fence and no explanation.",
    "- Include only files whose full replacement content should change.",
    "- Allowed paths are lab/index.html, lab/style.css, and lab/app.js.",
    "- Do not create or delete files.",
    "- Keep the visible change small and reviewable.",
    "- Do not change voting, selection, evidence, report, or canary policy logic.",
    "- Do not include external scripts, network calls, cookies, storage APIs, or dynamic code execution.",
    "",
    "Current allowed file contents:",
]
for name in files:
    content = Path(name).read_text(encoding="utf-8")
    parts.append(f"\n--- BEGIN {name} ---")
    parts.append(content)
    parts.append(f"--- END {name} ---")
Path(".tmp/codex-offline-json-prompt.md").write_text("\n".join(parts) + "\n", encoding="utf-8")
PY

prompt="$(cat .tmp/codex-offline-json-prompt.md)"

codex exec \
  --cd "$PWD/$context_dir" \
  --model "${CODEX_MODEL:-gpt-5.4-nano}" \
  --sandbox read-only \
  --json \
  --output-last-message "$PWD/.tmp/codex-last-message.txt" \
  "$prompt" \
  > "$PWD/.tmp/codex-events.jsonl"

python scripts/apply_codex_offline_json.py \
  --input .tmp/codex-last-message.txt \
  --json-out .tmp/codex-offline-output.json
