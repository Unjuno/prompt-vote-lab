# Participant Tutorial

## Purpose

This document is a participant-facing tutorial draft.

It may later be copied into GitHub Wiki if the project uses Wiki as a static tutorial area.

It is not the official experiment record.

Official records live in:

```text
data/snapshots/
runs/
logs/
reports/
```

## What is Prompt Vote Lab?

Prompt Vote Lab is a public experiment where participants propose prompts, vote on prompts, and observe constrained AI coding runs.

The experiment is designed to separate four layers:

| Layer | Purpose | Official? |
|---|---|---:|
| Root landing page | Explain the project and participation path | No |
| GitHub Issues | Collect prompt proposals and votes | Source input |
| Snapshot/run logs | Record official weekly evidence | Yes |
| `/lab/` | Constrained AI-editable experiment surface | Output target |

Do not confuse the landing page with `/lab/`.

`/lab/` is intentionally minimal until an accepted experiment run changes it.

## Quick start

1. Open the repository issues.
2. Read existing prompt proposals.
3. Add a `+1` reaction to prompts you support.
4. Create a new prompt issue if your idea is missing.
5. Wait for the weekly snapshot.
6. Read the weekly run log.
7. Compare expected result vs actual result.

## How to propose a prompt

Create a GitHub issue for one proposed prompt.

A good prompt proposal should include:

- the requested change
- the expected user-visible result
- why the change is useful
- what should not be changed
- any constraints that matter

Good example:

```text
Title: Show weekly run history on the lab page

Request:
Add a compact run-history section to /lab/.

Expected result:
A visitor can see the latest three accepted runs and their result labels.

Do not change:
Do not add external network calls. Do not edit files outside lab/.
```

Bad example:

```text
Make it better.
```

Reason: the expected result is not testable.

## How to vote

Voting uses public GitHub reactions.

Use:

```text
+1 reaction
```

Do not assume comments count as votes.

Comments may help explain an idea, but the selection workflow counts `+1` reactions.

## How weekly selection works

At the weekly cutoff, the snapshot workflow counts open prompt issues with the prompt label and their public `+1` reactions.

The official weekly decision comes from:

```text
data/snapshots/week-XXX.json
```

The human-readable run record comes from:

```text
runs/week-XXX.md
```

A prompt is selected only if it beats the no-change baseline.

Current baseline:

```text
[Baseline]: No change this week
20 virtual votes
```

A real prompt therefore needs more votes than the 20-vote baseline to receive the normal implementation attempt.

## What `/lab/` means

`/lab/` is the constrained AI-editable experiment surface.

It is not the public landing page.

It is not the official record.

It is the place where accepted experiment runs may change visible output.

The agent should normally be limited to:

```text
lab/index.html
lab/style.css
lab/app.js
```

Evidence files should not be edited by the agent.

## How to read results

Start with the weekly run log:

```text
runs/week-XXX.md
```

Look for:

- selected issue
- top prompts
- selected prompt votes
- implementation PR
- changed files
- safety-check result
- result status
- expectation-gap classification
- reviewer note

Then check the snapshot:

```text
data/snapshots/week-XXX.json
```

Use the snapshot to verify why the prompt was selected.

## What is an expectation gap?

The expectation gap is the difference between what participants expected and what the AI coding run actually produced.

Allowed result labels include:

- Hit
- Partial
- Misread
- Overbuild
- Underbuild
- Rule conflict
- Unsafe
- Rejected

A failed run is still useful if it is recorded clearly.

## What Hacker News drafts mean

HN drafts are generated for maintainer review.

They are not automatically posted.

Drafts live in:

```text
reports/hn/week-XXX.md
```

A draft should not be posted if it hides failures, exaggerates results, or if the run log still contains unfinished evidence.

## What not to put in prompts or comments

Do not include:

- private keys
- passwords
- private personal information
- requests to modify evidence files
- requests to bypass safety checks
- requests to post automatically to external sites

## FAQ

### Is `/lab/` the home page?

No.

The root page explains the project. `/lab/` is the experiment surface.

### Can I vote by commenting?

No.

Voting is based on public `+1` reactions.

### Can a losing prompt still matter?

Yes.

A losing prompt may influence future proposals, comments, and later experiments.

### Can the AI edit logs?

No.

Logs and snapshots are evidence. They should stay outside the AI-editable surface.

### Does a selected prompt guarantee merge?

No.

A selected prompt starts an implementation attempt. The maintainer can still reject the result.

## Tutorial boundary

This tutorial may be copied to Wiki later.

If copied to Wiki, keep it mostly static. Do not use Wiki as the official evidence store.
