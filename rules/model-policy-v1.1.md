# model-policy-v1.1

## Purpose

This policy fixes the current implementation model for Prompt Vote Lab canary execution paths.

Prompt Vote Lab evaluates prompt candidates. To compare prompts fairly, the implementation model must remain fixed within the same comparison period.

## Implementation model

```text
gpt-5.4-nano
```

## Scope

This model is used only to implement ranked prompt candidates inside `lab/`.

Editable files:

```text
lab/index.html
lab/style.css
lab/app.js
```

## Current canary paths covered

This policy applies to the currently active canary execution paths that record `model: gpt-5.4-nano`:

```text
first-canary-005: offline context + JSON full-file replacement
first-canary-008: selected prompt task packet container
first-canary-009: fixed GitHub Issue -> normalized instruction packet -> /task:ro
```

## Fixed comparison rule

For all candidates in the same weekly vote, use the same:

```text
model
sampling policy
max output budget
active rules
editable file scope
input context policy
retry policy
fallback policy
manual review policy
```

Do not run rank 1, rank 2, and rank 3 with different implementation models in the same comparison set.

## Initial settings

```text
model: gpt-5.4-nano
temperature_policy: model-default
top_p_policy: model-default
max_output_tokens: 12000
retry_count: 0
fallback_policy: none
auto_merge_policy: disabled
```

The implementation runner records the temperature and top_p policies as `model-default` rather than passing unsupported or unstable sampling overrides.

## Ranked candidates

If rank 1, rank 2, and rank 3 are executed in the same week, they must use the same implementation model settings.

Rank 2 and rank 3 are comparison candidates. They are not automatically promoted if rank 1 fails review.

## Retry policy

Default retry count is 0.

A failed implementation should normally be recorded as a result instead of silently retried with a stronger model.

If retries are introduced later, they must use the same implementation model and must be recorded in the weekly log.

## Model change from v1.0

`model-policy-v1.0` recorded:

```text
gpt-5-nano
```

The current implemented canary workflows and documentation use:

```text
gpt-5.4-nano
```

This file exists so the current comparison period has an explicit model-policy version rather than silently mutating v1.0.

Do not directly compare prompt results across v1.0 and v1.1 without noting the model-policy change.

## Separation from evaluation model

The implementation model is intentionally fixed and bounded.

A stronger model may be used for analysis and blog/report writing under a separate evaluation-model policy, but the evaluation model must not modify `lab/`.

## Rationale

If the implementation model changes between candidates, the experiment no longer evaluates only prompt quality.

The result becomes a mixture of prompt quality, model capability, context size, and retry behavior.

To evaluate prompts, keep the implementation model fixed within each comparison period.
