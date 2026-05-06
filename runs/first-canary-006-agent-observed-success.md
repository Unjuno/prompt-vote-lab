# first-canary-006 agent-observed direct-edit success

## Status

PASS.

## Fixed conditions

```text
canary_id: first-canary-006
runner: codex-cli-agent-observed-wrapper
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
execution_mode: agent-observed direct edit
sandbox_mode: danger-full-access-isolated-3file
visible_files: lab/index.html, lab/style.css, lab/app.js
final_writable_files: lab/index.html, lab/style.css, lab/app.js
manual_review: required
```

## Purpose

This canary was created because `first-canary-005` is operationally safer but API-like. It does not strongly expose Codex as a file-operating agent.

`first-canary-006` restores direct file operation in an isolated three-file worktree and wraps the run with additional diagnostics so prompt designers can inspect agent behavior.

## Observed behavior

The workflow completed successfully, copied back allowed changes, passed internal checks, created a pull request, and the pull request was merged.

Resulting PR:

```text
#131 Run Codex agent-observed canary
```

Merge commit:

```text
a262868194c0dc72985322ded850ecc75001c684
```

Changed files:

```text
lab/index.html
```

Diff summary:

```diff
-      <strong>Canary (5th):</strong> this is the fifth bounded Codex implementation-agent canary.
+      <strong>Canary (6th):</strong> this is the sixth bounded Codex implementation-agent canary.
```

## Captured diagnostics

The agent-observed wrapper captures these artifacts for analysis:

```text
codex-events.jsonl
codex-stdout.txt
codex-stderr.txt
codex-last-message.txt
codex-exit-code.txt
agent-wrapper-timeline.jsonl
agent-worktree-status.txt
agent-worktree-diff-name-only.txt
agent-worktree-diff-stat.txt
agent-worktree-diff.patch
agent-worktree-hashes-before.json
agent-worktree-hashes-after.json
agent-copied-files.txt
final repository diff via shared diagnostics collector
```

## Interpretation

This confirms that Codex can be run as an observed file-operating agent inside a constrained three-file worktree while preserving final output scope.

Previous results:

```text
first-canary-001: full repository + workspace-write -> sandbox failure
first-canary-002: isolated three-file worktree + workspace-write -> sandbox failure
first-canary-003: isolated three-file worktree + danger-full-access -> PR created
first-canary-004: read-only repository context + unified diff writeback -> writeback-control failure
first-canary-005: empty context + JSON full-file replacement -> PR created and merged
first-canary-006: isolated three-file agent-observed direct edit -> PR created and merged
```

## Limitations

This is not the safest production path. The sandbox mode is relaxed inside the isolated worktree. Final changed-file guards protect the repository output, but they do not prove that all attempted file access was denied at the OS boundary.

`first-canary-006` should therefore be treated as an agent-observation path, not as the default production-oriented path.

## Next valid option

Create a new canary for policy-enforced agent execution:

```text
first-canary-007-policy-enforced-agent
```

The next canary should test whether Codex can operate as an agent while the execution environment prevents access to unauthorized repository files.

## Rejected option

```text
Do not replace first-canary-005 as the current production-oriented path solely because first-canary-006 succeeded.
```
