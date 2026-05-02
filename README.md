# Prompt Vote Lab

Prompt Vote Lab is a public experiment for watching a prompt market steer a constrained AI coding agent.

People propose prompts, vote on them, and the selected prompt is given to an AI coding agent/Codex-style implementation run inside a small static `lab/` directory.

The lab is cumulative. Each week starts from the current `main` branch state of `lab/`, not from a clean initial template.

The point is not only to generate UI.

The point is to observe the gap between:

```text
what people expected from a prompt
vs.
what a constrained AI agent actually produced
```

There is also an entertainment layer: the weekly run is meant to be watchable. The memorable object is the **20-vote gate**.

```text
Prompt → 20-vote gate → agent PR → inherited lab state
```

## Short explanation

Prompt Vote Lab is a prompt market plus a constrained, cumulative implementation sandbox.

- Participants submit prompt candidates as GitHub Issues.
- Participants vote with 👍 reactions.
- A virtual no-change baseline is inserted every week with 20 virtual votes.
- If a real prompt beats the baseline, the selected prompt is passed to the implementation agent.
- The implementation agent attempts the change against the current `main` version of `lab/`.
- If merged, the result becomes the starting point for later weeks.
- The result is reviewed, classified, and recorded.

## What this is not

Prompt Vote Lab is not:

- a feature-request queue
- a paid merge system
- a paid review service
- a maintenance contract
- a general-purpose web app builder
- a guarantee that the most popular prompt will be merged
- a weekly reset contest

Support can unlock extra comparison runs. It does not buy success, adoption, merge, maintenance, review, support work, or specification control.

## Current scope

The AI agent may edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

The AI agent may create ordinary helper functions inside `lab/app.js`.

The AI agent must not edit:

- `.github/`
- `rules/`
- `runs/`
- `docs/`
- backend files
- config/secrets
- files outside `lab/`

The lab must not use external scripts, CDNs, hidden network calls, cookies, iframes, `eval`, `new Function(...)`, login, payment, or trackers.

## State inheritance

Each weekly implementation attempt starts from the current `main` branch version of `lab/`.

```text
week N merged lab state
→ week N+1 selected prompt is applied on top of that state
→ if merged, it becomes week N+2 starting state
```

This cumulative pressure is part of the experiment. Over time, the same three files may become easier, harder, stranger, or more coherent to modify.

Rejected, failed, unsafe, and unmerged comparison PRs do not become the next week's base state.

## Weekly loop

1. People propose prompts as GitHub Issues.
2. People vote with GitHub reactions.
3. A virtual no-change baseline is inserted with 20 virtual votes.
4. Candidates are ranked by vote count.
5. If the no-change baseline ranks first, no implementation run is created.
6. If a real prompt ranks first, rank 1 is the normal weekly run candidate.
7. Rank 2 and rank 3 may be executed as support-unlocked comparison runs.
8. The selected prompt is given to the implementation agent.
9. The implementation agent modifies only the current `main` state of `lab/` and opens a PR.
10. Safety and static-site checks run before the PR is created by automation.
11. `main` merge remains manual.
12. If merged, the PR becomes the future lab state.
13. After a terminal run state, a stronger evaluation model may classify the result and draft a report.
14. The result is recorded.

## Ranked candidates

Prompt Vote Lab uses ranked candidates, not a single permanent winner.

- `rank-1`: normal weekly run and default mainline candidate
- `rank-2`: optional support-unlocked comparison run
- `rank-3`: optional support-unlocked comparison run

Rank 2 and rank 3 are comparison candidates. They are not automatically promoted if rank 1 fails review.

Only merged PRs affect the inherited lab state.

## No-change baseline

Every weekly vote includes a virtual candidate:

```text
[Baseline]: No change this week
20 virtual votes
```

If this baseline ranks first, the workflow records the vote summary but does not create implementation PRs or spend an implementation-agent attempt.

See [`docs/no-change-baseline.md`](docs/no-change-baseline.md).

## Implementation agent policy

Implementation agent/model:

```text
gpt-5-nano
```

The implementation model is fixed by `rules/model-policy-v1.0.md`.

All ranked candidates in the same weekly vote must use the same implementation condition.

A stronger model may be used only for evaluation and blog/report writing. The evaluation model must not modify `lab/`.

## Agent run policy

Paid implementation runs are bounded agent attempts:

```text
agent attempt per candidate per workflow run: 1
SDK max_retries, when an SDK is used: 0
automatic fallback: no
automatic retry: no
automatic merge: no
```

Failure is recorded as experiment data. It is not hidden by rerunning the model.

Good partial progress may be continued only as an explicit, reviewable continuation run.

## Support-unlocked runs

Support may open additional comparison runs for rank 2 and rank 3 during the weekly run window.

Supported one-time tiers:

- 5 USD: Support Rank 2 Comparison Run
- 10 USD: Support Rank 3 Comparison Run

There is no general support tier.

Support applies to the current weekly vote only. It does not create a request channel, maintenance contract, paid review obligation, delivery promise, or support obligation.

See [`docs/support-policy.md`](docs/support-policy.md).

## Each run records

- selected prompt
- inherited lab base commit
- vote count
- candidate rank
- no-change baseline result
- selection rule
- implementation agent/model condition
- AI execution constraints
- PR diff
- safety/static check result
- merge/reject/failure decision
- expectation-gap classification, when evaluated

## Documentation

Start with [`docs/README.md`](docs/README.md).

Key documents:

- [`docs/experiment-model.md`](docs/experiment-model.md) — project concept and boundaries
- [`docs/how-to-participate.md`](docs/how-to-participate.md) — how to propose, vote, and review
- [`docs/no-change-baseline.md`](docs/no-change-baseline.md) — no-change baseline explanation
- [`docs/support-policy.md`](docs/support-policy.md) — support tiers and thresholds
- [`docs/automation-map.md`](docs/automation-map.md) — automation boundary

Operational rules live in [`rules/`](rules/).

## GitHub Pages

This repository is designed to work with GitHub Pages as a static site.

Recommended Pages source:

- Branch: `main`
- Folder: `/`

Useful paths after Pages is enabled:

- `/` — stable landing page
- `/lab/` — current lab UI

Markdown documentation should normally be read through GitHub's rendered view rather than as raw `.md` files on GitHub Pages.

## License

This project is licensed under the Apache License 2.0.
