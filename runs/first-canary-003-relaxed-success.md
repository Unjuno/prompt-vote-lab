# first-canary-003 relaxed direct-edit success

## Status

PASS.

## Fixed conditions

```text
canary_id: first-canary-003
runner: codex-cli-isolated-3file-relaxed-direct-edit
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
sandbox_mode: danger-full-access
visible_files: lab/index.html, lab/style.css, lab/app.js
final_writable_files: lab/index.html, lab/style.css, lab/app.js
```

## Changed condition from first-canary-002

```text
sandbox_mode: workspace-write -> danger-full-access
```

The canary ID changed because sandbox mode changed.

## Observed behavior

The runner authenticated successfully, Codex edited the isolated three-file worktree, the workflow copied the allowed changed files back to the repository, and a pull request was created.

Resulting PR:

```text
#122 Run Codex isolated three-file relaxed canary
```

Changed files:

```text
lab/index.html
lab/style.css
```

No final changes outside the allowed lab files were present.

## Interpretation

This supports the hypothesis that the earlier failures were caused by the GitHub-hosted runner `workspace-write` sandbox path rather than by the fixed model or prompt.

Previous results:

```text
first-canary-001: full repository + workspace-write -> sandbox failure
first-canary-002: isolated three-file worktree + workspace-write -> sandbox failure
first-canary-003: isolated three-file worktree + danger-full-access -> PR created
```

## Limitations

This is not a success for `workspace-write` sandboxing.

`danger-full-access` is a relaxed sandbox mode, so this result should be treated as direct-edit execution-path evidence, not as the final safest production design.

## Next valid options

```text
Option A: build a workflow-mediated writeback canary for safer production-oriented operation.
Option B: keep direct-edit as an experimental mode only, with diagnostics artifacts and manual review.
Option C: test workspace-write on a sandbox-compatible self-hosted runner under a new canary ID.
```

## Rejected option

```text
Do not backport danger-full-access into first-canary-001 or first-canary-002.
```
