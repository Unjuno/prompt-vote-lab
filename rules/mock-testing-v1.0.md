# mock-testing-v1.0

## Purpose

Mock testing verifies Prompt Vote Lab automation without spending API budget.

The mock path should exercise the same repository boundaries as a real implementation run.

## What mock tests verify

Mock tests may verify:

- weekly vote collection
- no-change baseline handling
- eligible-rank selection
- branch creation
- `lab/`-only edits
- safety checks
- static site checks
- PR creation
- terminal report wiring

## What mock tests must not verify

Mock tests must not be treated as evidence of model quality.

A mock run proves workflow plumbing, not AI implementation ability.

## Editable files

Mock implementation runs must edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

## API usage

Mock tests must not call OpenAI or any other paid model API.

Mock tests must not require API keys.

## Merge policy

Mock implementation PRs are normally closed after checks pass.

Do not merge a mock PR unless the maintainer intentionally wants to replace the current lab state with mock output.

## Rationale

The real implementation path should be exercised only after the GitHub automation path is stable.

Mock tests reduce cost, reduce risk, and make failures easier to isolate.
