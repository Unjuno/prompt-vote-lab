# Operator runbook

This runbook is for maintainers operating Prompt Vote Lab.

It describes what to check, what to merge, what to stop, and what must never be automated.

Repository-wide canonical, legacy, fixed-on weekly runner, auto-merge, manual-review, and release-gate status is governed by [Canonical status drift check](./canonical-status-drift-check.md). This runbook is the operating procedure, not a second status source of truth.

## Current production status

Verified live paths:

```text
Support Unlock Export -> data/support-unlocks/2026-W19.json
Weekly Auto Run no-eligible path -> runs/week-2026-W19-vote-summary.md
manual selected-prompt workflow smoke -> PASS
weekly canonical selected-prompt canary -> run 25858202166 -> PASS
ordinary default-on weekly no-eligible observation -> PR #333 -> PASS
canonical weekly fixed-on release -> approved
```

Canonical selected-prompt implementation is verified and fixed-on for eligible weekly implementation candidates:

```text
weekly default status: canonical selected-prompt runner fixed-on
weekly feature flag override: removed
weekly legacy override: removed from Weekly Auto Run
runner: codex-cli-selected-prompt-packet-container
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

Still not automated:

```text
auto-merge
external publishing
automatic continuation runs
automatic trust scoring
```

## Weekly operating loop

Run or confirm these in order:

```text
1. Support Unlock Export
2. Weekly Auto Run
3. vote summary PR review
4. implementation PR review, only if created
5. public evidence artifact review, if canonical implementation ran
6. Public Results Export refresh
7. GitHub Pages sanity check
8. cleanup temporary canary Issues/PRs when used
```

## Normal schedule

| Workflow | Schedule | JST | Expected output |
|---|---:|---:|---|
| `Support Unlock Export` | daily 00:17 UTC | daily 09:17 JST | `data/support-unlocks/<week-id>.json` |
| `Weekly Auto Run` | Monday 00:23 UTC | Monday 09:23 JST | `runs/week-<week-id>-vote-summary.md` PR, plus implementation PRs only when eligible |

The scheduled path should process the previous completed UTC ISO week.

## Weekly runner policy

`Weekly Auto Run` no longer has a legacy API/SDK branch.

Do not reintroduce a weekly legacy override during cleanup.

A future rollback would need an explicit PR that updates:

```text
.github/workflows/weekly-auto-run.yml
docs/canonical-status-drift-check.md
docs/weekly-automation.md
docs/current-codex-implementation-path.md
docs/operator-runbook.md
docs/workflow-family-map.md
docs/repository-cleanup-inventory.md
scripts/test_canonical_status_drift.py
```

## Legacy script status

Do not remove `scripts/openai_lab_run.py` during ordinary cleanup.

Current classification:

```text
scripts/openai_lab_run.py: present
status: non-canonical manual diagnostic / historical fallback
weekly reachability: none
canonical evidence status: invalid
```

A weekly implementation PR is canonical only when the evidence says:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

## Manual weekly run verification

Expected no-eligible result:

```text
vote summary PR is created
support unlock file is referenced
baseline_won: true
eligible_count: 0
implementation PR: none
implementation-agent attempt: none
auto-merge does not occur
```

Expected canonical eligible result:

```text
vote summary PR is created
implementation PR is created
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
weekly-selected-prompt-diagnostics-<run_number> artifact is present
weekly-selected-prompt-public-bundles-<run_number> artifact is present
weekly-selected-prompt-uploaded-bundle-verification-<run_number> artifact is present
changed files are only lab/index.html, lab/style.css, and/or lab/app.js
auto-merge does not occur
manual review remains required
```

## Vote summary PR review

A vote summary PR may be merged when:

```text
changed file is under runs/
week id is correct
support unlock file path is correct
baseline and eligible metadata are plausible
no implementation files are changed
```

Reject or fix if:

```text
week id points at the newly started week instead of the completed week
support unlock source is missing
support source silently falls back to manual or 0 without file evidence
summary modifies lab/, workflows, scripts, docs, rules, or data unexpectedly
```

## Implementation PR review

An implementation PR may be considered only when:

```text
it was created from an eligible prompt
changed files are only lab/index.html, lab/style.css, and/or lab/app.js
safety-check passed before PR creation
static-site-check passed before PR creation
diff is small enough to review manually
no external scripts, network calls, cookies, trackers, login, payment, eval, or unsafe dynamic code are added
```

For canonical weekly selected-prompt PRs, also require:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
weekly diagnostics artifact exists
weekly public bundle artifact exists
weekly uploaded bundle verification artifact exists
public bundle verification passed
uploaded bundle verification passed
Gitleaks finding count is 0
```

Do not merge if:

```text
files outside lab/ changed
workflow, rules, docs, runs, formal, or scripts changed
model appears to have ignored the selected prompt
implementation is too large to review comfortably
reviewer cannot explain the diff
safety/static checks failed or were skipped
canonical evidence artifacts are missing for a canonical run
auto-merge appears enabled
```

## Weekly Auto Run failure handling

| Failure | Likely cause | Action |
|---|---|---|
| missing support unlock file | Support Unlock Export has not produced the week file | Run/export the correct week first |
| wrong week id | resolver or manual window mismatch | Check `RUN_WEEK` and support unlock source |
| no eligible candidates | baseline won or no votes | Merge vote summary if correct |
| implementation secret missing | eligible candidates exist but implementation API secret is absent | Configure implementation secret or stop |
| preflight failure | model/retry/candidate policy mismatch | Fix policy mismatch; do not bypass preflight |
| generated no lab changes | model failed to make useful change | Record failure; do not auto-rerun |
| safety/static check failure | unsafe or invalid output | Stop and review; do not merge |
| canonical evidence artifact missing | canonical step failed before evidence was created or upload failed | Preserve logs, do not merge, inspect diagnostics/public bundle steps |
| uploaded bundle verification failed | artifact changed, missing, or leaked forbidden pattern | Do not merge; inspect verification report and Gitleaks findings |

## Token handling

`SPONSORS_GRAPHQL_TOKEN` is only for reading GitHub Sponsors activity.

Repository writes are performed by the workflow `GITHUB_TOKEN`.

Implementation-agent API secrets are separate and must not be reused as Sponsors tokens.

For canonical Docker/Codex runs, the evidence should show:

```text
OPENAI_API_KEY present before codex exec: no
```

## Output cap status

The old API-era `MAX_OUTPUT_TOKENS` value is not an active canonical Codex runner control.

Current active policy records:

```text
output_token_cap_enforced: false
```

Do not change or cite output-token caps as canonical runtime enforcement unless a future runner contract proves enforcement directly.

## Cleanup boundary

Do not delete public evidence casually.

Protected public evidence includes:

```text
data/public-results.json
data/public-results.md
data/support-unlocks/*.json
runs/*.md
lab/comparisons/**
lab/history/**
merged PRs and Issues
workflow artifacts referenced by run records or release evidence
```

Do not remove `scripts/openai_lab_run.py` during ordinary cleanup.

Do not reintroduce a weekly legacy override during cleanup.

A later PR may remove the legacy script only after the explicit removal gate in [Workflow family map](./workflow-family-map.md) passes.

## Stop rule

If uncertain, stop before spending a model call or merging a PR.

Failed runs are experiment data. Hidden retries are not allowed.
