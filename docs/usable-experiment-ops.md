# Usable experiment operations

## Status

Prompt Vote Lab is currently usable as a canonical weekly default-on experiment system with manual review and manual canary operations still available.

It is not yet a fully production-proven weekly system because the first ordinary post-default-on scheduled run still needs operational observation.

Current usable canonical loop:

```text
Issue submission
→ Issue safety scan
→ support unlock export
→ weekly vote collection
→ no-change baseline comparison
→ vote summary PR
→ canonical selected-prompt implementation PR, only if eligible
→ manual review
→ manual merge or close
→ runs/ record
→ public results export
```

Manual canary loop, still available for controlled experiments:

```text
Issue submission
→ Issue safety scan
→ optional manual rescan
→ fixed-Issue 009 runtime scan
→ execution gate
→ Codex implementation PR
→ manual review
→ manual merge or close
→ runs/ record
```

## What is currently usable

### 1. Issue submission and safety feedback

When an Issue is opened, edited, or reopened, the Issue Safety Scan workflow can classify it and post visible feedback.

If the event feedback is not visible, a maintainer can manually run:

```text
Actions → Issue Safety Scan → Run workflow → issue_number=<issue>
```

Expected labels:

```text
issue-safety:clear
issue-safety:review
issue-safety:blocked
issue-safety:submission-detected
issue-safety:runtime-detected
```

Status labels are mutually exclusive:

```text
issue-safety:clear
issue-safety:review
issue-safety:blocked
```

Phase labels are cumulative evidence:

```text
issue-safety:submission-detected
issue-safety:runtime-detected
```

## 2. Weekly default-on path

The weekly path is implemented and uses the canonical selected-prompt runner by default for eligible implementation candidates.

Expected no-eligible behavior:

```text
support unlock resolved
vote collection completed
no-change baseline wins or eligible_count is 0
vote summary PR is created
no implementation-agent attempt is made
Codex does not run
```

Expected eligible behavior:

```text
support unlock resolved
vote collection completed
real prompt beats the no-change baseline
canonical selected-prompt runner is selected by default
implementation PR is created
final writable files: lab/index.html, lab/style.css, lab/app.js
manual review: required
merge: manual only
```

The first ordinary post-default-on scheduled run still needs operational observation before calling the system fully production-proven.

## 3. Normal fixed-Issue run

A normal fixed-Issue run should use an Issue that is:

```text
issue-safety:clear
```

Run path:

```text
Actions → Codex Fixed Issue Instruction Canary Run → Run workflow → issue_number=<issue>
```

Expected behavior:

```text
fixed-Issue 009 runtime scan: clear
execution gate: PASS
Codex run: one attempt
PR: created
final writable files: lab/index.html, lab/style.css, lab/app.js
manual review: required
merge: manual only
```

## 4. Blocked Issue behavior

A blocked Issue must not run as a normal implementation candidate.

Expected behavior without exception:

```text
issue-safety:blocked
no authorized-canary
→ execution gate STOP
→ Codex does not run
→ PR is not created
```

## 5. Authorized canary behavior

A blocked Issue can be run only as a controlled canary if a maintainer explicitly adds:

```text
authorized-canary
```

Expected behavior with exception:

```text
issue-safety:blocked
authorized-canary
→ fixed-Issue 009 runtime scan: blocked but authorized
→ execution gate PASS
→ Codex runs once
→ PR is created
→ manual review: required
→ merge remains manual
```

This is for safety-boundary experiments only. It is not a normal implementation path.

## 6. Manual merge rule

The repository intentionally does not use automatic merge for the current experiment phase.

Every implementation PR must be reviewed manually.

Required review points:

```text
changed files are limited to lab/index.html, lab/style.css, lab/app.js
no external script/CDN
no network calls
no cookie access
no iframe
no eval or unsafe dynamic code
PR body records safety-check/static-site-check status
Issue labels and comments match the intended run class
```

## 7. Recording a completed run

After merge, add a `runs/` record.

Minimum record fields:

```text
Issue number
PR number
merge commit
model-policy version
runner path
candidate rank
vote count
selection rule
Issue safety status
execution gate result
changed files
manual merge decision
known limitations
```

A run is not considered closed until the record exists.

## Comparison experiments

Prompt Vote Lab supports comparison runs. The weekly path can unlock Rank 2 and Rank 3 comparison candidates only after the no-change baseline loses.

Comparison candidates:

```text
rank-1: normal weekly run candidate
rank-2: optional support-unlocked comparison run
rank-3: optional support-unlocked comparison run
```

Support thresholds are defined in `docs/support-policy.md` and `rules/support-unlocked-runs-v1.1.md`.

Current comparison-run rule:

```text
Rank 1, rank 2, and rank 3 must use the same implementation model policy, rules, input context, retry policy, fallback policy, and final writable file scope within the same comparison set.
```

Current implementation model policy:

```text
model-policy-v1.1: gpt-5.4-nano
```

Comparison runs do not automatically affect the inherited lab state.

Only merged PRs affect the future base state.

Rank 2 and rank 3 do not automatically replace rank 1 if rank 1 fails.

## Recommended next experiment sequence

Use this order before expanding beyond the current release candidate:

```text
1. Observe the first ordinary post-default-on no-eligible weekly run.
2. Confirm vote summary PR creation without a Codex attempt when eligible_count is 0.
3. Confirm support unlock export for the completed week.
4. Keep fixed-Issue canary runs available only for controlled safety-boundary experiments.
5. Confirm the first natural eligible canonical implementation PR after release.
6. Record run evidence and public results before closing weekly Issues.
```

## Current non-goals

Do not add these yet:

```text
auto-merge
automatic fallback to a stronger model
automatic retry after a failed model run
automatic reputation scoring
external publication
```

## Usable state definition

The repository is usable for the current release candidate when all of these hold:

```text
Issue Safety Scan can label and comment on Issues.
Manual rescan works.
Support Unlock Export writes anonymized aggregate support data.
Weekly Auto Run uses the canonical selected-prompt runner by default for eligible candidates.
No-eligible weeks stop after vote summary and do not run Codex.
Fixed-Issue canary runs remain available for controlled experiments.
Blocked Issues stop before Codex unless authorized-canary is present.
Authorized canary run can create a lab-only PR.
Maintainer manually reviews and merges or closes implementation PRs.
runs/ record is created after merge.
Public Results Export updates the public result surfaces.
```

The repository is not considered fully production-proven until at least the first ordinary post-default-on weekly run is observed and the first natural eligible canonical implementation PR is reviewed.