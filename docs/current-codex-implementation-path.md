# Current Codex implementation path

## Status

The current stable production-oriented implementation path remains:

```text
first-canary-005: offline context + JSON full-file replacement
```

The strongest implemented agent-boundary candidate path is now:

```text
first-canary-008: selected prompt task packet container
```

Do not silently replace `first-canary-005` with `first-canary-008` after one successful 008 run. Treat 008 as the stronger agent candidate until repeated runs and real selected-Issue ingestion demonstrate stability.

## Why this path is current

The canary series produced the following evidence:

```text
first-canary-001: full repository + workspace-write -> FAIL
first-canary-002: isolated three-file worktree + workspace-write -> FAIL
first-canary-003: isolated three-file worktree + danger-full-access -> PASS
first-canary-004: read-only repository context + unified diff writeback -> FAIL
first-canary-005: empty context + JSON full-file replacement -> PASS
first-canary-006: isolated three-file agent-observed direct edit -> PASS
first-canary-007: Docker-mounted workdir-only policy agent -> PASS
first-canary-008: Docker workdir + read-only selected prompt task packet -> PASS
```

The result means:

```text
- Codex can generate useful lab changes.
- GitHub-hosted runner workspace-write sandboxing failed through the local bwrap path.
- Relaxed direct editing can work, but it is not the safest default.
- Repo-context writeback still allowed Codex to attempt an internal patch/write path.
- Offline-context JSON writeback gives the workflow control over actual file writes.
- Agent-observed direct edit is useful for behavior analysis.
- Policy-enforced container execution can run Codex as an agent without mounting the repository root.
- Selected prompt task packets can be mounted read-only at /task while Codex edits /work/lab only.
- The API key can be present for codex login and absent before codex exec.
```

## Current default

Use `first-canary-005` style execution for routine production-oriented implementation runs.

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

## Stronger agent candidate path

Use `first-canary-008` for agent-style runs that need selected prompt task-packet evidence.

```text
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
repo_root_mounted: false
final_writable_files: lab/index.html, lab/style.css, lab/app.js
manual_review: required
```

008 is not yet the default production-oriented implementation path because it has one successful full run and still uses a fixed canary prompt packet rather than a real GitHub Issue selected by the selection layer.

## Next candidate

The next canary should be:

```text
first-canary-009: fixed GitHub Issue -> normalized instruction packet -> /task:ro
```

009 should verify Issue ingestion and instruction normalization only. It should not also introduce automatic vote-winner selection.

## How the current stable path works

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

## How the 008 candidate path works

```text
1. The workflow checks out the repository.
2. The workflow generates a selected prompt task packet.
3. The workflow copies lab/index.html, lab/style.css, and lab/app.js into a prepared work directory.
4. The workflow mounts the work directory into a Docker container as /work:rw.
5. The workflow mounts the task packet into the container as /task:ro.
6. The workflow mounts a separate runtime directory as /codex-runtime:rw.
7. The repository root is not mounted into the container.
8. Codex logs in, then OPENAI_API_KEY is removed before codex exec.
9. Codex reads /task and edits the prepared lab files under /work.
10. The workflow copies back only lab/index.html, lab/style.css, and lab/app.js.
11. The workflow runs changed-file guard, safety-check, and static-site-check.
12. The workflow creates a pull request.
13. A human reviews and merges manually.
```

## Allowed final write scope

Only these files may be changed by the implementation paths:

```text
lab/index.html
lab/style.css
lab/app.js
```

No other file path is a valid final output path.

## Safety boundary

The safety boundary is not the model prompt alone.

For 005, the boundary is the combination of:

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

For 008, the boundary is the combination of:

```text
- Docker workdir plus read-only task packet execution
- repository root not mounted into the agent container
- read-only selected prompt and policy packet at /task
- separate runtime mount at /codex-runtime
- API key absent before codex exec
- final copy-back limited to the three lab files
- changed-file guard
- safety-check
- static-site-check
- diagnostics artifact upload
- manual review
```

Prompt instructions are still used, but they are not treated as enforcement.

## Why direct editing is not the default

`first-canary-003` and `first-canary-006` proved that isolated direct editing can work with relaxed sandbox mode:

```text
first-canary-003: isolated three-file worktree + danger-full-access -> PASS
first-canary-006: isolated three-file agent-observed direct edit -> PASS
```

However, these modes remain experimental because they rely on broad write capability inside the runner process. The final changed-file guard still helps, but the execution-time boundary is weaker than 008 and the mediated output boundary is less operationally stable than 005.

## Why first-canary-004 is not the default

`first-canary-004` attempted read-only repository-context writeback using a unified diff patch. It failed because Codex still attempted an internal patch/write path under read-only conditions, and the final patch did not apply cleanly.

The lesson is:

```text
Do not give Codex a repository working tree if the intended protocol is purely mediated output.
```

For mediated output, provide only the required file contents and keep actual repository writes in workflow code.

## Remaining risks

Known residual risks for 005:

```text
- full-file JSON replacement can be verbose
- generated full-file content may accidentally drop unrelated markup
- schema is minimal and not a formal JSON Schema yet
- semantic quality is checked by review rather than formal validation
- safety-check and static-site-check only cover known static-site hazards
- manual review remains mandatory
```

Known residual risks for 008:

```text
- only one successful full run has been observed
- Docker and npm installation add moving parts
- network access is not narrowed to only required API endpoints
- full file-access tracing is not yet implemented
- container path coverage is sampled through diagnostics, not formally proven
- the first 008 used a fixed canary prompt, not a real selected GitHub Issue
- manual review remains mandatory
```

## Promotion rule for 008

Do not promote 008 to the standard agent path after a single success.

Promotion condition:

```text
008 may be promoted from candidate to standard agent path after at least 2 consecutive successful full 008 runs under the same fixed conditions, plus one successful fixed-Issue 009 run.
```

A successful repeated 008 run must show:

```text
- Codex exit code 0
- container exit code 0
- final changed files subset of lab/index.html, lab/style.css, lab/app.js
- repository root not mounted into the container work directory
- /task mounted read-only
- API key absent before codex exec
- policy-denied-access empty or explained
- safety-check PASS
- static-site-check PASS
- manual PR review and merge
```

## Compatible improvements

The following improvements are compatible if they preserve the same canary contract:

```text
- stricter JSON schema validation for 005
- tighter maximum size checks
- required rationale summary in a separate JSON field
- better diagnostics summaries
- stronger HTML/CSS/JS static checks
- snapshot tests for expected lab structure
- richer 008 diagnostics summaries
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
- container mount policy
- repository root visibility
- prompt input source
- selected Issue ingestion behavior
```

## Current recommendation

Use this for routine production-oriented implementation:

```text
first-canary-005-offline-context-json-writeback
```

Use this for agent-style implementation experiments with selected task packet evidence:

```text
first-canary-008-selected-prompt-task-packet
```

Design 009 as a fixed-Issue ingestion canary before attempting automatic vote-winner selection.
