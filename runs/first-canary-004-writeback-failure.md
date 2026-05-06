# first-canary-004 workflow-mediated writeback failure

## Status

FAIL.

## Fixed conditions

```text
canary_id: first-canary-004
runner: codex-cli-workflow-mediated-writeback
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
codex_sandbox_mode: read-only
writeback_mode: validated unified diff patch
final_writable_files: lab/index.html, lab/style.css, lab/app.js
```

## Observed behavior

The runner authenticated successfully and invoked Codex. Codex then attempted to use an internal patch/write path despite the read-only sandbox. That write attempt was rejected by the sandbox. The workflow still found a patch-like final message and attempted workflow-mediated application, but `git apply --check` rejected it.

Relevant log excerpts:

```text
Reading API key from stdin...
Successfully logged in
patch rejected: writing is blocked by read-only sandbox; rejected by user approval settings
RuntimeError: git apply --check failed:
error: patch failed: lab/index.html:1
error: lab/index.html: patch does not apply
Collected canary diagnostics in .tmp/canary-diagnostics
```

Diagnostics artifact:

```text
codex-writeback-canary-diagnostics-1
artifact_id: 6822238119
```

## Interpretation

This is not an authentication failure and not a no-output failure.

The failure is a writeback-control failure: the prompt did not sufficiently prevent Codex from trying the internal patch/write path under `read-only`, and the resulting final patch was not applicable to the checked-out repository state.

Under the fixed `first-canary-004` contract, this run remains a failure. Do not mutate this canary ID to force a pass.

## Next valid option

Create a new canary ID for a stricter mediated-writeback design.

Recommended next variant:

```text
first-canary-005-offline-context-writeback
```

The next design should avoid giving Codex an editable repository context. Instead, the workflow should provide the three allowed file contents as prompt context and require a machine-parseable patch or replacement payload. The workflow should then validate and apply the output.

## Rejected option

```text
Do not silently change first-canary-004 from read-only repo-context execution into a different offline-context protocol.
```
