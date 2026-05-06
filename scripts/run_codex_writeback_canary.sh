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

cat > .tmp/codex-writeback-prompt.md <<'EOF'
You are Codex running a workflow-mediated Prompt Vote Lab writeback canary.

Goal: add a small static canary panel explaining that this is the fourth bounded Codex implementation-agent canary.

Allowed files:
- lab/index.html
- lab/style.css
- lab/app.js

Critical write policy:
- Do not edit files directly.
- Return only a unified diff patch in your final answer.
- The workflow will validate and apply the patch.
- The patch may touch only the allowed files.
- Do not create or delete files.
- Keep the visible change small and reviewable.
- Do not add external network calls, external scripts, cookies, analytics, login, payment behavior, dependencies, eval, fetch, XMLHttpRequest, localStorage, or sessionStorage.
- Do not change voting, selection, evidence, report, or canary policy logic.
- Do not commit, branch, or open a PR. The workflow will do that.

Required final answer:
- A single unified diff beginning with `diff --git`.
- No markdown explanation outside the diff.
EOF

prompt="$(cat .tmp/codex-writeback-prompt.md)"

codex exec \
  --cd "$PWD" \
  --model "${CODEX_MODEL:-gpt-5.4-nano}" \
  --sandbox read-only \
  --json \
  --output-last-message "$PWD/.tmp/codex-last-message.txt" \
  "$prompt" \
  > "$PWD/.tmp/codex-events.jsonl"

python scripts/apply_codex_writeback_patch.py \
  --input .tmp/codex-last-message.txt \
  --patch-out .tmp/codex-writeback.patch
