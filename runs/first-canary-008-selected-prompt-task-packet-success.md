# first-canary-008 selected prompt task packet success

## Status

PASS.

## Fixed conditions

```text
canary_id: first-canary-008
runner: codex-cli-selected-prompt-task-packet-container
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
sandbox_mode: docker-workdir-plus-readonly-task-packet
execution_mode: selected prompt task packet agent direct edit
container_work_root: /work
container_task_root: /task
container_task_mount_mode: read-only
container_runtime_root: /codex-runtime
diagnostics_root: /diagnostics
repo_root_mounted: false
visible_work_files: lab/index.html, lab/style.css, lab/app.js
final_writable_files: lab/index.html, lab/style.css, lab/app.js
manual_review: required
```

## Purpose

This canary tests whether Codex can run as a file-editing agent while receiving the selected implementation prompt as a read-only task packet rather than as repository context.

It extends the successful 007 path by adding:

```text
/task:ro selected prompt packet
policy snapshots inside /task
credential hygiene check before codex exec
```

## Observed result

The workflow completed, created a pull request, passed checks, and the pull request was merged.

```text
PR: #152 Run Codex task packet canary
merge_commit_sha: f227a8fd694c9f6b6eb778bc9ad62fe3e663cf46
changed_files: lab/index.html
```

Diff summary:

```diff
-      <strong>Canary (7th):</strong> this is the seventh bounded Codex implementation-agent canary.
+      <strong>Canary (8th):</strong> this is the eighth bounded Codex implementation-agent canary.
```

## Task packet contents

The task packet mounted at `/task:ro` contained:

```text
/task/agent-run-policy-v1.0.md
/task/allowed-files.json
/task/execution-policy.md
/task/run-manifest.json
/task/selected-prompt.md
/task/static-ui-v1.0.md
/task/task-file-hashes.json
```

The diagnostics artifact also included raw policy snapshot copies:

```text
task-static-ui-v1.0.md
task-agent-run-policy-v1.0.md
```

## Diagnostics summary

The successful run diagnostics indicated:

```text
container exit code: 0
Codex exit code: 0
failure_type: none
policy denied access: empty
/task write test exit code: 1
OPENAI_API_KEY present before login: yes
OPENAI_API_KEY present before codex exec: no
```

The `/task` write test failed as expected because `/task` was mounted read-only.

## Checks passed

```text
selected-prompt task packet runner completed
changed-file guard passed
safety-check passed
static-site-check passed
manual PR review and merge completed
```

## Interpretation

This is the first successful canary in this repository showing Codex operating as a file-editing agent with a selected prompt packet mounted read-only at `/task`.

The successful run supports these claims:

```text
- Codex can read selected task input from /task.
- /task can be mounted read-only while /work remains writable.
- Codex can edit the prepared lab files under /work.
- The workflow can copy back only allowed files.
- The final repository diff can remain within the allowed lab file set.
- The API key can be present for login and absent before codex exec.
- Raw policy snapshot files can be included in diagnostics artifacts.
```

## Not proven

This single run does not prove:

```text
- production vote winner selection from real GitHub Issues
- repeated-run stability for task-packet execution
- full tracing of every file-access attempt
- network restriction to only required API endpoints
- formal proof that every possible container path outside the mounted areas is unreachable
- that 008 should immediately replace 005 as the stable production-oriented path
```

## Current classification

```text
first-canary-005: current stable production-oriented JSON writeback path
first-canary-007: successful policy-enforced agent candidate path
first-canary-008: successful selected-prompt task-packet agent candidate path
```

008 should become the stronger standard agent path only after repeated successful runs under the same fixed conditions and after a separate canary verifies real GitHub Issue prompt selection.

## Recommended next step

Design the next canary for real selected prompt ingestion:

```text
first-canary-009: GitHub Issue selected prompt -> /task/selected-prompt.md
```

Do not treat this single 008 success as proof that the full Prompt Vote Lab production selection pipeline is working. It proves the task packet execution mechanism, not the vote-winner selection layer.
