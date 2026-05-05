# Evidence Review Record Template

Use this template to record a reviewed `Evidence Pipeline Dry Run` artifact.

Copy this file to:

```text
runs/<week_id>-evidence-review.md
```

Do not edit this template in place for a specific run.

## Run metadata

```text
week_id:
source: fixture | live
workflow_run_url:
workflow_run_id:
head_sha:
artifact_name: evidence-pipeline-dry-run
artifact_id:
artifact_digest:
artifact_file_count:
reviewed_at:
reviewer:
```

## Machine validation

```text
validator_command: node scripts/validate-evidence-artifact.mjs tmp/evidence <week_id>
validator_result: PASS | FAIL
```

Required log evidence:

```text
Evidence artifact validation passed: tmp/evidence week=<week_id>
```

## Artifact file checklist

```text
[ ] tmp/evidence/data/snapshots/week-<week_id>.json
[ ] tmp/evidence/logs/aggregation/week-<week_id>.jsonl
[ ] tmp/evidence/runs/week-<week_id>.md
[ ] tmp/evidence/reports/summary/weekly-metrics.json
[ ] tmp/evidence/reports/summary/weekly-metrics.md
[ ] tmp/evidence/reports/briefings/week-<week_id>.md
[ ] tmp/evidence/reports/hn/week-<week_id>.md
```

## Snapshot review

```text
schema_version:
no_change_baseline:
no_change_baseline_candidate_votes:
top_prompts_count:
candidate_count:
total_votes:
selected_issue:
decision:
decision_reason:
identity_like_voter_fields_present: yes | no
```

PASS only if:

```text
schema_version == snapshot-v1.2
no_change_baseline == 20
no_change_baseline_candidate_votes == 20
top_prompts_count <= 3
identity_like_voter_fields_present == no
```

## Aggregation log review

```text
weekly_snapshot_started present: yes | no
weekly_snapshot_finished present: yes | no
finished event has candidate_count: yes | no
finished event has total_votes: yes | no
finished event has top_prompt_votes: yes | no
finished event has decision: yes | no
finished event has decision_reason: yes | no
```

## Summary review

```text
summary_schema_version:
week_count:
latest_week_present: yes | no
trend_present: yes | no
identity_like_voter_fields_present: yes | no
```

PASS only if:

```text
summary_schema_version == snapshot-summary-v1.0
week_count >= 1
latest_week_present == yes
trend_present == yes
identity_like_voter_fields_present == no
```

## Public briefing review

```text
Prompt Vote Lab Briefing present: yes | no
Public status present: yes | no
Observe present: yes | no
Orient present: yes | no
Decide present: yes | no
Act present: yes | no
Submit prompt link present: yes | no
Vote link present: yes | no
share warning present: yes | no
```

## HN draft review

```text
Do-not-post checklist present: yes | no
blocker present if unrecorded fields remain: yes | no | not applicable
```

Do not post externally if any blocker remains.

## Review decision

```text
machine_validation: PASS | FAIL
human_review: PASS | FAIL | UNCERTAIN
final_decision: PASS | FAIL | UNCERTAIN
```

## If final_decision is PASS

For `source=fixture`:

```text
Fixture evidence path is verified. Proceed to source=live dry run.
```

For `source=live`:

```text
Live evidence path is verified. A single low-risk implementation-agent canary may be considered, subject to pre-api-freeze.md.
```

## If final_decision is FAIL or UNCERTAIN

```text
Do not proceed to implementation-agent canary.
Open a fix PR for the failing generator, workflow, validator, or documentation layer.
```

## Notes

```text
<freeform notes>
```
