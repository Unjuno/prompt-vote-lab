# first-canary-007 policy-enforced agent success

## Status

PASS.

## Fixed conditions

```text
canary_id: first-canary-007
runner: codex-cli-policy-enforced-agent-container
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
sandbox_mode: docker-mounted-workdir-only
execution_mode: policy-enforced agent direct edit
container_work_root: /work
container_runtime_root: /codex-runtime
repo_root_mounted: false
visible_files: lab/index.html, lab/style.css, lab/app.js
final_writable_files: lab/index.html, lab/style.css, lab/app.js
manual_review: required
```

## Purpose

This canary tests whether Codex can operate as a file-editing agent while the container receives only the prepared lab work directory rather than the repository root.

## Observed result

The workflow completed, created a pull request, passed checks, and the pull request was merged.

```text
PR: #142 Run Codex policy-enforced agent canary
merge_commit_sha: 11ccdf4153a67a14970b12f7b8d21db337ff04c8
changed_files: lab/index.html
```

Diff summary:

```diff
-      <strong>Canary (6th):</strong> this is the sixth bounded Codex implementation-agent canary.
+      <strong>Canary (7th):</strong> this is the seventh bounded Codex implementation-agent canary.
```

## Diagnostics summary

The successful run diagnostics indicated:

```text
npm install: PASS
codex login: PASS
codex exec: PASS
container exit code: 0
Codex exit code: 0
Codex CLI version: codex-cli 0.128.0
container user: uid=1001 gid=1001
policy denied access: empty
```

Container-visible work files were limited to:

```text
/work/lab/app.js
/work/lab/index.html
/work/lab/style.css
```

Codex reported inspecting the three visible files and changing only `lab/index.html`.

## Checks passed

```text
policy-enforced container runner completed
changed-file guard passed
safety-check passed
static-site-check passed
manual PR review and merge completed
```

## Interpretation

This is the first successful canary in this repository showing Codex operating as a file-editing agent inside a Docker container where the repository root is not mounted into the agent work directory.

The run supports these claims:

```text
- Codex can run inside the policy container.
- Codex can authenticate and execute from a non-repository /work directory when --skip-git-repo-check is specified.
- Codex can edit the prepared lab files under /work.
- The workflow can copy back only allowed files.
- The final repository diff can remain within the allowed lab file set.
```

## Not proven

This single run does not prove:

```text
- full path-access coverage for every container path
- network narrowing to only required endpoints
- complete file-access tracing
- repeated-run stability
- immediate replacement of first-canary-005 as the default production-oriented path
```

## Current classification

```text
first-canary-005: current stable production-oriented writeback path
first-canary-006: agent-observed direct-edit path
first-canary-007: successful policy-enforced agent candidate path
```

007 should become the stronger default candidate only after repeated successful runs under the same fixed conditions.

## Recommended next step

Run the same 007 workflow again without changing model, retry, fallback, file scope, or policy mounts.

Suggested promotion condition:

```text
Promote 007 from candidate to standard agent path after at least 2 consecutive successful full 007 runs with matching policy diagnostics.
```
