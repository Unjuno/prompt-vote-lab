# First Canary Readiness Checklist

Use this checklist immediately before the first real implementation-agent canary.

Do not run the canary unless every required item is PASS.

## Required repository state

```text
[ ] open PRs: 0
[ ] remote branches: main only, before creating the canary branch
[ ] latest main includes docs/first-canary-prompt.md
[ ] latest main includes formal/Canary.lean
[ ] latest main includes scripts/test_canary_policy_alignment.py
[ ] latest main includes runs/dry-run-001-evidence-review.md with final_decision: PASS
```

## Required CI state

```text
[ ] Pre-API Freeze Audit: PASS
[ ] Script Check: PASS
[ ] Lean Proof Test: PASS
[ ] Implementation Preflight Test: PASS
[ ] Lab PR Scope Check: PASS
[ ] Static Site Check: PASS
```

## Required evidence state

```text
[ ] Weekly Auto Run no-eligible production path: PASS
[ ] Evidence Pipeline Dry Run source=fixture: PASS
[ ] Evidence Pipeline Dry Run source=live: PASS
[ ] live evidence human review: PASS
[ ] HN draft is not externally posted
```

## Required canary configuration

```text
[ ] model: gpt-5-nano
[ ] candidate count: 1
[ ] attempts per candidate: 1
[ ] SDK max_retries: 0
[ ] API call limit per candidate: 1
[ ] max output tokens: 5000
[ ] fallback model: none
[ ] auto-merge: disabled
[ ] external publishing: disabled
```

## Required prompt

Use only:

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

## Required output limit

The canary may create one implementation PR only.

Allowed changed files:

```text
lab/index.html
lab/style.css
lab/app.js
```

Forbidden changed files:

```text
.github/**
docs/**
rules/**
runs/**
formal/**
scripts/**
package files
configuration files
```

## Immediate stop conditions

Stop and do not merge if any of these occur:

```text
more than one model attempt
SDK retry is enabled or triggered
fallback model is used
files outside lab/ are changed
network calls are added
external scripts are added
cookies are added
analytics is added
login or payment behavior is added
eval is added
dynamic new Function uses user-controlled or external data
workflow attempts to auto-merge
CI fails
PR is too large to review comfortably
```

## PASS decision after PR creation

The canary path is considered PASS only if:

```text
one PR is created
changed files are inside lab/
diff is small and reviewable
safety-check passes
static-site-check passes
Lab PR Scope Check passes
no retry occurs
no fallback occurs
no auto-merge occurs
manual review remains required
```

## Non-goals

Do not attempt these in the first canary:

```text
persona route UI
leaderboard
ranking page
supporter UI
weekly report UI
external posting
GitHub Sponsors integration
large redesign
backend behavior
```

## Final command discipline

Before pressing the workflow run button, say explicitly:

```text
This is the first real implementation-agent canary.
The goal is execution-path verification, not product expansion.
```
