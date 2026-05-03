# agent-run-policy-v1.0

## Purpose

Prompt Vote Lab votes on prompts for an AI coding agent/Codex-style implementation run.

This rule defines how those runs are bounded without killing useful long-running ideas.

## Core distinction

The project does not vote on an API call.

The project votes on a prompt candidate.

If the prompt passes the 20-vote gate, that prompt may be given to a constrained implementation agent.

```text
Prompt → 20-vote gate → agent PR → inherited lab state
```

## Inherited lab state

Implementation attempts are cumulative.

Each weekly attempt starts from the current `main` branch version of `lab/`, including previously merged lab changes.

```text
current main lab state
→ selected prompt is applied
→ implementation PR is opened
→ if merged, that result becomes the next base state
```

Rejected, failed, unsafe, and unmerged comparison PRs do not become the next base state.

## One attempt, not infinite retry

Each automated implementation attempt is one bounded agent run for one candidate.

Default guardrails:

```text
agent attempts per candidate per workflow run: 1
automatic retry: no
automatic fallback model: no
automatic merge: no
SDK max_retries, when an SDK is used: 0
```

If the attempt fails, the failure is recorded. It is not hidden by automatically trying again.

## Continuation is allowed when explicit

A good prompt may produce useful partial progress and deserve more work.

That should be handled as a continuation run, not as a hidden retry.

A continuation run must be explicit and reviewable.

Allowed continuation reasons:

- the agent produced useful partial progress
- the PR passes safety and static-site checks
- the next step is clear
- the change remains inside `lab/`
- the continuation is recorded as a separate run or PR

Do not use continuation to hide failure, bypass review, or repair unsafe output silently.

## Run states

Useful agent-run terminal or intermediate states:

- `completed`: usable PR opened
- `partial`: useful but incomplete result
- `continued`: explicit follow-up run is justified
- `stalled`: long or costly run with little progress
- `budget-capped`: stopped by a configured budget or time cap
- `unsafe`: violated a safety boundary
- `failed`: failed before producing reviewable output

## What must stay forbidden

The agent must not:

- edit outside `lab/`
- add external scripts or CDNs
- perform hidden network calls
- use cookies or trackers
- add login or payment behavior
- use `eval`
- use `new Function(...)` with user input, URL data, stored local data, imported JSON, GitHub Issue text, or any external source
- merge its own PR
- weaken safety rules to pass itself

## What is allowed

The agent may:

- create ordinary helper functions inside `lab/app.js`
- reorganize local JavaScript for clarity
- use local state with `localStorage`, `sessionStorage`, or `IndexedDB`
- implement JSON export/import locally
- use controlled `new Function(...)` only when the function body is fixed by repository-authored code and small enough to review
- create a static UI prototype for otherwise unsupported ideas

Prefer ordinary functions when they are sufficient.

## Rationale

The goal is not to suppress good prompts.

The goal is to separate valuable continuation from unbounded spending, hidden retries, unsafe behavior, and accidental resets of the cumulative lab state.
