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

The generator also inserts a virtual no-change baseline candidate.

## Top prompt selection

Sort real prompt candidates by:

1. higher vote count
2. older issue number as deterministic tie-breaker

Do not use updated time as a tie-breaker for official weekly selection.

Reason: edited issues should not gain or lose rank because they were edited later.

## Selection rule

Parameters:

```text
no_change_baseline = 20
required_margin = 1
minimum_total_votes = 20
```

A prompt is selected only if:

```text
top_prompt_votes >= no_change_baseline + required_margin
```

and:

```text
total_votes >= minimum_total_votes
```

With the initial parameters, the top prompt must have at least 21 votes, and the weekly vote must have at least 20 total real prompt votes.

This is equivalent to saying that a real prompt must beat the 20-vote no-change baseline.

## Baseline candidate

Every snapshot records this virtual candidate:

```text
[Baseline]: No change this week
20 virtual votes
```

The baseline candidate is not a GitHub issue.

It exists to make `no_run` decisions explainable in the snapshot and run log.

## Snapshot schema

```json
{
  "schema_version": "snapshot-v1.1",
  "week": "001",
  "snapshot_at": "2026-05-11T00:00:00+09:00",
  "cutoff_timezone": "Asia/Tokyo",
  "source": "github-issues-reactions",
  "repository": "Unjuno/prompt-vote-lab",
  "selection_rule": {
    "rule": "selection-v1.1",
    "no_change_baseline": 20,
    "required_margin": 1,
    "minimum_total_votes": 20
  },
  "no_change_baseline_candidate": {
    "issue": null,
    "title": "[Baseline]: No change this week",
    "author": "system",
    "votes": 20,
    "url": null,
    "virtual": true,
    "created_at": null,
    "updated_at": null
  },
  "total_votes": 52,
  "top_prompt_votes": 24,
  "decision": "selected",
  "decision_reason": "top_prompt_beat_no_change_baseline",
  "selected_issue": 3,
  "ranked_candidates_with_baseline": [
    {
      "rank": 1,
      "issue": 3,
      "title": "Show weekly runs as a timeline",
      "author": "Unjuno",
      "votes": 24,
      "url": "https://github.com/Unjuno/prompt-vote-lab/issues/3",
      "created_at": "2026-05-02T00:55:32Z",
      "updated_at": "2026-05-02T01:32:25Z",
      "virtual": false
    },
    {
      "rank": 2,
      "issue": null,
      "title": "[Baseline]: No change this week",
      "author": "system",
      "votes": 20,
      "url": null,
      "created_at": null,
      "updated_at": null,
      "virtual": true
    }
  ],
  "top_prompts": [
    {
      "rank": 1,
      "issue": 3,
      "title": "Show weekly runs as a timeline",
      "author": "Unjuno",
      "votes": 24,
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
      "votes": 24,
      "url": "https://github.com/Unjuno/prompt-vote-lab/issues/3"
    }
  ]
}
```

## Required invariants

- `top_prompts.length <= 3`
- `top_prompts` contains only real prompt issues
- `top_prompts` is sorted by descending votes
- real prompt ties are resolved by ascending issue number
- `ranked_candidates_with_baseline` includes the virtual baseline candidate
- `ranked_candidates_with_baseline` is sorted by descending votes
- when the baseline and a real prompt tie at 20 votes, the baseline wins unless the prompt reaches the required margin
- `top_prompt_votes` equals `top_prompts[0].votes` when `top_prompts` is non-empty
- `selected_issue` equals `top_prompts[0].issue` when `decision = "selected"`
- `selected_issue` is `null` when `decision = "no_run"`
- `decision_reason` explains why the decision was selected or no-run
- no file under `lab/` is modified by the snapshot generator

## Decision values

Allowed `decision` values:

- `selected`
- `no_run`
- `invalid`

Use `invalid` only when data retrieval failed or the snapshot could not be trusted.

Allowed `decision_reason` values:

- `top_prompt_beat_no_change_baseline`
- `minimum_total_votes_not_met`
- `no_change_baseline_won_or_tied`
- `no_run`

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
