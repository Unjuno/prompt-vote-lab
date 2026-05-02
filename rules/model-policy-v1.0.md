# model-policy-v1.0

## Purpose

This policy fixes the implementation model for Prompt Vote Lab.

Prompt Vote Lab evaluates prompt candidates. To compare prompts fairly, the implementation model must remain fixed within the same comparison period.

## Implementation model

```text
gpt-5-nano
```

## Scope

This model is used only to implement ranked prompt candidates inside `lab/`.

Editable files:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

## Fixed comparison rule

For all candidates in the same weekly vote, use the same:

- model
- temperature
- top_p
- max output budget
- active rules
- editable file scope
- input context policy
- retry policy

## Initial settings

```text
model: gpt-5-nano
temperature: 0.2
top_p: 1.0
max_output_tokens: 12000
retry_count: 0
```

## Ranked candidates

If rank 1, rank 2, and rank 3 are executed in the same week, they must use the same implementation model settings.

Do not use different implementation models for different ranks in the same weekly vote.

## Retry policy

Default retry count is 0.

A failed implementation should normally be recorded as a result instead of silently retried with a stronger model.

If retries are introduced later, they must use the same implementation model and must be recorded in the weekly log.

## Model changes

If the implementation model changes, create a new policy version.

Example:

```text
model-policy-v1.0: gpt-5-nano
model-policy-v1.1: another model
```

Do not directly compare prompt results across different model-policy versions without noting the model change.

## Separation from evaluation model

The implementation model is intentionally low-cost and fixed.

A stronger model may be used for analysis and blog writing under `evaluation-model-policy-v1.0`, but the evaluation model must not modify `lab/`.

## Rationale

If the implementation model changes between candidates, the experiment no longer evaluates only prompt quality.

The result becomes a mixture of prompt quality, model capability, context size, and retry behavior.

To evaluate prompts, keep the implementation model fixed.
