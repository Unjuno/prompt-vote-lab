# Selection gate

Prompt Vote Lab includes a no-change baseline in the weekly selection rule.

It is the game's default opponent: a prompt should not receive an implementation-agent attempt merely because it exists.

## Current rule

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

Therefore:

```text
top prompt votes >= 7
and
total weekly votes >= 5
```

## Result

If the weekly gate passes, the top prompt becomes the normal implementation candidate.

If the weekly gate fails, no implementation-agent attempt is created for that week.

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

## Example: gate fails

| Candidate | Votes | Result |
|---|---:|---|
| Issue #1 | 6 | below top-prompt threshold |
| Issue #2 | 3 | below top-prompt threshold |

Total weekly votes: 9  
Top prompt votes: 6

Result:

```text
No implementation PR is created.
```

## Example: gate passes

| Candidate | Votes | Result |
|---|---:|---|
| Issue #1 | 7 | rank 1 |
| Issue #2 | 5 | rank 2 |

Total weekly votes: 12  
Top prompt votes: 7

Result:

```text
Issue #1 becomes the normal weekly implementation candidate.
```

## Support interaction

Support does not override the selection gate.

Support only opens additional comparison runs among real prompt candidates after the weekly candidate set has passed the gate.

## Reputation interaction

Reputation is not currently computed automatically.

However, players should remember which prompt styles pass the gate and still fail, and which prompts actually improve the lab.
