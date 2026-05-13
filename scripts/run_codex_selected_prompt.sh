#!/usr/bin/env bash
set -euo pipefail

canary_id="selected-prompt"
run_week="${RUN_WEEK:-selected-prompt}"
issue_number="0"
issue_title=""
issue_url=""
candidate_rank="1"
vote_count="0"
selection_policy="manual-selected-prompt"
prompt_body=""
prompt_file=""
work_label="selected-prompt"

usage() {
  cat <<'USAGE'
Usage: scripts/run_codex_selected_prompt.sh [options]

Creates a selected-prompt task packet, runs Codex in the canonical Docker sandbox,
and copies back only allowed lab files.

Options:
  --canary-id ID
  --run-week WEEK
  --issue-number N
  --issue-title TITLE
  --issue-url URL
  --candidate-rank N
  --vote-count N
  --selection-policy TEXT
  --prompt-body TEXT
  --prompt-file PATH
  --work-label TEXT
  -h, --help

Environment:
  OPENAI_API_KEY  Required
  CODEX_MODEL     Optional, default gpt-5.4-nano
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --canary-id) canary_id="${2:-}"; shift 2 ;;
    --run-week) run_week="${2:-}"; shift 2 ;;
    --issue-number) issue_number="${2:-}"; shift 2 ;;
    --issue-title) issue_title="${2:-}"; shift 2 ;;
    --issue-url) issue_url="${2:-}"; shift 2 ;;
    --candidate-rank) candidate_rank="${2:-}"; shift 2 ;;
    --vote-count) vote_count="${2:-}"; shift 2 ;;
    --selection-policy) selection_policy="${2:-}"; shift 2 ;;
    --prompt-body) prompt_body="${2:-}"; shift 2 ;;
    --prompt-file) prompt_file="${2:-}"; shift 2 ;;
    --work-label) work_label="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "Required API key environment variable is not configured."
  exit 1
fi
case "$candidate_rank" in 1|2|3) ;; *) echo "candidate_rank must be 1, 2, or 3" >&2; exit 2 ;; esac
case "$vote_count" in ''|*[!0-9]*) echo "vote_count must be a non-negative integer" >&2; exit 2 ;; *) ;; esac
case "$issue_number" in ''|*[!0-9]*) echo "issue_number must be a non-negative integer" >&2; exit 2 ;; *) ;; esac
if [ -n "$prompt_body" ] && [ -n "$prompt_file" ]; then
  echo "Use only one of --prompt-body or --prompt-file" >&2
  exit 2
fi

mkdir -p .tmp .tmp/canary-diagnostics
root="$PWD"
work="$root/.tmp/${work_label}-work"
base="$root/.tmp/${work_label}-base"
task="$root/.tmp/${work_label}-task"
runtime="$root/.tmp/${work_label}-runtime"
diag="$root/.tmp/canary-diagnostics"
rm -rf "$work" "$base" "$task" "$runtime"
mkdir -p "$work/lab" "$base/lab" "$runtime" "$diag"

packet_args=(
  --out-dir "$task"
  --canary-id "$canary_id"
  --run-week "$run_week"
  --issue-number "$issue_number"
  --issue-title "$issue_title"
  --issue-url "$issue_url"
  --candidate-rank "$candidate_rank"
  --vote-count "$vote_count"
  --selection-policy "$selection_policy"
  --model "${CODEX_MODEL:-gpt-5.4-nano}"
)
if [ -n "$prompt_body" ]; then packet_args+=(--prompt-body "$prompt_body"); fi
if [ -n "$prompt_file" ]; then packet_args+=(--prompt-file "$prompt_file"); fi
python scripts/create_codex_task_packet.py "${packet_args[@]}" > "$diag/selected-prompt-task-packet-generator-output.json"

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

cat > ".tmp/${work_label}-inner.sh" <<'EOF'
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
You are Codex running Prompt Vote Lab selected-prompt implementation.

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
chmod +x ".tmp/${work_label}-inner.sh"

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
  -v "$root/.tmp/${work_label}-inner.sh:/runner.sh:ro" \
  -w /work \
  node:20-bookworm \
  /runner.sh > ".tmp/${work_label}-container-stdout.txt" 2> ".tmp/${work_label}-container-stderr.txt"
container_rc=$?
set -e
printf '%s\n' "$container_rc" > ".tmp/${work_label}-container-exit-code.txt"
cp ".tmp/${work_label}-container-stdout.txt" "$diag/selected-prompt-container-stdout.txt" 2>/dev/null || true
cp ".tmp/${work_label}-container-stderr.txt" "$diag/selected-prompt-container-stderr.txt" 2>/dev/null || true
cp ".tmp/${work_label}-container-exit-code.txt" "$diag/selected-prompt-container-exit-code.txt" 2>/dev/null || true
chmod -R u+rwX "$diag" "$work" "$runtime" || true
cp "$diag/codex-events.jsonl" .tmp/codex-events.jsonl 2>/dev/null || : > .tmp/codex-events.jsonl
cp "$diag/codex-last-message.txt" .tmp/codex-last-message.txt 2>/dev/null || : > .tmp/codex-last-message.txt
cp "$diag/codex-stderr.txt" .tmp/codex-stderr.txt 2>/dev/null || cp ".tmp/${work_label}-container-stderr.txt" .tmp/codex-stderr.txt 2>/dev/null || : > .tmp/codex-stderr.txt
cp "$diag/codex-exit-code.txt" .tmp/codex-exit-code.txt 2>/dev/null || printf '%s\n' "$container_rc" > .tmp/codex-exit-code.txt

python - "$base" "$work" ".tmp/${work_label}-diff-name-only.txt" ".tmp/${work_label}-diff.patch" <<'PY'
from __future__ import annotations
import difflib
import sys
from pathlib import Path
base = Path(sys.argv[1])
work = Path(sys.argv[2])
name_only = Path(sys.argv[3])
patch_path = Path(sys.argv[4])
pairs = [('index.html','lab/index.html'),('style.css','lab/style.css'),('app.js','lab/app.js')]
changed=[]; patch=[]
for short, display in pairs:
    old=(base / 'lab' / short).read_text(encoding='utf-8').splitlines(True)
    new=(work / 'lab' / short).read_text(encoding='utf-8').splitlines(True)
    if old != new:
        changed.append(display)
        patch.extend(difflib.unified_diff(old,new,fromfile='a/'+display,tofile='b/'+display))
name_only.write_text('\n'.join(changed)+('\n' if changed else ''), encoding='utf-8')
patch_path.write_text(''.join(patch), encoding='utf-8')
PY
cp ".tmp/${work_label}-diff-name-only.txt" "$diag/selected-prompt-diff-name-only.txt"
cp ".tmp/${work_label}-diff.patch" "$diag/selected-prompt-diff.patch"
if [ "$container_rc" -ne 0 ]; then
  cat ".tmp/${work_label}-container-stderr.txt" >&2
  exit "$container_rc"
fi
: > ".tmp/${work_label}-copied-files.txt"
for file in lab/index.html lab/style.css lab/app.js; do
  if ! diff -q "$file" "$work/$file" >/dev/null; then
    cp "$work/$file" "$file"
    echo "$file" >> ".tmp/${work_label}-copied-files.txt"
  fi
done
cp ".tmp/${work_label}-copied-files.txt" "$diag/selected-prompt-copied-files.txt"
