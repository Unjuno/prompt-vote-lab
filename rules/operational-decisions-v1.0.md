# operational-decisions-v1.0

## Purpose

This document fixes previously undefined operational areas for Prompt Vote Lab.

The goal is to avoid ambiguous weekly execution.

## 1. Automation boundary

Allowed to automate:

- weekly candidate packaging
- rank-1 implementation run
- support-unlocked rank-2 and rank-3 implementation runs
- PR creation
- safety-check execution
- run log draft creation
- blog draft creation

Not automated:

- merge into `main`
- safety-check bypass
- maintainer review
- final expectation-gap classification
- final blog publication

## 2. Implementation model

Implementation model is fixed by `model-policy-v1.0`:

```text
gpt-5-nano
```

This model is used only for editing `lab/`.

## 3. Evaluation and blog model

The evaluation and blog-writing model may be stronger than the implementation model.

It must not modify `lab/`.

It may produce:

- analysis draft
- expectation-gap suggestion
- Hacker News draft
- rule-change suggestion

The maintainer makes the final decision.

## 4. File scope

The implementation model may edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

No additional files under `lab/` are allowed in v1.0.

Complexity accumulation inside these three files is intentional and part of the experiment.

## 5. Weekly candidate policy

Each weekly vote may produce:

- rank 1: normal weekly run
- rank 2: support-unlocked comparison run
- rank 3: support-unlocked comparison run

Rank 4 and below are not executed in v1.0.

## 6. Support policy

Initial support thresholds:

- rank 2 unlock: 5 USD weekly support
- rank 3 unlock: 10 USD total weekly support

Support applies only to the current weekly vote.

Support does not guarantee merge, success, or adoption.

## 7. Mainline merge policy

Rank 1 is the default mainline candidate.

Rank 2 and rank 3 are comparison runs.

If rank 1 is rejected, the default result is no merge for that weekly vote.

Rank 2 and rank 3 are not automatically promoted.

## 8. Retry policy

Default retry count is 0.

If an implementation run fails, record the failure.

Do not silently retry with a stronger model.

## 9. Hacker News policy

Do not post the same pitch every week.

Post to Hacker News only when there is a concrete weekly result, failure, comparison, or rule change worth discussing.

## 10. Blog policy

Blog output is analysis, not implementation.

The blog should record:

- selected prompt
- candidate rank
- votes
- implementation PR
- changed files
- safety-check result
- merge/reject decision
- expectation-gap classification
- missing data as `unrecorded`

Do not invent missing facts.

## 11. Cost policy

The project accepts small experimental cost.

Cost control rules:

- maximum 3 implementation runs per weekly vote
- implementation model fixed to low-cost model
- no automatic retry
- blog generation is limited to one draft per weekly result
- thresholds may be changed in later rule versions

## 12. Versioning policy

If any of these decisions change, create a new rule version.

Examples:

- `operational-decisions-v1.1`
- `model-policy-v1.1`
- `support-unlocked-runs-v1.1`

Do not compare results across changed rule versions without recording the change.
