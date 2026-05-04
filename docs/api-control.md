# API Control Policy

## Purpose

This document defines when Prompt Vote Lab may use a paid implementation-model call and what must be recorded.

The goal is to prevent uncontrolled spending, hidden retries, model drift, and irreproducible experiment runs.

## API gate

Do not run a real implementation-model call unless all gates are satisfied:

1. weekly snapshot exists
2. selected prompt is recorded in `runs/week-XXX.md`
3. implementation model policy is recorded
4. editable file scope is recorded
5. dry-run path has succeeded
6. API usage log path exists
7. safety-check workflow exists
8. maintainer explicitly approves the run

If any gate fails, stop before calling the model.

## Required model configuration

Each run must record:

- provider
- model
- model policy version
- temperature
- top_p
- max output tokens
- retry count
- timeout policy
- editable file scope
- prompt package hash
- snapshot reference

## Retry policy

Default retry count:

```text
0
```

Reason: hidden retries make prompt comparison unfair.

If a retry is allowed in a later policy, it must be recorded as a separate attempt with:

- attempt number
- same model settings unless a policy explicitly allows otherwise
- error reason
- output hash, if output exists

## Usage log

Canonical path:

```text
logs/api/week-XXX.jsonl
```

Each line should be one JSON object.

Example:

```json
{
  "event": "implementation_model_call",
  "week": "001",
  "attempt": 1,
  "provider": "openai",
  "model": "gpt-5-nano",
  "model_policy": "model-policy-v1.0",
  "temperature": 0.2,
  "top_p": 1.0,
  "max_output_tokens": 12000,
  "retry_count": 0,
  "snapshot": "data/snapshots/week-001.json",
  "prompt_package_hash": "sha256:unrecorded",
  "status": "success",
  "input_tokens": null,
  "output_tokens": null,
  "estimated_cost_usd": null,
  "started_at": "2026-05-11T00:05:00+09:00",
  "finished_at": "2026-05-11T00:05:30+09:00"
}
```

## Error log

Canonical path:

```text
logs/errors/week-XXX.jsonl
```

Record:

- error type
- status code, if any
- retryable boolean
- selected issue
- workflow run id
- commit SHA
- timestamp

Do not record credentials or private runtime configuration.

## Cost guardrails

Before enabling real calls, define:

- max implementation calls per week
- max attempts per selected prompt
- max estimated weekly budget
- allowed model list
- who may trigger the workflow

Initial recommendation:

```text
max_implementation_calls_per_week = 1
max_retry_count = 0
manual_approval_required = true
```

## Prompt package

The implementation prompt should be stored as a generated artifact or committed package before the model call.

Recommended path:

```text
run-packages/week-XXX/rank-1/prompt.md
run-packages/week-XXX/rank-1/metadata.json
```

The usage log should reference the prompt package hash instead of relying only on temporary workflow output.

## Separation from evaluation model

Implementation model calls may modify `lab/` through PR generation.

Evaluation model calls may draft analysis, blog posts, or HN posts, but must not modify `lab/` and must not decide merge automatically.

## Human approval

Until the experiment has at least three successful dry-runs, real implementation-model calls should require explicit maintainer approval.

Approved forms:

- manual workflow dispatch
- approving a PR that triggers the run
- explicit repository issue comment command, if a permission-checked command parser is later added

Do not trigger paid model calls from public comments without a permission check.
