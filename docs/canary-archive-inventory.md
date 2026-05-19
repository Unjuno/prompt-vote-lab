# Canary archive inventory

## Purpose

This inventory classifies historical canary workflows and canary-era docs before any further cleanup.

It is a deletion-prevention map. It does not approve removing any workflow, doc, run record, artifact, or generated evidence by itself.

## Current rule

```text
Do not delete historical canary evidence merely because the canonical selected-prompt runner is fixed-on.
Do not treat a historical canary workflow as current canonical evidence unless the evidence contains the canonical marker.
Do not remove a canary workflow without a replacement evidence path, affected-doc list, affected-test list, and rollback path.
```

Canonical evidence marker:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

## Inventory states

| State | Meaning | Default action |
|---|---|---|
| Canonical active | Current selected-prompt implementation or verification path | Keep and harden |
| Historical gated evidence | Old weaker canary retained for audit, gated against accidental rerun | Keep; do not run unless intentionally enabled |
| Historical evidence | Old canary retained for comparison and design history | Keep; label historical |
| Boundary evidence | Canary that proves a specific sandbox, task-packet, or Issue-safety boundary | Keep until replacement evidence is stronger and linked |
| Non-canonical compatibility evidence | Evidence for a path that can work but is not current canonical production evidence | Keep; never cite as current canonical |
| Cleanup candidate | Candidate for later consolidation or retirement | Do not delete until removal gate passes |

## Workflow inventory

| Workflow | State | Keep reason | Removal gate |
|---|---|---|---|
| `.github/workflows/codex-selected-prompt-run.yml` | Canonical active | Manual canonical selected-prompt smoke path | Not a cleanup candidate |
| `.github/workflows/weekly-auto-run.yml` | Canonical active / weekly active | Fixed-on canonical weekly selected-prompt path for eligible candidates | Not a cleanup candidate |
| `.github/workflows/codex-first-canary-run.yml` | Historical gated evidence | Records early workspace-write canary behavior | Replacement evidence map plus explicit retirement PR |
| `.github/workflows/codex-isolated-3file-canary-run.yml` | Historical gated evidence | Records isolated three-file execution attempt | Replacement evidence map plus explicit retirement PR |
| `.github/workflows/codex-isolated-3file-relaxed-canary-run.yml` | Historical gated evidence | Records relaxed sandbox canary behavior | Replacement evidence map plus explicit retirement PR |
| `.github/workflows/codex-agent-observed-canary-run.yml` | Historical gated evidence | Records agent-observed direct edit path | Replacement evidence map plus explicit retirement PR |
| `.github/workflows/codex-writeback-canary-run.yml` | Historical evidence | Records unified diff writeback attempt | Replacement evidence map plus explicit retirement PR |
| `.github/workflows/codex-offline-json-canary-run.yml` | Non-canonical compatibility evidence | Records offline JSON full-file replacement path | Legacy script policy finalized plus explicit retirement PR |
| `.github/workflows/canary-007-policy-feasibility.yml` | Boundary evidence | Records feasibility of policy-enforced container execution | Replacement evidence proves same or stronger boundary |
| `.github/workflows/codex-policy-agent-canary-run.yml` | Boundary evidence | Records policy-agent diagnostics and public bundle evidence | Replacement evidence proves same or stronger boundary |
| `.github/workflows/codex-task-packet-canary-run.yml` | Boundary evidence | Records read-only task-packet boundary evidence | Replacement evidence proves same or stronger boundary |
| `.github/workflows/codex-fixed-issue-instruction-canary-run.yml` | Boundary evidence | Records fixed-Issue instruction packet and safety-gate evidence | Replacement evidence proves same or stronger boundary |

## Doc inventory

| Doc | State | Keep reason | Cleanup rule |
|---|---|---|---|
| `docs/codex-path-005-vs-007.md` | Historical evidence | Explains path comparison and migration reasoning | Keep unless superseded by a linked archive summary |
| `docs/canary-007-policy-enforced-agent.md` | Boundary evidence | Explains policy-enforced agent canary | Keep until boundary evidence is summarized elsewhere |
| `docs/canary-008-selected-prompt-task-packet.md` | Boundary evidence | Explains selected-prompt task packet design | Keep; still relevant to canonical task-packet boundary |
| `docs/canary-009-selected-issue-instructions.md` | Boundary evidence | Explains fixed-Issue instruction packet design | Keep; still relevant to Issue-derived prompts |
| `docs/canary-policy.md` | Historical / compatibility evidence | Documents legacy API canary policy | Keep as historical unless legacy script is removed |
| `docs/first-canary-readiness.md` | Cleanup candidate | Pre-launch readiness record for old path | Summarize before removal |
| `docs/first-canary-prompt.md` | Cleanup candidate | Old canary prompt record | Preserve only if referenced by run records or archive summary |
| `docs/first-canary-report-template.md` | Cleanup candidate | Old report template | Replace with current evidence/report templates before removal |
| `docs/stop-rules.md` | Historical operating rule | May still encode useful stop policy | Review separately before removal |
| `docs/pre-api-freeze.md` | Historical guardrail record | Captures earlier API/SDK freeze assumptions | Keep while `scripts/openai_lab_run.py` remains present |

## Gated weak canary rule

These workflows must remain gated:

```text
.github/workflows/codex-first-canary-run.yml
.github/workflows/codex-isolated-3file-canary-run.yml
.github/workflows/codex-isolated-3file-relaxed-canary-run.yml
.github/workflows/codex-agent-observed-canary-run.yml
```

Required gate:

```text
ALLOW_HISTORICAL_WEAK_CANARY_WORKFLOWS=true
```

If a future PR removes the gate, it must explain why the old weak path is safe to run by default. That should normally be rejected.

## Removal gate for historical canary workflows

A future removal PR must include:

```text
Workflow removed:
Historical evidence role:
Current active role, if any:
Replacement evidence path:
Affected docs:
Affected tests:
Protected evidence check:
Generated snapshot check:
Run record check:
Rollback path:
Maintainer approval:
```

Minimum conditions:

```text
replacement evidence is documented
public docs no longer cite the workflow as required active evidence
contract tests are updated
run records remain inspectable
public generated snapshots remain untouched
rollback path is explicit
```

## Safe next actions

Current safe next actions are:

```text
1. Keep all listed canary workflows for now.
2. Keep gated weak canaries gated.
3. Audit cleanup-candidate docs one by one.
4. Summarize removable first-canary docs before deleting any of them.
5. Do not delete run records, public bundles, support unlock records, comparison dashboards, or history pages.
```
