# Release readiness review

This document is the release-facing review page for Prompt Vote Lab.

It answers three practical questions:

```text
Is the current system secure enough for a static public experiment?
Is there a participant path from first visit to useful action?
Is there a live preview path for the lab and recorded outcomes?
```

It is not a replacement for the canonical status contract. Canonical, legacy, default-on, auto-merge, and release-gate status remains owned by `docs/canonical-status-drift-check.md`.

## Current judgment

```text
security posture: PASS
participant journey: PASS
live preview: PASS
release blocker: none known from static review
ordinary default-on weekly no-eligible observation: PASS
```

The first ordinary post-default-on weekly no-eligible run has been observed and recorded.

Evidence:

```text
support unlock file: data/support-unlocks/2026-W20.json
vote summary PR: #333
merged run record: runs/week-2026-W20-vote-summary.md
baseline_won: true
eligible_count: 0
implementation-agent attempt: none
auto-merge: disabled
manual review: performed
```

This does not prove the next natural eligible weekly implementation will succeed. It does prove that the ordinary default-on no-eligible path resolves support data, records the weekly result, and stops before implementation-agent execution when the baseline wins.

## Security review

### Static-site boundary

Current public surfaces are static pages and repository-rendered documents.

The lab page sets a restrictive Content Security Policy:

```text
default-src 'self'
script-src 'self'
style-src 'self'
img-src 'self' data:
connect-src 'none'
frame-src 'none'
object-src 'none'
base-uri 'none'
form-action 'none'
```

Security consequence:

```text
external network calls are blocked by policy
iframes are blocked
forms are blocked
external scripts are blocked
object/embed surfaces are blocked
```

### Runtime behavior

Current `lab/app.js` only records that JavaScript is enabled:

```text
document.documentElement.dataset.js = 'enabled'
```

Current lab runtime does not fetch, post, track, authenticate, take payment, or store cookies.

### Repository guardrails

Implementation-agent changes are constrained by multiple layers:

```text
editable files: lab/index.html, lab/style.css, lab/app.js
changed-file guard: required
safety-check: required
static-site-check: required
manual review: required
auto-merge: disabled
```

The static UI rule forbids:

```text
fetch
XMLHttpRequest
WebSocket
EventSource
eval
document.cookie
external scripts
external APIs
trackers
login forms
payment forms
password fields
```

### Canonical runner boundary

The current canonical implementation runner is the Docker/Codex selected-prompt task-packet path:

```text
/work:rw
/task:ro
/codex-runtime:rw
repo root not mounted
OPENAI_API_KEY unset before codex exec
copyback restricted to lab/index.html, lab/style.css, lab/app.js
```

Canonical implementation evidence must include:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

### Legacy API/SDK isolation

The legacy API/SDK path remains present but is non-canonical.

It is isolated by wording and gates:

```text
first-canary workflow requires confirm_legacy_api_canary: RUN_LEGACY_API_CANARY
ordinary week-* legacy fallback requires PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true
```

The weekly canonical feature flag alone must not silently spend a legacy API/SDK attempt.

### Security limitations

The system is not a general secure application platform.

It does not provide:

```text
user accounts
server-side authorization
database isolation
private submissions
secret handling by the browser
moderation beyond GitHub and repository workflows
```

That is acceptable because the current product is a public static experiment, not a private app.

## Participant journey review

The intended participant path exists.

### First visit

Root landing page gives the high-level game model and primary actions:

```text
Submit a prompt
Vote on prompts
Watch the lab
Read rules
```

### Lowest-friction action

The participant docs correctly say that the first useful action is voting, not writing a prompt:

```text
1. Open Issues labeled prompt-proposal.
2. Read the prompt.
3. Add 👍 only if you trust it enough to spend one bounded implementation-agent attempt.
4. Submit your own prompt after you understand what good prompts look like.
```

### Lab page path

The lab page exposes participant navigation:

```text
Vote on prompt Issues
Live previews
Submit prompt
Participant guide
Latest comparison
History
Public results
Weekly runs
```

This is enough for a new participant to:

```text
understand the game
see the current lab
vote with 👍
submit a prompt
inspect prior outcomes
watch weekly automation
```

### Remaining journey weakness

The journey depends on GitHub.

Users without GitHub accounts can read the project and live previews, but they cannot vote with reactions or submit Issues.

This is acceptable for the current GitHub-native release.

## Live preview review

Live preview exists.

The repository is designed for GitHub Pages with:

```text
branch: main
folder: /
```

Useful preview paths are:

```text
/       stable landing page
/lab/   current accepted lab UI
/lab/comparisons/<week>/   comparison dashboard
/lab/comparisons/<week>/rank-<n>/   rank output preview
/lab/history/   historical state flow
```

The lab page already includes a `Live previews` section with links to:

```text
current accepted lab
2026-W20 rank 1 output
2026-W20 rank 2 output
2026-W20 rank 3 output
2026-W20 comparison dashboard
history
```

## Release blockers

No release blocker is known from this static review and the first ordinary default-on no-eligible observation.

Still required before claiming the next natural eligible weekly implementation path is production-proven:

```text
observe a natural eligible weekly implementation run
confirm canonical Docker/Codex selected-prompt runner evidence
confirm bounded lab-only diff
confirm diagnostics and public bundle artifacts
```

## Release decision rule

Use this decision rule:

```text
PASS if:
  static security boundary remains intact
  participant journey links remain visible
  live preview links render
  ordinary default-on weekly no-eligible run is observed
  manual review remains required
  auto-merge remains disabled

FAIL if:
  any external runtime dependency is added
  lab begins calling network APIs
  cookies, login, payment, iframe, or tracking behavior appears
  implementation runs when no eligible candidate exists
  legacy API/SDK runner is reached without explicit diagnostic gate
  auto-merge is enabled

UNCERTAIN if:
  generated evidence is stale or missing
  GitHub Pages deployment status is unknown
```

## Current next action

Do not delete the legacy fallback yet.

Next safe action:

```text
observe a natural eligible weekly implementation run when one occurs
then decide whether to retire the legacy fallback
```