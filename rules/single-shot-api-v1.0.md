# single-shot-api-v1.0

This file is kept for compatibility with existing workflow references.

The public concept is now defined as an agent-run policy, not an API-first policy.

Use:

- [`agent-run-policy-v1.0.md`](./agent-run-policy-v1.0.md)

## Compatibility summary

When an implementation agent is backed by a paid model API, the low-level safeguards remain:

```text
model/API calls per candidate per automated attempt: 1
SDK max_retries: 0
automatic retry: no
automatic fallback model: no
automatic merge: no
```

The higher-level rule is:

```text
one bounded agent attempt per candidate per workflow run
```

Continuation is allowed only as an explicit, reviewable follow-up run under `agent-run-policy-v1.0.md`.
