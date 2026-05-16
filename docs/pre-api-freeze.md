# Pre-API freeze checklist

This document is a historical guardrail record for the earlier API/SDK implementation-agent path.

It is no longer the active release gate for the canonical weekly implementation path.

Current active status:

```text
canonical selected-prompt runner: default-on
runner family: Docker/Codex selected-prompt task-packet runner
legacy API/SDK runner: present, non-canonical
manual review: required
auto-merge: disabled
```

The active release-gate and drift status are maintained in:

```text
docs/canonical-status-drift-check.md
docs/current-codex-implementation-path.md
docs/weekly-automation.md
docs/operator-runbook.md
```

## Historical purpose

This checklist originally prevented a failure mode where the workflow starts using a paid model API, fails, is patched repeatedly, and burns cost while the real defect remains unclear.

That concern is still valid for any legacy API/SDK runner, but it is not the current canonical selected-prompt implementation path.

## Historical freeze rule

Before enabling the old real implementation-agent API calls, the repository required:

```text
no new feature work
no automatic merge
no external publishing
no leaderboard
no automatic trust score
no hidden retry
no fallback model
```

Only verification, documentation, and guardrail fixes were allowed.

## Historical PASS gates

These gates were used before the first API-style canary and before later migration to the canonical Codex runner.

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
| Support Unlock Export live path | PASS, anonymized JSON only | `data/support-unlocks/2026-W19.json` |
| Weekly Auto Run no-eligible workflow | PASS, summary PR only | PR #243 / `runs/week-2026-W19-vote-summary.md` |
| Evidence Pipeline Dry Run with `source=fixture` | PASS, validator and artifact upload | run `25335321720` |
| Evidence Pipeline Dry Run with `source=live` | PASS, artifact review only | `runs/dry-run-001-evidence-review.md` |

## Historical API canary entry condition

The old API canary was allowed only after:

```text
Support Unlock Export live path has produced anonymized support unlock JSON
Weekly Auto Run no-eligible path has produced only a summary PR
Evidence Pipeline Dry Run source=fixture has passed the workflow validator
Evidence Pipeline Dry Run source=live has produced reviewable artifacts
the live artifact review passes docs/evidence-artifact-review.md
```

The no-eligible production path was verified in PR #243:

```text
support unlock file: data/support-unlocks/2026-W19.json
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

The live evidence dry-run path was verified in Actions run `25336303653` and recorded in `runs/dry-run-001-evidence-review.md`:

```text
source: live
week_id: dry-run-001
validator: PASS
artifact: evidence-pipeline-dry-run
artifact files: 7
artifact id: 6790655519
human_review: PASS
final_decision: PASS
```

## Legacy API canary constraints

These constraints describe the old API/SDK path. They must not be cited as the active canonical runner contract.

```text
model: gpt-5.4-nano
one agent attempt
one model
no retry
no fallback
SDK max_retries: 0
API call limit per candidate: 1
legacy max output tokens: 5000
lab/ only
safety-check PASS
static-site-check PASS
manual review before merge
```

The current canonical Codex CLI runner does not enforce this old API-era output-token cap as a runtime limit. Current active policy records:

```text
output_token_cap_enforced: false
```

Do not claim a canonical run is output-token-capped unless a future runner contract proves runtime enforcement.

## Stop conditions still valid for any implementation path

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

## Allowed maintenance

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

## Current conclusion

The pre-API freeze checklist is retained as historical evidence and as a warning for legacy API/SDK paths.

It is not the release gate for the current canonical weekly selected-prompt runner.