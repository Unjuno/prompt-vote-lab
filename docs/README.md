# Prompt Vote Lab docs

This directory contains the stable public explanation layer for Prompt Vote Lab.

The landing page should stay short. Details belong here.

## Start here

1. [Experiment model](./experiment-model.md) — what the project is and what it is not.
2. [How to participate](./how-to-participate.md) — how to propose prompts, vote, and review results.
3. [No-change baseline](./no-change-baseline.md) — why every week starts with 20 virtual votes for no change.
4. [Automation map](./automation-map.md) — what is automated, what is manual, and how workflow boundaries are drawn.
5. [Support policy](./support-policy.md) — what support can fund and what it cannot buy.

## Rule documents

Operational rules live in [`../rules/`](../rules/).

Important rules:

- [`static-ui-v1.0.md`](../rules/static-ui-v1.0.md) — lab edit scope and runtime restrictions.
- [`agent-run-policy-v1.0.md`](../rules/agent-run-policy-v1.0.md) — one bounded agent attempt, explicit continuation, no hidden retries.
- [`event-logging-v1.0.md`](../rules/event-logging-v1.0.md) — JSONL and Markdown logging policy.
- [`support-unlocked-runs-v1.1.md`](../rules/support-unlocked-runs-v1.1.md) — $5/$10 comparison-run thresholds.
- [`mock-testing-v1.0.md`](../rules/mock-testing-v1.0.md) — API-free mock testing.
- [`exception-testing-v1.0.md`](../rules/exception-testing-v1.0.md) — failure-path tests.
- [`multi-fuzz-testing-v1.0.md`](../rules/multi-fuzz-testing-v1.0.md) — weighted random boundary testing.

Compatibility note:

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
/docs/ = rendered project explanation
/rules/ = operational constraints
/runs/ = recorded run history
```

Do not collapse these layers unless a future policy deliberately changes the experiment model.
