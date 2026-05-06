#!/usr/bin/env bash
set -euo pipefail

key_env_name="OPENAI_API_KEY"
if [ -z "${!key_env_name:-}" ]; then
  echo "Required API key environment variable is not configured."
  exit 1
fi

mkdir -p "${CODEX_HOME:-.codex-home}"
mkdir -p .tmp

worktree=".tmp/codex-3file-relaxed-worktree"
rm -rf "$worktree"
mkdir -p "$worktree/lab"
cp lab/index.html "$worktree/lab/index.html"
cp lab/style.css "$worktree/lab/style.css"
cp lab/app.js "$worktree/lab/app.js"

printf '%s' "${!key_env_name}" | codex login --with-api-key

cat > .tmp/codex-isolated-3file-relaxed-prompt.md <<'EOF'
You are Codex running an isolated three-file Prompt Vote Lab canary.

Goal: add a small static canary panel explaining that this is the third bounded Codex implementation-agent canary.

Visible files:
- lab/index.html
- lab/style.css
- lab/app.js

Hard constraints:
- Edit only the three visible files.
- Keep the visible change small and reviewable.
- Do not add external network calls, external scripts, cookies, analytics, login, payment behavior, dependencies, eval, fetch, XMLHttpRequest, localStorage, or sessionStorage.
- Do not change voting, selection, evidence, report, or canary policy logic.
- Do not commit, branch, or open a PR. The workflow will do that.

At the end, provide a short rationale summary with:
- files changed
- why each change was necessary
- files deliberately not changed
- constraints considered
Do not include private chain-of-thought.
EOF

prompt="$(cat .tmp/codex-isolated-3file-relaxed-prompt.md)"

codex exec \
  --cd "$PWD/$worktree" \
  --model "${CODEX_MODEL:-gpt-5.4-nano}" \
  --sandbox danger-full-access \
  --json \
  --output-last-message "$PWD/.tmp/codex-last-message.txt" \
  "$prompt" \
  > "$PWD/.tmp/codex-events.jsonl"

if ! diff -q lab/index.html "$worktree/lab/index.html" >/dev/null; then
  cp "$worktree/lab/index.html" lab/index.html
fi
if ! diff -q lab/style.css "$worktree/lab/style.css" >/dev/null; then
  cp "$worktree/lab/style.css" lab/style.css
fi
if ! diff -q lab/app.js "$worktree/lab/app.js" >/dev/null; then
  cp "$worktree/lab/app.js" lab/app.js
fi
