# Stop rules

This document defines hard stop conditions for implementation-agent runs.

The goal is to prevent uncontrolled API usage and undefined system behavior.

## Immediate stop conditions

Stop the system immediately if any of the following occur:

```text
more than one implementation-agent attempt for a single candidate
SDK retry is enabled or triggered
fallback model is used
model other than gpt-5-nano is used
implementation runs when eligible_count = 0
implementation PR appears during no-eligible run
changes outside lab/ are made
static-site-check fails
safety-check fails
workflow attempts auto-merge
```

## Conditional stop conditions

Stop unless explicitly approved if:

```text
output is too large or complex
multiple files changed without clear reason
behavior deviates from prompt intent
```

## Resume condition

The system may resume only after:

```text
root cause identified
fix applied without API calls
preflight passes
freeze audit passes
manual approval
```

## Principle

```text
Do not retry blindly.
Do not continue without understanding failure.
```
