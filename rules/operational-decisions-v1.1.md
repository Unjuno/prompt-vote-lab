# operational-decisions-v1.1

## Purpose

This version updates the automation boundary for Prompt Vote Lab.

## Automated in v1.1

The system may automate:

- weekly candidate packaging
- rank-1 implementation run
- support-unlocked rank-2 and rank-3 implementation runs
- implementation PR creation
- safety-check execution
- safety failure handling
- run log creation
- final expectation-gap classification
- blog report creation
- blog report publication
- Hacker News draft creation

## Not automated in v1.1

The system must not automate:

- merge into `main`
- weakening safety rules to accept a failed PR
- HN submission
- maintainer emergency override

## Safety failure handling

Safety failure is handled fail-closed.

If a run fails safety checks:

- do not merge the PR
- mark the result as `Unsafe` or `Rejected`
- record the failure in the run log
- publish a blog report about the failed run
- do not rerun with a stronger implementation model

## Final classification

Final expectation-gap classification is automated.

Allowed labels:

- Hit
- Partial
- Misread
- Overbuild
- Underbuild
- Rule conflict
- Unsafe
- Rejected

The classifier must use only recorded data. Missing data must be written as `unrecorded`.

## Blog publication

Blog publication is automated after a terminal run state:

- merged
- rejected
- unsafe
- failed
- no-change

A blog report must not claim success unless the implementation PR was merged.

## Implementation model

Implementation uses `model-policy-v1.0`:

```text
gpt-5-nano
```

The implementation model edits only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

## Evaluation model

A stronger evaluation model may classify results and write blog reports.

It must not modify `lab/`.

## Weekly rank policy

- rank 1: normal weekly implementation run
- rank 2: support-unlocked comparison run
- rank 3: support-unlocked comparison run

Rank 4 and below are not executed.

## Support policy

Initial thresholds:

- rank 2: 5 USD weekly support
- rank 3: 10 USD total weekly support

Support opens additional experiment runs only. It does not guarantee success, adoption, or merge.

## Mainline policy

Rank 1 is the default mainline candidate.

Rank 2 and rank 3 are comparison runs and are not automatically promoted.

If rank 1 is rejected, the default weekly result is no merge.

## Cost policy

- maximum 3 implementation runs per weekly vote
- no automatic retry
- one published blog report per weekly result

## Versioning

If this policy changes, create a new version.
