# Legacy API canary policy

This document defines the historical first paid implementation-agent API run.

It is retained as a guardrail for the legacy API/SDK path. It is not the current canonical weekly selected-prompt runner policy.

Current active implementation path:

```text
canonical selected-prompt runner: default-on
runner family: Docker/Codex selected-prompt task-packet runner
legacy API/SDK runner: present, non-canonical
manual review: required
auto-merge: disabled
```

The active canonical runner status is governed by:

```text
docs/current-codex-implementation-path.md
docs/weekly-automation.md
docs/operator-runbook.md
docs/canonical-status-drift-check.md
rules/model-policy-v1.1.md
```

## Historical entry condition

A real API canary could start only after:

```text
Pre-API Freeze Audit: PASS
Weekly Auto Run no-eligible path: PASS
open verification PRs: none
implementation-agent secret: configured
```

## Historical first canary prompt

The old first canary prompt was small, visible, and easy to review.

Recommended prompt:

```text
Add a small visible canary panel to the lab page explaining that this is the first bounded implementation-agent test. Keep the change static, local, and inside lab/ only.
```

## Legacy API hard limits

These limits describe the old API/SDK canary path, not the canonical Codex selected-prompt runner.

```text
model: gpt-5.4-nano
candidate count: 1
attempts per candidate: 1
SDK max_retries: 0
fallback model: none
legacy max_output_tokens: 5000
automatic merge: no
```

The current canonical Codex CLI runner does not enforce this legacy API-era output-token cap as a runtime limit.

Current active model policy records:

```text
output_token_cap_enforced: false
```

Do not claim a canonical run is output-token-capped unless a future runner contract proves runtime enforcement.

## Allowed output

The legacy API canary could create one implementation PR changing only:

```text
lab/index.html
lab/style.css
lab/app.js
```

The PR had to pass:

```text
safety-check
static-site-check
```

## Forbidden output

Any implementation canary must fail review if it:

```text
edits outside lab/
adds network calls
adds external scripts
uses cookies
uses eval
uses dynamic new Function with user or external data
adds login
adds payment behavior
modifies workflows
modifies rules
modifies docs
tries to auto-merge
```

## Review requirement

The canary PR must be reviewed manually.

Do not merge automatically.

Do not run a second paid implementation-agent attempt until the first canary result is classified.

## Result labels

Use one label in the canary report:

```text
PASS
PARTIAL
FAIL
UNSAFE
UNCERTAIN
```

## Partial continuation decision

`PARTIAL` does not mean retry.

`PARTIAL` means the first run produced useful progress but did not complete the requested change.

Default decision for `PARTIAL` is:

```text
STOP
```

## Automatic continuation (mechanical)

Automatic continuation is allowed only if all gates pass:

```text
continuation_gate.py = CONTINUE_ALLOWED
semantic_gate.py = SEMANTIC_CONTINUE_ALLOWED
safety-check = PASS
static-site-check = PASS
```

## Continuation limits

```text
max continuation runs per candidate: 1
```

If a second PARTIAL occurs after continuation:

```text
FORCE STOP
```

## Forced stop outcomes

These outcomes always stop:

```text
FAIL
UNSAFE
UNCERTAIN
```

Do not continue from these labels.

## Principle

```text
CONTINUE is a strictly bounded second run, not an iterative loop.
```

## Current conclusion

This file is a legacy API canary policy.

It must not be cited as proof that the active canonical weekly path uses the API/SDK runner or enforces the old output-token cap.