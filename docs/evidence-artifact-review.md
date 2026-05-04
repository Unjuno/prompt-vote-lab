# Evidence Artifact Review

This guide is for reviewing a manually executed `Evidence Pipeline Dry Run` artifact.

Use it after running:

```text
Actions
→ Evidence Pipeline Dry Run
→ Run workflow
→ source: fixture or live
→ week_id: <week_id>
```

Do not treat a successful workflow run as sufficient evidence. The artifact must be inspected.

## Expected artifact

Artifact name:

```text
evidence-pipeline-dry-run
```

Expected files inside the artifact:

```text
tmp/evidence/data/snapshots/week-<week_id>.json
tmp/evidence/logs/aggregation/week-<week_id>.jsonl
tmp/evidence/runs/week-<week_id>.md
tmp/evidence/reports/summary/weekly-metrics.json
tmp/evidence/reports/summary/weekly-metrics.md
tmp/evidence/reports/briefings/week-<week_id>.md
tmp/evidence/reports/hn/week-<week_id>.md
```

If any file is missing, the dry run is not acceptable.

## Fast CLI check

After downloading and extracting the artifact so that `tmp/evidence/` exists locally, run:

```bash
node scripts/validate-evidence-artifact.mjs tmp/evidence <week_id>
```

Example:

```bash
node scripts/validate-evidence-artifact.mjs tmp/evidence dry-run-001
```

The CLI check does not replace human review. It catches missing files, schema mismatches, missing sections, missing baseline data, and identity-like voter fields.

## Review order

### 1. Snapshot

Open:

```text
tmp/evidence/data/snapshots/week-<week_id>.json
```

Check:

- `schema_version` is `snapshot-v1.2`
- `selection_rule.no_change_baseline` is `20`
- `no_change_baseline_candidate.votes` is `20`
- `top_prompts.length <= 3`
- `metrics` exists
- `metrics.candidate_count` matches `all_candidates.length`
- no voter login list appears anywhere

Forbidden identity-like keys:

```text
_voter_logins
voter_logins
voters
reaction_users
```

### 2. Aggregation log

Open:

```text
tmp/evidence/logs/aggregation/week-<week_id>.jsonl
```

Check that it contains both events:

```text
weekly_snapshot_started
weekly_snapshot_finished
```

The finished event should include:

- `candidate_count`
- `total_votes`
- `top_prompt_votes`
- `decision`
- `decision_reason`

### 3. Run log

Open:

```text
tmp/evidence/runs/week-<week_id>.md
```

Check that it contains:

- `Participation Metrics`
- `Ranked Candidates With Baseline`
- `Selection Rule`
- `Decision reason`
- `Agent Conditions`
- `Safety Check`
- `Expectation Gap`

For a dry run, some fields may remain `unrecorded`. That is acceptable for fixture evidence review, but not for a final external report.

### 4. Weekly metrics summary

Open:

```text
tmp/evidence/reports/summary/weekly-metrics.json
tmp/evidence/reports/summary/weekly-metrics.md
```

Check JSON:

- `schema_version` is `snapshot-summary-v1.0`
- `week_count >= 1`
- `latest_week` exists
- `trend` exists
- no voter login list appears anywhere

Check Markdown:

- title is `Weekly Metrics Summary`
- table contains the dry-run week

### 5. Public briefing

Open:

```text
tmp/evidence/reports/briefings/week-<week_id>.md
```

Check that it contains:

- `Prompt Vote Lab Briefing`
- `Public status`
- `Observe`
- `Orient`
- `Decide`
- `Act`
- `Submit prompt`
- `Vote`
- a share warning

The briefing is a status draft. It is not an official evidence source and must not be auto-posted externally.

### 6. HN draft

Open:

```text
tmp/evidence/reports/hn/week-<week_id>.md
```

Check that it contains:

- `Do-not-post checklist`
- a blocker when the run log has `unrecorded` fields

Do not post the HN draft if any blocker remains.

## PASS / FAIL

PASS only if:

```text
all expected files exist
snapshot schema is valid
20-vote baseline is visible
metrics are present
summary is generated
briefing is generated
HN draft includes the do-not-post checklist
no voter login list appears in snapshot, summary, or briefing
```

FAIL if:

```text
any expected file is missing
baseline is missing or not 20
summary is missing
briefing is missing
HN draft lacks a do-not-post checklist
identity-like voter fields appear in generated files
```

## Next action after PASS

After a fixture PASS, run the same workflow with:

```text
source: live
```

Live mode reads current repository issues and public `+1` reactions. It still must not commit generated evidence files.

## Next action after FAIL

Do not continue to live mode.

Open a fix PR for the failing generator, workflow, or documentation layer.
