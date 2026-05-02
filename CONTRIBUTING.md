# Contributing

Prompt Vote Lab is a public experiment for analyzing the gap between collective expectation and AI-implemented results.

## Propose a prompt

Create an issue using the Prompt Proposal template.

A good prompt should:

- fit inside `lab/`
- be implementable with static HTML/CSS/vanilla JavaScript
- describe the expected result
- avoid backend, login, payment, database, external API, or secrets

## Vote

Use 👍 on prompt proposal issues.

The vote is a signal of collective expectation. It does not guarantee execution.

A prompt must pass `rules/selection-v1.0.md` before the maintainer runs an implementation.

## Review a result

When an implementation PR is opened, react or comment on whether the result matched the expectation.

Suggested reaction meaning:

- 👍 = matches expectation
- 👀 = interesting but off
- 👎 = worse than expected

## Merge policy

Voting is advisory.

The maintainer decides whether to merge, request changes, or reject.

## Analysis labels

Run results should be classified as one of:

- Hit
- Partial
- Misread
- Overbuild
- Underbuild
- Rule conflict
- Unsafe
- Rejected
