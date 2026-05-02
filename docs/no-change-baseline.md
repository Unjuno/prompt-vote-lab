# No-change baseline

Prompt Vote Lab includes a virtual no-change candidate in every weekly vote.

It is the game's default opponent.

## Baseline

```text
[Baseline]: No change this week
20 virtual votes
```

## Rule

If the no-change baseline ranks first, no implementation-agent attempt is created for that week.

Only real `prompt-proposal` issues can create implementation-agent attempts.

## Why this exists

The baseline makes doing nothing a competitor.

A prompt should not receive an agent attempt merely because it exists. It has to persuade players that it is better than preserving the current lab state.

The baseline protects:

- implementation-agent budget
- review time
- game signal quality
- public trust in the vote
- the inherited lab state

## Example

| Candidate | Votes | Result |
|---|---:|---|
| No change baseline | 20 | wins |
| Issue #1 | 7 | not attempted |
| Issue #2 | 5 | not attempted |

Result:

```text
No implementation PR is created.
```

## Strong prompt example

| Candidate | Votes | Result |
|---|---:|---|
| Issue #1 | 24 | rank 1 |
| No change baseline | 20 | loses |
| Issue #2 | 12 | rank 2 |

Result:

```text
Issue #1 becomes the normal weekly implementation candidate.
```

## Support interaction

Support does not override the no-change baseline.

Support only opens additional comparison runs among real prompt candidates that remain eligible after the baseline is inserted.

## Reputation interaction

Reputation is not currently computed automatically.

However, players should remember which prompt styles repeatedly beat the baseline and still failed, and which prompts actually improved the lab.
