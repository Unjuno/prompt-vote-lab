# Public page architecture

## Purpose

Prompt Vote Lab has separate public pages for four jobs:

```text
1. attract people
2. let people participate
3. show the current lab state
4. let people verify the experiment history
```

GitHub remains the source of truth. The public site is a readable index over that evidence.

## Route map

```text
/                                      Landing page / public entry
/lab/                                  Current lab state / latest adopted experiment surface
/lab/history/                          Cross-week progression and experiment history
/lab/comparisons/<week_id>/            Weekly rank comparison dashboard
/lab/comparisons/<week_id>/rank-1/     Rank 1 generated artifact
/lab/comparisons/<week_id>/rank-2/     Rank 2 generated artifact
/lab/comparisons/<week_id>/rank-3/     Rank 3 generated artifact
/docs/                                 Rules, policies, and implementation notes
```

## Landing page

Canonical route:

```text
/
```

The landing page is the public entry point. It explains the game loop and sends visitors to voting, submission, the current lab, and evidence pages.

It must show:

```text
what Prompt Vote Lab is
how the weekly loop works
how to propose a prompt
how to vote with GitHub reactions
why the 20-vote baseline exists
how support expands run capacity without buying outcomes
link to /lab/
link to /lab/history/
link to the latest comparison page when available
link to GitHub Issues
link to public results
```

It must not include:

```text
login inside the static site
payment handling inside the static site
external scripts
analytics or tracking
network calls
cookies
```

## Current lab page

Canonical route:

```text
/lab/
```

This is not the landing page. It is the current visible lab state and latest adopted experiment surface.

It should show:

```text
current experiment state
latest adopted Issue or PR when available
next action for participants
links to history and latest comparison
short note that results are publicly recorded
```

It must not become:

```text
marketing-heavy landing page
payment page
login surface
external-service UI
```

## History page

Canonical route:

```text
/lab/history/
```

The history page shows how the experiment moved across weeks.

It should show, per week:

```text
week_id
candidate Issue count
eligible clear count
blocked count
review count
executed rank count
adopted rank when known
comparison page link
public results snapshot time
```

Candidate state flow:

```text
Issue posted
→ submission safety scan
→ clear / review / blocked
→ eligible candidate
→ rank selected
→ comparison run
→ PR created
→ merged / not selected / blocked
→ finalizer close
```

## Weekly comparison page

Canonical route:

```text
/lab/comparisons/<week_id>/
```

The weekly comparison page compares rank candidates from the same weekly selection set.

It should show, per rank:

```text
rank
Issue number
Issue title
vote count
safety scan status
runtime scan status
implementation PR
changed files
output root
run record path
public bundle link when available
decision
```

Critical comparison rule:

```text
Do not let rank2 inherit rank1's merged root lab output.
```

Use rank-specific roots:

```text
lab/comparisons/<week_id>/rank-1/
lab/comparisons/<week_id>/rank-2/
lab/comparisons/<week_id>/rank-3/
```

## Rank output pages

Canonical routes:

```text
/lab/comparisons/<week_id>/rank-1/
/lab/comparisons/<week_id>/rank-2/
/lab/comparisons/<week_id>/rank-3/
```

Each rank root should contain only:

```text
index.html
style.css
app.js
```

Rank pages must not contain:

```text
external scripts
external network calls
cookies
tracking
credential handling
iframes
dynamic code execution
```

## Source evidence

Canonical sources:

```text
data/public-results.json
data/public-results.md
runs/*.md
GitHub Issues
GitHub PRs
GitHub commits
redacted public Actions artifacts when intentionally published
```

The public pages index these sources. They do not replace them.

## Support relation

Support affects only run capacity.

```text
votes decide ranking
safety scan decides eligibility
support amount decides how many ranks can run
maintainer review decides what is adopted
```

Bad design:

```text
supporter buys a specific outcome
```

Good design:

```text
support expands total experiment capacity
```

## Minimum implementation sequence

```text
1. keep / as the landing page
2. keep /lab/ as the current lab state
3. auto-generate /lab/comparisons/<week_id>/ from public results
4. run comparison candidates into rank-specific roots
5. auto-generate /lab/history/ from public results
6. update / and /lab/ to link history and latest comparison
```

## Security posture

All generated public pages must remain static.

```text
connect-src 'none'
frame-src 'none'
object-src 'none'
form-action 'none'
```

No page should publish raw private diagnostics or sensitive operational data.

## Evaluation question

A participant should be able to answer this within one minute:

```text
What happened this week, which rank was adopted, and what evidence supports that decision?
```
