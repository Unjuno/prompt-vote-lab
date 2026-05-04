# Hacker News Draft Policy

## Purpose

Prompt Vote Lab may generate Hacker News submission drafts, but it must not automatically submit to Hacker News.

The goal is to help the maintainer publish clear public updates while avoiding account automation risk, accidental spam, and unauthorized posting.

## Policy

Allowed:

- generate HN title candidates
- generate an HN text draft
- generate a short experiment summary
- generate a link checklist
- generate a post-publication follow-up checklist

Disallowed:

- automatically logging in to Hacker News
- automatically submitting a story
- automatically commenting
- browser automation for posting
- storing HN credentials
- asking public issue commenters to trigger HN posting

## Human action boundary

The maintainer must manually decide whether to post.

The generated draft is only a draft. It is not an instruction to publish.

## Canonical output path

Generated HN drafts should live outside `lab/`:

```text
reports/hn/week-XXX.md
```

The draft should reference evidence files:

- `data/snapshots/week-XXX.json`
- `runs/week-XXX.md`
- implementation PR URL, if available
- final report URL, if available

## Required draft sections

Each generated HN draft should contain:

1. title candidates
2. recommended title
3. submission URL candidate
4. text draft
5. evidence checklist
6. do-not-post checklist

## Draft schema in Markdown

```md
# HN Draft: Week XXX

## Title candidates

1. ...
2. ...
3. ...

## Recommended title

...

## Submission URL candidate

...

## Text draft

...

## Evidence checklist

- [ ] Weekly snapshot exists
- [ ] Run log exists
- [ ] Implementation PR exists or no-run is explicitly recorded
- [ ] Safety result is recorded
- [ ] Expectation gap classification is recorded

## Do-not-post checklist

Do not post if any of these are true:

- [ ] The run log is still mostly `unrecorded`
- [ ] The snapshot is missing
- [ ] The implementation PR is missing for a selected run
- [ ] The safety result is missing
- [ ] The draft exaggerates results
- [ ] The draft hides failures
```

## Writing constraints

HN drafts must be factual and restrained.

Do not claim:

- the experiment proves AI coding quality
- the system is autonomous end-to-end
- the result is statistically significant
- the voting mechanism is Sybil-resistant
- the AI output is safe without maintainer review

Prefer concrete wording:

- `This is a small public experiment`
- `The weekly snapshot records vote state`
- `The implementation is constrained to lab/`
- `The result was classified as Partial/Misread/etc.`

## Publication timing

A draft can be generated after the weekly run log reaches one of these states:

- `merged`
- `rejected`
- `no_run`
- `invalidated`

Do not generate a public-facing HN draft from a half-filled run log unless it is explicitly labeled as internal draft.

## Privacy and attribution

Use only public repository data.

Contributor mentions should use GitHub login only when already visible in public issues or PRs.

Do not include private analytics, IP-level data, or non-public supporter information.
