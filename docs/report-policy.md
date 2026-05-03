# Report policy

Prompt Vote Lab reports should turn weekly game outcomes into reviewable public memory.

Reports are not automatic final judgments.

They are draft records that help players remember which prompts, authors, and prompt styles deserved trust.

## Current status

Report generation is currently model-free.

The workflow can create a draft Markdown report from explicit inputs and existing repository files.

It does not yet use a stronger evaluation model to classify outcomes automatically.

It does not publish to an external blog.

## Report purpose

A report should answer:

- What prompt won attention?
- Did it beat the no-change baseline?
- What agent attempt happened?
- What was the public outcome?
- Did the result match the expected visible result?
- What should players remember next week?

## Report output

Canonical report drafts should be written under:

```text
runs/<week>-report.md
```

The report should be added through a PR.

## Required sections

A report draft should include:

1. Round summary
2. Selected candidate
3. Outcome
4. Expectation gap
5. Reputation memory
6. Human review note
7. Source material

## Reputation memory

Reputation memory is social, not an automated score.

Reports may say what players should remember, but they must not claim that the workflow has computed:

- player scores
- author ratings
- trust scores
- automatic penalties
- leaderboard placement

unless such a system is later implemented and documented.

## Tone

Reports should be direct and useful.

Allowed:

- concise judgment
- clear failure labels
- explicit uncertainty
- notes about overpromising, underbuilding, or unsafe output

Avoid:

- personal attacks
- unverifiable accusations
- claims of intent
- calling a player dishonest without evidence
- pretending a draft is final

## Publication boundary

The first implementation target is a report draft PR only.

External blog publishing, social posting, Hacker News submission, or website syndication must remain manual until a future policy explicitly allows it.

## Model use

A stronger model may later help classify expectation gaps or draft summaries.

If model-assisted reports are introduced, the report must disclose that it is model-assisted and the workflow must still create a reviewable PR rather than publishing automatically.
