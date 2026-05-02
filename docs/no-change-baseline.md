# No-change baseline

Prompt Vote Lab includes a virtual no-change candidate in every weekly vote.

## Baseline

```text
[Baseline]: No change this week
20 virtual votes
```

## Rule

If the no-change baseline ranks first, no implementation run is created for that week.

Only real `prompt-proposal` issues can create implementation runs.

## Why this exists

The baseline prevents weak or low-interest prompt votes from triggering AI implementation work.

It protects:

- API budget
- review time
- experiment quality
- public signal quality

## Example

| Candidate | Votes | Result |
|---|---:|---|
| No change baseline | 20 | wins |
| Issue #1 | 7 | not implemented |
| Issue #2 | 5 | not implemented |

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
