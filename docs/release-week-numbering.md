# Release week numbering

Prompt Vote Lab uses two different week concepts.

They must not be collapsed.

## Short answer

Public release numbering starts at:

```text
Release Week 1
```

Pre-release evidence does not count as Release Week 1.

Existing pre-release records such as `2026-W20` stay as historical evidence and must not be renamed.

## Internal week ID

Automation, support unlocks, run records, generated snapshots, and audit trails use UTC ISO week identifiers.

Examples:

```text
2026-W20
week-2026-W20
data/support-unlocks/2026-W20.json
runs/week-2026-W20-vote-summary.md
lab/comparisons/2026-W20/
```

These IDs are stable evidence keys. They are allowed to be technical and date-based.

Do not rewrite them to make the public release appear cleaner.

## Public release week label

Participant-facing release labels use a product-relative counter:

```text
Release Week 1
Release Week 2
Release Week 3
```

This counter starts only after public release.

The label is a display label. It does not replace the internal ISO week ID.

## Pre-release evidence

All evidence created before public release is pre-release evidence.

Examples:

```text
2026-W20 comparison dashboards
2026-W20 support unlock files
2026-W20 vote summary records
canonical canary evidence
manual verification evidence
```

These records may remain public, but public pages should not imply that they are Release Week 1.

Correct wording:

```text
Pre-release comparison: 2026-W20
Pre-release no-eligible observation: 2026-W20
Pre-release canonical canary evidence
```

Incorrect wording:

```text
Release Week 1: 2026-W20
Week 1 comparison: 2026-W20
First public week: 2026-W20
```

## Release Week 1 rule

Release Week 1 should be the first full scheduled weekly cycle after the public release announcement.

If public release happens in the middle of an active weekly cycle, the partial launch window should be treated as:

```text
Launch window
```

or:

```text
Release Week 0
```

It should not be counted as Release Week 1 unless the maintainer deliberately chooses to release exactly at the start of the weekly cycle.

The default weekly cycle is documented in `docs/weekly-automation.md`.

## Mapping table

After release, maintainers may add a mapping table that connects public labels to internal evidence IDs:

```text
Release Week 1 -> 2026-Wxx
Release Week 2 -> 2026-Wyy
Release Week 3 -> 2026-Wzz
```

This table is an index for readers. It must not rename historical paths.

## Display rule

User-facing pages should prefer both labels when space allows:

```text
Release Week 1 · internal ID 2026-Wxx
```

Pre-release pages should say:

```text
Pre-release · internal ID 2026-W20
```

## Do not do this

Do not:

```text
rename data/support-unlocks/2026-W20.json
rename runs/week-2026-W20-vote-summary.md
rename lab/comparisons/2026-W20/
rewrite PR titles to hide pre-release week IDs
change historical evidence labels to make them look current
```

The repository has already chosen evidence preservation over cosmetic cleanup.

## Implementation implication

Future generator work should add release labels as metadata or display aliases.

It should not change the internal week ID format used by automation.

Expected future data shape:

```text
internal_week_id: 2026-Wxx
public_release_label: Release Week 1
release_phase: public
```

For pre-release records:

```text
internal_week_id: 2026-W20
public_release_label: Pre-release
release_phase: pre-release
```