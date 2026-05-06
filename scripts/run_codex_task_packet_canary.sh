#!/usr/bin/env bash
set -euo pipefail

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "Required API key environment variable is not configured."
  exit 1
fi

mkdir -p .tmp .tmp/canary-diagnostics
root="$PWD"
work="$root/.tmp/task-packet-work"
base="$root/.tmp/task-packet-base"
task="$root/.tmp/task-packet"
runtime="$root/.tmp/task-packet-runtime"
diag="$root/.tmp/canary-diagnostics"
rm -rf "$work" "$base" "$task" "$runtime"
mkdir -p "$work/lab" "$base/lab" "$runtime" "$diag"

python scripts/create_codex_task_packet.py \
  --out-dir "$task" \
  --canary-id first-canary-008 \
  --run-week "${RUN_WEEK:-first-canary-008}" \
  --model "${CODEX_MODEL:-gpt-5.4-nano}" \
  > "$diag/task-packet-generator-output.json"

cp lab/index.html "$work/lab/index.html"
cp lab/style.css "$work/lab/style.css"
cp lab/app.js "$work/lab/app.js"
cp lab/index.html "$base/lab/index.html"
cp lab/style.css "$base/lab/style.css"
cp lab/app.js "$base/lab/app.js"
chmod -R a+rwX "$work" "$runtime" "$diag"
chmod -R a-w "$task"

find "$task" -maxdepth 1 -type f -printf '%f\n' | sort > "$diag/task-visible-files.txt"
cp "$task/task-file-hashes.json" "$diag/task-file-hashes.json"
cp "$task/run-manifest.json" "$diag/task-run-manifest.json"
cp "$task/allowed-files.json" "$diag/task-allowed-files.json"
cp "$task/execution-policy.md" "$diag/task-execution-policy.md"
cp "$task/selected-prompt.md" "$diag/task-selected-prompt.md"
cp "$task/static-ui-v1.0.md" "$diag/task-static-ui-v1.0.md"
cp "$task/agent-run-policy-v1.0.md" "$diag/task-agent-run-policy-v1.0.md"

cat > "$diag/policy-allowed-paths.json" <<'EOF'
{
  "container_work_root": "/work",
  "container_task_root": "/task",
  "container_task_mount_mode": "read-only",
  "container_runtime_root": "/codex-runtime",
  "repo_root_mounted": false,
  "allowed_container_paths": ["/work/lab/index.html", "/work/lab/style.css", "/work/lab/app.js"],
  "final_copyback_paths": ["lab/index.html", "lab/style.css", "lab/app.js"]
}
EOF

cat > .tmp/task-packet-inner.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
mkdir -p /diagnostics /codex-runtime/home /codex-runtime/codex-home /codex-runtime/npm-global /codex-runtime/npm-cache /codex-runtime/tmp
export HOME=/codex-runtime/home
export TMPDIR=/codex-runtime/tmp
export NPM_CONFIG_USERCONFIG=/codex-runtime/npmrc
export NPM_CONFIG_PREFIX=/codex-runtime/npm-global
export NPM_CONFIG_CACHE=/codex-runtime/npm-cache
export CODEX_HOME=/codex-runtime/codex-home
export PATH="/codex-runtime/npm-global/bin:$PATH"

id > /diagnostics/container-id.txt
find /work -maxdepth 3 -type f | sort > /diagnostics/container-visible-files-before.txt
find /task -maxdepth 2 -type f | sort > /diagnostics/task-visible-files-container.txt
find /codex-runtime -maxdepth 2 -type d | sort > /diagnostics/container-runtime-dirs-before.txt
mount > /diagnostics/policy-container-mounts.txt

: > /diagnostics/policy-denied-access.txt
for forbidden in /work/.git /work/.github /work/scripts /work/docs /work/runs; do
  if test -e "$forbidden"; then echo "$forbidden" >> /diagnostics/policy-denied-access.txt; exit 20; fi
done

set +e
echo test > /task/.write-test 2> /diagnostics/task-write-test-stderr.txt
task_write_rc=$?
set -e
printf '%s\n' "$task_write_rc" > /diagnostics/task-write-test-exit-code.txt
if [ "$task_write_rc" -eq 0 ]; then
  echo "/task unexpectedly writable" >> /diagnostics/policy-denied-access.txt
  exit 21
fi

node --version > /diagnostics/node-version.txt
npm --version > /diagnostics/npm-version.txt
npm install -g @openai/codex > /diagnostics/npm-install-codex.txt 2> /diagnostics/npm-install-codex-stderr.txt
codex --version > /diagnostics/codex-version.txt

if [ -n "${OPENAI_API_KEY:-}" ]; then
  echo "OPENAI_API_KEY present before login: yes" > /diagnostics/credential-presence-check.txt
else
  echo "OPENAI_API_KEY present before login: no" > /diagnostics/credential-presence-check.txt
fi
printf '%s' "$OPENAI_API_KEY" | codex login --with-api-key > /diagnostics/codex-login-stdout.txt 2> /diagnostics/codex-login-stderr.txt
unset OPENAI_API_KEY
if [ -n "${OPENAI_API_KEY:-}" ]; then
  echo "OPENAI_API_KEY present before codex exec: yes" >> /diagnostics/credential-presence-check.txt
else
  echo "OPENAI_API_KEY present before codex exec: no" >> /diagnostics/credential-presence-check.txt
fi

cat > /codex-runtime/prompt.md <<'PROMPT'
You are Codex running Prompt Vote Lab first-canary-008.

Read these task packet files:
- /task/execution-policy.md
- /task/run-manifest.json
- /task/allowed-files.json
- /task/static-ui-v1.0.md
- /task/agent-run-policy-v1.0.md
- /task/selected-prompt.md

Implement the selected prompt by editing only:
- /work/lab/index.html
- /work/lab/style.css
- /work/lab/app.js

Do not edit /task. It is read-only.
The repository root is intentionally unavailable.
At the end, summarize files inspected, files changed, unavailable paths, and ignored unsafe or unsupported parts.
PROMPT
prompt="$(cat /codex-runtime/prompt.md)"
set +e
codex exec --cd /work --skip-git-repo-check --model "${CODEX_MODEL:-gpt-5.4-nano}" --sandbox danger-full-access --json --output-last-message /diagnostics/codex-last-message.txt "$prompt" > /diagnostics/codex-events.jsonl 2> /diagnostics/codex-stderr.txt
rc=$?
set -e
printf '%s\n' "$rc" > /diagnostics/codex-exit-code.txt
find /work -maxdepth 3 -type f | sort > /diagnostics/container-visible-files-after.txt
find /task -maxdepth 2 -type f | sort > /diagnostics/task-visible-files-container-after.txt
find /codex-runtime -maxdepth 3 -type f | sort > /diagnostics/container-runtime-files-after.txt
exit "$rc"
EOF
chmod +x .tmp/task-packet-inner.sh

set +e
docker run --rm \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --user "$(id -u):$(id -g)" \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -e CODEX_MODEL="${CODEX_MODEL:-gpt-5.4-nano}" \
  -v "$work:/work:rw" \
  -v "$task:/task:ro" \
  -v "$runtime:/codex-runtime:rw" \
  -v "$diag:/diagnostics:rw" \
  -v "$root/.tmp/task-packet-inner.sh:/runner.sh:ro" \
  -w /work \
  node:20-bookworm \
  /runner.sh > .tmp/task-packet-container-stdout.txt 2> .tmp/task-packet-container-stderr.txt
container_rc=$?
set -e
printf '%s\n' "$container_rc" > .tmp/task-packet-container-exit-code.txt
cp .tmp/task-packet-container-stdout.txt "$diag/task-packet-container-stdout.txt" 2>/dev/null || true
cp .tmp/task-packet-container-stderr.txt "$diag/task-packet-container-stderr.txt" 2>/dev/null || true
cp .tmp/task-packet-container-exit-code.txt "$diag/task-packet-container-exit-code.txt" 2>/dev/null || true

chmod -R u+rwX .tmp/canary-diagnostics .tmp/task-packet-work .tmp/task-packet-runtime || true
cp "$diag/codex-events.jsonl" .tmp/codex-events.jsonl 2>/dev/null || : > .tmp/codex-events.jsonl
cp "$diag/codex-last-message.txt" .tmp/codex-last-message.txt 2>/dev/null || : > .tmp/codex-last-message.txt
cp "$diag/codex-stderr.txt" .tmp/codex-stderr.txt 2>/dev/null || cp .tmp/task-packet-container-stderr.txt .tmp/codex-stderr.txt 2>/dev/null || : > .tmp/codex-stderr.txt
cp "$diag/codex-exit-code.txt" .tmp/codex-exit-code.txt 2>/dev/null || printf '%s\n' "$container_rc" > .tmp/codex-exit-code.txt

python - <<'PY'
from __future__ import annotations
import difflib
from pathlib import Path
pairs = [('index.html','lab/index.html'),('style.css','lab/style.css'),('app.js','lab/app.js')]
changed=[]; patch=[]
for short, display in pairs:
    old=Path('.tmp/task-packet-base/lab', short).read_text(encoding='utf-8').splitlines(True)
    new=Path('.tmp/task-packet-work/lab', short).read_text(encoding='utf-8').splitlines(True)
    if old != new:
        changed.append(display)
        patch.extend(difflib.unified_diff(old,new,fromfile='a/'+display,tofile='b/'+display))
Path('.tmp/task-packet-diff-name-only.txt').write_text('\n'.join(changed)+('\n' if changed else ''), encoding='utf-8')
Path('.tmp/task-packet-diff.patch').write_text(''.join(patch), encoding='utf-8')
PY

cp .tmp/task-packet-diff-name-only.txt "$diag/task-packet-diff-name-only.txt"
cp .tmp/task-packet-diff.patch "$diag/task-packet-diff.patch"

if [ "$container_rc" -ne 0 ]; then
  cat .tmp/task-packet-container-stderr.txt >&2
  exit "$container_rc"
fi

: > .tmp/task-packet-copied-files.txt
for file in lab/index.html lab/style.css lab/app.js; do
  if ! diff -q "$file" ".tmp/task-packet-work/$file" >/dev/null; then
    cp ".tmp/task-packet-work/$file" "$file"
    echo "$file" >> .tmp/task-packet-copied-files.txt
  fi
done
cp .tmp/task-packet-copied-files.txt "$diag/task-packet-copied-files.txt"
