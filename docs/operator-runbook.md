# Operator runbook

This runbook is for maintainers operating Prompt Vote Lab.

It describes what to check, what to merge, what to stop, and what must never be automated.

Repository-wide canonical, legacy, default-off, auto-merge, manual-review, and release-gate status is governed by [Canonical status drift check](./canonical-status-drift-check.md). This runbook is the operating procedure, not a second status source of truth.

## Current production status

Verified live paths:

```text
Support Unlock Export -> data/support-unlocks/2026-W19.json
Weekly Auto Run -> runs/week-2026-W19-vote-summary.md
no-change baseline won -> no implementation PR created
manual selected-prompt workflow smoke -> PASS
weekly canonical selected-prompt canary -> run 25858202166 -> PASS
```

Canonical selected-prompt implementation is verified behind a default-off feature flag:

```text
PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true
runner: codex-cli-selected-prompt-packet-container
selected Issue: #282
summary PR: #283
implementation PR: #284
artifacts:
  - weekly-selected-prompt-diagnostics-7
  - weekly-selected-prompt-public-bundles-7
  - weekly-selected-prompt-uploaded-bundle-verification-7
```

Still not default-on:

```text
scheduled weekly canonical execution for ordinary weeks
legacy runner removal
auto-merge
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
8. cleanup temporary canary variables and canary Issues/PRs
```

## Normal schedule

| Workflow | Schedule | JST | Expected output |
|---|---:|---:|---|
| `Support Unlock Export` | daily 00:17 UTC | daily 09:17 JST | `data/support-unlocks/<week-id>.json` |
| `Weekly Auto Run` | Monday 00:23 UTC | Monday 09:23 JST | `runs/week-<week-id>-vote-summary.md` PR |

The scheduled path should process the previous completed UTC ISO week.

## Canonical weekly feature flag policy

The weekly canonical selected-prompt path is controlled by a repository variable:

```text
PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER
```

Allowed values:

```text
true
false
unset
```

Interpretation:

| Value | Effect | Release status |
|---|---|---|
| unset | legacy weekly fallback path | allowed during migration |
| `false` | legacy weekly fallback path | allowed during migration |
| `true` | canonical Docker/Codex selected-prompt runner for eligible candidates | canary / controlled use only |

The legacy `scripts/openai_lab_run.py` path is non-canonical. It is preserved as a migration fallback only.

Do not treat a legacy weekly run as canonical evidence.

A weekly implementation PR is canonical only when the evidence says:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

## Temporary canary variable policy

Temporary canary variables must be removed or reset after verification.

Variables used during the controlled weekly canonical canary:

```text
PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=true
PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0
```

Required cleanup after a canary:

```text
PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false or unset
PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=20 or unset
close canary prompt Issue
close evidence-only canary PRs without merge unless product adoption is intended
record run URL and artifact names in durable docs or PR comments
```

Never leave `PROMPT_VOTE_LAB_NO_CHANGE_BASELINE=0` after a canary. That changes weekly selection behavior.

Never leave the canonical weekly runner enabled unintentionally before default-on release approval.

## Default-on release gate

Do not make the canonical weekly runner default-on until all of these are true:

```text
manual selected-prompt smoke: PASS
weekly feature-flag canary with eligible candidate: PASS
weekly diagnostics artifact: present
weekly public bundle artifact: present
weekly uploaded bundle verification artifact: present
bounded lab diff: PASS
legacy fallback documented as non-canonical
participant evidence guide published
operator runbook feature-flag cleanup documented
manual review remains required
auto-merge remains disabled
```

Default-on means changing the repository/workflow default, not just temporarily setting a repository variable for a controlled run.

## Manual support export verification

Use this after token rotation or support automation changes.

```text
Actions -> Support Unlock Export -> Run workflow
```

Example:

```text
week_id: 2026-W19
since: 2026-05-04T00:00:00Z
until: 2026-05-11T00:00:00Z
```

Expected result for zero support:

```text
support_total_usd: 0.0
rank_2_unlocked: false
rank_3_unlocked: false
privacy flags: all false
```

## Manual weekly run verification

Use this after support export has produced the matching support unlock file.

```text
Actions -> Weekly Auto Run -> Run workflow
```

Expected no-eligible result:

```text
vote summary PR is created
support unlock file is referenced
baseline_won: true
eligible_count: 0
implementation PR: none
```

Expected canonical eligible result when the canonical feature flag is deliberately enabled:

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
```

## Merge policy

Automation may create PRs.

Automation must not merge PRs.

Merge only after checking:

```text
PR scope is correct
changed files are expected
CI or internal workflow checks passed
public evidence is not weakened
no forbidden secret or identity data is present
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
```

## Support unlock failure handling

| Failure | Likely cause | Action |
|---|---|---|
| `test -n "$GH_TOKEN"` fails | `SPONSORS_GRAPHQL_TOKEN` missing or empty | Check repository secret name |
| 401 | invalid or expired token | Rotate token |
| 403 | insufficient token permission | Recreate token with the minimum working scope |
| GraphQL field error | sponsors query permission or schema issue | Inspect `Fetch support activity` log |
| privacy validation fails | public JSON contains forbidden key/value or validator bug | Do not commit; inspect generated JSON shape |
| no commit created | generated file unchanged | Check whether the target file already exists with same content |

## Weekly Auto Run failure handling

| Failure | Likely cause | Action |
|---|---|---|
| missing support unlock file | Support Unlock Export has not produced the week file | Run/export the correct week first |
| wrong week id | resolver or manual window mismatch | Check `RUN_WEEK` and support unlock source |
| no eligible candidates | baseline won or no votes | Merge vote summary if correct |
| implementation secret missing | eligible candidates exist but implementation API secret is absent | Configure implementation secret or stop |
| preflight failure | model/token/retry/candidate policy mismatch | Fix policy mismatch; do not bypass preflight |
| generated no lab changes | model failed to make useful change | Record failure; do not auto-rerun |
| safety/static check failure | unsafe or invalid output | Stop and review; do not merge |
| canonical evidence artifact missing | canonical step failed before evidence was created or upload failed | Preserve logs, do not merge, inspect diagnostics/public bundle steps |
| uploaded bundle verification failed | artifact changed, missing, or leaked forbidden pattern | Do not merge; inspect verification report and Gitleaks findings |

## Public results and Pages checks

After merging evidence PRs, confirm:

```text
Public Results Export completed successfully
queued/in-progress workflow runs are not committed as current evidence
GitHub Pages deployed or a later Pages deployment superseded a cancelled one
lab/comparisons pages still have one card per rank
lab/history page still renders
```

## Token handling

`SPONSORS_GRAPHQL_TOKEN` is only for reading GitHub Sponsors activity.

It must not need repository write permission.

Repository writes are performed by the workflow `GITHUB_TOKEN`.

Implementation-agent API secrets are separate and must not be reused as Sponsors tokens.

For canonical Docker/Codex runs, the evidence should show:

```text
OPENAI_API_KEY present before codex exec: no
```

## Reset and cleanup policy

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
```

Development cleanup scripts must default to dry-run and must refuse to delete protected public evidence paths.

## Deferred configuration decisions

`MAX_OUTPUT_TOKENS` remains at the current configured limit until the system is complete.

Do not change it during the current stabilization phase.

Revisit only after:

```text
participant docs are complete
operator runbook is complete
reset script is safe
implementation PR path has passed at least one live E2E run
review burden and diff size are known
```

## Stop rule

If uncertain, stop before spending a model call or merging a PR.

Failed runs are experiment data. Hidden retries are not allowed.
