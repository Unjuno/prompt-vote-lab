# Persona Routes

Prompt Vote Lab has several participant roles.

This guide defines the minimum route for each role so the public site does not collapse every visitor into the same generic call to action.

## Why this exists

The project currently has a clear general loop:

```text
Submit prompt -> vote -> weekly run -> review outcome -> update trust
```

That is not enough for first-time visitors.

A visitor needs to quickly answer:

```text
What role am I playing here?
What should I click first?
What counts as a good action?
What should I not expect?
```

## Route 1: Writer

A Writer wants to submit a prompt that can survive one bounded implementation-agent attempt.

Primary action:

```text
Submit a prompt
```

Primary link:

```text
https://github.com/Unjuno/prompt-vote-lab/issues/new?template=prompt_proposal.yml
```

What the Writer needs:

```text
- exact prompt request
- expected visible result
- reason this is worth one weekly run
- constraints and non-goals
- confirmation that the idea fits the static lab scope
```

Good Writer behavior:

```text
Write a prompt that is concrete, bounded, visible, and reviewable.
```

Bad Writer behavior:

```text
Ask the agent to make the whole project better.
Ask for backend, login, payment, external services, or workflow changes.
```

## Route 2: Voter

A Voter decides which prompt deserves trust.

Primary action:

```text
Vote with a 👍 / +1 reaction on a prompt proposal issue.
```

Primary link:

```text
https://github.com/Unjuno/prompt-vote-lab/issues?q=is%3Aissue+is%3Aopen+label%3Aprompt-proposal
```

What the Voter needs:

```text
- comments do not count as votes
- votes are public trust signals
- popularity does not guarantee merge
- the 20-vote no-change baseline must be beaten
```

Good Voter behavior:

```text
Vote for prompts that are specific, safe, and likely to improve the inherited lab state.
```

Bad Voter behavior:

```text
Vote only for vague hype or impossible requests.
```

## Route 3: Spectator

A Spectator watches whether the crowd's judgment survives implementation.

Primary action:

```text
Watch the lab and read run records.
```

Primary links:

```text
/lab/
/runs/
```

What the Spectator needs:

```text
- what changed in the lab
- which prompt won
- whether the implementation was mergeable
- whether the crowd's trust was deserved
```

Good Spectator behavior:

```text
Treat failures as public game information, not as hidden errors.
```

Bad Spectator behavior:

```text
Assume the highest-vote prompt was necessarily the best prompt.
```

## Route 4: Supporter

A Supporter funds comparison runs without buying votes or control.

Primary action:

```text
Read the support policy before sponsoring.
```

Primary links:

```text
https://github.com/sponsors/Unjuno
https://github.com/Unjuno/prompt-vote-lab/blob/main/docs/support-policy.md
```

What the Supporter needs:

```text
- support does not buy votes
- support does not guarantee merge
- support does not control the specification
- support can unlock bounded comparison runs only under policy
```

Good Supporter behavior:

```text
Support the experiment's capacity while preserving the baseline rule.
```

Bad Supporter behavior:

```text
Treat support as paid feature delivery.
```

## Route 5: Reviewer

A Reviewer decides whether a run result is safe and useful enough to merge.

Primary action:

```text
Review the generated PR, checks, changed files, and run evidence.
```

Primary links:

```text
/docs/pre-api-freeze.md
/docs/evidence-artifact-review.md
/docs/repository-cleanup.md
/rules/static-ui-v1.0.md
/rules/agent-run-policy-v1.0.md
```

What the Reviewer needs:

```text
- changed files are inside the allowed scope
- safety checks pass
- static checks pass
- no external network calls or scripts are added
- no auto-merge occurs
- no retry or fallback model is used
```

Good Reviewer behavior:

```text
Reject a popular result if it violates scope, safety, or reviewability.
```

Bad Reviewer behavior:

```text
Merge because the prompt was popular.
```

## Route map for the public page

The public landing page should eventually show a compact role picker:

```text
Writer -> Submit a prompt
Voter -> Vote on prompts
Spectator -> Watch the lab
Supporter -> Read support policy
Reviewer -> Read rules
```

Do not add this to the first real implementation-agent canary if the canary is meant only to prove the safe execution path.

The first real implementation-agent canary should remain smaller:

```text
Add a small bounded canary panel inside lab/ only.
```

Persona route UI can be added later as a separate human-reviewed product PR or a later bounded agent run with explicit non-canary scope.
