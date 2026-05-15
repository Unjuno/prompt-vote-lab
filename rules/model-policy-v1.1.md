# model-policy-v1.1

## Purpose

This policy fixes the active implementation model and bounded-agent operating conditions for Prompt Vote Lab stabilization runs.

Prompt Vote Lab evaluates prompt candidates. To compare prompts fairly, the implementation model, attempt count, retry policy, fallback policy, editable file scope, and manual-review policy must remain fixed within the same comparison period.

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
active rules
editable file scope
input context policy
retry policy
fallback policy
manual review policy
```

Do not run rank 1, rank 2, and rank 3 with different implementation models or execution policies in the same comparison set.

## Active settings

```text
model: gpt-5.4-nano
temperature_policy: model-default
top_p_policy: model-default
attempts_per_candidate: 1
retry_count: 0
fallback_policy: none
auto_merge_policy: disabled
output_token_cap_enforced: false
```

The implementation runner records the temperature and top_p policies as `model-default` rather than passing unsupported or unstable sampling overrides.

## Output-token cap status

`max_output_tokens` is not an active enforced implementation condition for the current canonical Codex CLI runner.

Earlier API-oriented runner designs used a `max_output_tokens` setting. The current canonical selected-prompt path invokes the Codex CLI runner and does not enforce that API-era cap as a runtime limit.

Therefore this policy treats output-token caps as non-active metadata unless a future runner can enforce them directly and records that enforcement in its runner contract.

The active cost and scope guards are instead:

```text
attempts_per_candidate: 1
retry_count: 0
fallback_policy: none
rank support unlock limits
manual review required
editable files limited to lab/index.html, lab/style.css, lab/app.js
```

Do not claim a run is output-token-capped unless the runner passes and verifies an actual runtime cap.

## Ranked candidates

If rank 1, rank 2, and rank 3 are executed in the same week, they must use the same implementation model settings and execution policy.

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

`model-policy-v1.1` records the active stabilization model and execution policy:

```text
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_count: 0
fallback_policy: none
output_token_cap_enforced: false
```

Do not directly compare prompt results across v1.0 and v1.1 without noting the model-policy change.

Do not directly compare prompt results across model, runner, retry, fallback, file-scope, or output-cap-enforcement changes without noting the policy change.

## Separation from evaluation model

The implementation model is intentionally fixed and bounded.

A stronger model may be used for analysis and blog/report writing under a separate evaluation-model policy, but the evaluation model must not modify `lab/`.

## Rationale

If the implementation model or execution policy changes between candidates, the experiment no longer evaluates only prompt quality.

The result becomes a mixture of prompt quality, model capability, context size, runner capability, retry behavior, fallback behavior, and review policy.

To evaluate prompts, keep the implementation model and bounded-agent policy fixed within each comparison period.