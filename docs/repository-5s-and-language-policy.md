# Repository 5S and language policy

## Purpose

This policy keeps Prompt Vote Lab maintainable while the canonical runner migration continues.

It applies to maintainer-authored repository content, including source files, workflows, rules, scripts, lab UI files, and documentation.

The repository language for maintainer-authored content is English.

## 5S operating model

The project uses 5S as a repository maintenance discipline.

```text
Sort
Set in order
Shine
Standardize
Sustain
```

## 1. Sort

Keep active, evidence-bearing, or policy-bearing files.

Remove or close items that are only temporary canary scaffolding after their evidence has been recorded.

Do not delete protected public evidence casually.

Protected evidence includes:

```text
data/public-results.json
data/public-results.md
data/support-unlocks/*.json
runs/*.md
lab/comparisons/**
lab/history/**
merged PRs and Issues
workflow artifacts referenced by release evidence
```

If a file is legacy but still needed as a migration fallback, label it as legacy and non-canonical rather than deleting it.

## 2. Set in order

Every concept should have one primary home.

Current primary homes:

| Concept | Primary file |
|---|---|
| Canonical implementation path | `docs/current-codex-implementation-path.md` |
| Participant evidence reading | `docs/canonical-runner-evidence-guide.md` |
| Operator weekly controls | `docs/operator-runbook.md` |
| Weekly workflow behavior | `docs/weekly-automation.md` |
| Script Check registration | `.github/workflows/script-check.yml` |
| Script Check self-contract | `scripts/test_script_check_workflow_contract.py` |

Avoid duplicating policy text across many files. When duplication is necessary, add a contract test so drift is detected.

## 3. Shine

Clean small inconsistencies immediately when they are safe:

```text
stale status text
obsolete default claims
missing doc index links
unregistered doc tests
ambiguous legacy/canonical wording
missing cleanup instructions for temporary variables
```

Do not combine unrelated cleanups with runner behavior changes.

Do not hide functional changes inside cleanup PRs.

## 4. Standardize

All maintainer-authored text should be English.

This includes:

```text
Markdown docs
workflow names and comments
script comments and test messages
lab UI copy
rules
run records written by maintainers
```

Allowed exceptions:

```text
raw external evidence
quoted user-provided prompt text
third-party names that are not English
machine-generated public result snapshots
binary artifacts
```

Non-English source text should not be added to maintainer-authored docs, scripts, workflows, rules, or lab UI files.

Canonical and legacy wording must stay explicit:

```text
canonical: Docker/Codex selected-prompt runner
legacy: non-canonical fallback
```

## 5. Sustain

Each cleanup rule must have a mechanical guard where practical.

The current sustain guards are:

```text
Script Check
Lab PR Scope Check
current Codex path doc test
canonical runner evidence guide test
weekly operator docs test
script-check workflow contract test
repository language policy test
```

A cleanup PR should normally state:

```text
what was sorted
what was set in order
what was cleaned
what was standardized
what guard sustains it
```

## English-only guard

The repository has a CI guard for maintainer-authored paths.

The guard rejects CJK and other non-Latin script characters in authored source/docs/config paths.

It intentionally does not scan generated public result snapshots or raw external evidence files because those may contain user-provided text.

## Cleanup PR checklist

Before merging a cleanup PR, confirm:

```text
No workflow behavior changed unless the PR says so.
No runner implementation changed unless the PR says so.
No canonical default changed unless the PR says so.
No auto-merge was added.
No protected public evidence was deleted.
All new maintainer-authored content is English.
The relevant contract test was updated.
Script Check passed.
Lab PR Scope Check passed when applicable.
```

## Current migration boundary

The repository is cleaner when this distinction stays visible:

```text
canonical selected-prompt path: scripts/run_codex_selected_prompt.sh
legacy non-canonical fallback: scripts/openai_lab_run.py
```

Do not remove the legacy fallback until the release plan explicitly approves removal.

Do not flip the weekly canonical runner default until the default-on release gate is satisfied.
