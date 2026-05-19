# Current Codex implementation path

## Status

The canonical production implementation path for Prompt Vote Lab is:

```text
Docker-mounted workdir-only + Codex CLI + selected-prompt task packet
```

More precisely:

```text
runner_family: codex-cli-container-agent
runner: codex-cli-selected-prompt-packet-container
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
sandbox_mode: docker-workdir-plus-readonly-selected-prompt-packet
container_work_root: /work
container_task_root: /task
container_task_mount_mode: read-only
container_runtime_root: /codex-runtime
repo_root_mounted: false
final_writable_files: lab/index.html, lab/style.css, lab/app.js
manual_review: required
```

The Python SDK / Responses API full-file JSON path is not the canonical production implementation path. It may remain as a non-canonical manual diagnostic / historical fallback, but it must not be counted as canonical eligible implementation E2E verification.

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
manual selected-prompt workflow smoke: PASS
weekly selected-prompt canonical canary: PASS
ordinary default-on weekly no-eligible observation: PASS
canonical weekly fixed-on release: approved
```

The result means:

```text
- Codex can generate useful lab changes.
- Earlier GitHub-hosted workspace-write sandboxing was not strong enough.
- Offline-context JSON writeback worked, but it is no longer the production canonical path.
- Docker/Codex selected-prompt task packets can execute without mounting the repository root.
- The weekly selected-prompt path is now fixed to the canonical Docker/Codex task-packet runner for eligible candidates.
```

## Weekly selected-prompt canonical path

Current weekly status:

```text
weekly default status: canonical selected-prompt runner fixed-on
weekly feature flag override: removed
weekly legacy override: removed from Weekly Auto Run
Weekly Auto Run no longer has a legacy API/SDK branch.
```

Eligible selected prompts are routed through:

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

The first ordinary no-eligible weekly observation also passed:

```text
support unlock file: data/support-unlocks/2026-W20.json
vote summary PR: #333
merged run record: runs/week-2026-W20-vote-summary.md
baseline_won: true
eligible_count: 0
implementation-agent attempt: none
```

## Non-canonical legacy script

`scripts/openai_lab_run.py` remains present as a non-canonical manual diagnostic / historical fallback.

It is not part of `Weekly Auto Run`.

It does not satisfy canonical selected-prompt evidence.

Do not merge or report a run as canonical implementation E2E merely because the API/JSON path produced a small valid lab diff.

A weekly run only satisfies canonical selected-prompt verification when the PR/run evidence says:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

## Canonical Docker/Codex flow

```text
1. The workflow checks out the repository.
2. The workflow copies only lab/index.html, lab/style.css, and lab/app.js into a prepared work directory.
3. The workflow creates the selected prompt task packet outside the agent work root.
4. The workflow starts a Docker container.
5. The workflow mounts the prepared work directory into the container as /work:rw.
6. The workflow mounts the task packet as /task:ro.
7. The workflow mounts a separate runtime directory as /codex-runtime:rw.
8. The repository root is not mounted into the container.
9. Codex CLI runs inside the container.
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
- read-only /task packet for selected prompt evidence
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

## Current cleanup state

The obsolete legacy first API canary launch path has been retired:

```text
removed workflow: .github/workflows/first-canary-run.yml
removed helper: scripts/create_first_canary_candidate.py
protected evidence removed: no
generated snapshots touched: no
run records touched: no
```

The legacy script itself remains:

```text
scripts/openai_lab_run.py: present, non-canonical, manual diagnostic / historical fallback
```

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
- Runner: codex-cli-selected-prompt-packet-container
- Canonical selected-prompt runner: true
```

A non-canonical API/JSON run may be recorded, but it must be labeled non-canonical and must not satisfy the canonical production E2E requirement.
