# Prompt Vote Lab docs

This directory contains the stable public explanation layer for Prompt Vote Lab.

The landing page should stay short. Details belong here.

Prompt Vote Lab is a prompt game and experiment. Players compete by writing prompts that other players trust enough to spend a bounded implementation-agent attempt.

## Start here

1. [Experiment model](./experiment-model.md) — game model and boundaries.
2. [How to participate](./how-to-participate.md) — submit, vote, and review.
3. [Usable experiment operations](./usable-experiment-ops.md) — current manual canary and comparison-run operations.
4. [Public results export](./public-results-export.md) — raw public data snapshots for participant analysis.
5. [Public agent run bundle](./public-agent-run-bundle.md) — redacted raw agent-run evidence; summaries are not primary evidence.
6. [Issue lifecycle](./issue-lifecycle.md) — weekly close policy; Issues are closed, not deleted.
7. [Persona routes](./persona-routes.md) — role-specific paths for writers, voters, spectators, supporters, and reviewers.
8. [No-change baseline](./no-change-baseline.md) — the 20-vote baseline.
9. [Weekly automation](./weekly-automation.md) — weekly schedule, support unlock prerequisite, and E2E status.
10. [Automation map](./automation-map.md) — workflow boundaries.
11. [Weekly operations doctrine](./weekly-ops-doctrine.md) — weekly evidence-to-action loop.
12. [Evidence artifact review](./evidence-artifact-review.md) — dry-run artifact checks.
13. [Repository cleanup checklist](./repository-cleanup.md) — stale branch and pre-canary cleanup.
14. [Fixed first canary prompt](./first-canary-prompt.md) — the only allowed first real canary prompt.
15. [First canary readiness checklist](./first-canary-readiness.md) — final check before running the first real canary.
16. [Codex path comparison](./codex-path-005-vs-007.md) — prompt selection layer versus 005/007/008/009 execution paths.
17. [Canary 008 task packet design](./canary-008-selected-prompt-task-packet.md) — selected prompt packet, `/task:ro`, and credential hygiene design.
18. [Canary 009 selected Issue instruction design](./canary-009-selected-issue-instructions.md) — fixed GitHub Issue ingestion into a bounded instruction packet.
19. [Support policy](./support-policy.md) — support boundaries and comparison-run thresholds.
20. [Report policy](./report-policy.md) — weekly report draft policy.
21. [Pre-API freeze checklist](./pre-api-freeze.md) — gates before paid agent runs.

## Current reputation status

Reputation is currently social memory, not an automated score.

The repository records outcomes. Workflows do not yet compute player rankings, trust scores, author scores, or penalties.

## Report status

Report generation is currently model-free.

The workflow can draft `runs/<week>-report.md` from explicit inputs and repository files, then open a reviewable PR.

It does not publish externally and does not compute automated trust ratings.

## Public results status

Public results export is raw data, not analysis.

Participants can inspect:

```text
data/public-results.json
data/public-results.md
```

The export is intended for participant-side analysis of prompt outcomes, votes, labels, PRs, workflow runs, and run records.

## Public agent-run evidence status

Fixed-Issue 009 runs also upload a redacted raw agent-run evidence bundle.

The primary evidence is the allowlisted raw files in the bundle. The bundle index is a manifest only. It must not replace raw evidence with a model-written summary.

## Issue lifecycle status

Weekly Issues may be closed automatically after the experiment cycle is recorded.

Closure requires:

```text
week:* label
outcome:* label
public results membership
finalizer comment before close
```

Closed Issues remain visible. They are not deleted.

## Current usable experiment status

The repository has scheduled weekly automation and support-unlock gates implemented, but live production verification is still pending.

Manual canary and comparison operations remain available:

```text
Issue safety scan
→ optional manual rescan
→ fixed-Issue 009 runtime scan
→ execution gate
→ Codex implementation PR
→ manual review/merge
→ runs/ record
```

Scheduled weekly automation is documented in [Weekly automation](./weekly-automation.md). It still requires live `SPONSORS_GRAPHQL_TOKEN` verification and Weekly Auto Run E2E verification before it should be called fully production-verified.

## Pre-API freeze status

Paid implementation-agent runs are not considered ready for broad weekly automation until the pre-API freeze checklist is green.

The project should prefer extra offline verification over debugging after paid API calls begin.

## Rule documents

Operational rules live in [`../rules/`](../rules/).

Important rules:

- [`static-ui-v1.0.md`](../rules/static-ui-v1.0.md) — lab edit scope and runtime restrictions.
- [`agent-run-policy-v1.0.md`](../rules/agent-run-policy-v1.0.md) — one bounded agent attempt, explicit continuation, no hidden retries.
- [`model-policy-v1.1.md`](../rules/model-policy-v1.1.md) — current canary implementation model policy.
- [`report-generation-v1.0.md`](../rules/report-generation-v1.0.md) — model-free weekly report draft boundaries.
- [`event-logging-v1.0.md`](../rules/event-logging-v1.0.md) — JSONL and Markdown logging policy.
- [`support-unlocked-runs-v1.1.md`](../rules/support-unlocked-runs-v1.1.md) — $5/$10 comparison-run thresholds.
- [`mock-testing-v1.0.md`](../rules/mock-testing-v1.0.md) — agent-free mock testing.
- [`exception-testing-v1.0.md`](../rules/exception-testing-v1.0.md) — failure-path tests.
- [`multi-fuzz-testing-v1.0.md`](../rules/multi-fuzz-testing-v1.0.md) — weighted random boundary testing.

Compatibility note:

- [`model-policy-v1.0.md`](../rules/model-policy-v1.0.md) is preserved as historical model-policy evidence.
- [`single-shot-api-v1.0.md`](../rules/single-shot-api-v1.0.md) remains as a low-level compatibility rule for workflows backed by a paid model API.
- Public explanations should prefer "agent run" over "API call".

## Public page policy

The root landing page links to GitHub-rendered Markdown pages rather than directly to `.md` files on GitHub Pages.

Reason:

```text
GitHub Pages may display Markdown files as raw text.
GitHub rendered views show the documents as readable Markdown.
```

## Stable distinction

```text
/      = stable explanation layer
/lab/  = changing implementation target
/data/ = raw public results snapshots
/docs/ = rendered project explanation
/rules/ = operational constraints
/runs/ = recorded run history
```

Do not collapse these layers unless a future policy deliberately changes the game model.
