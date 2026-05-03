# report-generation-v1.0

## Purpose

This rule defines how Prompt Vote Lab creates weekly report drafts.

The report system exists to preserve public memory for the prompt game.

## Current phase

The current phase is model-free report drafting.

Reports are generated from explicit workflow inputs and repository files.

They are not automatically published outside the repository.

## Allowed report action

Allowed:

- create or update `runs/<week>-report.md`
- open a report draft PR
- include links to related issues, PRs, vote summaries, and run logs
- include a human-review note

Not allowed:

- edit `lab/`
- edit game rules
- publish to an external blog automatically
- post to Hacker News or social media automatically
- claim an automated reputation score exists
- claim final judgment without review

## Report classifications

Allowed expectation-gap labels:

- Hit
- Partial
- Misread
- Overbuild
- Underbuild
- Rule conflict
- Unsafe
- Rejected
- Unknown

`Unknown` should be used when there is not enough information.

## Reputation memory rule

Reports may include a short reputation-memory note.

This note is qualitative only.

It must not create numeric scores, author ratings, automatic penalties, or leaderboard placement.

## Source rule

A report must identify its source material.

At minimum, it should record:

- week
- selected prompt or candidate description
- vote count
- baseline votes
- outcome
- related issue or PR when known

## Review rule

A report draft PR is reviewable and may be edited before merge.

The workflow must not merge the report draft automatically unless a future merge policy explicitly allows report-only auto-merge.
