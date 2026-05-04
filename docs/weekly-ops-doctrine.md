# Weekly Operations Doctrine

This document defines the weekly operating loop for Prompt Vote Lab.

It is not a military document. It borrows the useful structure of observation, orientation, decision, and action to reduce confusion during a public experiment.

## Purpose

Prompt Vote Lab needs more than automation.

Each week must produce:

- evidence
- interpretation
- a public hook
- a next action for participants
- a record of what changed or did not change

If those are missing, the project may technically run while failing to attract useful participation.

## Weekly loop

```text
Observe → Orient → Decide → Act → Record → Improve
```

## 1. Observe

Use the generated evidence artifact.

Primary files:

```text
tmp/evidence/data/snapshots/week-<week_id>.json
tmp/evidence/reports/summary/weekly-metrics.json
tmp/evidence/runs/week-<week_id>.md
```

Check at minimum:

- candidate count
- unique author count
- total votes
- unique voter count when available
- top prompt vote share
- selected/no-run decision
- no-change baseline result
- whether generated files contain identity-like voter fields

Do not rely on impressions from the GitHub issue list after cutoff. The snapshot is the frozen evidence.

## 2. Orient

Interpret what the week means.

Use these diagnostic questions:

| Signal | Possible interpretation | Risk |
|---|---|---|
| Candidate count is zero | no proposal supply | participants do not know what to submit |
| Total votes are low | low attention or high friction | vote path is unclear |
| Unique authors are low | few people are creating prompts | prompt creation is too hard or unrewarding |
| Top prompt vote share is very high | consensus or lack of alternatives | one dominant prompt may hide weak competition |
| No-run result | no prompt beat the baseline | the baseline protected the lab, but public momentum may drop |
| Selected result | prompt crossed the gate | implementation quality becomes the main risk |

A high vote count is not proof of a good prompt. It is only proof that the prompt attracted attention.

## 3. Decide

Pick the weekly posture.

Allowed postures:

| Posture | Use when | Message focus |
|---|---|---|
| Recruit prompts | few or no candidates | ask for concrete prompt proposals |
| Recruit votes | enough candidates, low votes | explain that votes are +1 reactions |
| Review selected prompt | selected prompt exists | ask people to inspect expectation vs output |
| Explain no-run | baseline wins | show why doing nothing beat the field |
| Compare alternatives | rank 2/3 are interesting | explain comparison value without promising merge |

Do not pretend that every week is progress. A no-run week is useful if it teaches what did not earn trust.

## 4. Act

Use the generated public briefing as the starting point.

Primary file:

```text
tmp/evidence/reports/briefings/week-<week_id>.md
```

Before sharing, check:

- the briefing matches the snapshot
- the briefing links to submit and vote paths
- it does not claim final implementation success when run fields are unrecorded
- it does not include voter login lists
- it tells participants exactly one or two next actions

Recommended public action patterns:

```text
No-run week:
This week, no prompt beat the 20-vote no-change baseline. Submit a more concrete prompt or vote with +1 on a proposal you trust.
```

```text
Selected week:
A prompt beat the baseline. Now the useful question is whether the implementation result matches what voters expected. Review the PR before trusting it.
```

```text
Low candidate week:
The experiment needs more prompt proposals. Submit one concrete change that can be implemented inside the three lab files.
```

## 5. Record

Keep public memory separate from the changing lab.

Evidence belongs in:

```text
data/snapshots/
logs/
runs/
reports/
```

The lab belongs in:

```text
lab/index.html
lab/style.css
lab/app.js
```

Do not let a lab implementation PR modify evidence, workflow, rules, reports, or documentation.

## 6. Improve

After reviewing the week, choose one improvement only.

Examples:

- improve the prompt proposal template
- improve the landing page call to action
- improve the lab smoke test
- improve the snapshot metric set
- improve the public briefing wording
- improve the artifact review process

Do not change rules, UI, evidence schema, and workflow behavior in the same PR unless the dependency is unavoidable.

## Codex / AI agent risk posture

Assume agent outputs may be:

- locally plausible but strategically wrong
- safe by static checks but useless to participants
- overfitted to the latest prompt
- tempted to modify surrounding process files
- vague about evidence and outcomes

Required defenses:

- lab scope guard
- static site check
- lab smoke test
- evidence artifact smoke test
- manual artifact review
- maintainer merge decision

## Entertainment layer

Prompt Vote Lab is partly a game.

The weekly public message should preserve game tension:

- the baseline is the opponent
- votes open the gate
- implementation can still fail
- reputation is social memory
- no-run is a visible outcome, not silence

Avoid over-polishing the game into a normal feature queue. The uncertainty is part of the entertainment value.

## Data discipline

Do not introduce a metric unless it answers a decision question.

Current core questions:

| Question | Current metric |
|---|---|
| Are people proposing prompts? | candidate count, unique author count |
| Are people voting? | total votes, unique voter count when available |
| Is attention concentrated? | top prompt vote share |
| Is the baseline too strong or too weak? | selected/no-run count over time |
| Are generated public artifacts usable? | artifact smoke test and artifact review |

If a new metric cannot change a weekly decision, do not add it yet.

## Minimum weekly PASS

A week is operationally acceptable only if:

```text
snapshot exists
run log exists
summary exists
briefing exists
HN draft exists
artifact review passes
20-vote baseline is visible
no voter login list is stored
next participant action is clear
```

If this minimum is not met, do not move to paid implementation runs.
