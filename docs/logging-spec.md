# Logging Specification

## Purpose

Prompt Vote Lab must preserve enough evidence to reconstruct why a prompt was selected, what the AI coding agent changed, whether the result passed review, and how the outcome was classified.

This document separates three log classes:

1. experiment logs
2. aggregation logs
3. system logs

Do not mix these classes. Mixing them makes later analysis ambiguous.

## Log classes

### 1. Experiment log

Experiment logs describe one weekly experiment run.

Canonical location:

```text
runs/week-XXX.md
```

Required fields:

- week id
- vote snapshot reference
- selected issue number
- selected prompt title
- selected prompt author login
- selected prompt vote count
- implementation model policy
- implementation model settings
- AI execution constraints
- implementation PR
- changed files
- safety-check result
- maintainer merge/reject decision
- expectation-gap classification
- reviewer note
- rule change for the next run

Experiment logs are human-readable and should link to machine-readable evidence.

### 2. Aggregation log

Aggregation logs preserve vote-count evidence.

Canonical locations:

```text
data/snapshots/week-XXX.json
logs/aggregation/week-XXX.jsonl
```

`data/snapshots/week-XXX.json` is the weekly fixed vote snapshot.

`logs/aggregation/week-XXX.jsonl` records operational events produced while creating that snapshot.

Aggregation logs must not be stored under `lab/` because `lab/` is the AI-editable implementation target.

### 3. System log

System logs preserve automation behavior.

Canonical locations:

```text
logs/system/week-XXX.jsonl
logs/api/week-XXX.jsonl
logs/errors/week-XXX.jsonl
```

System logs should record:

- workflow name
- workflow run id
- commit SHA
- started_at
- finished_at
- status
- error type, if any
- model name, if an API call is made
- token/cost estimate, if available
- retry count
- fallback status

## Trust boundary

The following paths have different trust levels:

| Path | Trust role | Editable by AI agent? |
|---|---|---:|
| `lab/` | UI implementation target | Yes |
| `data/` | generated experiment data | No |
| `runs/` | weekly experiment record | No |
| `logs/` | operational evidence | No |
| `rules/` | experiment policy | No |
| `.github/workflows/` | automation | No |
| `scripts/` | maintainer-controlled scripts | No |

The AI coding agent must not edit evidence files.

## Minimum evidence chain

Each week must produce this chain:

```text
GitHub Issues + reactions
  -> data/snapshots/week-XXX.json
  -> runs/week-XXX.md
  -> implementation PR
  -> safety-check result
  -> merge/reject decision
  -> expectation-gap classification
```

If any link is missing, the run is incomplete.

## Required weekly status values

Allowed `run_status` values:

- `no_run`
- `selected_pending_implementation`
- `implementation_pr_open`
- `merged`
- `rejected`
- `invalidated`

Allowed `gap_classification` values:

- `Hit`
- `Partial`
- `Misread`
- `Overbuild`
- `Underbuild`
- `Rule conflict`
- `Unsafe`
- `Rejected`

## Redaction and privacy

Only use public GitHub information for public logs:

- issue number
- issue title
- issue URL
- author login
- public reaction counts
- public PR URL

Do not log:

- IP address
- device fingerprint
- location
- private email
- access tokens
- raw API keys
- private browser/session data

## API-before-log rule

Do not run a real implementation-model API call until these exist:

- weekly snapshot schema
- weekly snapshot generation workflow
- run log template with snapshot reference
- API usage log schema
- safety-check workflow
- dry-run path

If the API is called before these exist, the experiment is not reproducible enough.
