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

prompt="$(cat .tmp/codex-first-canary-prompt.md)"

codex exec \
  --cd "$PWD" \
  --model "${CODEX_MODEL:-gpt-5.4-nano}" \
  --sandbox workspace-write \
  --json \
  --output-last-message .tmp/codex-last-message.txt \
  "$prompt" \
  > .tmp/codex-events.jsonl
