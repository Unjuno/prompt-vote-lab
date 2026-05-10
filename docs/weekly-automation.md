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

## Weekly run order

`Weekly Auto Run` runs in this order:

```text
1. checkout repository
2. set RUN_WEEK as week-<ISO-year>-W<ISO-week>
3. require data/support-unlocks/<week-id>.json
4. collect prompt proposal votes
5. insert no-change baseline
6. select eligible ranks
7. write weekly vote summary PR
8. if eligible candidates exist, require implementation secret
9. preflight the implementation run
10. create implementation PRs for eligible candidates
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

Both workflows use UTC ISO weeks.

`Weekly Auto Run` uses:

```text
RUN_WEEK=week-$(date -u +%G-W%V)
```

`Support Unlock Export` writes:

```text
data/support-unlocks/<ISO-year>-W<ISO-week>.json
```

The resolver normalizes these two forms:

```text
week-2026-W20 -> 2026-W20
```

The weekly workflow requires the matching support unlock file for its `RUN_WEEK`.

## Manual verification

Before trusting the scheduled path, run `Support Unlock Export` manually after `SPONSORS_GRAPHQL_TOKEN` is configured.

Example:

```text
week_id: 2026-W20
since: 2026-05-04T00:00:00Z
until: 2026-05-11T00:00:00Z
```

Expected public output:

```text
data/support-unlocks/2026-W20.json
```

Then run `Weekly Auto Run` manually and confirm that it reads the support unlock file before vote collection.

## Merge policy

Automation may create PRs, but it must not merge them.

`main` merge remains manual.

## Current production status

The schedules and gates are implemented.

Still required before calling this fully production-verified:

- configure `SPONSORS_GRAPHQL_TOKEN`
- run `Support Unlock Export` against live Sponsors data
- confirm public support unlock JSON validation passes
- run `Weekly Auto Run` end-to-end with the generated unlock file
