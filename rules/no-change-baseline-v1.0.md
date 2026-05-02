# no-change-baseline-v1.0

## Purpose

The no-change baseline prevents weak weekly prompt votes from triggering implementation runs.

## Baseline candidate

Every weekly vote includes a virtual candidate:

```text
[Baseline]: No change this week
```

Initial baseline vote count:

```text
20
```

## Rule

If the no-change baseline ranks first, no implementation PR is created for that week.

Only real `prompt-proposal` issues can create implementation runs.

## Support interaction

Support can unlock rank-2 and rank-3 comparison runs only among real prompt candidates that remain eligible after the baseline is inserted.

Support does not override the no-change baseline.

## Rationale

The project should not run the implementation model just because the workflow is scheduled.

A prompt should beat a minimum public-interest threshold before spending API budget and maintainer review time.
