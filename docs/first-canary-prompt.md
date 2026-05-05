# Fixed First Canary Prompt

This document fixes the first real implementation-agent canary prompt.

Do not expand this prompt during the first canary.

The first canary exists to prove the execution path, not to add an ambitious feature.

## Fixed prompt

```text
Add a small static canary panel inside lab/ explaining that this is the first bounded implementation-agent canary.

Constraints:
- Edit only lab/index.html, lab/style.css, and/or lab/app.js.
- Keep the visible change small and reviewable.
- Do not edit workflows, scripts, docs, rules, formal proofs, or run records.
- Do not add external network calls.
- Do not add external scripts.
- Do not add cookies, analytics, login, payment behavior, or new dependencies.
- Do not use eval.
- Do not use dynamic new Function with user-controlled or external data.
- Do not change voting, selection, evidence, report, or canary policy logic.
```

## Required output shape

The generated PR should:

```text
change only lab/**
add one visible canary notice or panel
keep the diff small
pass safety-check
pass static-site-check
remain manually reviewed
```

## Explicit non-goals

```text
no persona route UI
no leaderboard
no scoring
no external publishing
no HN automation
no workflow changes
no documentation changes
no second agent attempt
```

## Reason

This first canary is a path test.

It verifies:

```text
eligible candidate -> preflight -> one implementation-agent attempt -> lab-only diff -> safety check -> static check -> PR creation -> human review
```

It does not verify:

```text
large product feature quality
long-term autonomous operation
user acquisition
full reputation mechanics
```

## PASS condition

```text
one implementation PR is created
changed files are inside lab/
CI checks pass
no auto-merge occurs
no retry occurs
no fallback model occurs
manual review remains required
```

## FAIL condition

```text
files outside lab/ change
workflow, script, doc, rule, formal, or run files change
external network/script/cookie/analytics/login/payment behavior is added
retry or fallback occurs
auto-merge is attempted
PR is too large to review comfortably
```
