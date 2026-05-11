# Weekly automation

This document explains what runs automatically, when it runs, and what must exist before each weekly run can proceed.

## Short answer

Yes. `Weekly Auto Run` is scheduled to run every week.

```text
.github/workflows/weekly-auto-run.yml
cron: 23 0 * * 1
```

That means:

```text
Monday 00:23 UTC
Monday 09:23 JST
```

It can also be started manually with `workflow_dispatch`.

## Related scheduled workflow

Support unlock aggregation is a separate workflow.

```text
.github/workflows/support-unlock-export.yml
cron: 17 0 * * *
```

That means:

```text
every day 00:17 UTC
every day 09:17 JST
```

The support export workflow writes the anonymized aggregate file used by the weekly run:

```text
data/support-unlocks/<week-id>.json
```

On scheduled runs, support export defaults to the previous UTC ISO week. Manual `workflow_dispatch` inputs can still override `week_id`, `since`, and `until` for verification or backfill.

## Weekly run order

`Weekly Auto Run` runs in this order:

```text
1. checkout repository
2. set an initial RUN_WEEK
3. resolve the required support unlock file
4. prefer the previous UTC ISO week when its support unlock file exists
5. collect prompt proposal votes
6. insert no-change baseline
7. select eligible ranks
8. write weekly vote summary PR
9. if eligible candidates exist, require implementation secret
10. preflight the implementation run
11. create implementation PRs for eligible candidates
```

The support unlock file is required before vote collection and rank selection.

If the file is missing, the weekly workflow fails before selecting eligible ranks. It must not silently treat missing support data as 0 USD.

## Why support export is separate

Support aggregation and prompt implementation are different jobs.

Support export:

- reads GitHub Sponsors activity
- writes only anonymized weekly aggregate data
- validates public JSON before commit
- must not call the implementation model
- must not modify `lab/`

Weekly auto run:

- reads prompt Issues and reactions
- reads the weekly support unlock file
- creates vote summary PRs
- creates implementation PRs only when candidates are eligible
- must not merge PRs automatically

## Time-window caveat

The scheduled production path should process the UTC ISO week that just ended, not the week that has just started.

`Support Unlock Export` scheduled runs therefore default to:

```text
target = current UTC time - 7 days
```

This writes the previous ISO week by default.

`Weekly Auto Run` resolves the support unlock file before vote collection. When a previous-week support unlock file exists, the resolver writes this resolved week back into the job environment as:

```text
RUN_WEEK=week-<previous-ISO-year>-W<previous-ISO-week>
```

This prevents the Monday morning run from recording the newly started week by mistake.

`Support Unlock Export` writes:

```text
data/support-unlocks/<ISO-year>-W<ISO-week>.json
```

The resolver normalizes these two forms:

```text
week-2026-W20 -> 2026-W20
```

The weekly workflow requires the matching support unlock file for its resolved `RUN_WEEK`.

## Manual verification

The live no-eligible path has been verified.

Verified support export evidence:

```text
Support Unlock Export: PASS
data/support-unlocks/2026-W19.json
support_total_usd: 0.0
rank_2_unlocked: false
rank_3_unlocked: false
privacy flags: all false
```

Verified weekly automation evidence:

```text
Weekly Auto Run: PASS
runs/week-2026-W19-vote-summary.md
PR #243 merged
baseline_won: true
eligible_count: 0
implementation PR: none
```

Manual verification is still useful after token rotation, workflow changes, or backfills.

Example support export input:

```text
week_id: 2026-W19
since: 2026-05-04T00:00:00Z
until: 2026-05-11T00:00:00Z
```

Expected public output:

```text
data/support-unlocks/2026-W19.json
```

Then run `Weekly Auto Run` manually and confirm that it reads the support unlock file before vote collection.

## Merge policy

Automation may create PRs, but it must not merge them.

`main` merge remains manual.

## Current production status

Implemented and live-verified:

- `SPONSORS_GRAPHQL_TOKEN` can read support activity for the export path.
- `Support Unlock Export` can generate and validate an anonymized support unlock file.
- `Weekly Auto Run` can read that unlock file and create a no-eligible vote summary PR.
- The no-change baseline path can complete without creating an implementation PR.

Still not fully production-verified:

- eligible prompt -> implementation-agent preflight -> implementation-agent run -> lab-only implementation PR
