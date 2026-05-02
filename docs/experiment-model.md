# Experiment model

Prompt Vote Lab is a public experiment about prompt selection, constrained AI-agent implementation, cumulative UI change, and expectation-gap analysis.

## One-line explanation

People propose and vote on prompts. The selected prompt is given to a fixed implementation agent/Codex-style run inside the current static lab. The project records whether the result matched what people expected.

## What this is

Prompt Vote Lab is not a normal product roadmap.

It is an observable experiment with six layers:

1. Participation layer: people submit prompt candidates as GitHub Issues.
2. Vote layer: people rank prompt candidates with GitHub reactions.
3. Baseline layer: a virtual no-change candidate is inserted each week.
4. State layer: the current merged `lab/` state is inherited from previous weeks.
5. Implementation layer: the selected prompt is attempted by a fixed AI coding agent inside the static `lab/` files.
6. Evaluation layer: the result is classified and reported.

There is also an entertainment layer. The weekly run is meant to be watchable: a public prompt tries to pass the **20-vote gate**, then the constrained lab changes or fails visibly.

```text
Prompt → 20-vote gate → agent PR → inherited lab state
```

## What this is not

Prompt Vote Lab is not:

- a direct feature-request queue
- a paid specification market
- a paid review service
- a maintenance contract
- a guarantee that the most popular prompt will be merged
- a general-purpose web app builder
- a backend, database, login, or payment experiment
- a weekly reset contest

## Why the no-change baseline exists

Every weekly vote includes a virtual candidate:

```text
[Baseline]: No change this week
```

Initial baseline:

```text
20 virtual votes
```

If no real prompt beats this baseline, the week produces no implementation-agent attempt.

This prevents low-interest weeks from spending model-run budget and review time.

## Why the lab state is inherited

Each weekly implementation attempt starts from the current `main` branch version of `lab/`.

```text
week N merged lab state
→ week N+1 selected prompt is applied on top of that state
→ if merged, it becomes week N+2 starting state
```

This cumulative pressure is intentional.

Over time, the same three files may become easier, harder, stranger, more coherent, or more fragile to modify. That trajectory is part of the experiment.

Rejected, failed, unsafe, and unmerged comparison PRs do not become the next week's base state.

## Why the implementation scope is small

The implementation agent may edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

The agent may create ordinary helper functions inside `lab/app.js`.

The constraint is intentional.

As experiments accumulate, the three files become harder to modify cleanly. That rising difficulty is part of what the project observes.

## Why the implementation condition is fixed

Prompt candidates should be compared under the same implementation condition.

The implementation model is fixed by `rules/model-policy-v1.0.md`:

```text
gpt-5-nano
```

A stronger model may be used for reports, but it must not modify `lab/`.

## Result classifications

Allowed expectation-gap labels include:

- Hit
- Partial
- Misread
- Overbuild
- Underbuild
- Rule conflict
- Unsafe
- Rejected

The classification describes the gap between the public prompt expectation and the actual implementation outcome.
