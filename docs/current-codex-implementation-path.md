# Current Codex implementation path

## Status

The current production-oriented implementation path is:

```text
first-canary-005: offline context + JSON full-file replacement
```

This path is preferred over direct repository editing for routine Prompt Vote Lab implementation runs.

## Why this path is current

The canary series produced the following evidence:

```text
first-canary-001: full repository + workspace-write -> FAIL
first-canary-002: isolated three-file worktree + workspace-write -> FAIL
first-canary-003: isolated three-file worktree + danger-full-access -> PASS
first-canary-004: read-only repository context + unified diff writeback -> FAIL
first-canary-005: empty context + JSON full-file replacement -> PASS
```

The result means:

```text
- Codex can generate useful lab changes.
- GitHub-hosted runner workspace-write sandboxing failed through the local bwrap path.
- Relaxed direct editing can work, but it is not the safest default.
- Repo-context writeback still allowed Codex to attempt an internal write path.
- Offline-context JSON writeback gives the workflow control over actual file writes.
```

## Current default

Use `first-canary-005` style execution for production-oriented implementation runs.

```text
runner: codex-cli-offline-json-writeback
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
sandbox_mode: read-only-empty-context
writeback_mode: validated JSON full-file replacement
final_writable_files: lab/index.html, lab/style.css, lab/app.js
manual_review: required
```

## How the current path works

```text
1. The workflow checks out the repository.
2. The workflow captures diagnostics baseline data.
3. The workflow reads the three allowed lab files.
4. The workflow builds a prompt containing those file contents.
5. Codex runs in an empty temporary directory.
6. Codex returns JSON containing full replacement content for changed allowed files.
7. The workflow validates the JSON payload.
8. The workflow applies replacements only for allowed files.
9. The workflow runs changed-file guard, safety-check, and static-site-check.
10. The workflow creates a pull request.
11. A human reviews and merges manually.
```

## Allowed final write scope

Only these files may be changed by the workflow-mediated writeback path:

```text
lab/index.html
lab/style.css
lab/app.js
```

No other file path is a valid final output path.

## Safety boundary

The safety boundary is not the model prompt alone.

The boundary is the combination of:

```text
- empty Codex execution context
- prompt-provided file contents only
- JSON parser
- allowed-path validator
- duplicate-path rejection
- empty-content rejection
- max file size check
- changed-file guard
- safety-check
- static-site-check
- diagnostics artifact upload
- manual review
```

Prompt instructions are still used, but they are not treated as enforcement.

## Why direct editing is not the default

`first-canary-003` proved that isolated direct editing can work with relaxed sandbox mode:

```text
isolated three-file worktree + danger-full-access -> PASS
```

However, this mode should remain experimental because it relies on broad write capability inside the runner process. The final changed-file guard still helps, but the execution-time boundary is weaker than offline JSON writeback.

Direct editing may still be useful for experiments that specifically evaluate Codex tool behavior, action traces, or sandbox behavior.

## Why first-canary-004 is not the default

`first-canary-004` attempted read-only repository-context writeback using a unified diff patch. It failed because Codex still attempted an internal patch/write path under read-only conditions, and the final patch did not apply cleanly.

The lesson is:

```text
Do not give Codex a repository working tree if the intended protocol is purely mediated output.
```

For mediated output, provide only the required file contents and keep actual repository writes in workflow code.

## Remaining risks

The current path is safer than relaxed direct editing, but not risk-free.

Known residual risks:

```text
- full-file JSON replacement can be verbose
- generated full-file content may accidentally drop unrelated markup
- schema is minimal and not a formal JSON Schema yet
- semantic quality is checked by review rather than formal validation
- safety-check and static-site-check only cover known static-site hazards
- manual review remains mandatory
```

## Compatible improvements

The following improvements are compatible with the current path if they preserve the same canary contract:

```text
- stricter JSON schema validation
- tighter maximum size checks
- required rationale summary in a separate JSON field
- better diagnostics summaries
- stronger HTML/CSS/JS static checks
- snapshot tests for expected lab structure
```

These can be added without changing the core protocol if they remain backward-compatible.

## Changes requiring a new canary ID

Use a new canary ID if any of these change:

```text
- model
- attempts
- retry policy
- fallback policy
- auto-merge policy
- final writable files
- execution context model
- writeback protocol
- direct-edit versus mediated-writeback mode
- patch versus JSON replacement protocol
```

## Current recommendation

Use this as the default implementation path:

```text
first-canary-005-offline-context-json-writeback
```

Keep `first-canary-003` as an experimental direct-edit proof and `first-canary-004` as a documented negative result.
