# Legacy first API canary readiness checklist

This checklist is retained for the historical API/SDK implementation-agent canary path.

It is not the active readiness checklist for the current canonical weekly selected-prompt runner.

Current active status:

```text
canonical selected-prompt runner: default-on
runner family: Docker/Codex selected-prompt task-packet runner
legacy API/SDK first-canary workflow: present, non-canonical
manual review: required
auto-merge: disabled
```

Do not run the legacy first-canary workflow as a normal release step.

## Historical repository state

```text
[ ] open PRs: 0
[ ] remote branches: main only, before creating the canary branch
[ ] latest main includes docs/first-canary-prompt.md
[ ] latest main includes formal/Canary.lean
[ ] latest main includes scripts/test_canary_policy_alignment.py
[ ] latest main includes runs/dry-run-001-evidence-review.md with final_decision: PASS
```

## Historical CI state

```text
[ ] Pre-API Freeze Audit: PASS
[ ] Script Check: PASS
[ ] Lean Proof Test: PASS
[ ] Implementation Preflight Test: PASS
[ ] Lab PR Scope Check: PASS
[ ] Static Site Check: PASS
```

## Historical evidence state

```text
[ ] Support Unlock Export live path: PASS
[ ] Weekly Auto Run no-eligible live path: PASS
[ ] Evidence Pipeline Dry Run source=fixture: PASS
[ ] Evidence Pipeline Dry Run source=live: PASS
[ ] live evidence human review: PASS
[ ] HN draft is not externally posted
```

## Legacy API canary configuration

These fields describe the old API/SDK path. They must not be cited as active canonical runner requirements.

```text
[ ] model: gpt-5.4-nano
[ ] candidate count: 1
[ ] attempts per candidate: 1
[ ] SDK max_retries: 0
[ ] API call limit per candidate: 1
[ ] legacy max output tokens: 5000
[ ] fallback model: none
[ ] auto-merge: disabled
[ ] external publishing: disabled
```

The current canonical Codex CLI runner records:

```text
output_token_cap_enforced: false
```

Do not claim a canonical run is output-token-capped unless a future runner contract proves runtime enforcement.

## Historical prompt

The legacy first canary used:

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

## Output limit

The legacy API canary could create one implementation PR only.

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

The legacy canary path was considered PASS only if:

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

Do not attempt these through the legacy first canary:

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

## Current conclusion

This is a legacy API canary readiness checklist. It is not a current release checklist.

For current release operations, use:

```text
docs/weekly-automation.md
docs/operator-runbook.md
docs/current-codex-implementation-path.md
docs/canonical-status-drift-check.md
```