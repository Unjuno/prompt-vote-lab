# Repository Cleanup Checklist

Use this checklist before the first real implementation-agent canary.

The goal is to reduce accidental rollback, stale-branch PRs, and ambiguous evidence state.

## Current cleanup status

As of the live evidence review PASS:

```text
open PRs: 0
live evidence review: PASS
fixture evidence dry-run: PASS
weekly no-eligible workflow: PASS
real implementation-agent canary: not yet executed
```

## Branch cleanup

Many old working branches remain after squash merges and verification loops.

These branches should not be used as canary bases.

Create new canary branches only from current `main`.

### Safe-to-delete branch classes

Delete only after confirming there is no open PR and the work is already merged or obsolete:

```text
p84a
p85a
p86a
p87a
p88a
p89a
p90a
p91a
terminal-report-pr-*
report-draft-week-report-test-*
ci-trigger-exception-multifuzz-001
verify-exception-fuzz-001
verify-implementation-preflight-001
verify-pre-api-freeze-audit-001
verify-report-draft-001
verify-report-draft-002
script-check-workflow
test-lab-pr-scope-guard
upload-dry-run-artifacts
```

Do not delete `main`.

Do not delete a branch with an open PR.

Do not create a canary PR from any branch listed above.

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

## Manual branch deletion commands

Use GitHub UI or local git.

Example local commands:

```bash
git fetch --prune origin
git push origin --delete <branch-name>
```

Delete in small batches. After each batch, check open PRs again.

## Final pre-canary check

Before running the canary:

```text
[ ] no open PRs
[ ] no stale canary candidate branch
[ ] current main has live evidence PASS
[ ] pre-API freeze audit is green
[ ] canary prompt is low-risk and lab-only
[ ] no external publishing is enabled
[ ] no auto-merge is enabled
```
