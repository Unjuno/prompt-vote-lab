# merge-policy-v1.0

## Purpose

This policy defines how Prompt Vote Lab chooses the mainline implementation candidate when multiple ranked candidates are executed.

## Principle

Voting rank has priority.

Rank 1 is the normal mainline candidate. Rank 2 and rank 3 are comparison candidates, even when they are executed through support-unlocked runs.

## Normal rule

- Rank 1 is the default merge candidate.
- Rank 2 and rank 3 are comparison runs.
- At most one implementation PR should be merged into `main` for one weekly vote.

## If Rank 1 is not accepted

If rank 1 does not pass review, the default result is no merge for that weekly vote.

Rank 2 and rank 3 should be recorded as comparison results. They are not automatically promoted to mainline.

## Exception

A lower-ranked candidate may be considered only with explicit maintainer justification in the weekly log.

## Rationale

Prompt Vote Lab studies whether collective voting predicts a good AI implementation result. Preserving vote order is part of the experiment.
