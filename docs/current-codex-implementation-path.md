# Current Codex implementation path

## Status

The canonical production implementation path for Prompt Vote Lab is now:

```text
Docker-mounted workdir-only + Codex CLI
```

More precisely, the canonical implementation-agent boundary is:

```text
runner_family: codex-cli-container-agent
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
sandbox_mode: docker-mounted-workdir-only
container_work_root: /work
container_runtime_root: /codex-runtime
repo_root_mounted: false
final_writable_files: lab/index.html, lab/style.css, lab/app.js
manual_review: required
```

The Python SDK / Responses API full-file JSON path is not the canonical production implementation path. It may remain as a legacy or non-canonical rollback/debug path, but it must not be counted as canonical eligible implementation E2E verification.

## Current evidence summary

The canary series produced the following evidence:

```text
first-canary-001: full repository + workspace-write -> FAIL
first-canary-002: isolated three-file worktree + workspace-write -> FAIL
first-canary-003: isolated three-file worktree + danger-full-access -> PASS
first-canary-004: read-only repository context + unified diff writeback -> FAIL
first-canary-005: offline context + JSON full-file replacement -> PASS, now non-canonical
first-canary-006: isolated three-file agent-observed direct edit -> PASS
first-canary-007: Docker-mounted workdir-only policy agent -> PASS
first-canary-008: Docker workdir + read-only selected prompt task packet -> PASS
first-canary-009: fixed GitHub Issue instruction packet -> PASS
first-canary-009 hostile Issue boundary: Issue #164 -> PR #165 -> PASS
first-canary-009 sanitizer static penetration test: PR #166 -> PASS
manual selected-prompt workflow smoke: run artifact diagnostics -> PASS
weekly selected-prompt canonical canary: run 25858202166 -> PASS
canonical weekly default-on release: approved
```

The result means:

```text
- Codex can generate useful lab changes.
- GitHub-hosted runner workspace-write sandboxing failed through the local bwrap path.
- Relaxed direct editing can work, but it is not the safest default.
- Repo-context writeback still allowed Codex to attempt an internal patch/write path.
- Offline-context JSON writeback works as mediated output, but it is no longer the production canonical path.
- Policy-enforced container execution can run Codex as an agent without mounting the repository root.
- Selected prompt task packets can be mounted read-only at /task while Codex edits /work/lab only.
- Fixed GitHub Issue text can be fetched and normalized into an instruction packet.
- Hostile Issue text can be preserved as raw evidence while the executable objective is narrowed to a safe_user_task.
- The weekly selected-prompt path uses the canonical Docker/Codex task-packet runner by default for eligible candidates.
```

## Canonical production path

Use a Docker-contained Codex CLI runner for production-oriented implementation-agent verification and eligible implementation runs.

The minimal canonical form is the 007-style policy-enforced container boundary:

```text
runner: codex-cli-policy-enforced-agent-container
sandbox_mode: docker-mounted-workdir-only
execution_mode: containerized Codex direct edit of prepared lab files
container_work_root: /work
container_runtime_root: /codex-runtime
repo_root_mounted: false
final_writable_files: lab/index.html, lab/style.css, lab/app.js
manual_review: required
```

For real selected prompt execution, prefer the stronger task-packet form:

```text
runner: codex-cli-selected-prompt-task-packet-container
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

For fixed or selected GitHub Issue ingestion, use the issue-instruction packet form:

```text
runner: codex-cli-fixed-issue-instruction-packet-container
sandbox_mode: docker-workdir-plus-readonly-issue-instruction-packet
execution_mode: GitHub Issue instruction packet agent direct edit
container_work_root: /work
container_task_root: /task
container_task_mount_mode: read-only
container_runtime_root: /codex-runtime
repo_root_mounted: false
final_writable_files: lab/index.html, lab/style.css, lab/app.js
manual_review: required
```

The production direction is therefore Docker + Codex CLI, not Python SDK JSON replacement.

## Weekly selected-prompt canonical path

The weekly eligible implementation path now defaults to the canonical selected-prompt runner:

```text
DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true
```

The optional override remains available only for emergency rollback or controlled diagnosis:

```text
PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false
```

When the override is unset or explicitly `true`, `Weekly Auto Run` routes eligible selected prompts through:

```text
scripts/run_codex_selected_prompt.sh
runner: codex-cli-selected-prompt-packet-container
sandbox_mode: docker-workdir-plus-readonly-selected-prompt-packet
prompt_transport: --prompt-file
repo_root_mounted: false
final_writable_files: lab/index.html, lab/style.css, lab/app.js
auto_merge_policy: disabled
manual_review: required
```

The weekly canonical canary passed in workflow run `25858202166`:

```text
summary_pr: #283
implementation_pr: #284
selected_issue: #282
runner: codex-cli-selected-prompt-packet-container
artifacts:
  - weekly-selected-prompt-diagnostics-7
  - weekly-selected-prompt-public-bundles-7
  - weekly-selected-prompt-uploaded-bundle-verification-7
result: PASS
```

The canary PRs were closed without merge because they were evidence-only canary artifacts, not product changes.

## Non-canonical legacy path

`first-canary-005` proved that offline context + JSON full-file replacement can work:

```text
runner: codex-cli-offline-json-writeback
sandbox_mode: read-only-empty-context
writeback_mode: validated JSON full-file replacement
```

This path is useful as historical evidence and possible emergency fallback, but it is not the canonical production implementation path.

Do not merge or report a run as canonical implementation E2E merely because the API/JSON path produced a small valid lab diff.

`weekly-auto-run.yml` still contains a non-canonical branch that can call the legacy `scripts/openai_lab_run.py` path when `PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER` is explicitly set to `false`. That override is preserved only for emergency rollback or controlled diagnosis, and it is non-canonical.

The legacy weekly fallback also has a downstream script gate. For ordinary `week-*` runs, `scripts/openai_lab_run.py` refuses to proceed unless this explicit environment override is present:

```text
PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true
```

That downstream gate prevents accidental API/SDK execution if the weekly canonical feature flag is misconfigured. It does not make the API/SDK path canonical.

A weekly run only satisfies canonical selected-prompt verification when the PR/run evidence says:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

## Canonical Docker/Codex flow

```text
1. The workflow checks out the repository.
2. The workflow copies only lab/index.html, lab/style.css, and lab/app.js into a prepared work directory.
3. The workflow creates any selected prompt or Issue instruction packet outside the agent work root.
4. The workflow starts a Docker container.
5. The workflow mounts the prepared work directory into the container as /work:rw.
6. If a task packet is used, the workflow mounts it as /task:ro.
7. The workflow mounts a separate runtime directory as /codex-runtime:rw.
8. The repository root is not mounted into the container.
9. Codex CLI logs in and runs inside the container.
10. Codex edits only the prepared lab files under /work.
11. The workflow copies back only lab/index.html, lab/style.css, and lab/app.js.
12. The workflow runs changed-file guard, safety-check, and static-site-check.
13. The workflow creates a pull request.
14. A human reviews and merges manually.
```

## Allowed final write scope

Only these files may be changed by the canonical implementation paths:

```text
lab/index.html
lab/style.css
lab/app.js
```

No other file path is a valid final output path.

## Safety boundary

The canonical safety boundary is not the model prompt alone. It is the combination of:

```text
- Docker workdir-only execution
- repository root not mounted into the agent container
- prepared /work directory containing only allowed lab files
- optional read-only /task packet for selected prompt or Issue instruction evidence
- separate /codex-runtime mount for Codex state, npm cache, temporary files, and diagnostics
- final copy-back limited to the three lab files
- changed-file guard
- safety-check
- static-site-check
- diagnostics artifact upload
- manual review
```

For Issue-derived tasks, the boundary also includes:

```text
- GitHub Issue body preserved as raw evidence, not policy
- issue-safety-analysis.json recording detected unsafe categories
- safe_user_task separated from raw Issue text
- execution-policy.md ranking issue-safety-analysis.json above instruction-brief.md and raw-issue-body.md
- runner prompt instructing Codex to follow policy and safety analysis over raw Issue text
```

Prompt instructions are still used, but they are not treated as enforcement.

## Current migration state

The weekly eligible implementation workflow now uses the canonical selected-prompt path by default. The legacy `openai_lab_run.py` path remains available only as a non-canonical fallback through an explicit rollback override plus the downstream legacy runner gate.

The next implementation work should verify the first ordinary scheduled default-on run, then decide whether and when to remove the legacy fallback through a separate removal gate.

## Required verification for canonical E2E

A canonical successful run must show:

```text
- Docker container started
- Codex CLI executed inside the container
- repository root not mounted into the container work directory
- final changed files subset of lab/index.html, lab/style.css, lab/app.js
- Codex exit code 0
- container exit code 0
- safety-check PASS
- static-site-check PASS
- PR created
- auto-merge disabled
- manual review required
```

A non-canonical API/JSON run may be recorded, but it must be labeled non-canonical and must not satisfy the canonical production E2E requirement.