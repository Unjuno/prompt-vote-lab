# multi-fuzz-testing-v1.0

## Purpose

Multi-fuzz testing explores Prompt Vote Lab failure boundaries with weighted random mutations.

It is not a model-quality benchmark.

It is a workflow-boundary test for:

- safety-check sensitivity
- static-site-check sensitivity
- false positives
- false negatives
- unstable assumptions in the automation structure

## Method

A multi-fuzz run creates temporary repository copies, applies one mutation per trial, runs the relevant checks, and records:

- seed
- trial number
- mutation name
- mutation class
- expected result
- observed result
- check used
- pass/fail agreement

## Mutation classes

Initial classes:

- `unsafe_runtime`: external script, fetch, cookie, eval, iframe
- `scope_escape`: non-lab file mutation in an implementation-like context
- `allowed_local_state`: localStorage and local static-only behavior
- `public_site_breakage`: missing `/lab/` link or missing baseline explanation
- `bad_support_claim`: support framed as buying merge, adoption, or control
- `safe_docs_change`: safe documentation-only update

## Probability weights

Weights are intentionally heuristic at first.

The weights should be corrected later from observed failures and false positives.

A mutation with high false-negative risk should receive higher future weight.

A mutation that causes repeated uninformative failures should receive lower future weight.

## API usage

Multi-fuzz tests must not call OpenAI or any other paid model API.

## Output

A multi-fuzz run should emit machine-readable and human-readable outputs:

- JSON result artifact
- Markdown summary artifact

These outputs should normally be workflow artifacts, not committed as canonical data.

## Rationale

Single exception tests are necessary but brittle.

Weighted random testing helps discover combinations and assumptions that fixed test cases miss.

## Verification note

This harmless note is used to exercise the multi-fuzz workflow.
