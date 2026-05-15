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

Baseline passing is decided by the weekly candidate set after the baseline is inserted and candidates are sorted by votes:

```text
no-change baseline ranks first -> no implementation candidates
real prompt ranks first -> baseline passed -> rank 1 is eligible
```

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

Support only opens additional comparison runs among real prompt candidates after the weekly candidate set has passed the baseline rule.

Current support interaction:

```text
baseline ranks first -> support unlocks nothing
real prompt ranks first and support is 0 USD -> rank 1 only
real prompt ranks first and support is at least 5 USD -> rank 1 and rank 2
real prompt ranks first and support is at least 10 USD -> rank 1, rank 2, and rank 3
```

Rank 2 and rank 3 do not independently need 20+ votes after rank 1 beats the baseline.

## Support example

| Candidate | Votes | Result |
|---|---:|---|
| Issue #1 | 25 | rank 1, normal weekly candidate |
| No change baseline | 20 | loses |
| Issue #2 | 12 | rank 2, support-unlocked at 5 USD |
| Issue #3 | 8 | rank 3, support-unlocked at 10 USD |

Result at 10 USD weekly support:

```text
Issue #1, Issue #2, and Issue #3 are eligible implementation candidates.
```

## Support counterexample

| Candidate | Votes | Result |
|---|---:|---|
| No change baseline | 20 | wins |
| Issue #1 | 18 | not attempted |
| Issue #2 | 12 | not attempted |
| Issue #3 | 8 | not attempted |

Result even at 10 USD weekly support:

```text
No implementation PR is created.
```

## Reputation interaction

Reputation is not currently computed automatically.

However, players should remember which prompt styles repeatedly beat the baseline and still failed, and which prompts actually improved the lab.
