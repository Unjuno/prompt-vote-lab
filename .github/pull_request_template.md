# Prompt Vote Lab PR

## Summary

<!-- What changed? Keep this specific. -->

## Change type

- [ ] Codex / AI agent lab implementation
- [ ] Documentation or policy change
- [ ] Workflow or script change
- [ ] Evidence, log, snapshot, run, or report change
- [ ] Other

## Voted prompt

For Codex / AI agent lab implementation PRs only.

Issue: #

> 

## Rule profile

For Codex / AI agent lab implementation PRs:

- `rules/static-ui-v1.0.md`

## Expected result

<!-- What should a user see or be able to do after this PR? -->

## Changed files

For Codex / AI agent lab implementation PRs, only these files may change:

- [ ] `lab/index.html`
- [ ] `lab/style.css`
- [ ] `lab/app.js`

For non-lab PRs:

- [ ] This PR does not mix lab implementation changes with policy, workflow, evidence, or documentation changes.

## Scope checklist

- [ ] I checked the changed-file list before review.
- [ ] This PR does not hide unrelated changes.
- [ ] If `lab/` changed, no non-lab files changed in the same PR.
- [ ] If non-lab files changed, `lab/` did not change in the same PR.
- [ ] Generated evidence files are not manually edited unless this PR is an explicit correction.

## Safety checklist

For lab implementation PRs:

- [ ] Only approved `lab/` files were changed.
- [ ] No external network calls were added.
- [ ] No cookie access was added.
- [ ] No `eval` or unsafe `new Function` was added.
- [ ] No external scripts were added.
- [ ] No login, payment, tracker, or backend behavior was added.
- [ ] Browser display check completed.

## User-facing review

- [ ] A first-time participant can still understand how to submit a prompt.
- [ ] A first-time participant can still understand that voting means a 👍 / +1 reaction.
- [ ] The 20-vote no-change baseline remains consistent.
- [ ] `/lab/` remains the constrained implementation surface, not the landing page or evidence store.

## Snapshot / logging review

For snapshot, run-log, report, or workflow PRs:

- [ ] Schema changes include matching tests or documentation updates.
- [ ] The no-change baseline remains visible in generated evidence when relevant.
- [ ] Dry-run behavior is safe by default, or this PR explains why not.
- [ ] No OpenAI/model call or Hacker News posting is introduced without an explicit gate.

## Result review

React to Codex / AI agent lab implementation PRs:

- 👍 = matches expectation
- 👀 = interesting but off
- 👎 = worse than expected

Maintainer classification:

- [ ] Hit
- [ ] Partial
- [ ] Misread
- [ ] Overbuild
- [ ] Underbuild
- [ ] Rule conflict
- [ ] Unsafe
- [ ] Rejected

## Merge policy

Result votes are advisory. The maintainer decides whether to merge.

Do not merge a Codex / AI agent lab implementation PR that mixes `lab/` changes with `.github/`, `docs/`, `rules/`, `data/`, `logs/`, `runs/`, `reports/`, or script changes.

## Notes for reviewer

<!-- Mention anything surprising, risky, or intentionally out of scope. -->
