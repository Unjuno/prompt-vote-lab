# Operator runbook

This runbook is for maintainers operating Prompt Vote Lab.

It describes what to check, what to merge, what to stop, and what must never be automated.

## Current production status

Verified live paths:

```text
Support Unlock Export -> data/support-unlocks/2026-W19.json
Weekly Auto Run -> runs/week-2026-W19-vote-summary.md
no-change baseline won -> no implementation PR created
```

Not yet verified:

```text
eligible prompt -> implementation-agent preflight -> implementation-agent run -> lab-only implementation PR
```

## Weekly operating loop

Run or confirm these in order:

```text
1. Support Unlock Export
2. Weekly Auto Run
3. vote summary PR review
4. implementation PR review, only if created
5. Public Results Export refresh
6. GitHub Pages sanity check
```

## Normal schedule

| Workflow | Schedule | JST | Expected output |
|---|---:|---:|---|
| `Support Unlock Export` | daily 00:17 UTC | daily 09:17 JST | `data/support-unlocks/<week-id>.json` |
| `Weekly Auto Run` | Monday 00:23 UTC | Monday 09:23 JST | `runs/week-<week-id>-vote-summary.md` PR |

The scheduled path should process the previous completed UTC ISO week.

## Manual support export verification

Use this after token rotation or support automation changes.

```text
Actions -> Support Unlock Export -> Run workflow
```

Example:

```text
week_id: 2026-W19
since: 2026-05-04T00:00:00Z
until: 2026-05-11T00:00:00Z
```

Expected result for zero support:

```text
support_total_usd: 0.0
rank_2_unlocked: false
rank_3_unlocked: false
privacy flags: all false
```

## Manual weekly run verification

Use this after support export has produced the matching support unlock file.

```text
Actions -> Weekly Auto Run -> Run workflow
```

Expected no-eligible result:

```text
vote summary PR is created
support unlock file is referenced
baseline_won: true
eligible_count: 0
implementation PR: none
```

## Merge policy

Automation may create PRs.

Automation must not merge PRs.

Merge only after checking:

```text
PR scope is correct
changed files are expected
CI or internal workflow checks passed
public evidence is not weakened
no forbidden secret or identity data is present
```

## Vote summary PR review

A vote summary PR may be merged when:

```text
changed file is under runs/
week id is correct
support unlock file path is correct
baseline and eligible metadata are plausible
no implementation files are changed
```

Reject or fix if:

```text
week id points at the newly started week instead of the completed week
support unlock source is missing
support source silently falls back to manual or 0 without file evidence
summary modifies lab/, workflows, scripts, docs, rules, or data unexpectedly
```

## Implementation PR review

An implementation PR may be considered only when:

```text
it was created from an eligible prompt
changed files are only lab/index.html, lab/style.css, and/or lab/app.js
safety-check passed before PR creation
static-site-check passed before PR creation
diff is small enough to review manually
no external scripts, network calls, cookies, trackers, login, payment, eval, or unsafe dynamic code are added
```

Do not merge if:

```text
files outside lab/ changed
workflow, rules, docs, runs, formal, or scripts changed
model appears to have ignored the selected prompt
implementation is too large to review comfortably
reviewer cannot explain the diff
safety/static checks failed or were skipped
```

## Support unlock failure handling

| Failure | Likely cause | Action |
|---|---|---|
| `test -n "$GH_TOKEN"` fails | `SPONSORS_GRAPHQL_TOKEN` missing or empty | Check repository secret name |
| 401 | invalid or expired token | Rotate token |
| 403 | insufficient token permission | Recreate token with the minimum working scope |
| GraphQL field error | sponsors query permission or schema issue | Inspect `Fetch support activity` log |
| privacy validation fails | public JSON contains forbidden key/value or validator bug | Do not commit; inspect generated JSON shape |
| no commit created | generated file unchanged | Check whether the target file already exists with same content |

## Weekly Auto Run failure handling

| Failure | Likely cause | Action |
|---|---|---|
| missing support unlock file | Support Unlock Export has not produced the week file | Run/export the correct week first |
| wrong week id | resolver or manual window mismatch | Check `RUN_WEEK` and support unlock source |
| no eligible candidates | baseline won or no votes | Merge vote summary if correct |
| implementation secret missing | eligible candidates exist but implementation API secret is absent | Configure implementation secret or stop |
| preflight failure | model/token/retry/candidate policy mismatch | Fix policy mismatch; do not bypass preflight |
| generated no lab changes | model failed to make useful change | Record failure; do not auto-rerun |
| safety/static check failure | unsafe or invalid output | Stop and review; do not merge |

## Public results and Pages checks

After merging evidence PRs, confirm:

```text
Public Results Export completed successfully
queued/in-progress workflow runs are not committed as current evidence
GitHub Pages deployed or a later Pages deployment superseded a cancelled one
lab/comparisons pages still have one card per rank
lab/history page still renders
```

## Token handling

`SPONSORS_GRAPHQL_TOKEN` is only for reading GitHub Sponsors activity.

It must not need repository write permission.

Repository writes are performed by the workflow `GITHUB_TOKEN`.

Implementation-agent API secrets are separate and must not be reused as Sponsors tokens.

## Reset and cleanup policy

Do not delete public evidence casually.

Protected public evidence includes:

```text
data/public-results.json
data/public-results.md
data/support-unlocks/*.json
runs/*.md
lab/comparisons/**
lab/history/**
merged PRs and Issues
```

Development cleanup scripts must default to dry-run and must refuse to delete protected public evidence paths.

## Deferred configuration decisions

`MAX_OUTPUT_TOKENS` remains at the current configured limit until the system is complete.

Do not change it during the current stabilization phase.

Revisit only after:

```text
participant docs are complete
operator runbook is complete
reset script is safe
implementation PR path has passed at least one live E2E run
review burden and diff size are known
```

## Stop rule

If uncertain, stop before spending a model call or merging a PR.

Failed runs are experiment data. Hidden retries are not allowed.
