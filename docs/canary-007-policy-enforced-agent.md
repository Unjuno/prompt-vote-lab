# Canary 007: policy-enforced agent design

## Status

Design and feasibility phase.

Do not implement the full canary until the runner environment can support the required isolation and observation primitives.

## Goal

`first-canary-007` should test whether Codex can operate as a file-operating agent while the execution environment prevents access to unauthorized repository files.

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
are not readable or writable from the agent process.
```

## Required properties

A valid 007 implementation must provide these properties:

```text
- Codex sees and edits only an isolated work directory.
- The full repository is not mounted into the Codex execution environment.
- The final copy-back path remains limited to lab/index.html, lab/style.css, and lab/app.js.
- Access attempts and denials are logged when feasible.
- The run uploads thick diagnostics artifacts.
- Auto-merge remains disabled.
```

## Candidate enforcement mechanisms

### Docker isolation

Preferred first feasibility target.

The container should mount only a prepared work directory, for example:

```text
/work/lab/index.html
/work/lab/style.css
/work/lab/app.js
```

The repository root should not be mounted.

### File-access tracing

Useful for observation. It is not sufficient as enforcement by itself.

Potential mechanism:

```text
strace -f -e trace=file
```

The trace should be treated as an analysis artifact, not as a security boundary.

### Final output guard

Still required even if Docker isolation works.

```text
changed_files subset of:
  lab/index.html
  lab/style.css
  lab/app.js
```

## Feasibility smoke test

Before implementing the full 007 canary, add a manual workflow that checks whether GitHub-hosted runners support the required primitives.

Minimum smoke checks:

```text
- docker version works
- docker run works
- a mounted isolated work directory is visible inside the container
- repository root is not mounted inside the container
- strace is available on the host or can be installed in a temporary step
- file access trace can be written as an artifact
```

## PASS conditions for feasibility

```text
PASS:
- Docker can run a container on ubuntu-latest.
- The container can read a mounted allowed work directory.
- The container cannot read repository files that were not mounted.
- A file-access trace or equivalent observation artifact can be produced.
```

## FAIL conditions for feasibility

```text
FAIL:
- Docker is unavailable.
- Container run fails.
- The test unintentionally exposes the repository root to the container.
- No useful access trace or denial evidence can be collected.
```

## UNCERTAIN conditions

```text
UNCERTAIN:
- Docker works but strace is unavailable.
- Isolation works but action tracing is too noisy or incomplete.
- Codex CLI dependencies cannot be represented in the isolated environment.
```

## Expected 007 artifacts

A full 007 run should upload at least:

```text
policy-allowed-paths.json
policy-container-mounts.txt
policy-denied-access.txt
file-access-trace.txt
agent-wrapper-timeline.jsonl
codex-events.jsonl
codex-stdout.txt
codex-stderr.txt
codex-last-message.txt
codex-exit-code.txt
worktree-hashes-before.json
worktree-hashes-after.json
worktree-diff.patch
worktree-diff-stat.txt
copied-back-files.txt
failure-summary.json
artifact-manifest.json
```

## Security note

The goal is not to trust the model to obey path rules. The goal is to make unauthorized paths unavailable or denied by the execution environment.

Prompt rules are instructions. They are not enforcement.

## Current recommendation

Proceed in this order:

```text
1. Add a feasibility smoke workflow.
2. Run it manually on GitHub-hosted ubuntu-latest.
3. Record the result in runs/.
4. Implement full first-canary-007 only if feasibility is PASS or sufficiently understood.
```
