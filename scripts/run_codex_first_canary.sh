#!/usr/bin/env bash
set -euo pipefail

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "OPENAI_API_KEY is not configured."
  exit 1
fi

mkdir -p "${CODEX_HOME:-.codex-home}"
mkdir -p .tmp

printf '%s' "$OPENAI_API_KEY" | codex login --with-api-key

codex exec \
  --cd "$PWD" \
  --model "${CODEX_MODEL:-gpt-5.1-codex}" \
  --sandbox workspace-write \
  --json \
  --output-last-message .tmp/codex-last-message.txt \
  - < .tmp/codex-first-canary-prompt.md \
  > .tmp/codex-events.jsonl
