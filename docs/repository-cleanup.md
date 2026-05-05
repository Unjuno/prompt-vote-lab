# Repository Cleanup Checklist

Use this checklist before the first real implementation-agent canary.

The goal is to reduce accidental rollback, stale-branch PRs, and ambiguous evidence state.

## Current cleanup status

As of the live evidence review PASS and branch cleanup:

```text
open PRs: 0
branches: main only
live evidence review: PASS
fixture evidence dry-run: PASS
weekly no-eligible workflow: PASS
real implementation-agent canary: not yet executed
```

## Branch cleanup

Branch cleanup is complete.

Current intended state:

```text
main
```

Do not reuse old branch names for the first canary.

Create new canary branches only from current `main`.

## Branch policy after cleanup

Do not delete `main`.

Do not create canary PRs from stale local branches.

Do not recreate old verification branch names such as:

```text
p84a
terminal-report-pr-*
weekly-auto-summary-*
weekly-mock-summary-*
mock-lab-week-*
verify-*
```

If an old local branch still exists on a machine, delete it locally or reset it before use.

Recommended local cleanup:

```bash
git fetch --prune origin
git branch --merged main
```

Delete local stale branches only after confirming they are not the active worktree branch.

## Pre-canary evidence state

Before a paid implementation-agent canary, confirm these files agree:

```text
docs/current-features.md
docs/pre-api-freeze.md
runs/dry-run-001-evidence-review.md
```

Required state:

```text
live evidence dry-run path: verified
human_review: PASS
final_decision: PASS
real implementation-agent canary: not yet executed
```

## Must-not-change files during cleanup

Repository cleanup must not change runtime behavior.

Do not edit these during cleanup-only PRs:

```text
lab/**
.github/workflows/weekly-auto-run.yml
.github/workflows/evidence-pipeline-dry-run.yml
scripts/collect_votes.py
scripts/select_eligible.py
scripts/preflight_implementation_agent.py
formal/Selection.lean
```

If one of these must change, it is not a cleanup PR. Treat it as a separate implementation or verification PR.

## Canary branch rule

For the first real implementation-agent canary:

```text
base: current main
branch: new clean branch only
scope: lab/ only
model: gpt-5-nano
attempts: 1
SDK max_retries: 0
fallback: none
auto-merge: forbidden
```

Recommended branch name:

```text
canary-001
```

## Final pre-canary check

Before running the canary:

```text
[ ] open PRs are 0
[ ] remote branches list contains only main before creating canary-001
[ ] canary-001 is created from current main
[ ] current main has live evidence PASS
[ ] pre-API freeze audit is green
[ ] canary prompt is low-risk and lab-only
[ ] no external publishing is enabled
[ ] no auto-merge is enabled
```
