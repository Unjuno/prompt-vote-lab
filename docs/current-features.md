# Current feature inventory

This document lists the current implemented and intentionally not implemented features of Prompt Vote Lab.

It exists to reduce maintenance ambiguity after the first stable release.

## Public site

Implemented:

- root landing page
- static lab page under `lab/`
- public explanation docs under `docs/`
- operational rules under `rules/`
- recorded run history under `runs/`
- landing page links to GitHub-rendered Markdown docs instead of raw `.md` pages on GitHub Pages

Not implemented:

- dynamic backend
- user accounts
- database server
- external publishing
- automatic blog posting
- leaderboard
- automatic trust score

## Prompt game

Implemented:

- prompt proposals through GitHub Issues
- GitHub reactions as votes
- no-change baseline with 20 virtual votes by default
- issue-form prompt extraction
- legacy heading prompt extraction
- fallback to issue title when prompt body cannot be extracted
- top candidate ranking by vote count and issue number tie-break

Not implemented:

- paid votes
- user reputation score
- author score
- player ranking
- automatic penalties

## Vote collection and selection

Implemented:

- `scripts/collect_votes.py`
- `scripts/select_eligible.py`
- `scripts/test_collect_votes.py`
- `scripts/test_select_eligible.py`
- `scripts/test_weekly_auto_no_eligible.py`
- CI for collect-votes tests
- CI for eligible-selection tests
- CI for weekly no-eligible selector test

Current selection rule:

```text
baseline rank 1 => eligible = []
otherwise rank 1 prompt => normal-weekly-run
otherwise rank 2 prompt => support >= 5 unlocks support-unlocked-run
otherwise rank 3 prompt => support >= 10 unlocks support-unlocked-run
baseline itself is never eligible
```

## Weekly automation

Implemented:

- `Support Unlock Export`
- `Weekly Auto Run`
- `Weekly Mock Run`
- `Weekly Report Draft`
- support unlock JSON generation under `data/support-unlocks/`
- synthetic mock vote summary PR
- synthetic mock implementation PR
- model-free weekly report draft PR
- no-eligible summary PR path
- implementation-agent preflight before model dependency install

Verified:

- Support Unlock Export live path: verified.
- `data/support-unlocks/2026-W19.json` was generated and validated as anonymized aggregate output.
- Weekly Auto Run no-eligible production path created only `runs/week-2026-W19-vote-summary.md` in PR #243.
- The recorded summary had baseline rank 1 with 20 virtual votes.
- `eligible_count` was 0.
- `eligible_ranks` was empty.
- No implementation PR was created during that no-eligible run.
- Earlier no-eligible evidence also exists in PR #81, before the support-unlock prerequisite was added.

Not implemented:

- automatic merge
- automatic continuation run
- automatic external publishing
- automatic selection of fallback model
- automatic retry after model failure

## Implementation-agent API path

Prepared but not yet executed:

- fixed implementation model: `gpt-5.4-nano`
- one implementation attempt per candidate
- SDK retry must be 0
- no fallback model
- max output tokens capped at 5000
- eligible candidate secret requirement
- no-eligible path does not require implementation-agent secret
- preflight script before API dependency install

Deferred:

- raising max output tokens to 12000

Not yet done:

- real paid implementation-agent canary
- real implementation PR from model output
- merge of a real implementation PR

## Lab runtime boundary

Implemented:

- static HTML/CSS/JS only
- `lab/` is the implementation target
- safety checks block edits outside allowed scope for implementation PRs
- external scripts blocked
- external network calls blocked
- cookies blocked
- `eval` blocked
- dynamic or user-controlled `new Function(...)` blocked
- controlled fixed-body `new Function(...)` allowed
- `localStorage` allowed
- `sessionStorage` allowed
- `IndexedDB` allowed
- JSON export/import allowed locally

## Validation and safety checks

Implemented:

- static site structure check
- safety check
- exception matrix test
- multi-fuzz test
- collect-votes test
- select-eligible test
- weekly auto no-eligible selector test
- implementation preflight test
- Lean proof test
- pre-API freeze audit
- pre-API freeze audit self-test
- evidence artifact smoke test
- reusable evidence artifact validator

Verified:

- Evidence Pipeline Dry Run with `source=fixture` passed in Actions run `25335321720`.
- The fixture run executed `node scripts/validate-evidence-artifact.mjs tmp/evidence "${WEEK_ID}"` successfully.
- The fixture run uploaded artifact `evidence-pipeline-dry-run` with 7 files.
- Evidence Pipeline Dry Run with `source=live` passed in Actions run `25336303653`.
- The live run executed `node scripts/validate-evidence-artifact.mjs tmp/evidence "${WEEK_ID}"` successfully.
- The live artifact was opened and reviewed file-by-file in `runs/dry-run-001-evidence-review.md`.
- The live evidence review final decision is `PASS`.

## Formal proof

Implemented:

- Lean 4 model under `formal/Selection.lean`
- Lean 4 model under `formal/Canary.lean`
- `lean-toolchain`
- CI workflow for Lean proof checking

Currently proven:

```text
baselineWon candidates = true -> selectEligible candidates support = []
baseline candidate is not individually eligible
other candidate is not individually eligible
first canary policy satisfies the closed canary safety predicate
safe canary implies lab-only scope, one attempt, no SDK retry, one API call, no fallback, no auto-merge, and no external publishing
```

Scope limitation:

The Lean proof models the closed selection and canary-policy cores. It does not prove the full GitHub Actions runtime, GitHub API behavior, or model output behavior.

## Reporting

Implemented:

- model-free weekly report draft generation
- report draft PR workflow
- report policy
- report-generation rule

Not implemented:

- external blog publishing
- model-written final report
- automatic public syndication

## Support policy

Implemented:

- support policy docs
- support-unlocked comparison-runs policy
- support does not override the no-change baseline
- support cannot buy merge, adoption, or specification control

Not implemented:

- $20 support tier
- support as a maintenance or service contract

## Freeze state

Implemented:

- pre-API freeze checklist
- pre-API freeze audit script
- pre-API freeze audit CI
- Support Unlock Export live path verification
- Weekly Auto Run no-eligible production path verification
- Evidence Pipeline Dry Run fixture path verification
- Evidence Pipeline Dry Run live path verification

Current policy:

```text
No real implementation-agent API call until all offline gates are green and a single low-risk canary candidate is selected.
```

## Current release judgment

Current state:

```text
MVP structure: mostly complete
offline verification: strong
support unlock live path: verified
no-eligible production workflow path: verified
fixture evidence dry-run path: verified
live evidence dry-run path: verified
real implementation-agent canary: not yet executed
production autonomy: not complete
```

Operational recommendation:

Select one low-risk canary prompt and run exactly one bounded implementation-agent attempt under `docs/pre-api-freeze.md` and `docs/canary-policy.md`.
