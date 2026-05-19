# Weekly automation

This document explains what runs automatically, when it runs, and what must exist before each weekly run can proceed.

Repository-wide canonical, legacy, fixed-on weekly runner, auto-merge, manual-review, and release-gate status is governed by [Canonical status drift check](./canonical-status-drift-check.md). This page is the weekly workflow operation detail, not a second status source of truth.

## Short answer

`Weekly Auto Run` is scheduled to run every week.

```text
.github/workflows/weekly-auto-run.yml
cron: 23 0 * * 1
```

That means:

```text
Monday 00:23 UTC
Monday 09:23 JST
```

It can also be started manually with `workflow_dispatch`.

## Related scheduled workflow

Support unlock aggregation is separate.

```text
.github/workflows/support-unlock-export.yml
cron: 17 0 * * *
```

That means:

```text
every day 00:17 UTC
every day 09:17 JST
```

The support export workflow writes the anonymized aggregate file used by the weekly run:

```text
data/support-unlocks/<week-id>.json
```

The weekly workflow requires the matching support unlock file before vote collection. Missing support data is not treated as 0 USD.

## Weekly run order

`Weekly Auto Run` runs in this order:

```text
1. checkout repository
2. set an initial RUN_WEEK
3. resolve the required support unlock file
4. prefer the previous UTC ISO week when its support unlock file exists
5. collect prompt proposal votes
6. insert no-change baseline
7. select eligible ranks
8. write weekly vote summary PR
9. if eligible candidates exist, require implementation secret
10. preflight the implementation run
11. create implementation PRs for eligible candidates through the canonical runner
12. upload canonical weekly diagnostics and public evidence
13. reverify uploaded canonical public bundles
```

If no candidate beats the no-change baseline, the workflow records a vote summary PR and stops before any implementation-agent attempt.

## Canonical weekly runner status

Current weekly status:

```text
weekly default status: canonical selected-prompt runner fixed-on
weekly feature flag override: removed
weekly legacy override: removed from Weekly Auto Run
Weekly Auto Run no longer has a legacy API/SDK branch.
```

Eligible selected prompts are routed through:

```text
scripts/run_codex_selected_prompt.sh
runner: codex-cli-selected-prompt-packet-container
sandbox_mode: docker-workdir-plus-readonly-selected-prompt-packet
prompt_transport: --prompt-file
repo_root_mounted: false
final_writable_files: lab/index.html, lab/style.css, lab/app.js
auto_merge_policy: disabled
manual_review: required
```

Canonical evidence must include:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

## Legacy script status

`scripts/openai_lab_run.py` still exists, but it is not part of `Weekly Auto Run`.

Current classification:

```text
scripts/openai_lab_run.py: non-canonical manual diagnostic / historical fallback
weekly reachability: none
canonical evidence status: invalid
```

Do not reintroduce a weekly legacy override during cleanup. A future rollback would need an explicit PR that updates workflow code, docs, and contract tests together.

## Canonical weekly evidence artifacts

A successful canonical weekly selected-prompt run should produce:

```text
weekly-selected-prompt-diagnostics-<run_number>
weekly-selected-prompt-public-bundles-<run_number>
weekly-selected-prompt-uploaded-bundle-verification-<run_number>
```

The evidence chain should include:

```text
public bundle verification: ok
uploaded bundle verification: ok
Gitleaks finding count: 0
changed files subset of lab/index.html, lab/style.css, lab/app.js
repo_root_mounted: false
OPENAI_API_KEY present before codex exec: no
```

## Observed no-eligible production evidence

The first ordinary default-on weekly no-eligible observation has passed.

```text
ordinary default-on weekly no-eligible observation: PASS
support unlock file: data/support-unlocks/2026-W20.json
vote summary PR: #333
merged run record: runs/week-2026-W20-vote-summary.md
baseline_won: true
eligible_count: 0
implementation-agent attempt: none
auto-merge: disabled
manual review: performed
```

This proves the ordinary no-eligible path resolves support data, records the weekly result, and stops before implementation-agent execution when the baseline wins. It does not prove that a future natural eligible implementation will succeed.

## Default-on release status

The complete release-gate checklist is owned by [Canonical status drift check](./canonical-status-drift-check.md).

Weekly workflow release result:

```text
manual selected-prompt smoke: PASS
weekly selected-prompt canary with eligible candidate: PASS
weekly diagnostics artifact: present
weekly public bundle artifact: present
weekly uploaded bundle verification artifact: present
bounded lab diff: PASS
ordinary default-on weekly no-eligible observation: PASS
manual review remains required
auto-merge remains disabled
weekly canonical fixed-on release: approved
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
```

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
```

Cleanup PRs should not touch generated snapshots unless they are explicitly generated snapshot PRs.
