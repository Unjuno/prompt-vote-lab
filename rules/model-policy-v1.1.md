# model-policy-v1.1

## Purpose

This policy fixes the active implementation model for Prompt Vote Lab stabilization runs.

Prompt Vote Lab evaluates prompt candidates. To compare prompts fairly, the implementation model and output budget must remain fixed within the same comparison period.

## Active implementation model

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

## Active canary and weekly automation paths covered

This policy applies to the currently active implementation paths that are guarded by preflight checks and CI:

```text
first-canary-run
weekly-auto-run eligible implementation path
```

Historical canary evidence may still mention earlier isolated paths, including `first-canary-009`, but current active paid implementation settings are defined by this file and the current workflows.

The canonical selected-prompt canary has passed, and the weekly canonical selected-prompt runner is default-on for eligible candidates. The first ordinary post-default-on weekly run still needs operational observation.

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

## Active settings

```text
model: gpt-5.4-nano
temperature_policy: model-default
top_p_policy: model-default
max_output_tokens: 5000
retry_count: 0
fallback_policy: none
auto_merge_policy: disabled
```

The implementation runner records the temperature and top_p policies as `model-default` rather than passing unsupported or unstable sampling overrides.

## Deferred settings

The following setting is not active during the stabilization phase:

```text
max_output_tokens: 12000
```

It may be reconsidered only after the system is complete and the eligible implementation PR path has passed at least one live end-to-end run.

Do not change the active token budget during stabilization merely to increase implementation capacity.

## Ranked candidates

If rank 1, rank 2, and rank 3 are executed in the same week, they must use the same implementation model settings.

Rank 2 and rank 3 are comparison candidates. They are not automatically promoted if rank 1 fails review.

## Retry policy

Default retry count is 0.

A failed implementation should normally be recorded as a result instead of silently retried with a stronger model.

If retries are introduced later, they must use the same implementation model and must be recorded in the weekly log.

## Relationship to v1.0

`model-policy-v1.0` recorded:

```text
gpt-5-nano
```

`model-policy-v1.1` records the active stabilization model and output budget:

```text
model: gpt-5.4-nano
max_output_tokens: 5000
```

This file also records that `max_output_tokens: 12000` is deferred, not active.

Do not directly compare prompt results across v1.0 and v1.1 without noting the model-policy change.

Do not directly compare prompt results across model or token-budget changes without noting the policy change.

## Separation from evaluation model

The implementation model is intentionally fixed and bounded.

A stronger model may be used for analysis and blog/report writing under a separate evaluation-model policy, but the evaluation model must not modify `lab/`.

## Rationale

If the implementation model or output budget changes between candidates, the experiment no longer evaluates only prompt quality.

The result becomes a mixture of prompt quality, model capability, context size, output budget, and retry behavior.

To evaluate prompts, keep the implementation model and budget fixed within each comparison period.