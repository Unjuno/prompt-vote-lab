# Workflow family map

## Purpose

This map classifies GitHub Actions workflows before cleanup or deletion work.

It is not a removal plan.

It answers one question first:

```text
Which workflows are evidence-bearing, and which workflows are historical scaffolding?
```

## Family states

| State | Meaning | Default action |
|---|---|---|
| Canonical active | Current canonical implementation, verification, or evidence path | Keep and harden |
| Weekly active | Scheduled or manually runnable weekly operation | Keep and harden |
| Public generated snapshot | Owns generated public data or pages evidence | Keep; edit through owning generator |
| Safety gate | Blocks unsafe or out-of-scope execution | Keep |
| Canary evidence | Historical or controlled canary path with evidence value | Keep until replacement evidence is documented |
| Legacy fallback | Non-canonical migration fallback | Keep with explicit legacy wording and explicit gate |
| Test and guard | CI guard, scope guard, or contract verification | Keep |
| Cleanup candidate | Candidate for later consolidation or retirement | Do not delete until a removal gate is recorded |

## Canonical active workflows

| Workflow | Path | Reason |
|---|---|---|
| Codex Selected Prompt Run | `.github/workflows/codex-selected-prompt-run.yml` | Manual canonical selected-prompt Docker/Codex runner smoke path |
| Weekly Auto Run | `.github/workflows/weekly-auto-run.yml` | Weekly vote summary and default-on canonical selected-prompt implementation path |

Canonical evidence requires the selected-prompt Docker/Codex runner evidence:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

## Weekly active workflows

| Workflow | Path | Reason |
|---|---|---|
| Support Unlock Export | `.github/workflows/support-unlock-export.yml` | Produces anonymized weekly support unlock data |
| Weekly Auto Run | `.github/workflows/weekly-auto-run.yml` | Reads support unlock data and prompt votes |
| Weekly Issue Finalizer | `.github/workflows/weekly-issue-finalizer.yml` | Closes weekly Issues after public results membership and outcome labeling |

These workflows are not cleanup candidates while weekly operation depends on them.

## Public generated snapshot workflows

| Workflow | Path | Reason |
|---|---|---|
| Public Results Export | `.github/workflows/public-results-export.yml` | Owns `data/public-results.json`, `data/public-results.md`, and derived public evidence surfaces |

Generated snapshot files should be changed through the owning workflow or generator, not by unrelated cleanup PRs.

## Safety gate workflows

| Workflow | Path | Reason |
|---|---|---|
| Issue Safety Scan | `.github/workflows/issue-safety-scan.yml` | Scans Issue text and labels unsafe or review-required Issues before execution |

Safety gate workflows are not optional cleanup targets.

## Test and guard workflows

| Workflow | Path | Reason |
|---|---|---|
| Script Check | `.github/workflows/script-check.yml` | Runs syntax, contract, doc, runner, bundle, and cleanup guards |

Script Check is the primary sustain mechanism for repository 5S.

## Canary evidence workflows

These workflows are evidence-bearing historical or controlled canary paths.

They should not be deleted merely because the selected-prompt runner is now canonical.

| Workflow | Path | Current role |
|---|---|---|
| Codex First Canary Run | `.github/workflows/codex-first-canary-run.yml` | Historical first canary path; gated by `ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS=true` |
| Codex Isolated 3file Canary Run | `.github/workflows/codex-isolated-3file-canary-run.yml` | Historical isolated three-file canary path; gated by `ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS=true` |
| Codex Isolated 3file Relaxed Canary Run | `.github/workflows/codex-isolated-3file-relaxed-canary-run.yml` | Historical relaxed canary path; gated by `ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS=true` |
| Codex Writeback Canary Run | `.github/workflows/codex-writeback-canary-run.yml` | Historical writeback canary path |
| Codex Offline JSON Canary Run | `.github/workflows/codex-offline-json-canary-run.yml` | Historical non-canonical JSON writeback path |
| Codex Agent Observed Canary Run | `.github/workflows/codex-agent-observed-canary-run.yml` | Historical agent-observed canary path; gated by `ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS=true` |
| Canary 007 Policy Feasibility | `.github/workflows/canary-007-policy-feasibility.yml` | Feasibility check for policy-enforced container execution |
| Codex Policy Agent Canary Run | `.github/workflows/codex-policy-agent-canary-run.yml` | Policy-agent public bundle and diagnostics evidence path |
| Codex Task Packet Canary Run | `.github/workflows/codex-task-packet-canary-run.yml` | Task-packet boundary evidence path |
| Codex Fixed Issue Instruction Canary Run | `.github/workflows/codex-fixed-issue-instruction-canary-run.yml` | Fixed-Issue instruction packet and safety-gate evidence path |

## Historical weak canary gate

Some historical canary workflows are intentionally weaker than the current canonical selected-prompt boundary because they tested earlier execution designs.

These weak historical canaries remain as archive evidence, but their jobs require an explicit repository variable before they run:

```text
ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS=true
```

Gated workflows:

```text
.github/workflows/codex-first-canary-run.yml
.github/workflows/codex-isolated-3file-canary-run.yml
.github/workflows/codex-isolated-3file-relaxed-canary-run.yml
.github/workflows/codex-agent-observed-canary-run.yml
```

The gate prevents accidental reruns of old workspace-write or relaxed-sandbox experiments without deleting historical evidence surfaces.

The gate does not apply to the current canonical selected-prompt path:

```text
.github/workflows/codex-selected-prompt-run.yml
.github/workflows/weekly-auto-run.yml
```

## Canary-era archive boundary

Canary-era names are historical evidence labels, not active canonical status claims.

Examples:

```text
first-canary
canary-007
canary-008
canary-009
isolated-3file
writeback-canary
offline-json-canary
policy-agent-canary
task-packet-canary
fixed-issue-instruction-canary
```

Archive boundary rule:

```text
Keep the historical name when it identifies old evidence.
Do not rename historical evidence to make it look current.
Do not delete historical canary surfaces merely to make the active path easier to see.
Do not cite canary-era names as canonical selected-prompt status unless the evidence also contains the canonical runner marker.
```

A PR that changes a canary-era workflow, doc, or run-record reference must state:

```text
Historical evidence role:
Current active role, if any:
Canonical status claim: none / explicit marker present
Affected run records:
Affected public docs:
Affected contract tests:
Replacement evidence path:
Rollback path:
```

Retirement is allowed only after a release record says the historical evidence remains reachable through docs or run records and the canonical replacement is documented.

## Legacy fallback workflows and paths

The legacy fallback is primarily a script path, not a separate workflow family:

```text
scripts/openai_lab_run.py
```

It may still be reachable through weekly override behavior when `PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false` is set for emergency rollback or controlled diagnosis.

It is non-canonical.

For ordinary `week-*` runs, the legacy script has a downstream gate and refuses to proceed unless this explicit override is present:

```text
PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true
```

This second gate is intentional. The weekly feature flag alone must not silently spend a legacy API/SDK attempt.

It should not be removed merely because the canonical weekly runner is default-on. Removal requires a separate legacy-removal gate after ordinary default-on operation is verified.

## Legacy fallback removal gate

This gate defines when it is permissible to open a later PR that removes the legacy API/SDK fallback path.

It does not remove `scripts/openai_lab_run.py`.

It does not approve deletion by itself.

A future legacy fallback removal PR must record all of these conditions:

```text
ordinary default-on weekly no-eligible run observed
vote summary PR created
implementation PR: none for the no-eligible run
no implementation-agent attempt made for the no-eligible run
no Codex/API call made for the no-eligible run
legacy API/SDK runner not reached for the no-eligible run
eligible canonical run has selected-prompt canary evidence or a next natural eligible-run observation plan
canonical diagnostics artifact remains verified
canonical public bundle artifact remains verified
canonical uploaded bundle verification artifact remains verified
manual review remains required
auto-merge remains disabled
rollback plan exists
public docs no longer cite legacy fallback as an active requirement
maintainer explicitly approves removal
```

The removal PR must also state:

```text
Legacy files removed:
Legacy workflows or branches affected:
Observed no-eligible run:
Observed eligible canonical evidence or planned natural eligible observation:
Generated snapshots intentionally untouched: true
Rollback path:
Contract tests updated:
```

Failing any condition means the legacy fallback remains present, non-canonical, and gated.

## Cleanup candidates

These are candidates for future consolidation. They are not deletion instructions.

| Candidate | Why it may be cleaned later | Required removal gate |
|---|---|---|
| Older canary workflow family | Many historical canary workflows make the active path harder to see | Replacement evidence map exists and release record approves retirement |
| Offline JSON canary workflow | Non-canonical path can be confused with canonical evidence | Legacy fallback policy is finalized and references are updated |
| First canary workflow family | Superseded by Docker/Codex selected-prompt task-packet evidence | Historical evidence remains linked from docs and run records |

## Removal gate for workflows

A workflow removal PR must state:

```text
Evidence role:
Canonical or legacy role:
Generated snapshot ownership:
Replacement path:
Affected docs:
Affected contract tests:
Rollback path:
```

A workflow should not be removed if any public doc still lists it as required active evidence.

## Current safe next actions

The next safe cleanup work is:

```text
1. Verify the first ordinary scheduled default-on weekly run.
2. Keep scripts/openai_lab_run.py labeled as legacy and non-canonical.
3. Keep weak historical canary workflows gated unless a maintainer intentionally enables ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS=true.
4. Keep the legacy weekly fallback gated by PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true unless a separate removal PR retires it.
5. Defer legacy fallback removal until a separate legacy-removal gate exists and passes.
6. Defer workflow deletion until a release readiness record approves it.
```