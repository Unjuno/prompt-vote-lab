# Root folder audit

This document records a top-level repository audit before cleanup.

## Current judgment

```text
static security posture: acceptable
participant journey: present
live preview: present
bulk cleanup: not recommended yet
ordinary default-on weekly observation: pending
```

## Top-level surfaces

| Surface | Role | Status | Action |
|---|---|---|---|
| `.github/` | workflows and templates | active plus historical | keep and classify |
| `data/` | public generated data | protected evidence | keep under owning workflows |
| `docs/` | explanation and operations | active documentation | keep and consolidate |
| `formal/` | Lean policy evidence | contract or historical evidence | keep for now |
| `lab/` | public static lab and previews | active product surface | keep |
| `rules/` | agent and experiment constraints | active plus historical policy | keep and label |
| `runs/` | weekly summaries and records | protected evidence | keep |
| `scripts/` | automation, generators, guards, tests | active machinery plus legacy path | keep and map dependencies |
| `tests/` | fixtures and test support | support surface | keep when referenced |
| `index.html` | landing page | active entry | keep |
| `README.md` | repository entry | active entry | keep |
| `LICENSE` | license | required | keep |

## Findings

1. No top-level surface is obviously misplaced for the current static GitHub Pages experiment.
2. The repository is evidence-heavy, not automatically messy.
3. Historical and legacy surfaces must stay clearly labeled.
4. The largest remaining release condition is ordinary default-on weekly observation.
5. Cleanup should be staged by gates, not performed as a broad sweep.

## Questions before cleanup

```text
Q1. Should historical canary workflows stay until after ordinary default-on weekly observation?
Q2. Should old canary docs later move under an archive index?
Q3. Should the Lean formal layer remain active after release?
Q4. Should live previews use a generated latest-comparison pointer?
Q5. Should run records be treated as stable after merge?
Q6. Should scripts stay flat until after release?
Q7. Should fixture ownership be documented if fixtures grow?
```

## Recommended order

```text
1. Define legacy fallback removal gate.
2. Observe ordinary default-on weekly run.
3. Add script dependency map if script cleanup is desired.
4. Add workflow retirement plan if old canary workflows are retired.
5. Add archive indexes for historical docs or rules if desired.
6. Change only items whose gate is satisfied.
```

## Current answer

The repository should not receive broad cleanup yet.

It should receive staged cleanup after the release gates are explicit.