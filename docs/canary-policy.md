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

## Continuation rule

A continuation is not a retry.

A continuation may be considered only if:

```text
the first canary produced useful partial progress
the PR changed lab/ only
safety-check passed
static-site-check passed
the next step is explicit
human review approves a second run
```

Otherwise, stop.
