# Canonical status drift check

## Purpose

This document defines the repository-wide status language for the selected-prompt runner, weekly automation, legacy API surfaces, and cleanup boundaries.

It prevents documentation drift between participant docs, operator docs, workflow docs, and implementation path docs.

## Stable status contract

All maintainer-authored docs should preserve these facts until a later PR deliberately changes them:

```text
canonical selected-prompt runner: Docker/Codex selected-prompt task-packet runner
canonical runner script: scripts/run_codex_selected_prompt.sh
canonical runner name: codex-cli-selected-prompt-packet-container
canonical evidence marker: Canonical selected-prompt runner: true
weekly default status: canonical selected-prompt runner fixed-on
weekly feature flag override: removed
weekly legacy override: removed from Weekly Auto Run
legacy fallback script: scripts/openai_lab_run.py
legacy fallback status: non-canonical manual diagnostic / historical fallback
legacy fallback removal status: not approved until the explicit legacy fallback removal gate passes
ordinary default-on weekly no-eligible observation: PASS
workflow deletion status: obsolete Legacy First API Canary Run retired
auto-merge status: disabled
manual review status: required
final write scope: lab/index.html, lab/style.css, lab/app.js
```

## Source-of-truth map

| Topic | Source of truth | Pointer docs |
|---|---|---|
| Repository-wide canonical, legacy, fixed-on weekly, auto-merge, manual-review, and release-gate status | `docs/canonical-status-drift-check.md` | `docs/README.md`, `docs/weekly-automation.md`, `docs/operator-runbook.md` |
| Technical implementation boundary | `docs/current-codex-implementation-path.md` | `docs/canonical-runner-evidence-guide.md`, `docs/workflow-family-map.md` |
| Participant/reviewer evidence decision rule | `docs/canonical-runner-evidence-guide.md` | `docs/README.md`, `docs/operator-runbook.md`, `docs/weekly-automation.md` |
| Weekly workflow operation | `docs/weekly-automation.md` | `docs/operator-runbook.md` |
| Maintainer operating procedure and stop rules | `docs/operator-runbook.md` | `docs/README.md` |
| Cleanup and deletion boundaries | `docs/repository-cleanup-inventory.md`, `docs/workflow-family-map.md` | `docs/README.md`, `docs/operator-runbook.md` |

Pointer docs may summarize status, but they should not become a second source of truth for release-gate wording.

## Documents covered by this drift check

| Document | Required role |
|---|---|
| `docs/README.md` | Short public status and navigation |
| `docs/current-codex-implementation-path.md` | Full canonical and legacy path definition |
| `docs/canonical-runner-evidence-guide.md` | Participant/reviewer evidence decision rule |
| `docs/weekly-automation.md` | Weekly schedule, support unlock prerequisite, and fixed canonical runner operation |
| `docs/operator-runbook.md` | Maintainer operation and cleanup instructions |
| `docs/workflow-family-map.md` | Workflow-family classification and deletion boundary |
| `docs/repository-cleanup-inventory.md` | Cleanup protection and not-yet-removable inventory |

## Non-drift rules

Docs may use different wording, but they must not contradict these rules:

```text
1. Do not call scripts/openai_lab_run.py canonical.
2. Do not imply the weekly canonical selected-prompt runner is default-off or feature-flagged.
3. Do not say auto-merge is enabled.
4. Do not omit the canonical evidence marker from evidence-facing docs.
5. Do not treat a useful lab diff as sufficient canonical evidence.
6. Do not reintroduce a weekly legacy override without an explicit rollback PR.
7. Do not describe legacy fallback removal as approved before the explicit legacy fallback removal gate passes.
8. Do not delete protected evidence, generated snapshots, run records, or comparison output during cleanup.
```

## Required canonical evidence marker

Evidence-facing docs should preserve this exact marker:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

Reason:

```text
Participants and maintainers need one grep-able marker that distinguishes canonical Docker/Codex selected-prompt evidence from legacy or historical runs.
```

## Required legacy script language

Docs that mention `scripts/openai_lab_run.py` should identify it as:

```text
non-canonical
manual diagnostic / historical fallback
not reachable from Weekly Auto Run
not selected-prompt canonical evidence
```

Reason:

```text
The script may remain useful for manual diagnosis or historical comparison, but the active weekly workflow no longer branches to it.
```

## Required weekly status language

Weekly-operation docs should preserve the current fixed canonical status:

```text
weekly default status: canonical selected-prompt runner fixed-on
weekly feature flag override: removed
weekly legacy override: removed from Weekly Auto Run
Weekly Auto Run no longer has a legacy API/SDK branch.
```

A future rollback PR may change this status only if it also updates:

```text
docs/weekly-automation.md
docs/operator-runbook.md
docs/current-codex-implementation-path.md
docs/canonical-runner-evidence-guide.md
docs/README.md
docs/workflow-family-map.md
docs/repository-cleanup-inventory.md
scripts/test_canonical_status_drift.py
```

## Required release gate language

Docs should preserve the release-gate result:

```text
manual selected-prompt smoke: PASS
weekly selected-prompt canary with eligible candidate: PASS
weekly diagnostics artifact: present
weekly public bundle artifact: present
weekly uploaded bundle verification artifact: present
bounded lab diff: PASS
ordinary default-on weekly no-eligible observation: PASS
legacy script documented as non-canonical manual diagnostic / historical fallback
obsolete Legacy First API Canary Run workflow retired
manual review remains required
auto-merge remains disabled
weekly canonical fixed-on release: approved
```

## Current release status

Current status is:

```text
manual selected-prompt workflow: verified
weekly canonical selected-prompt canary: verified
ordinary default-on weekly no-eligible observation: PASS
canonical weekly runner: fixed-on
weekly legacy branch: removed
legacy script: present and non-canonical
legacy script removal: not approved until the explicit legacy fallback removal gate passes
obsolete Legacy First API Canary Run workflow: retired
auto-merge: disabled
manual review: required
```

## Required legacy fallback removal gate

The legacy fallback removal gate is a deletion-prevention gate, not a deletion approval by itself.

`docs/workflow-family-map.md` owns the detailed checklist. Maintainer-facing docs may summarize it, but they must preserve these minimum conditions:

```text
ordinary default-on weekly no-eligible run observed
vote summary PR created
no implementation-agent attempt made for no-eligible run
no Codex/API call made for no-eligible run
weekly legacy branch absent from Weekly Auto Run
eligible canonical run has selected-prompt canary evidence or a next natural eligible-run observation plan
canonical evidence artifacts remain verified
rollback plan exists
public docs no longer cite legacy script as an active weekly requirement
maintainer explicitly approves removal
```

Until those conditions are deliberately recorded for removal, `scripts/openai_lab_run.py` remains present and non-canonical.

## Retired cleanup record

This cleanup retired only the obsolete legacy first API canary launch path:

```text
removed workflow: .github/workflows/first-canary-run.yml
removed helper: scripts/create_first_canary_candidate.py
protected evidence removed: no
generated snapshots touched: no
run records touched: no
scripts/openai_lab_run.py removed: no
```

## Change discipline

A PR that changes any canonical, legacy, fixed weekly, or cleanup status should state:

```text
Status changed:
Affected docs:
Affected tests:
Evidence supporting change:
Rollback path:
```

Do not update one status document without updating the drift contract.
