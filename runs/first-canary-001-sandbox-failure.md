# first-canary-001 sandbox failure

## Status

FAIL.

## Fixed conditions

```text
model: gpt-5.4-nano
week: first-canary-001
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
sandbox_mode: workspace-write
allowed_changed_files: lab/index.html, lab/style.css, lab/app.js
```

## Observed behavior

The runner authenticated successfully and Codex attempted to modify `lab/index.html`.

The run then failed because the Codex workspace-write sandbox helper could not operate on the GitHub-hosted runner environment.

Relevant internal log excerpts:

```text
Reading API key from stdin...
Successfully logged in
Failed to read file to update .../lab/index.html: fs sandbox helper failed with status exit status: 1: bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
Failed to write file /tmp/pvll_test_codex.txt
Codex produced no changes.
```

## Interpretation

This is not a model no-op.

Codex reached the editing step, but the local sandbox helper failed before the working tree could be modified.

Under the fixed `first-canary-001` contract, this run remains a failure. Do not change the model, prompt, retry policy, fallback policy, or sandbox setting inside this canary ID to force a pass.

## Next valid options

```text
Option A: keep first-canary-001 closed as FAIL and create a new canary ID with a different runner environment.
Option B: keep the same fixed canary conditions but run on a sandbox-compatible self-hosted runner.
Option C: create a new canary ID that explicitly changes sandbox_mode, then compare it separately.
```

## Rejected option

```text
Do not silently switch sandbox_mode away from workspace-write under first-canary-001.
```
