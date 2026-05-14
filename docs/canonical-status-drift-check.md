# Canonical status drift check

## Purpose

This document defines the repository-wide status language for the selected-prompt runner migration.

It prevents documentation drift between participant docs, operator docs, workflow docs, and implementation path docs.

## Stable status contract

All maintainer-authored docs should preserve these facts until a later release PR deliberately changes them:

```text
canonical selected-prompt runner: Docker/Codex selected-prompt task-packet runner
canonical runner script: scripts/run_codex_selected_prompt.sh
canonical runner name: codex-cli-selected-prompt-packet-container
canonical evidence marker: Canonical selected-prompt runner: true
legacy fallback script: scripts/openai_lab_run.py
legacy fallback status: non-canonical migration fallback
weekly default status: default-off during migration
weekly feature flag: PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER
current default constant: DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false
auto-merge status: disabled
manual review status: required
final write scope: lab/index.html, lab/style.css, lab/app.js
```

## Source-of-truth map

Use this map before adding or editing status text.

| Topic | Source of truth | Pointer docs |
|---|---|---|
| Repository-wide canonical, legacy, default-off, auto-merge, manual-review, and release-gate status | `docs/canonical-status-drift-check.md` | `docs/README.md`, `docs/weekly-automation.md`, `docs/operator-runbook.md` |
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
| `docs/weekly-automation.md` | Weekly feature flag, default, and evidence artifact status |
| `docs/operator-runbook.md` | Maintainer operating and cleanup instructions |
| `docs/workflow-family-map.md` | Workflow-family classification and deletion boundary |
| `docs/repository-cleanup-inventory.md` | Cleanup protection and not-yet-removable inventory |

## Non-drift rules

Docs may use different wording, but they must not contradict these rules:

```text
1. Do not call scripts/openai_lab_run.py canonical.
2. Do not imply the weekly canonical selected-prompt runner is already default-on.
3. Do not say auto-merge is enabled.
4. Do not omit the canonical evidence marker from evidence-facing docs.
5. Do not treat a useful lab diff as sufficient canonical evidence.
6. Do not describe workflow or legacy runner deletion as safe without a release gate.
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

## Required legacy fallback language

Docs that mention `scripts/openai_lab_run.py` should also identify it as:

```text
non-canonical
fallback
legacy or migration fallback
```

Reason:

```text
The script may still exist and may still produce useful lab diffs, but those facts do not make it canonical selected-prompt evidence.
```

## Required default status language

Weekly-operation docs should preserve the default-off migration state:

```text
PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER
DEFAULT_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false
Still not default-on
```

A future default-on release PR may change this status only if it also updates:

```text
docs/weekly-automation.md
docs/operator-runbook.md
docs/current-codex-implementation-path.md
docs/canonical-runner-evidence-guide.md
docs/README.md
scripts/test_canonical_status_drift.py
```

## Required release gate language

Docs should preserve the release-gate rule:

```text
manual selected-prompt smoke: PASS
weekly feature-flag canary with eligible candidate: PASS
weekly diagnostics artifact: present
weekly public bundle artifact: present
weekly uploaded bundle verification artifact: present
bounded lab diff: PASS
legacy fallback documented as non-canonical
manual review remains required
auto-merge remains disabled
```

## Current release status

Current status is:

```text
manual selected-prompt workflow: verified
weekly canonical selected-prompt canary: verified
canonical weekly default: not default-on
legacy fallback: present and non-canonical
workflow deletion: not approved
auto-merge: disabled
manual review: required
```

## Change discipline

A PR that changes any canonical/legacy/default status should state:

```text
Status changed:
Affected docs:
Affected tests:
Evidence supporting change:
Rollback path:
```

Do not update one status document without updating the drift contract.
