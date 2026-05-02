# Automation map

This document maps Prompt Vote Lab automation boundaries.

## Core boundary

```text
/      = stable public explanation page
/lab/  = changing implementation target
/docs/ = human-readable explanation
/rules/ = operational constraints
/runs/ = recorded run history
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
- vote summary PR creation
- event log artifact creation
- blog/report draft PR creation

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

| Workflow | Status | Purpose | API cost |
|---|---|---|---:|
| `setup-labels.yml` | implemented | Create project labels | 0 |
| `safety-check.yml` | implemented | Check lab PRs when PR-triggered checks run | 0 |
| `static-site-check.yml` | implemented | Check public page structure and support wording | 0 |
| `exception-matrix-test.yml` | implemented | Test known pass/fail boundary cases | 0 |
| `multi-fuzz-test.yml` | implemented | Run weighted random boundary mutations | 0 |
| `weekly-mock-run.yml` | implemented | Test weekly selection and PR creation without model API calls | 0 |
| `weekly-auto-run.yml` | implemented, not fully production-verified | Collect votes and create implementation PRs for eligible prompts | paid only if eligible |
| `blog-report.yml` | implemented, not fully production-verified | Generate report PRs from recorded run data | paid when manually confirmed |
| `terminal-state-report.yml` | implemented | Record final PR state from labels | 0 |

## Important GitHub Actions caveat

PRs created by `GITHUB_TOKEN` may not trigger follow-up workflow runs because GitHub suppresses most recursive workflow events created by the token.

Therefore, implementation workflows should run internal checks before opening PRs.

Current expected internal checks before implementation PR creation:

```text
bash scripts/safety-check.sh origin/main HEAD
bash scripts/static-site-check.sh
```

## Data flow

```text
GitHub Issues
→ GitHub reactions
→ vote collection
→ no-change baseline comparison
→ eligible candidate list
→ implementation attempt, if eligible
→ internal safety/static checks
→ implementation PR
→ maintainer review
→ terminal state label
→ run/report record
```

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
