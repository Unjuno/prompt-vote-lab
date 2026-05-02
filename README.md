# Prompt Vote Lab

Prompt Vote Lab is a public experiment for observing vibe coding.

People propose prompts, vote on them, and an AI coding agent implements ranked prompt candidates inside a constrained `lab/` directory.

The goal is not only to generate UI. The goal is to study the gap between collective expectation and AI-implemented reality.

## Short explanation

Prompt Vote Lab is a prompt market plus a constrained implementation sandbox.

- Participants submit prompt candidates as GitHub Issues.
- Participants vote with 👍 reactions.
- A virtual no-change baseline is inserted every week.
- If a real prompt beats the baseline, a fixed low-cost model implements it in `lab/`.
- The result is reviewed, classified, and reported.

## What this is not

Prompt Vote Lab is not a feature-request queue, a paid merge system, or a general-purpose web app builder.

Support contributes to additional experiment runs and project operation. It does not guarantee success, adoption, merge, or specification control.

## Each run records

- the voted prompt
- vote count
- candidate rank
- no-change baseline result
- selection rule
- implementation model policy
- evaluation model policy
- AI execution constraints
- PR diff
- safety checks
- merge/reject decision
- expectation gap classification

## Current scope

The AI agent may edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

The AI agent must not edit:

- `.github/`
- `rules/`
- `runs/`
- `docs/`
- `run-packages/`
- backend files
- config/secrets
- files outside `lab/`

## Weekly loop

1. People propose prompts as GitHub issues.
2. People vote with GitHub reactions.
3. A virtual no-change baseline is inserted with 20 votes.
4. Candidates are ranked by vote count.
5. If the no-change baseline ranks first, no implementation run is created.
6. If a real prompt ranks first, rank 1 is the normal weekly run candidate.
7. Rank 2 and rank 3 may be executed as support-unlocked comparison runs.
8. The implementation model modifies only `lab/` and opens a PR.
9. Safety checks run.
10. `main` merge remains manual.
11. After a terminal run state, a stronger evaluation model may classify the result and publish a blog report.
12. The result is recorded in `runs/week-XXX.md`.

## Ranked candidates

Prompt Vote Lab uses ranked candidates, not a single permanent winner.

- `rank-1`: normal weekly run and default mainline candidate
- `rank-2`: optional support-unlocked comparison run
- `rank-3`: optional support-unlocked comparison run

## No-change baseline

Every weekly vote includes a virtual candidate:

```text
[Baseline]: No change this week
20 virtual votes
```

If this baseline ranks first, the workflow records the vote summary but does not create implementation PRs.

See `rules/no-change-baseline-v1.0.md` and `docs/no-change-baseline.md`.

## Model policy

Implementation model:

```text
gpt-5-nano
```

The implementation model is fixed by `rules/model-policy-v1.0.md`.

All ranked candidates in the same weekly vote must use the same implementation model settings.

A stronger model may be used only for evaluation and blog-writing under `rules/evaluation-model-policy-v1.0.md`. The evaluation model must not modify `lab/`.

## Merge policy

Voting rank has priority.

Rank 1 is the default merge candidate. Rank 2 and rank 3 are comparison candidates.

If rank 1 does not pass review, the default result is no merge for that weekly vote. Rank 2 and rank 3 are not automatically promoted.

See `rules/merge-policy-v1.0.md`.

## Support-unlocked runs

Support may open additional comparison runs for rank 2 and rank 3 during the weekly run window.

Recommended one-time support tiers:

- 5 USD: Support Rank 2 Comparison Run
- 10 USD: Support Rank 3 Comparison Run
- 20 USD: Support the Experiment

Support contributes to additional experiment runs and project operation. It does not guarantee success, adoption, merge, or specification control.

See `rules/support-unlocked-runs-v1.1.md` and `docs/support-policy.md`.

## Documentation

- `docs/experiment-model.md` — project concept and boundaries
- `docs/how-to-participate.md` — how to propose, vote, and review
- `docs/no-change-baseline.md` — no-change baseline explanation
- `docs/support-policy.md` — support tiers and thresholds
- `docs/automation-map.md` — automation boundary
- `docs/wiki-draft.md` — copy-ready Wiki draft

## GitHub Pages

This repository is designed to work with GitHub Pages as a static site.

Recommended Pages source:

- Branch: `main`
- Folder: `/`

Useful paths after Pages is enabled:

- `/lab/` — current lab UI
- `/runs/week-001.md` — run log template
- `/rules/static-ui-v1.0.md` — implementation rule profile

## License

This project is licensed under the Apache License 2.0.
