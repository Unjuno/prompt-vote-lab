# Pre-API freeze checklist

Prompt Vote Lab must not start paid implementation-agent runs until this checklist is green.

The goal is to prevent a failure mode where the workflow starts using a paid model API, fails, is patched repeatedly, and burns cost while the real defect remains unclear.

## Freeze rule

Before enabling real implementation-agent API calls:

```text
no new feature work
no automatic merge
no external publishing
no leaderboard
no automatic trust score
no hidden retry
no fallback model
```

Only verification, documentation, and guardrail fixes are allowed.

## Required PASS gates

All of these must pass before the first real canary run.

| Gate | Required result | Current evidence |
|---|---|---|
| Static Site Check | PASS | CI |
| Safety Check | PASS | CI |
| Exception Matrix Test | PASS | CI |
| Multi-Fuzz Test | PASS | CI |
| Collect Votes Test | PASS | CI |
| Select Eligible Test | PASS | CI |
| Weekly Auto no-eligible selector test | PASS | CI |
| Implementation Preflight Test | PASS | CI |
| Lean Proof Test | PASS | CI |
| Weekly Report Draft workflow | PASS, report PR only | completed before canary |
| Weekly Mock Run workflow | PASS, summary PR + mock implementation PR only | completed before canary |
| Weekly Auto Run no-eligible workflow | PASS, summary PR only | PR #81 |
| Evidence Pipeline Dry Run with `source=fixture` | PASS, validator and artifact upload | run `25335321720` |
| Evidence Pipeline Dry Run with `source=live` | PASS, artifact review only | not yet verified |

## Real API canary entry condition

A real implementation-agent canary is allowed only after:

```text
Weekly Auto Run no-eligible path has produced only a summary PR
Evidence Pipeline Dry Run source=fixture has passed the workflow validator
Evidence Pipeline Dry Run source=live has produced reviewable artifacts
the live artifact review passes docs/evidence-artifact-review.md
```

The no-eligible production path was verified in PR #81:

```text
changed file: runs/week-2026-W19-vote-summary.md
baseline_won: true
eligible_count: 0
eligible_ranks: []
implementation PR created: no
```

The fixture evidence dry-run path was verified in Actions run `25335321720`:

```text
source: fixture
week_id: dry-run-001
validator: PASS
artifact: evidence-pipeline-dry-run
artifact files: 7
artifact id: 6790257600
```

## Canary constraints

The first real API canary must use one low-risk prompt only.

Allowed canary shape:

```text
Add a small visible canary panel to lab/ explaining that this is the first bounded implementation-agent test.
```

Required canary run constraints:

```text
model: gpt-5-nano
one agent attempt
one model
no retry
no fallback
SDK max_retries: 0
API call limit per candidate: 1
max output tokens: 12000
lab/ only
safety-check PASS
static-site-check PASS
manual review before merge
```

## Stop conditions

Stop immediately if any of these happen:

```text
more than one implementation-agent attempt for one candidate
model fallback occurs
SDK retry is enabled
API dependency is installed in a no-eligible run
implementation PR appears during no-eligible run
files outside lab/ are changed by implementation run
safety/static check fails after model output
workflow attempts to auto-merge
```

## Allowed maintenance during freeze

Allowed:

```text
add tests
add formal proof
tighten static checks
tighten preflight checks
clarify docs
close verification PRs
```

Forbidden:

```text
change product behavior
add scoring
add external integrations
add publishing
add auto-merge
relax cost or retry guards
```

## Completion statement

The pre-API freeze is complete only when the repository has proof or CI evidence for every required gate above.

Until then, real implementation-agent API calls remain disabled by policy.
