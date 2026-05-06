# first-canary-005 offline JSON writeback success

## Status

PASS.

## Fixed conditions

```text
canary_id: first-canary-005
runner: codex-cli-offline-json-writeback
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
sandbox_mode: read-only-empty-context
writeback_mode: validated JSON full-file replacement
final_writable_files: lab/index.html, lab/style.css, lab/app.js
```

## Changed condition from first-canary-004

```text
first-canary-004: read-only repository context + unified diff patch
first-canary-005: empty execution context + prompt-provided file contents + JSON full-file replacement
```

The canary ID changed because the writeback protocol changed.

## Observed behavior

The runner authenticated successfully, created an empty temporary execution context, embedded the three allowed lab file contents into the prompt, received JSON output, validated the output, applied the allowed replacement, and created a pull request.

Resulting PR:

```text
#127 Run Codex offline JSON canary
```

Merge commit:

```text
729dbfc61a76ad7dd6ae14435b736f1863367153
```

Changed files:

```text
lab/index.html
```

Diff summary:

```diff
-      <strong>Canary (3rd):</strong> this is the third bounded Codex implementation-agent canary.
+      <strong>Canary (5th):</strong> this is the fifth bounded Codex implementation-agent canary.
```

## Interpretation

This is the first successful workflow-mediated writeback canary that does not rely on Codex directly editing repository files.

Previous results:

```text
first-canary-001: full repository + workspace-write -> sandbox failure
first-canary-002: isolated three-file worktree + workspace-write -> sandbox failure
first-canary-003: isolated three-file worktree + danger-full-access -> PR created
first-canary-004: read-only repository context + unified diff writeback -> writeback-control failure
first-canary-005: empty context + JSON full-file replacement -> PR created and merged
```

## Operational significance

This mode is safer than the relaxed direct-edit canary because the model does not directly write repository files. The workflow remains responsible for parsing, validating, applying, and checking the final changes.

## Limitations

The output protocol uses full-file JSON replacement, which can be verbose for larger files. For the current three-file static lab, this is acceptable. Future work may add smaller structured operations, but that should be a new canary ID if it changes the protocol.

## Next valid options

```text
Option A: treat first-canary-005 as the current production-oriented implementation path.
Option B: add stronger schema validation and size checks under the same path if behavior is strictly compatible.
Option C: create a new canary ID for a smaller operation-based writeback protocol.
```

## Rejected option

```text
Do not mutate first-canary-004 to match this protocol.
```
