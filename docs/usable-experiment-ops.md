# Usable experiment operations

## Status

Prompt Vote Lab is currently usable as a manual canary experiment system.

It is not yet a fully automatic weekly production system.

Current usable loop:

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

## 2. Normal fixed-Issue run

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

## 3. Blocked Issue behavior

A blocked Issue must not run as a normal implementation candidate.

Expected behavior without exception:

```text
issue-safety:blocked
no authorized-canary
→ execution gate STOP
→ Codex does not run
→ PR is not created
```

## 4. Authorized canary behavior

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

## 5. Manual merge rule

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

## 6. Recording a completed run

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

Prompt Vote Lab supports comparison runs, but they are still manual and evidence-oriented.

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

Use this order before expanding to selected weekly automation:

```text
1. Clear Issue normal-path run.
2. Clear Issue second normal-path run.
3. Rank 2 comparison dry-run or controlled live run.
4. Rank 3 comparison dry-run or controlled live run.
5. Disguised unsafe Issue test: compatibility wording that tries to add external scripts.
6. Disguised unsafe Issue test: evidence wording that tries to modify docs/ or runs/.
7. Weekly selected-Issue ingestion only after the above evidence is recorded.
```

## Current non-goals

Do not add these yet:

```text
auto-merge
automatic fallback to a stronger model
automatic retry after a failed model run
automatic vote-winner execution without additional recorded evidence
automatic reputation scoring
external publication
```

## Usable state definition

The repository is usable for manual canary experiments when all of these hold:

```text
Issue Safety Scan can label and comment on Issues.
Manual rescan works.
009 fixed-Issue run can create a PR for clear Issues.
Blocked Issues stop before Codex unless authorized-canary is present.
Authorized canary run can create a lab-only PR.
Maintainer manually reviews and merges or closes the PR.
runs/ record is created after merge.
```

The repository is not considered production-ready until normal clear-Issue runs and comparison runs have repeated recorded success.
