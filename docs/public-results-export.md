# Public results export

## Purpose

Prompt Vote Lab is an experiment. Participants should be able to inspect raw public result data and analyze it themselves.

This export is intentionally descriptive, not interpretive.

It does not score prompts, rank authors, recommend improvements, or explain why a prompt succeeded.

## Outputs

The public results export writes:

```text
data/public-results.json
data/public-results.md
```

The JSON file is the primary machine-readable data source.

The Markdown file is a lightweight table view for humans.

## What is collected

The export collects public GitHub repository data:

```text
Issues
Pull Requests
Issue labels
PR labels
Issue reactions
PR reactions
Issue comment counts
PR comment counts
PR changed file counts
PR additions/deletions
PR changed file paths
workflow run metadata
run record markdown files under runs/
```

## What is not collected

The export does not collect:

```text
API keys
GitHub tokens
secrets
raw Actions logs
payment identifiers
private user data
unpublished local files
raw model stderr
raw Codex JSONL beyond committed public artifacts
```

## Workflow

Manual run:

```text
Actions → Public Results Export → Run workflow
```

Inputs:

```text
limit: max Issues, PRs, and workflow runs to export
commit_results: true/false
```

Scheduled run:

```text
17 3 * * * UTC
```

## Participant usage

Participants may use `data/public-results.json` to analyze:

```text
which prompt styles attracted votes
which Issues were blocked or clear
which PRs changed more files or lines
which runs merged or failed
which safety labels appeared before runtime
which workflow runs failed or passed
how comparison runs behaved over time
```

The project does not automatically turn this data into a score.

## Current limitation

This is a public repository snapshot, not a data warehouse.

If deeper analysis is needed, participants should download the JSON and analyze it externally.

## Stability

The current schema is:

```text
prompt-vote-lab-public-results-export-v1
```

Breaking schema changes should use a new schema version.
