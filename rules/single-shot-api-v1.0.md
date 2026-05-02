# single-shot-api-v1.0

## Purpose

Prompt Vote Lab must not burn tokens through hidden retries, repeated agent loops, or unbounded workflow reruns.

Each implementation attempt should be a single paid model call per candidate.

## Implementation run rule

For each eligible candidate:

```text
maximum model calls: 1
SDK retries: 0
manual retry: not automatic
workflow retry: not automatic
```

If the model call fails, the run fails closed and should be recorded as failed.

Do not automatically retry with:

- the same model
- a stronger model
- modified prompt text
- larger output budget
- a new branch

## Evaluation/blog run rule

Blog/report generation should also be single-shot by default.

If Hacker News draft generation is enabled, it is a separate optional model call and must be visible in workflow inputs.

## Required guards

Paid API workflows must use:

- explicit confirmation input for manual paid runs
- `max_retries=0` in the OpenAI SDK client
- job-level timeout
- bounded `max_output_tokens`
- prompt/input length checks
- no automatic fallback model

## Failure behavior

On API failure:

```text
FAIL workflow
NO automatic retry
NO automatic fallback
NO merge
record failure if terminal-state reporting is enabled
```

## Rationale

The project should pay for one controlled attempt, not an unbounded repair loop.

A failed implementation is useful experimental data. It should not be hidden by automatic retries.
