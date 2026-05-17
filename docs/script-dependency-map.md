# Script dependency map

This map classifies important scripts before cleanup.

It is not a retirement plan.

A script should stay until its workflow callers, documentation callers, tests, and rollback role are understood.

## Current judgment

```text
scripts cleanup: not ready for broad retirement
canonical runner helpers: keep
legacy fallback: keep gated
public evidence builders: keep
contract tests: keep
ordinary default-on weekly observation: pending
```

## Script families

| Family | Examples | Current role | Cleanup posture |
|---|---|---|---|
| canonical runner | `run_codex_selected_prompt.sh` | active implementation path | keep and harden |
| weekly selection | `collect_votes.py`, `select_eligible.py`, `resolve_support_unlock.py` | active weekly path | keep |
| safety and static checks | `safety-check.sh`, `static-site-check.sh`, lab scope tests | active guards | keep |
| public evidence bundles | `build_public_agent_run_bundle.py`, `verify_public_agent_run_bundle.py` | active evidence path | keep |
| generated public outputs | public results, dashboards, history builders | generated evidence support | keep under owning flows |
| issue safety | issue scan and execution gate scripts | active safety gate | keep |
| legacy API path | `openai_lab_run.py` | non-canonical gated fallback | keep until removal gate passes |
| historical canary helpers | canary packet or older writeback helpers | historical or diagnostic support | keep until workflow-family gate passes |
| contract tests | `test_*.py`, shell self-tests | sustain layer | keep |

## Known active anchors

### Canonical selected-prompt implementation

```text
script: scripts/run_codex_selected_prompt.sh
workflow: .github/workflows/weekly-auto-run.yml
workflow: .github/workflows/codex-selected-prompt-run.yml
evidence marker: Runner: codex-cli-selected-prompt-packet-container
evidence marker: Canonical selected-prompt runner: true
```

### Weekly vote and support selection

```text
scripts/collect_votes.py
scripts/select_eligible.py
scripts/resolve_support_unlock.py
.github/workflows/weekly-auto-run.yml
.github/workflows/support-unlock-export.yml
```

### Public result and comparison evidence

```text
scripts/build_public_results_export.py
scripts/build_comparison_dashboard.py
scripts/create-weekly-snapshot.mjs
scripts/create-snapshot-summary.mjs
scripts/create-public-briefing.mjs
scripts/validate-evidence-artifact.mjs
```

### Public agent-run evidence

```text
scripts/build_public_agent_run_bundle.py
scripts/enrich_public_agent_run_bundle.py
scripts/verify_public_agent_run_bundle.py
scripts/run_gitleaks_public_bundle_scan.sh
```

### Issue safety and execution gate

```text
scripts/scan_issue_safety.py
scripts/check_issue_execution_gate.py
.github/workflows/issue-safety-scan.yml
```

### Legacy non-canonical fallback

```text
scripts/openai_lab_run.py
status: non-canonical gated fallback
ordinary week-* gate: PROMPT_VOTE_LAB_ALLOW_LEGACY_OPENAI_LAB_RUN=true
```

The legacy fallback remains present until the explicit legacy fallback removal gate passes.

## Retirement prerequisites

Before retiring a script, a later PR must record:

```text
script path:
current family:
workflow callers:
documentation references:
contract tests:
replacement path:
rollback path:
generated evidence impact:
maintainer approval:
```

## Do not retire yet

Do not retire these before ordinary default-on weekly observation:

```text
scripts/openai_lab_run.py
scripts/run_codex_selected_prompt.sh
weekly selection scripts
support unlock scripts
public evidence bundle scripts
workflow contract tests
safety and static checks
```

## Current next action

Use this map with `docs/root-folder-audit.md` and `docs/workflow-family-map.md` before any script cleanup.

The next cleanup work should still be:

```text
observe ordinary default-on weekly run
then decide which legacy or historical helpers can move toward retirement
```