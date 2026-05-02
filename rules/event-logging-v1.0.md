# event-logging-v1.0

## Purpose

Prompt Vote Lab should record automation behavior in a form that can be reviewed by humans and parsed by scripts.

GitHub Actions logs are useful, but they are not the canonical experiment record.

## Log layers

Use two layers:

1. Machine-readable JSONL events.
2. Human-readable Markdown summaries.

## JSONL event format

Each event is one JSON object on one line.

Required fields:

- `schema_version`
- `event_type`
- `timestamp_utc`
- `source`
- `status`

Recommended fields:

- `week`
- `candidate_rank`
- `issue_number`
- `pr_number`
- `workflow`
- `run_id`
- `run_attempt`
- `commit_sha`
- `branch`
- `model`
- `api_call_count`
- `sdk_max_retries`
- `payload`

## Canonical versus artifact logs

Canonical logs:

- `runs/*.md`
- `data/events.jsonl` if explicitly committed through a PR

Artifact logs:

- `.tmp/**/*.jsonl`
- `.tmp/**/*.md`
- uploaded workflow artifacts

Mock, fuzz, and exception tests should normally upload artifact logs rather than commit canonical logs to `main`.

Weekly accepted runs may create PRs that append canonical JSONL events.

## API cost logging

Paid API runs must record:

- model
- max output token budget
- SDK retry setting
- timeout setting
- API call count
- whether HN draft generation caused an additional call

## Failure logging

Failures are data.

If a workflow fails after it has enough context to write a failure event, it should record:

- failed step or phase
- expected behavior
- observed behavior
- whether an API call was made

## Security

Logs must not contain:

- API keys
- GitHub tokens
- secrets
- payment identifiers
- private user data

## Rationale

The project depends on comparing runs over time.

Without structured logs, failed runs become anecdotes instead of usable experimental data.
