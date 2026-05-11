# first-canary-007 policy-agent evidence-only result

## Status

PASS as canonical Docker/Codex policy-agent E2E evidence.

Not adopted into `main` as a lab UI change.

This record closes the evidence loop for workflow run `25670780249` and PR #263.

## Source

```text
Workflow: Codex Policy Agent Canary Run
Workflow run id: 25670780249
Event: workflow_dispatch
Head branch at run time: main
Head SHA at run time: 7f0a34f763b76a3a4ccb2a05890d1edcb7c0e643
Conclusion: success
```

## Runner configuration

```text
Canary id: first-canary-007
Provider: openai-codex
Runner: codex-cli-policy-enforced-agent-container
Sandbox mode: docker-mounted-workdir-only
Model: gpt-5.4-nano
Attempts: 1
Retry policy: none
Fallback policy: none
Auto-merge: disabled
Final writable files: lab/index.html, lab/style.css, lab/app.js
```

The intended boundary for this run was:

```text
- repository root is not mounted into the Codex work directory
- Codex edits a prepared /work directory
- final copyback is limited to lab/index.html, lab/style.css, and lab/app.js
- manual review is required before any adoption
```

## PR result

```text
PR: #263
Title: Run Codex policy-enforced agent canary
State: CLOSED
Merged: false
Head branch: codex-policy-agent-canary-007-7
Head commit: b00a5852d1d4972c0d0207dea4462644d72dab0a
Base commit at PR creation: 7f0a34f763b76a3a4ccb2a05890d1edcb7c0e643
Changed files: 1
Additions: 1
Deletions: 0
```

Changed file:

```text
lab/index.html
```

Diff summary:

```text
Added one status pill:
Codex bounded implementation-agent Canary #7
```

## Internal checks

The PR body records that the workflow completed these checks before PR creation:

```text
- policy-enforced container runner completed before PR creation
- changed-file guard passed before PR creation
- safety-check passed before PR creation
- static-site-check passed before PR creation
```

No PR-side follow-up CI status was observed on the PR head commit. This is expected for a branch pushed by `GITHUB_TOKEN` in some GitHub Actions configurations, but it means the pre-PR workflow checks are the recorded verification source for this canary PR.

## Public artifacts

The workflow run uploaded these artifacts:

```text
codex-policy-agent-canary-public-bundle-7
artifact_id: 6918707781
size: 28859 bytes
expired: false

action artifact digest:
sha256:b73cab169e98d9599ba4b6e50d805ca836146f0f002e42cc084bae48f1beb19f
```

```text
codex-policy-agent-canary-public-log-7
artifact_id: 6918708759
size: 584 bytes
expired: false

action artifact digest:
sha256:cc25992185d90a7ab467bf5dfd54ea2410f36b6e4ec10f47793a16124c47b7cc
```

```text
codex-policy-agent-canary-diagnostics-7
artifact_id: 6918708255
size: 14352 bytes
expired: false

action artifact digest:
sha256:24a2815363a100a5367e084573a16f8c41af4570382e695fad316528a9f1b220
```

Expected public bundle contents include:

```text
index.json
README.md
observation-summary.md
observation-summary.json
raw/
sanitized/
reasoning-traces/
```

## Reasoning trace evidence policy

For this canary series, exposed reasoning / CoT-like trace artifacts are part of the experiment when they exist in run artifacts.

The intended publication rule is:

```text
if a run artifact exposes reasoning / CoT-like trace text:
    publish it under reasoning-traces/ after sanitizer replacement
else:
    record it as unavailable
```

Provider-private internals that are not exposed to the workflow are not claimed to be available.

## Verification limit

Artifact existence and metadata were verified through the GitHub Actions artifact listing.

ZIP contents were not manually inspected in this review environment. Therefore this record does not claim manual inspection of:

```text
observation-summary.md
observation-summary.json
sanitized/
reasoning-traces/
```

This is a narrow evidence record, not an overclaim.

## Disposition

PR #263 was closed as evidence-only and not merged.

Reason:

```text
- the Docker/Codex canary path completed and produced a bounded lab PR
- the visible lab change was only a canary status pill
- later publication fixes landed after the canary PR was created
- force-updating the PR branch would weaken the original Codex-generated head commit evidence
- the visible canary pill is not needed in the accepted live lab
```

## Interpretation

This run supports the following limited claim:

```text
The canonical Docker/Codex policy-agent canary path can complete on GitHub Actions, create a lab-scoped PR, and upload public/internal evidence artifacts without auto-merging.
```

It does not prove:

```text
- production readiness for weekly-auto-run migration
- correctness of every public bundle file without manual ZIP inspection
- general prompt-injection safety
- semantic quality of the generated lab change
- readiness for auto-merge
```

## Follow-up work

```text
1. Add an automated artifact-content verification path, or manually inspect the public bundle ZIP for a future run.
2. Migrate weekly eligible implementation path to the canonical Docker/Codex runner only after artifact verification is repeatable.
3. Keep auto-merge disabled.
4. Keep generated implementation PRs separate from evidence/docs/test changes.
```
