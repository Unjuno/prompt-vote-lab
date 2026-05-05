#!/usr/bin/env bash
set -euo pipefail

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "OPENAI_API_KEY is not configured."
  exit 1
fi

mkdir -p "${CODEX_HOME:-.codex-home}"
mkdir -p .tmp

printf '%s' "$OPENAI_API_KEY" | codex login --with-api-key

prompt="$(cat .tmp/codex-first-canary-prompt.md)"

codex exec \
  --cd "$PWD" \
  --model "${CODEX_MODEL:-gpt-5.1-codex}" \
  --sandbox workspace-write \
  --json \
  --output-last-message .tmp/codex-last-message.txt \
  "$prompt" \
  > .tmp/codex-events.jsonl

# `codex exec` can leave the generated diff as the latest Codex output rather
# than directly modifying the working tree. Try to apply it, then let the
# workflow's changed-file guard decide whether the run actually produced a
# valid lab-only diff.
if ! codex apply > .tmp/codex-apply.log 2>&1; then
  cat .tmp/codex-apply.log
fi
