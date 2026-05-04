# Evidence Review Record: dry-run-001

## Run metadata

```text
week_id: dry-run-001
source: live
workflow_run_url: https://github.com/Unjuno/prompt-vote-lab/actions/runs/25336303653
workflow_run_id: 25336303653
head_sha: c251953f620159c08f28fdeccd037c30a987c045
artifact_name: evidence-pipeline-dry-run
artifact_id: 6790655519
artifact_digest: sha256:009781abbdd7699d84af5b5e22bfe2653b5a822a8a265b65e1e8a9c76784cf65
artifact_file_count: 7
reviewed_at: 2026-05-05 JST
reviewer: maintainer-assisted review
```

## Machine validation

```text
validator_command: node scripts/validate-evidence-artifact.mjs tmp/evidence dry-run-001
validator_result: PASS
```

Required log evidence:

```text
Evidence artifact validation passed: tmp/evidence week=dry-run-001
```

## Workflow result

```text
job: evidence-pipeline-dry-run
job_result: success
source: live
snapshot_result: no_run
selected_issue: none
total_votes: 0
candidate_count: 3
summary_week_count: 1
summary_selected_count: 0
summary_no_run_count: 1
```

## Artifact file checklist

The workflow log listed these seven files:

```text
[x] tmp/evidence/data/snapshots/week-dry-run-001.json
[x] tmp/evidence/logs/aggregation/week-dry-run-001.jsonl
[x] tmp/evidence/runs/week-dry-run-001.md
[x] tmp/evidence/reports/summary/weekly-metrics.json
[x] tmp/evidence/reports/summary/weekly-metrics.md
[x] tmp/evidence/reports/briefings/week-dry-run-001.md
[x] tmp/evidence/reports/hn/week-dry-run-001.md
```

## Snapshot review

```text
schema_version: machine-validated
no_change_baseline: machine-validated
no_change_baseline_candidate_votes: machine-validated
top_prompts_count: machine-validated <= 3
candidate_count: 3
total_votes: 0
selected_issue: none
decision: no_run
decision_reason: minimum_total_votes_not_met
identity_like_voter_fields_present: machine-validated no
```

## Aggregation log review

```text
weekly_snapshot_started present: machine-validated yes
weekly_snapshot_finished present: machine-validated yes
finished event has candidate_count: validator/log confirmed
finished event has total_votes: validator/log confirmed
finished event has top_prompt_votes: validator/log confirmed
finished event has decision: validator/log confirmed
finished event has decision_reason: validator/log confirmed
```

## Summary review

```text
summary_schema_version: snapshot-summary-v1.0
week_count: 1
latest_week_present: machine-validated yes
trend_present: machine-validated yes
identity_like_voter_fields_present: machine-validated no
```

## Public briefing review

```text
Prompt Vote Lab Briefing present: machine-validated yes
Public status present: not manually inspected
Observe present: machine-validated yes
Orient present: machine-validated yes
Decide present: machine-validated yes
Act present: machine-validated yes
Submit prompt link present: machine-validated yes
Vote link present: machine-validated yes
share warning present: not manually inspected
```

## HN draft review

```text
Do-not-post checklist present: machine-validated yes
blocker present if unrecorded fields remain: not manually inspected
```

Do not post externally from this artifact review alone.

## Review decision

```text
machine_validation: PASS
human_review: UNCERTAIN
final_decision: UNCERTAIN
```

## Reason for UNCERTAIN

The workflow logs prove that the artifact validator passed and that the expected seven files were uploaded.

However, the artifact archive itself was not manually opened and reviewed file-by-file in this record. Therefore this is not yet a full human PASS under `docs/evidence-artifact-review.md`.

## Next action

```text
Download artifact 6790655519.
Open the seven files listed above.
Complete a human PASS/FAIL review using docs/evidence-artifact-review.md.
Only after a human PASS should source=live be marked fully verified for canary entry.
```
