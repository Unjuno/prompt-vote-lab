# Experiment model

Prompt Vote Lab is a public prompt game and experiment about prompt selection, reputation, constrained AI-agent implementation, cumulative UI change, and expectation-gap analysis.

## One-line explanation

Players submit prompts, vote on prompts, and learn whether the winning prompt survives a fixed implementation agent/Codex-style run inside the current static lab.

A prompt can win votes and still fail.

## What this is

Prompt Vote Lab is not a normal product roadmap.

It is a competitive prompt game with experimental measurement.

The game has seven layers:

1. Player layer: people submit prompt candidates as GitHub Issues.
2. Persuasion layer: players try to make other players trust their prompt.
3. Vote layer: players rank prompt candidates with GitHub reactions.
4. Baseline layer: a virtual no-change candidate is inserted each week.
5. State layer: the current merged `lab/` state is inherited from previous weeks.
6. Implementation layer: the selected prompt is attempted by a fixed AI coding agent inside the static `lab/` files.
7. Memory layer: players use past outcomes to decide which authors, prompt styles, and promises deserve future trust.

There is also an entertainment layer. The weekly round is meant to be watchable: a public prompt tries to pass the **20-vote gate**, then the constrained lab changes, fails, overbuilds, underbuilds, or refuses to move.

```text
Prompt → 20-vote gate → agent PR → public outcome → reputation memory
```

## What counts as winning

Winning the vote is not the same as winning the round.

A prompt wins attention when it gets votes.

A prompt wins trust only if the resulting agent PR is useful, reviewable, and compatible with the inherited lab state.

Bad outcomes should matter. If a prompt author repeatedly makes flashy promises that produce weak or unmergeable results, voters should rationally become less willing to support that style later.

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

This prevents low-interest weeks from spending model-run budget and review time. It also makes the vote game harder: doing nothing is always a competitor.

## Why the lab state is inherited

Each weekly implementation attempt starts from the current `main` branch version of `lab/`.

```text
week N merged lab state
→ week N+1 selected prompt is applied on top of that state
→ if merged, it becomes week N+2 starting state
```

This cumulative pressure is intentional.

Over time, the same three files may become easier, harder, stranger, more coherent, or more fragile to modify. That trajectory is part of the game and the experiment.

Rejected, failed, unsafe, and unmerged comparison PRs do not become the next week's base state.

## Why the implementation scope is small

The implementation agent may edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

The agent may create ordinary helper functions inside `lab/app.js`.

The constraint is intentional.

As rounds accumulate, the three files become harder to modify cleanly. That rising difficulty is part of what the project observes.

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

These labels also feed the reputation game: they help players remember which prompt styles deserved trust.
