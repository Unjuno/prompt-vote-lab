# Prompt Vote Lab docs

This directory contains the stable public explanation layer for Prompt Vote Lab.

The landing page should stay short. Details belong here.

This README is a navigation entry point, not a release-gate source of truth.

Prompt Vote Lab is a prompt game and experiment. Players compete by writing prompts that other players trust enough to spend a bounded implementation-agent attempt.

## Start here

1. [Participant guide](./for-participants.md) — start by voting with 👍, then submit prompts when ready.
2. [Experiment model](./experiment-model.md) — game model and boundaries.
3. [How to participate](./how-to-participate.md) — submit, vote, and review.
4. [Canonical runner evidence guide](./canonical-runner-evidence-guide.md) — how to verify Docker/Codex selected-prompt evidence.
5. [Canonical status drift check](./canonical-status-drift-check.md) — canonical, legacy, default-on, auto-merge, and release-gate status contract.
6. [Release readiness review](./release-readiness-review.md) — security posture, participant journey, live preview, and release decision review.
7. [Root folder audit](./root-folder-audit.md) — top-level folder roles, cleanup posture, and maintainer questions before cleanup.
8. [Repository 5S and language policy](./repository-5s-and-language-policy.md) — cleanup, English-only, and sustain rules.
9. [Repository cleanup inventory](./repository-cleanup-inventory.md) — protected evidence, canonical surfaces, legacy fallbacks, generated snapshots, and cleanup candidates.
10. [Workflow family map](./workflow-family-map.md) — canonical, weekly, generated, safety, canary, legacy, and test workflow classification.
11. [Usable experiment operations](./usable-experiment-ops.md) — current manual canary and comparison-run operations.
12. [Operator runbook](./operator-runbook.md) — maintainer checklist for weekly operation, failures, merge decisions, tokens, and cleanup boundaries.
13. [Public results export](./public-results-export.md) — raw public data snapshots for participant analysis.
14. [Public agent run bundle](./public-agent-run-bundle.md) — redacted raw agent-run evidence; summaries are not primary evidence.
15. [Issue lifecycle](./issue-lifecycle.md) — weekly close policy; Issues are closed, not deleted.
16. [Persona routes](./persona-routes.md) — role-specific paths for writers, voters, spectators, supporters, and reviewers.
17. [No-change baseline](./no-change-baseline.md) — the 20-vote baseline.
18. [Weekly automation](./weekly-automation.md) — weekly schedule, support unlock prerequisite, and E2E status.
19. [Automation map](./automation-map.md) — workflow boundaries.
20. [Weekly operations doctrine](./weekly-ops-doctrine.md) — weekly evidence-to-action loop.
21. [Evidence artifact review](./evidence-artifact-review.md) — dry-run artifact checks.
22. [Repository cleanup checklist](./repository-cleanup.md) — stale branch and pre-canary cleanup.
23. [Fixed first canary prompt](./first-canary-prompt.md) — the only allowed first real canary prompt.
24. [First canary readiness checklist](./first-canary-readiness.md) — final check before running the first real canary.
25. [Codex path comparison](./codex-path-005-vs-007.md) — prompt selection layer versus 005/007/008/009 execution paths.
26. [Canary 008 task packet design](./canary-008-selected-prompt-task-packet.md) — selected prompt packet, `/task:ro`, and credential hygiene design.
27. [Canary 009 selected Issue instruction design](./canary-009-selected-issue-instructions.md) — fixed GitHub Issue ingestion into a bounded instruction packet.
28. [Support policy](./support-policy.md) — support boundaries and comparison-run thresholds.
29. [Report policy](./report-policy.md) — weekly report draft policy.
30. [Pre-API freeze checklist](./pre-api-freeze.md) — gates before paid agent runs.
31. [Release week numbering](./release-week-numbering.md) — public Release Week 1/2/3 labels versus internal ISO week evidence IDs.

## Current reputation status

Reputation is currently social memory, not an automated score.

The repository records outcomes. Workflows do not yet compute player rankings, trust scores, author scores, or penalties.

## Participant status

Participants should start with [Participant guide](./for-participants.md).

The first useful action is usually voting with 👍 on an existing `prompt-proposal` Issue. Prompt submission is the second step, not the first step.

## Release readiness status

The [Release readiness review](./release-readiness-review.md) is the release-facing check for three user-visible questions:

```text
security posture
participant journey
live preview
```

It currently records:

```text
security posture: PASS
participant journey: PASS
live preview: PASS
ordinary default-on weekly no-eligible observation: PASS
```

## Release week status

Public release numbering starts at `Release Week 1` after launch.

Pre-release evidence such as `2026-W20` remains preserved under its internal ISO week ID and should not be presented as Release Week 1.

See [Release week numbering](./release-week-numbering.md).

## Repository cleanup status

Maintainer-authored repository content should be English.

The [Repository 5S and language policy](./repository-5s-and-language-policy.md) defines Sort, Set in order, Shine, Standardize, and Sustain rules for cleanup PRs.

The [Root folder audit](./root-folder-audit.md) records top-level folder roles, cleanup posture, and maintainer questions before broad cleanup.

The [Repository cleanup inventory](./repository-cleanup-inventory.md) classifies protected evidence, canonical active surfaces, legacy fallbacks, generated snapshots, cleanup candidates, and not-yet-removable items before any deletion work.

The [Workflow family map](./workflow-family-map.md) classifies workflows before consolidation or deletion work so historical scaffolding is not mistaken for active canonical evidence.

The [Canonical status drift check](./canonical-status-drift-check.md) keeps canonical runner, legacy fallback, default-on, auto-merge, and release-gate wording aligned across maintainer-authored docs.

Generated public result snapshots and raw external evidence are treated separately because they may contain user-provided text.

## Canonical runner evidence status

The selected-prompt Docker/Codex runner is the canonical evidence path for default weekly eligible implementation runs when the PR/run evidence says:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

Participants should use the [Canonical runner evidence guide](./canonical-runner-evidence-guide.md) to inspect diagnostics, public bundles, uploaded bundle verification, Gitleaks results, and bounded lab diffs.

The legacy `scripts/openai_lab_run.py` path is non-canonical and does not satisfy the selected-prompt canonical runner requirement.

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

The repository has scheduled weekly automation, support-unlock gates, and a verified canonical selected-prompt path enabled by default for eligible weekly implementation runs.

Broad default-on canonical weekly execution is approved; manual review remains required and auto-merge remains disabled.

Status ownership:

```text
current status contract -> docs/canonical-status-drift-check.md
weekly workflow operation -> docs/weekly-automation.md
maintainer operating procedure -> docs/operator-runbook.md
canonical evidence decision rule -> docs/canonical-runner-evidence-guide.md
```

Manual canary experiments and comparison operations remain available through [Usable experiment operations](./usable-experiment-ops.md).

## Pre-API freeze status

Paid implementation-agent runs remain governed by preflight, bounded-run evidence, public bundle verification, and manual review.

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