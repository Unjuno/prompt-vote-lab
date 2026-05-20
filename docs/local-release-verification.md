# Local release verification

## Purpose

This checklist defines how to verify Prompt Vote Lab locally before a soft release or public release.

Local verification is not a replacement for GitHub Actions, GitHub Pages smoke checks, weekly workflow evidence, or manual review. It is a pre-release operator check that reduces avoidable mistakes before announcing the project.

## Release rule

```text
Local pass is necessary but not sufficient.
GitHub Actions pass is required.
GitHub Pages public rendering must be checked.
Manual review remains required.
Auto-merge remains disabled.
```

## Scope

This checklist covers:

```text
clone and clean working tree
local syntax checks
contract tests for canonical/cleanup/release docs
static page preview
participant route check
operator route check
release-blocking failure conditions
```

It does not cover:

```text
running the paid implementation agent locally
calling external model APIs
publishing externally
turning on auto-merge
rewriting run records
regenerating public result snapshots
```

## Clone or refresh

Fresh clone:

```bash
git clone https://github.com/Unjuno/prompt-vote-lab.git
cd prompt-vote-lab
git switch main
git pull --ff-only origin main
```

Existing clone:

```bash
cd prompt-vote-lab
git fetch origin --prune
git switch main
git pull --ff-only origin main
git status
```

Required clean state:

```text
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

If the working tree is not clean, stop and decide whether the local changes should be committed, stashed, or discarded. Do not release from an ambiguous local tree.

## Runtime prerequisites

Minimum local tools:

```text
git
python 3
node 20 or compatible local Node for syntax checks
bash for shell syntax checks, or Git Bash on Windows
```

Windows PowerShell users can run Python and Node checks directly, but shell script syntax checks need Bash-compatible tooling.

## Local syntax checks

Python syntax check:

```powershell
Get-ChildItem scripts -Recurse -Filter *.py | ForEach-Object {
  python -m py_compile $_.FullName
}
```

Node syntax check:

```powershell
Get-ChildItem scripts -Recurse -Filter *.mjs | ForEach-Object {
  node --check $_.FullName
}
```

Bash syntax check:

```bash
find scripts -name '*.sh' -print0 | xargs -0 -I{} bash -n {}
```

## Required local contract checks

Run these before release review:

```bash
python scripts/test_canonical_status_drift.py
python scripts/test_current_codex_path_doc.py
python scripts/test_canonical_runner_evidence_guide.py
python scripts/test_repository_cleanup_inventory.py
python scripts/test_workflow_family_map.py
python scripts/test_canary_archive_inventory.py
python scripts/test_weekly_operator_docs.py
python scripts/test_local_release_verification.py
python scripts/test_script_check_workflow_contract.py
```

These checks cover the current release-critical documentation contract:

```text
canonical selected-prompt runner status
fixed-on weekly runner status
legacy script non-canonical status
cleanup and protected-evidence boundaries
canary archive classification
operator release procedure
local release verification procedure
Script Check wiring
```

## Static page preview

Start a local static server:

```bash
python -m http.server 8000
```

Open:

```text
http://localhost:8000/
http://localhost:8000/lab/
```

Minimum checks:

```text
root page loads
lab page loads
root page explains prompt proposals and voting
root page mentions the 20-vote baseline
lab page remains static and does not require a backend
external scripts are not required for the static preview
```

## Participant route check

Before release, an unfamiliar participant should be able to answer:

```text
Where do I submit a prompt?
Where do I vote?
What does 👍 mean?
What is the no-change baseline?
What files can the implementation agent change?
Where can I inspect results and evidence?
```

If these answers are not obvious from the landing page, docs, and Issue template, do not public-release yet.

## Operator route check

Before release, the maintainer should be able to answer:

```text
Where is the canonical status contract?
Where is the weekly automation runbook?
Where is the selected-prompt evidence guide?
Where is the cleanup inventory?
Where is the canary archive inventory?
How do I stop after an unsafe or unclear run?
How do I verify that auto-merge remains disabled?
```

## GitHub Actions requirement

Local checks do not replace CI.

Required GitHub Actions status before release:

```text
Pre-API Freeze Audit: success
Static Site Check: success
Lab PR Scope Check: success
Script Check: success
```

If CI fails, local success does not matter. Fix CI first.

## GitHub Pages requirement

Before public release, open the deployed site and verify:

```text
https://unjuno.github.io/prompt-vote-lab/
https://unjuno.github.io/prompt-vote-lab/lab/
```

Minimum public checks:

```text
root page renders as HTML
lab page renders as HTML
links to GitHub-rendered docs work
Issue proposal route works
no raw Markdown page is presented as the main reader path
```

## Soft release versus public release

Soft release is acceptable when:

```text
local checks pass
CI passes
GitHub Pages renders correctly
manual review remains required
auto-merge remains disabled
participant route is understandable for a small trusted group
```

Public release should wait until:

```text
soft release path has been exercised
first ordinary release-week evidence is understandable
weekly no-eligible or eligible behavior can be explained publicly
Release Week numbering is not confused with internal ISO week IDs
maintainer can explain the canonical evidence chain without guessing
```

## Release blockers

Do not release if any of these are true:

```text
working tree is dirty
local syntax checks fail
release-critical contract tests fail
GitHub Actions fail
GitHub Pages root or lab page fails to render
participant cannot find prompt submission or voting route
auto-merge appears enabled
manual review requirement is unclear
legacy script is described as canonical
protected evidence, run records, generated snapshots, or history pages were deleted without a gate
```

## Current recommendation

For the current state of Prompt Vote Lab, the recommended path is:

```text
1. local verification
2. GitHub Actions verification
3. GitHub Pages verification
4. soft release to a small trusted group
5. observe Release Week 1 behavior
6. decide whether to broaden public release
```

Do not skip soft release. The first public impression will be shaped more by participant route clarity than by the internal runner architecture.
