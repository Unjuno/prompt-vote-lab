# Issue lifecycle

## Purpose

Prompt Vote Lab should not keep weekly experiment Issues open forever.

Closed Issues remain visible in GitHub. Closing is not deletion.

The project should keep evidence in:

```text
Issue comments
runs/
data/public-results.json
data/public-results.md
public agent-run artifacts
```

## Core rule

Weekly cleanup is allowed only after the weekly experiment cycle is recorded.

```text
run
→ review
→ merge/reject
→ runs/ record
→ Public Results Export
→ comment before close
→ close eligible Issues
```

Do not close Issues before Public Results Export has run.

## Required labels for automatic close

An Issue is eligible only if it has exactly one matching week label and exactly one supported outcome label.

```text
week:<week_id>
outcome:<result>
```

Example:

```text
week:2026-W19
outcome:implemented
```

## Supported outcomes

Completed:

```text
outcome:implemented
outcome:archived-fixture
```

Closed as not planned:

```text
outcome:not-selected
outcome:blocked
outcome:rejected-after-run
```

## Protected labels

The finalizer must skip Issues with any of these labels:

```text
carryover
future-candidate
discussion
bug
admin
do-not-close
pinned
```

Use `carryover` for prompts that should remain open for another week.

Use `do-not-close` for any Issue that should never be touched by the weekly finalizer.

## Close comment

Before closing, the finalizer posts a comment with:

```text
week
outcome
close_reason
public_results path
public_results generation time
run record hint
statement that the Issue is closed, not deleted
```

This keeps the experiment trail visible inside the Issue thread.

## Workflow

The workflow is manual at first:

```text
Actions
→ Weekly Issue Finalizer
→ Run workflow
```

Inputs:

```text
week_id: 2026-W19
dry_run: true by default
require_public_results_membership: true by default
run_record_hint: runs/
```

Default mode is `dry_run=true`.

When `dry_run=true`, the workflow only uploads a plan artifact.

When `dry_run=false`, the workflow posts the generated close comment and closes eligible Issues.

## Why not close every open Issue

Open Issues may include future proposals, carryover prompts, discussions, bugs, and admin tasks.

Therefore the finalizer only searches for Issues with a matching `week:*` label.

It then requires an `outcome:*` label before closing.

## Recommended weekly operation

```text
1. Assign week:<week_id> to weekly candidate Issues.
2. Run the weekly experiment.
3. Review and merge/reject PRs.
4. Add outcome:* labels.
5. Add carryover or do-not-close where needed.
6. Write runs/ records.
7. Run Public Results Export.
8. Run Weekly Issue Finalizer with dry_run=true.
9. Inspect artifact plan.
10. Run Weekly Issue Finalizer with dry_run=false.
```

## Current limitation

The finalizer does not infer outcomes.

A human or another explicit workflow must set `outcome:*` before the Issue can be closed.
