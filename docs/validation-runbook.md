# Validation Runbook

## Purpose

This runbook defines the next validation steps before any real implementation-model API call.

The goal is to verify the evidence pipeline in this order:

1. offline smoke test
2. manual workflow dry-run
3. artifact inspection
4. optional committed test run
5. real weekly snapshot

Do not skip directly to real API usage.

## Current validation status

Completed:

- Script syntax check exists.
- Offline workflow smoke test exists.
- Offline smoke test validates fixture snapshot generation.
- Offline smoke test validates run-log draft generation.
- Offline smoke test validates HN draft generation.
- Manual workflow runs default to `commit_changes=false`.
- Manual dry-run outputs are uploaded as short-retention artifacts.

Not completed:

- Manual `Weekly Vote Snapshot` dry-run against live repository issues.
- Manual `Generate HN Draft` dry-run against generated snapshot/run-log artifacts.
- Inspection of generated artifacts.
- Committed test snapshot, if needed.
- Real weekly snapshot.

## Rule: no real model API before validation

Do not run a paid implementation-model API call until:

- weekly snapshot dry-run succeeds
- generated snapshot artifact is inspected
- generated run-log artifact is inspected
- HN draft dry-run succeeds
- generated HN draft artifact is inspected
- API control policy is implemented in workflow form

## Step 1: confirm CI smoke test

Open the latest `Script Check` workflow run.

Required passing steps:

- `Check JavaScript module syntax`
- `Run offline workflow smoke test`

PASS:

```text
Both steps succeed.
```

FAIL:

```text
Either step fails.
```

If FAIL, do not run live workflow dry-runs.

## Step 2: run weekly snapshot dry-run

Open GitHub Actions:

```text
Actions -> Weekly Vote Snapshot -> Run workflow
```

Use:

```text
week_id: test-001
snapshot_at: 2026-05-11T00:00:00+09:00
commit_changes: false
```

Expected behavior:

- workflow completes successfully
- no commit is pushed
- git diff is printed in logs
- artifact is uploaded

Artifact name:

```text
weekly-snapshot-dry-run
```

Expected artifact contents:

```text
data/snapshots/week-test-001.json
logs/aggregation/week-test-001.jsonl
runs/week-test-001.md
```

PASS:

```text
All expected files exist in the artifact and contain plausible data.
```

FAIL:

```text
Workflow fails, artifact is missing, or snapshot/run-log contents are malformed.
```

## Step 3: inspect weekly snapshot artifact

Download `weekly-snapshot-dry-run`.

Check `data/snapshots/week-test-001.json`:

Required fields:

- `schema_version`
- `week`
- `snapshot_at`
- `source`
- `repository`
- `selection_rule`
- `total_votes`
- `top_prompt_votes`
- `decision`
- `selected_issue`
- `top_prompts`
- `all_candidates`

Required invariants:

- `top_prompts.length <= 3`
- candidates are sorted by votes descending
- ties are sorted by issue number ascending
- if `decision = selected`, `selected_issue = top_prompts[0].issue`
- if `decision = no_run`, `selected_issue = null`

Check `runs/week-test-001.md`:

Required sections:

- Vote Snapshot
- Top Prompts
- Selection Rule
- Agent Conditions
- Pull Request
- Safety Check
- Result
- Expectation Gap

It is acceptable for implementation fields to remain `unrecorded` at this stage.

## Step 4: run HN draft dry-run

Only run this after Step 2 succeeds.

Open GitHub Actions:

```text
Actions -> Generate HN Draft -> Run workflow
```

Use:

```text
week_id: test-001
site_url: https://unjuno.github.io/prompt-vote-lab/
commit_changes: false
```

Expected behavior:

- workflow completes successfully
- no commit is pushed
- git diff is printed in logs
- artifact is uploaded

Artifact name:

```text
hn-draft-dry-run
```

Expected artifact contents:

```text
reports/hn/week-test-001.md
```

PASS:

```text
HN draft exists and includes title candidates, text draft, evidence checklist, and do-not-post checklist.
```

FAIL:

```text
Workflow fails, artifact is missing, or draft does not warn about incomplete run logs.
```

## Step 5: inspect HN draft artifact

Download `hn-draft-dry-run`.

Check:

- title candidates are factual
- recommended title is not exaggerated
- text draft does not claim statistical significance
- text draft does not claim full autonomy
- do-not-post checklist flags incomplete evidence when appropriate
- maintainer action says manual review and manual submission are required

## Step 6: optional committed test run

Only after dry-run artifacts are inspected.

Run `Weekly Vote Snapshot` again with:

```text
week_id: test-001
commit_changes: true
```

This intentionally commits test evidence files.

Use only if a committed test artifact is useful.

If committed test files are not wanted, skip this step.

## Step 7: real weekly snapshot

For a real weekly snapshot, use the scheduled run or manual run with the real week id.

Before committing, verify:

- issue labels are correct
- prompt-proposal issues are open
- vote cutoff time is correct
- no duplicate snapshot exists for that week

## Failure handling

If a workflow fails:

1. inspect job logs
2. inspect generated partial artifacts if available
3. create a focused fix PR
4. re-run offline smoke test
5. re-run manual dry-run

Do not patch generated evidence manually unless creating an explicit correction file.

## Current known limitation

The HN draft workflow reads files from the repository checkout.

If the weekly snapshot dry-run was not committed, the HN draft workflow cannot automatically read that dry-run snapshot unless the files are committed or manually supplied later by a future artifact-chaining workflow.

For now, HN draft live testing is most useful after either:

- a committed test snapshot exists, or
- a real weekly snapshot exists.

## Next engineering improvement

A future workflow may chain snapshot generation and HN draft generation in one dry-run job so the HN draft can consume uncommitted snapshot output directly.
