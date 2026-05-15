# Participant guide

This guide is for people who want to participate in Prompt Vote Lab.

The fastest useful action is not writing a prompt. It is voting on an existing prompt.

## What this is

Prompt Vote Lab is a public prompt game.

Participants propose prompts as GitHub Issues. Other participants vote with GitHub 👍 reactions. Each week, the highest-trust prompt may get one bounded implementation-agent attempt against the current static lab.

The result is public:

```text
prompt -> votes -> no-change baseline comparison -> agent PR or no run -> public outcome
```

## Start here

Do this first:

```text
1. Open the prompt proposal Issues.
2. Read a few prompts.
3. Add 👍 to prompts you trust.
4. Do not vote for vague prompts just because they sound ambitious.
```

Voting is the lowest-friction way to participate.

## Why voting matters

Every week includes a virtual baseline:

```text
[Baseline]: No change this week
20 virtual votes
```

If no real prompt beats the baseline, no implementation-agent attempt is created.

That is not failure. It means the group preferred not to spend a bounded attempt on weak prompts.

Baseline passing is decided by the weekly candidate set:

```text
baseline ranks first -> no implementation candidates
real prompt ranks first -> baseline passed -> rank 1 is eligible
```

If the baseline is passed, support can unlock extra comparison runs:

```text
5 USD weekly support -> rank 2 can also be attempted
10 USD weekly support -> rank 2 and rank 3 can also be attempted
```

Rank 2 and rank 3 do not independently need 20+ votes after rank 1 beats the baseline. Support does not help if the baseline ranks first.

## How to vote

1. Go to the repository Issues page.
2. Find Issues labeled `prompt-proposal`.
3. Open a prompt.
4. Click the 👍 reaction on the Issue.

Use 👍 only when the prompt is specific enough that you would be willing to see an implementation attempt.

## How to judge a prompt

Prefer prompts that are:

```text
small
specific
static-site compatible
reviewable
clear about visible user value
possible inside lab/index.html, lab/style.css, and lab/app.js
```

Be skeptical of prompts that are:

```text
vague
large redesigns
backend-dependent
login/payment dependent
network/API dependent
unclear about what should change
hard to review
```

## How to submit a prompt

Create a GitHub Issue using the prompt proposal format.

A useful prompt should include:

```text
1. What should change visibly?
2. Why is it useful to participants?
3. What should stay unchanged?
4. What would count as a bad implementation?
```

Good example:

```text
Add a compact "How to participate" panel to the lab page.
It should explain: vote with 👍, submit prompts as Issues, and check weekly results.
Keep it static and do not add external scripts or network calls.
Bad implementation: a large redesign, login flow, or external dependency.
```

Weak example:

```text
Make the site better and more viral.
```

The weak example is not actionable. It hides too many decisions inside the implementation agent.

## What the implementation agent can edit

The implementation agent may edit only:

```text
lab/index.html
lab/style.css
lab/app.js
```

It must not edit workflows, docs, rules, run records, backend files, configuration, secrets, or files outside `lab/`.

It must not add:

```text
external scripts
CDNs
network calls
trackers
cookies
login
payment behavior
iframes
eval
unsafe dynamic code
```

## What support can and cannot do

Support can unlock extra comparison runs for rank 2 and rank 3 when the weekly support threshold is met and the real prompt set has already beaten the no-change baseline.

Support cannot buy:

```text
votes
merge
success
review priority
maintenance
feature control
private request handling
```

Support increases comparison capacity. It does not override the no-change baseline.

## Where to see results

Useful places:

```text
/lab/                                  current lab UI
runs/                                  weekly vote summaries and run records
data/public-results.json               raw public result data
data/public-results.md                 readable public result summary
lab/comparisons/<week>/                comparison dashboards
lab/history/                           historical state flow
```

## What happens after a prompt wins

If a prompt beats the no-change baseline and is eligible:

```text
1. The workflow selects the candidate.
2. The implementation agent gets one bounded attempt.
3. The agent may open a PR changing only lab files.
4. Checks run before or during PR creation.
5. A maintainer reviews the PR manually.
6. Only merged PRs become the inherited lab state for future weeks.
```

If the agent fails, that failure is recorded. It is not hidden by automatic retries.

## Common questions

### Do I need to code?

No. Voting is enough.

### Do I need a GitHub account?

Yes, to vote with reactions or create Issues.

### Does the most popular prompt always merge?

No. Votes select candidates for bounded attempts. Merge still requires review.

### Can rank 2 or rank 3 run without 20 votes?

Yes, but only after a real prompt beats the no-change baseline. After that, support can unlock rank 2 or rank 3 comparison runs. If the baseline ranks first, support unlocks nothing.

### Can a failed prompt be useful?

Yes. A failed prompt teaches participants what kinds of prompts are too vague, too large, unsafe, or hard to implement.

### Are supporter identities published?

No. Public support unlock files should contain aggregate unlock information only, not sponsor identity or event-level amounts.

### Why is there a no-change baseline?

The baseline prevents weak prompts from consuming implementation attempts. A prompt must be better than doing nothing that week.

## Good participant behavior

Do:

```text
vote carefully
write small prompts
explain expected visible behavior
mention what should not change
review outcomes after voting
learn from failed runs
```

Do not:

```text
vote for vague hype
ask for private handling
try to buy merge
request external services
hide requirements in comments after selection
pressure maintainers to rerun failures
```

## First action

Start by voting.

If you can explain why a prompt deserves one bounded implementation attempt, give it 👍.

If you cannot explain that, do not vote for it.
