# Weekly automation

This document explains what runs automatically, when it runs, and what must exist before each weekly run can proceed.

Repository-wide canonical, legacy, default-on, auto-merge, manual-review, and release-gate status is governed by [Canonical status drift check](./canonical-status-drift-check.md). This page is the weekly workflow operation detail, not a second status source of truth.

## Short answer

Yes. `Weekly Auto Run` is scheduled to run every week.

```text
.github/workflows/weekly-auto-run.yml
cron: 23 0 * * 1
```

That means:

```text
Monday 00:23 UTC
Monday 09:23 JST
```

It can also be started manually with `workflow_dispatch`.

## Related scheduled workflow

Support unlock aggregation is a separate workflow.

```text
.github/workflows/support-unlock-export.yml
cron: 17 0 * * *
```

That means:

```text
every day 00:17 UTC
every day 09:17 JST
```

The support export workflow writes the anonymized aggregate file used by the weekly run:

```text
data/support-unlocks/<week-id>.json
```

On scheduled runs, support export defaults to the previous UTC ISO week. Manual `workflow_dispatch` inputs can still override `week_id`, `since`, and `until` for verification or backfill.

## Weekly run order

`Weekly Auto Run` runs in this order:

```text
1. checkout repository
2. set an initial RUN_WEEK
3. resolve the required support unlock file
4. prefer the previous UTC ISO week when its support unlock file exists
5. collect prompt proposal votes
6. insert no-change baseline
7. select eligible ranks
8. write weekly vote summary PR
9. if eligible candidates exist, require implementation secret
10. preflight the implementation run
11. create implementation PRs for eligible candidates
12. upload canonical weekly diagnostics and public evidence for canonical runs
13. reverify uploaded canonical public bundles
```

The support unlock file is required before vote collection and rank selection.

If the file is missing, the weekly workflow fails before selecting eligible ranks. It must not silently treat missing support data as 0 USD.

## Canonical selected-prompt default

The weekly selected-prompt path now defaults to the canonical Docker/Codex runner:

```text
DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true
```

The repository variable can still override the default for an explicit rollback or diagnostic run:

```text
PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER
```

When the variable is unset, `Weekly Auto Run` uses the canonical Docker/Codex selected-prompt runner for eligible implementation candidates:

```text
scripts/run_codex_selected_prompt.sh
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

When the variable is explicitly set to `true`, the same canonical path is used.

When the variable is explicitly set to `false`, `Weekly Auto Run` uses the legacy fallback path for emergency rollback or controlled diagnosis only.

The legacy `scripts/openai_lab_run.py` path is non-canonical and does not satisfy the selected-prompt canonical runner requirement.

## Canonical weekly evidence artifacts

A successful canonical weekly selected-prompt run should produce:

```text
weekly-selected-prompt-diagnostics-<run_number>
weekly-selected-prompt-public-bundles-<run_number>
weekly-selected-prompt-uploaded-bundle-verification-<run_number>
```

The evidence chain must include:

```text
public bundle verification: ok
uploaded bundle verification: ok
Gitleaks finding count: 0
changed files subset of lab/index.html, lab/style.css, lab/app.js
repo_root_mounted: false
OPENAI_API_KEY present before codex exec: no
```

## Override and rollback settings

A controlled diagnostic run may temporarily set:

```text
PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false
```

After the diagnostic run, remove the override or set it back to:

```text
PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true or unset
```

A controlled canary may temporarily set:

```text
PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0
```

After the canary, reset or remove it:

```text
PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=20 or unset
```

Leaving `PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0` changes selection behavior and is not acceptable for normal scheduled operation.

## Why support export is separate

Support aggregation and prompt implementation are different jobs.

Support export:

- reads GitHub Sponsors activity
- writes only anonymized weekly aggregate data
- validates public JSON before commit
- must not call the implementation model
- must not modify `lab/`

Weekly auto run:

- reads prompt Issues and reactions
- reads the weekly support unlock file
- creates vote summary PRs
- creates implementation PRs only when candidates are eligible
- uses the canonical Docker/Codex selected-prompt runner by default
- may use the legacy fallback only through an explicit rollback override
- must not merge PRs automatically

## Time-window caveat

The scheduled production path should process the UTC ISO week that just ended, not the week that has just started.

`Support Unlock Export` scheduled runs therefore default to:

```text
target = current UTC time - 7 days
```

This writes the previous ISO week by default.

`Weekly Auto Run` resolves the support unlock file before vote collection. When a previous-week support unlock file exists, the resolver writes this resolved week back into the job environment as:

```text
RUN_WEEK=week-<previous-ISO-year>-W<previous-ISO-week>
```

This prevents the Monday morning run from recording the newly started week by mistake.

`Support Unlock Export` writes:

```text
data/support-unlocks/<ISO-year>-W<ISO-week>.json
```

The resolver normalizes these two forms:

```text
week-2026-W20 -> 2026-W20
```

The weekly workflow requires the matching support unlock file for its resolved `RUN_WEEK`.

## Manual verification

The live no-eligible path has been verified.

Verified support export evidence:

```text
Support Unlock Export: PASS
data/support-unlocks/2026-W19.json
support_total_usd: 0.0
rank_2_unlocked: false
rank_3_unlocked: false
privacy flags: all false
```

Verified no-eligible weekly automation evidence:

```text
Weekly Auto Run: PASS
runs/week-2026-W19-vote-summary.md
PR #243 merged
baseline_won: true
eligible_count: 0
implementation PR: none
```

Verified canonical weekly selected-prompt canary evidence:

```text
Weekly Auto Run: PASS
run: 25858202166
selected Issue: #282
summary PR: #283
implementation PR: #284
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
artifacts:
  - weekly-selected-prompt-diagnostics-7
  - weekly-selected-prompt-public-bundles-7
  - weekly-selected-prompt-uploaded-bundle-verification-7
bounded lab diff: PASS
auto-merge: disabled
```

The canary Issue and PRs were closed without merge because they were evidence-only artifacts, not product changes.

Manual verification is still useful after token rotation, workflow changes, backfills, or changes to the canonical runner boundary.

Example support export input:

```text
week_id: 2026-W19
since: 2026-05-04T00:00:00Z
until: 2026-05-11T00:00:00Z
```

Expected public output:

```text
data/support-unlocks/2026-W19.json
```

Then run `Weekly Auto Run` manually and confirm that it reads the support unlock file before vote collection.

## Merge policy

Automation may create PRs, but it must not merge them.

`main` merge remains manual.

## Default-on release status

The complete release-gate checklist is owned by [Canonical status drift check](./canonical-status-drift-check.md).

Weekly workflow default-on release result:

```text
weekly feature-flag canary with eligible candidate: PASS
weekly diagnostics artifact: present
weekly public bundle artifact: present
weekly uploaded bundle verification artifact: present
bounded lab diff: PASS
manual review remains required
auto-merge remains disabled
weekly canonical default-on release: approved
```

## Current production status

Implemented and live-verified:

- `SPONSORS_GRAPHQL_TOKEN` can read support activity for the export path.
- `Support Unlock Export` can generate and validate an anonymized support unlock file.
- `Weekly Auto Run` can read that unlock file and create a no-eligible vote summary PR.
- The no-change baseline path can complete without creating an implementation PR.
- The weekly canonical selected-prompt path can create a bounded lab-only implementation PR with diagnostics, public bundle, and uploaded bundle reverification artifacts.
- Canonical weekly execution is now default-on for eligible candidates.

Still not automated:

- removal of the legacy fallback
- auto-merge