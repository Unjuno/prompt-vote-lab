# Weekly Snapshot Specification

## Purpose

A weekly snapshot freezes the vote state at the official cutoff time.

The snapshot is the evidence used to decide whether a prompt is selected for the weekly implementation run.

Do not use the live GitHub issue state after cutoff as the decision source. Reactions can change after the cutoff.

## Canonical path

```text
data/snapshots/week-XXX.json
```

Example:

```text
data/snapshots/week-001.json
```

## Time policy

Default cutoff:

```text
Monday 00:00 Asia/Tokyo
```

In UTC cron form:

```text
0 15 * * 0
```

Reason: Sunday 15:00 UTC equals Monday 00:00 in Japan Standard Time.

If this cutoff changes, update this document and record the policy version in the weekly run log.

## Input source

The snapshot generator reads:

- open GitHub issues labeled `prompt-proposal`
- public `+1` reactions on those issues
- issue title
- issue number
- issue author login
- issue URL
- issue created_at and updated_at
- issue body sections when available

## Top prompt selection

Sort candidates by:

1. higher vote count
2. older issue number as deterministic tie-breaker

Do not use updated time as a tie-breaker for official weekly selection.

Reason: edited issues should not gain or lose rank because they were edited later.

## Selection rule

Parameters:

```text
no_change_baseline = 5
required_margin = 2
minimum_total_votes = 5
```

A prompt is selected only if:

```text
top_prompt_votes >= no_change_baseline + required_margin
```

and:

```text
total_votes >= minimum_total_votes
```

With the initial parameters, the top prompt must have at least 7 votes and the weekly vote must have at least 5 total votes.

## Snapshot schema

```json
{
  "schema_version": "snapshot-v1.0",
  "week": "001",
  "snapshot_at": "2026-05-11T00:00:00+09:00",
  "cutoff_timezone": "Asia/Tokyo",
  "source": "github-issues-reactions",
  "repository": "Unjuno/prompt-vote-lab",
  "selection_rule": {
    "rule": "selection-v1.0",
    "no_change_baseline": 5,
    "required_margin": 2,
    "minimum_total_votes": 5
  },
  "total_votes": 15,
  "top_prompt_votes": 8,
  "decision": "selected",
  "selected_issue": 3,
  "top_prompts": [
    {
      "rank": 1,
      "issue": 3,
      "title": "Show weekly runs as a timeline",
      "author": "Unjuno",
      "votes": 8,
      "url": "https://github.com/Unjuno/prompt-vote-lab/issues/3",
      "created_at": "2026-05-02T00:55:32Z",
      "updated_at": "2026-05-02T01:32:25Z"
    }
  ],
  "all_candidates": [
    {
      "issue": 3,
      "title": "Show weekly runs as a timeline",
      "author": "Unjuno",
      "votes": 8,
      "url": "https://github.com/Unjuno/prompt-vote-lab/issues/3"
    }
  ]
}
```

## Required invariants

- `top_prompts.length <= 3`
- `top_prompts` is sorted by descending votes
- ties are resolved by ascending issue number
- `top_prompt_votes` equals `top_prompts[0].votes` when `top_prompts` is non-empty
- `selected_issue` equals `top_prompts[0].issue` when `decision = "selected"`
- `selected_issue` is `null` when `decision = "no_run"`
- no file under `lab/` is modified by the snapshot generator

## Decision values

Allowed `decision` values:

- `selected`
- `no_run`
- `invalid`

Use `invalid` only when data retrieval failed or the snapshot could not be trusted.

## Immutability policy

A snapshot file should not be edited after it is used for a weekly run.

If a mistake is discovered, create a correction file:

```text
data/snapshots/week-001.correction-001.json
```

The run log must link both the original snapshot and the correction.

## LP display

The landing page may display the current top 3 prompts, but that display is not the official selection record.

The official weekly record is the snapshot file.

## Contributor credit

A contributor receives accepted-prompt credit only when:

- the contributor authored the selected issue
- the selected issue comes from a valid weekly snapshot
- the run log marks the weekly result as `merged` or another explicitly accepted status

A contributor should not receive accepted-prompt credit merely for being rank 1 if the run is rejected or invalidated.
