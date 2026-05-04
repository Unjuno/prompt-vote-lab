# Canary policy

This policy defines the first paid implementation-agent API run.

The canary exists to test the full production path with the smallest useful change.

It is not a feature expansion phase.

## Entry condition

A real API canary may start only after:

```text
Pre-API Freeze Audit: PASS
Weekly Auto Run no-eligible path: PASS
open verification PRs: none
implementation-agent secret: configured
```

## Allowed first canary prompt

The first canary prompt must be small, visible, and easy to review.

Recommended prompt:

```text
Add a small visible canary panel to the lab page explaining that this is the first bounded implementation-agent test. Keep the change static, local, and inside lab/ only.
```

## Hard limits

The canary must use:

```text
model: gpt-5-nano
candidate count: 1
attempts per candidate: 1
SDK max_retries: 0
fallback model: none
max_output_tokens: 12000
automatic merge: no
```

## Allowed output

The canary may create one implementation PR changing only:

```text
lab/index.html
lab/style.css
lab/app.js
```

The PR must pass:

```text
safety-check
static-site-check
```

## Forbidden output

The canary must fail review if it:

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
