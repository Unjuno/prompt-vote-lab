# Canonical runner evidence guide

## Purpose

This guide is for participants and reviewers who want to decide whether a Prompt Vote Lab implementation run used the canonical Docker/Codex selected-prompt runner.

A run is not canonical merely because it produced a small valid lab diff.

A run is canonical only when the public PR/run evidence shows the Docker/Codex selected-prompt task-packet path and the bounded evidence chain.

## Quick decision rule

Treat a weekly implementation PR as canonical only when the PR or run evidence says:

```text
Runner: codex-cli-selected-prompt-packet-container
Canonical selected-prompt runner: true
```

If those lines are missing, treat the run as non-canonical until proven otherwise.

## What to inspect first

For a weekly canonical selected-prompt run, inspect these in order:

```text
1. The implementation PR body
2. The Weekly Auto Run workflow run
3. The diagnostics artifact
4. The public bundle artifact
5. The uploaded bundle verification artifact
6. The changed file list
```

Do not start by trusting the visible UI change. The UI diff is only the output. The evidence chain tells you whether the boundary held.

## Expected artifacts

A successful weekly canonical selected-prompt run should expose artifacts named like:

```text
weekly-selected-prompt-diagnostics-<run_number>
weekly-selected-prompt-public-bundles-<run_number>
weekly-selected-prompt-uploaded-bundle-verification-<run_number>
```

For the verified weekly canary, the artifact names were:

```text
weekly-selected-prompt-diagnostics-7
weekly-selected-prompt-public-bundles-7
weekly-selected-prompt-uploaded-bundle-verification-7
```

## What each artifact proves

| Evidence | What it is used for | What it does not prove alone |
|---|---|---|
| diagnostics artifact | Internal boundary and run diagnostics | Public safety by itself |
| public bundle artifact | Redacted participant-facing evidence | That upload/download preserved it |
| uploaded bundle verification artifact | Reverification after artifact upload/download | That the implementation diff is desirable |
| implementation PR diff | Final changed files and review target | That the runner was canonical |

## Boundary checks to look for

A canonical selected-prompt Docker/Codex run should show:

```text
/work:rw
/task:ro
/codex-runtime:rw
repo_root_mounted: false
OPENAI_API_KEY present before codex exec: no
changed files subset of lab/index.html, lab/style.css, lab/app.js
forbidden changed files: none
```

The `/task:ro` write-test may have a failing write exit code. That is expected when the read-only mount rejects writes.

## Changed file rule

Only these final files may change:

```text
lab/index.html
lab/style.css
lab/app.js
```

If a canonical implementation PR changes workflows, scripts, rules, docs, data, run records, or repository policy, treat it as a boundary failure unless a separate human-authored PR explains the non-agent change.

## Secret and redaction checks

Public evidence should pass both bundle verification and Gitleaks-style scanning.

Expected result:

```text
public bundle verification: ok
uploaded bundle verification: ok
Gitleaks finding count: 0
```

Redaction is a publication guard, not a mathematical proof that secrets are impossible. If a token-like secret appears in any public artifact, rotate the token and treat it as an incident.

## Non-canonical fallback

The legacy `scripts/openai_lab_run.py` path may still exist as a migration fallback.

It is non-canonical.

It does not satisfy the selected-prompt canonical runner requirement, even if it produces a useful lab diff.

The fallback should be used only through an explicit rollback or diagnostic override, not as the normal weekly default.

## Verified weekly canary

The first verified weekly canonical selected-prompt canary used:

```text
workflow run: 25858202166
selected Issue: #282
summary PR: #283
implementation PR: #284
runner: codex-cli-selected-prompt-packet-container
canonical selected-prompt runner: true
artifacts:
  - weekly-selected-prompt-diagnostics-7
  - weekly-selected-prompt-public-bundles-7
  - weekly-selected-prompt-uploaded-bundle-verification-7
result: PASS
```

The canary PRs were closed without merge because they were evidence-only canary artifacts, not product changes.

## Release status

The weekly canonical selected-prompt runner is default-on after the release gate passed:

```text
manual selected-prompt smoke: PASS
weekly feature-flag canary with eligible candidate: PASS
weekly diagnostics artifact: present
weekly public bundle artifact: present
weekly uploaded bundle verification artifact: present
bounded lab diff: PASS
legacy fallback documented as non-canonical
participant evidence guide published
manual review remains required
auto-merge remains disabled
weekly canonical default-on release: approved
```

A future rollback may set `PROMPT_VOTE_LAB_USE_CANONICAL_SELECTED_PROMPT_RUNNER=false`, but that run is non-canonical unless its evidence still shows the canonical marker.

## What participants should conclude

A canonical evidence chain supports this conclusion:

```text
The implementation was produced through the bounded Docker/Codex selected-prompt runner, with public evidence sufficient for participant review.
```

It does not automatically prove:

```text
The change is desirable.
The prompt was the best prompt.
The model reasoned correctly.
The run should be merged.
```

Merge decisions remain manual.