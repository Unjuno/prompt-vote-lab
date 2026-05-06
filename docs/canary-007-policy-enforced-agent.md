# Canary 007: policy-enforced agent design

## Status

PASS, candidate phase.

`first-canary-007` has completed one successful full run and produced a merged pull request.

```text
success_record: runs/first-canary-007-policy-enforced-agent-success.md
successful_pr: #142 Run Codex policy-enforced agent canary
merge_commit_sha: 11ccdf4153a67a14970b12f7b8d21db337ff04c8
```

Do not treat this single success as a complete proof of filesystem security. Treat it as evidence that the policy-enforced agent path is feasible and can now be tested for repeated-run stability.

## Goal

`first-canary-007` tests whether Codex can operate as a file-operating agent while the execution environment avoids mounting the full repository into the agent container.

This differs from previous paths:

```text
first-canary-005: safe production-oriented offline JSON writeback
first-canary-006: agent-observed direct edit in an isolated three-file worktree
first-canary-007: agent behavior plus policy-enforced filesystem boundary
```

## Core hypothesis

```text
H:
If Codex runs inside an OS-level isolated environment containing only the allowed lab files,
then Codex can still perform agent-style file operations while unauthorized repository files
are not present in the agent work directory.
```

## Implemented design

The full 007 workflow uses:

```text
workflow: Codex Policy Agent Canary Run
runner: scripts/run_codex_policy_agent_canary.sh
container image: node:20-bookworm
container_work_root: /work
container_runtime_root: /codex-runtime
diagnostics_root: /diagnostics
repo_root_mounted: false
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
final_writable_files: lab/index.html, lab/style.css, lab/app.js
```

The container receives:

```text
/work/lab/index.html
/work/lab/style.css
/work/lab/app.js
```

The container also receives a separate runtime mount:

```text
/codex-runtime
```

The repository root is not mounted into the container.

## Required properties

A valid 007 implementation must provide these properties:

```text
- Codex sees and edits only an isolated work directory.
- The full repository is not mounted into the Codex execution environment.
- Runtime state is separated from the work directory.
- The final copy-back path remains limited to lab/index.html, lab/style.css, and lab/app.js.
- Access checks and diagnostics are uploaded when feasible.
- The run uploads thick diagnostics artifacts.
- Auto-merge remains disabled.
```

## Feasibility result

The feasibility smoke test passed before the full implementation.

Recorded at:

```text
runs/canary-007-policy-feasibility-pass.md
```

Observed feasibility summary:

```text
Docker available: true
container write test: true
isolated mount has lab files: true
unexpected repo paths visible: false
strace available: true
```

## Full run result

The first full 007 run passed.

```text
PR: #142
merge_commit_sha: 11ccdf4153a67a14970b12f7b8d21db337ff04c8
changed_files: lab/index.html
```

Diff summary:

```diff
-      <strong>Canary (6th):</strong> this is the sixth bounded Codex implementation-agent canary.
+      <strong>Canary (7th):</strong> this is the seventh bounded Codex implementation-agent canary.
```

The successful diagnostics indicated:

```text
npm install: PASS
codex login: PASS
codex exec: PASS
container exit code: 0
Codex exit code: 0
policy denied access: empty
```

## Expected 007 artifacts

A full 007 run should upload artifacts such as:

```text
policy-allowed-paths.json
policy-container-mounts.txt
policy-denied-access.txt
container-visible-files-before.txt
container-visible-files-after.txt
container-runtime-files-after.txt
codex-events.jsonl
codex-stderr.txt
codex-last-message.txt
codex-exit-code.txt
policy-agent-diff.patch
policy-agent-diff-name-only.txt
policy-agent-copied-files.txt
failure-summary.json
artifact-manifest.json
```

## Security note

The goal is not to trust the model to obey path rules. The goal is to make the intended repository paths absent from the agent work directory and to keep final copy-back constrained to the allowed lab files.

Prompt rules are instructions. They are not enforcement.

## What this canary proves

The first successful run supports these claims:

```text
- Codex can run inside the policy container.
- Codex can authenticate and execute from a non-repository /work directory when --skip-git-repo-check is specified.
- Codex can edit the prepared lab files under /work.
- The workflow can copy back only allowed files.
- The final repository diff can remain within the allowed lab file set.
```

## What this canary does not yet prove

This canary does not yet prove:

```text
- repeated-run stability
- full tracing of every file-access attempt
- network restriction to only required API endpoints
- formal proof that every possible container path outside the mounted areas is unreachable
- that 007 should immediately replace 005 as the stable production-oriented path
```

## Promotion rule

007 is currently a successful candidate path.

Promotion condition:

```text
Promote 007 from candidate to standard agent path after at least 2 consecutive successful full 007 runs under the same fixed conditions, with matching policy diagnostics.
```

A successful repeated run must show:

```text
- Codex exit code 0
- container exit code 0
- final changed files subset of lab/index.html, lab/style.css, lab/app.js
- repository root not mounted into the container work directory
- container-visible work files limited to the prepared lab files plus expected runtime files
- policy-denied-access empty or explained
- safety-check PASS
- static-site-check PASS
- manual PR review and merge
```

## Current recommendation

Use 005 for routine production-oriented implementation until 007 has at least one repeated success under unchanged fixed conditions.

Use 007 for agent-style implementation experiments that require stronger filesystem-boundary evidence.
