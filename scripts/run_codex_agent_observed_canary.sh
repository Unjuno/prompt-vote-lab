#!/usr/bin/env bash
set -euo pipefail

key_env_name="OPENAI_API_KEY"
if [ -z "${!key_env_name:-}" ]; then
  echo "Required API key environment variable is not configured."
  exit 1
fi

mkdir -p "${CODEX_HOME:-.codex-home}"
mkdir -p .tmp .tmp/canary-diagnostics

root="$PWD"
worktree=".tmp/codex-agent-observed-worktree"
timeline="$root/.tmp/agent-wrapper-timeline.jsonl"

log_event() {
  python - "$timeline" "$1" "$2" <<'PY'
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
path, event, detail = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path, "a", encoding="utf-8") as handle:
    handle.write(json.dumps({
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "detail": detail,
    }, sort_keys=True) + "\n")
PY
}

rm -f "$timeline"
log_event start "agent observed canary wrapper started"

rm -rf "$worktree"
mkdir -p "$worktree/lab"
cp lab/index.html "$worktree/lab/index.html"
cp lab/style.css "$worktree/lab/style.css"
cp lab/app.js "$worktree/lab/app.js"
log_event prepare_worktree "copied allowed lab files into isolated worktree"

python - <<'PY' > .tmp/agent-worktree-hashes-before.json
from __future__ import annotations
import hashlib
import json
from pathlib import Path
files = [
    ".tmp/codex-agent-observed-worktree/lab/index.html",
    ".tmp/codex-agent-observed-worktree/lab/style.css",
    ".tmp/codex-agent-observed-worktree/lab/app.js",
]
out = {}
for name in files:
    path = Path(name)
    out[name] = {
        "exists": path.exists(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None,
        "size_bytes": path.stat().st_size if path.exists() else None,
    }
print(json.dumps(out, indent=2, sort_keys=True))
PY

(
  cd "$worktree"
  git init -q
  git config user.name "agent-observer"
  git config user.email "agent-observer@example.invalid"
  git add lab/index.html lab/style.css lab/app.js
  git commit -q -m "baseline"
)
log_event baseline_commit "created isolated worktree baseline commit"

printf '%s' "${!key_env_name}" | codex login --with-api-key
log_event codex_login "codex login completed"

cat > .tmp/codex-agent-observed-prompt.md <<'EOF'
You are Codex running an agent-observed Prompt Vote Lab canary.

Goal: make a small static lab change that clearly marks this as the sixth bounded Codex implementation-agent canary.

Visible files:
- lab/index.html
- lab/style.css
- lab/app.js

Experiment purpose:
- This is not a pure API-style JSON generation test.
- This run is meant to observe Codex as an agent operating on files.
- Use available file tools normally, but keep the final change small.

Hard constraints:
- Edit only the three visible files.
- Keep the visible change small and reviewable.
- Do not add external network calls, external scripts, cookies, analytics, login, payment behavior, dependencies, eval, fetch, XMLHttpRequest, localStorage, or sessionStorage.
- Do not change voting, selection, evidence, report, or canary policy logic.
- Do not commit, branch, or open a PR. The workflow will do that.

At the end, provide a short action summary with:
- files inspected
- files changed
- any tool or write failures encountered
- why the final change was selected
- files deliberately not changed
Do not include private chain-of-thought.
EOF

prompt="$(cat .tmp/codex-agent-observed-prompt.md)"
log_event codex_exec_start "starting codex exec in isolated worktree"
set +e
codex exec \
  --cd "$root/$worktree" \
  --model "${CODEX_MODEL:-gpt-5.4-nano}" \
  --sandbox danger-full-access \
  --json \
  --output-last-message "$root/.tmp/codex-last-message.txt" \
  "$prompt" \
  > "$root/.tmp/codex-events.jsonl" \
  2> "$root/.tmp/codex-stderr.txt"
rc=$?
set -e
printf '%s\n' "$rc" > .tmp/codex-exit-code.txt
log_event codex_exec_exit "exit_code=$rc"

(
  cd "$worktree"
  git status --porcelain > "$root/.tmp/agent-worktree-status.txt"
  git diff --name-only -- > "$root/.tmp/agent-worktree-diff-name-only.txt"
  git diff --stat -- > "$root/.tmp/agent-worktree-diff-stat.txt"
  git diff -- lab/index.html lab/style.css lab/app.js > "$root/.tmp/agent-worktree-diff.patch"
)
log_event collect_worktree_diff "captured isolated worktree diff artifacts"

python - <<'PY' > .tmp/agent-worktree-hashes-after.json
from __future__ import annotations
import hashlib
import json
from pathlib import Path
files = [
    ".tmp/codex-agent-observed-worktree/lab/index.html",
    ".tmp/codex-agent-observed-worktree/lab/style.css",
    ".tmp/codex-agent-observed-worktree/lab/app.js",
]
out = {}
for name in files:
    path = Path(name)
    out[name] = {
        "exists": path.exists(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None,
        "size_bytes": path.stat().st_size if path.exists() else None,
    }
print(json.dumps(out, indent=2, sort_keys=True))
PY

if [ "$rc" -ne 0 ]; then
  log_event stop_before_copyback "codex failed; preserving diagnostics without copyback"
  exit "$rc"
fi

: > .tmp/agent-copied-files.txt
if ! diff -q lab/index.html "$worktree/lab/index.html" >/dev/null; then
  cp "$worktree/lab/index.html" lab/index.html
  echo "lab/index.html" >> .tmp/agent-copied-files.txt
fi
if ! diff -q lab/style.css "$worktree/lab/style.css" >/dev/null; then
  cp "$worktree/lab/style.css" lab/style.css
  echo "lab/style.css" >> .tmp/agent-copied-files.txt
fi
if ! diff -q lab/app.js "$worktree/lab/app.js" >/dev/null; then
  cp "$worktree/lab/app.js" lab/app.js
  echo "lab/app.js" >> .tmp/agent-copied-files.txt
fi
log_event copyback "copied changed allowed files back to repository"

cp .tmp/agent-wrapper-timeline.jsonl .tmp/canary-diagnostics/agent-wrapper-timeline.jsonl
cp .tmp/agent-worktree-status.txt .tmp/canary-diagnostics/agent-worktree-status.txt
cp .tmp/agent-worktree-diff-name-only.txt .tmp/canary-diagnostics/agent-worktree-diff-name-only.txt
cp .tmp/agent-worktree-diff-stat.txt .tmp/canary-diagnostics/agent-worktree-diff-stat.txt
cp .tmp/agent-worktree-diff.patch .tmp/canary-diagnostics/agent-worktree-diff.patch
cp .tmp/agent-worktree-hashes-before.json .tmp/canary-diagnostics/agent-worktree-hashes-before.json
cp .tmp/agent-worktree-hashes-after.json .tmp/canary-diagnostics/agent-worktree-hashes-after.json
cp .tmp/agent-copied-files.txt .tmp/canary-diagnostics/agent-copied-files.txt

cat .tmp/codex-stderr.txt >&2
log_event finish "agent observed wrapper finished"
