# Automation map

This document maps Prompt Vote Lab automation boundaries.

## Core boundary

```text
/       = stable public explanation page
/lab/   = changing implementation target
/docs/  = human-readable explanation
/rules/ = operational constraints
/runs/  = recorded run history
```

The implementation model may edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

It may create ordinary helper functions inside `lab/app.js`.

It must not create external dependencies, hidden network behavior, backend logic, login, payment, tracking, or merge decisions.

## Automated

The project may automate:

- label setup
- prompt proposal vote collection
- no-change baseline insertion
- eligible rank selection
- API-free mock implementation runs
- exception matrix tests
- multi-fuzz boundary tests
- internal safety and static-site checks before implementation PR creation
- implementation PR creation
- vote snapshot artifact creation
- weekly run-log draft creation
- weekly metrics summary artifact creation
- weekly public briefing draft artifact creation
- event log artifact creation
- HN/blog/report draft artifact creation
- anonymized support unlock export
- support unlock file validation before export commit

## Not automated

The project must not automate:

- merge into `main`
- weakening safety rules to accept a failed implementation
- bypassing the no-change baseline
- buying merge rights through support
- submitting posts to external communities
- automatic retry after a failed paid model call
- automatic fallback to a stronger or more expensive model

## Main workflows

| Workflow | Status | Schedule | Purpose | API cost |
|---|---|---|---|---:|
| `setup-labels.yml` | implemented | manual | Create project labels | 0 |
| `safety-check.yml` | implemented | PR/path-triggered | Check lab PRs when PR-triggered checks run | 0 |
| `static-site-check.yml` | implemented | PR/path-triggered | Check public page structure, support wording, and lab smoke expectations | 0 |
| `lab-pr-scope-check.yml` | implemented | PR/path-triggered | Prevent lab implementation PRs from mixing lab and non-lab files | 0 |
| `script-check.yml` | implemented | PR/path-triggered + manual | Check scripts, offline workflow smoke tests, and workflow contracts | 0 |
| `support-unlock-export.yml` | implemented, live-token verification pending | daily 00:17 UTC / 09:17 JST + manual | Export anonymized support unlock aggregates and validate them before commit | 0 |
| `weekly-auto-run.yml` | implemented, not fully production-verified | Monday 00:23 UTC / 09:23 JST + manual | Collect votes and create implementation PRs for eligible prompts | paid only if eligible |
| `evidence-pipeline-dry-run.yml` | implemented | manual | Manually generate snapshot, run log, weekly summary, public briefing, and HN draft as artifact | 0 |
| `exception-matrix-test.yml` | implemented | PR/manual | Test known pass/fail boundary cases | 0 |
| `multi-fuzz-test.yml` | implemented | PR/manual | Run weighted random boundary mutations | 0 |
| `weekly-mock-run.yml` | implemented | manual | Test weekly selection and PR creation without model API calls | 0 |
| `blog-report.yml` | implemented, not fully production-verified | manual | Generate report PRs from recorded run data | paid when manually confirmed |
| `terminal-state-report.yml` | implemented | PR/label-triggered | Record final PR state from labels | 0 |

## Scheduled weekly path

The scheduled production path is split into two workflows:

```text
Support Unlock Export
→ data/support-unlocks/<week-id>.json
→ Weekly Auto Run
→ vote summary PR
→ implementation PRs, if eligible
→ manual review/merge
```

`Support Unlock Export` runs daily and writes only anonymized aggregate data. It validates public support unlock JSON before committing.

`Weekly Auto Run` runs every Monday. It requires the matching support unlock file for `RUN_WEEK` before collecting votes. Missing support data is a hard failure, not 0 USD.

See [`weekly-automation.md`](weekly-automation.md).

## Important GitHub Actions caveat

PRs created by `GITHUB_TOKEN` may not trigger follow-up workflow runs because GitHub suppresses most recursive workflow events created by the token.

Therefore, implementation workflows should run internal checks before opening PRs.

Current expected internal checks before implementation PR creation:

```text
bash scripts/safety-check.sh origin/main HEAD
bash scripts/static-site-check.sh
```

For lab implementation PR review, a separate PR-triggered guard also checks:

```text
bash scripts/check-lab-pr-scope.sh
```

## Evidence dry-run flow

`evidence-pipeline-dry-run.yml` is manual and API-free except for GitHub issue/reaction reads when `source=live`.

It generates artifacts under:

```text
tmp/evidence/
```

Expected artifact paths:

```text
tmp/evidence/data/snapshots/week-<week_id>.json
tmp/evidence/logs/aggregation/week-<week_id>.jsonl
tmp/evidence/runs/week-<week_id>.md
tmp/evidence/reports/summary/weekly-metrics.json
tmp/evidence/reports/summary/weekly-metrics.md
tmp/evidence/reports/briefings/week-<week_id>.md
tmp/evidence/reports/hn/week-<week_id>.md
```

The dry-run workflow must not commit generated evidence files.

## Data flow

```text
GitHub Issues
→ GitHub reactions
→ vote collection
→ no-change baseline comparison
→ weekly snapshot
→ weekly run-log draft
→ weekly metrics summary
→ public weekly briefing draft
→ HN/report draft
→ artifact review
→ implementation attempt, if eligible and explicitly run
→ internal safety/static checks
→ implementation PR
→ maintainer review
→ terminal state label
→ run/report record
```

## Public briefing data

Weekly public briefing generation may summarize:

- observed vote and candidate metrics
- interpretation of the current week
- selected/no-run decision
- next participant action
- links for submit and vote actions

The briefing is a draft artifact. It must not auto-post externally. It must not store voter login lists.

## Metrics summary data

Weekly summary generation may aggregate:

- candidate count trend
- unique author count trend
- total vote trend
- unique voter trend when available
- top prompt vote-share trend
- selected/no-run counts

The summary must use aggregate metrics only. It must not store voter login lists.

## Paid API policy

Paid implementation runs are single-shot:

```text
model call per candidate: 1
SDK max_retries: 0
automatic fallback: no
automatic retry: no
automatic merge: no
```

Failure is recorded as experiment data. It is not hidden by rerunning the model.
