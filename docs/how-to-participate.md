# How to participate

Prompt Vote Lab uses GitHub as the public game board.

You participate as a player by submitting prompts, voting on prompts, and learning from what the implementation agent actually produces.

This is not a normal feature-request queue.

Winning attention is only the first step. A prompt still has to survive implementation.

## The game loop

```text
Submit a prompt
→ persuade other players
→ pass the weekly selection gate
→ receive one bounded agent attempt
→ review the public outcome
→ update trust for the next round
```

## 1. Submit a prompt

Open a new prompt proposal issue:

```text
https://github.com/Unjuno/prompt-vote-lab/issues/new?template=prompt_proposal.yml
```

A strong proposal should include:

- the exact prompt
- the expected visible result
- why this is worth the next agent attempt
- how it fits the current inherited `lab/` state
- confirmation that it fits the static `lab/` scope

Bad proposal pattern:

```text
Make it better.
```

Better proposal pattern:

```text
Add a visible round-history panel to the lab page that explains the last selected prompt, vote count, result label, and whether the PR was merged.
```

## 2. Understand what you are risking

A voted prompt can fail.

Failure is not hidden. It becomes public game information.

A prompt may fail because it:

- was too vague
- overpromised
- conflicted with the three-file lab scope
- produced unsafe or unmergeable output
- sounded attractive but did not guide the agent well
- ignored the inherited lab state

If a style, author, or promise repeatedly fails, other players should become less willing to trust it.

## 3. Vote

Vote with GitHub reactions on prompt proposal issues.

The default vote signal is:

```text
👍 / +1 reaction
```

Comments can explain or challenge an idea, but comments are not counted as votes.

Votes are treated as public trust signals, not as a binding election.

A prompt with many votes receives attention. It does not receive guaranteed merge.

## 4. Pass the weekly selection gate

The current weekly selection rule is:

```text
top prompt votes >= no-change baseline + required margin
and
total weekly votes >= minimum total votes
```

Initial values:

| Parameter | Value |
|---|---:|
| no-change baseline | 5 |
| required margin | 2 |
| minimum total votes | 5 |

Therefore, the top prompt initially needs at least 7 votes, and the week needs at least 5 total votes.

If the gate fails, the lab does not move that week.

Doing nothing is always in the game.

## 5. Review outcomes

After a weekly run, review:

- the implementation PR
- the changed `lab/` files
- the safety-check result
- the static-site check result
- the run log, when available
- the expectation-gap classification, when available

Useful questions:

- Did the prompt produce what voters probably expected?
- Was the output mergeable?
- Did it improve the inherited lab state?
- Did the prompt waste the agent attempt?
- Should this author or prompt style earn more trust next week?

## 6. Scope

The implementation agent may edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

The agent may create ordinary helper functions inside `lab/app.js`.

The static lab page does not store submissions or votes directly.

GitHub Issues and reactions are the public game board.

## 7. Current reputation status

Reputation is currently social, not automatic.

The workflow records outcomes, but it does not yet compute player scores, author ratings, automatic trust scores, or penalties.

Use the public history yourself.
