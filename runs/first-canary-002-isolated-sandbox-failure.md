# first-canary-002 isolated sandbox failure

## Status

FAIL.

## Fixed conditions

```text
canary_id: first-canary-002
runner: codex-cli-isolated-3file-direct-edit
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
sandbox_mode: workspace-write
visible_files: lab/index.html, lab/style.css, lab/app.js
final_writable_files: lab/index.html, lab/style.css, lab/app.js
```

## Observed behavior

The runner authenticated successfully and Codex attempted to update the isolated copy of `lab/index.html` inside `.tmp/codex-3file-worktree/`.

The run then failed because the Codex workspace-write sandbox helper could not update the file on the GitHub-hosted runner environment.

Relevant internal log excerpts:

```text
Reading API key from stdin...
Successfully logged in
Failed to read file to update .../.tmp/codex-3file-worktree/lab/index.html: fs sandbox helper failed with status exit status: 1: bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
Codex produced no changes.
Collected canary diagnostics in .tmp/canary-diagnostics
```

## Interpretation

This is not a model no-op.

Codex reached the edit step, but the local sandbox helper failed before the isolated worktree could be modified. Isolating the visible working tree to three files did not avoid the GitHub-hosted runner `workspace-write` sandbox failure.

Under the fixed `first-canary-002` contract, this run remains a failure. Do not change the model, retry policy, fallback policy, or sandbox mode inside this canary ID to force a pass.

## Diagnostics

The workflow collected a diagnostics artifact for prompt-design analysis.

Expected artifact prefix:

```text
codex-isolated-3file-canary-diagnostics-
```

## Next valid options

```text
Option A: keep first-canary-002 closed as FAIL and create first-canary-003 with a relaxed sandbox mode.
Option B: keep workspace-write but move to a sandbox-compatible self-hosted runner under a new canary ID.
Option C: use a workflow-mediated writeback approach under a new canary ID if direct editing is no longer required.
```

## Rejected option

```text
Do not silently change first-canary-002 from workspace-write to relaxed sandbox.
```
