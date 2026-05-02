# selection-v1.0

## Purpose

This rule prevents noisy prompt votes from triggering unnecessary AI-agent runs.

A prompt should beat the no-change baseline before it is executed.

## Parameters

- `no_change_baseline`: 5 points
- `required_margin`: 2 points
- `minimum_total_votes`: 5 votes

## Selection rule

A prompt is selected only if:

```text
top_prompt_votes >= no_change_baseline + required_margin
```

and:

```text
total_votes >= minimum_total_votes
```

With the initial parameters, the top prompt must have at least 7 votes and the weekly vote must have at least 5 total votes.

## If no prompt passes

No AI-agent implementation run is executed for that week.

The weekly log should explicitly record:

- top prompt
- top prompt votes
- no-change baseline
- required margin
- minimum total votes
- reason for no run

## Rationale

The no-change baseline represents the cost of changing the system.

It is not a fake vote. It is a threshold.
