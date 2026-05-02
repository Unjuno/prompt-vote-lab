# support-unlocked-runs-v1.0

## Purpose

Support-unlocked runs allow additional ranked candidates to be executed after the normal weekly run.

## Weekly candidates

Each weekly vote may produce ranked candidates:

- rank 1: normal weekly run
- rank 2: optional support-unlocked comparison run
- rank 3: optional support-unlocked comparison run

## Support timing

Support does not trigger immediate execution.

Support is considered during the weekly run window.

## Initial thresholds

Initial thresholds:

- rank 2 unlock: 5 USD weekly support
- rank 3 unlock: 10 USD total weekly support

These thresholds are experimental and may change.

## Scope

Support applies to the current weekly vote only.

Old weekly candidates are not automatically reopened.

## Safety policy

Support unlocks an additional experiment run only.

Support does not grant:

- merge rights
- specification control
- safety-check bypass
- rule bypass

All support-unlocked runs must still follow:

- `static-ui-v1.0`
- `merge-policy-v1.0`
- maintainer review
- PR-only workflow

## Naming

Use ranked names:

- `week-XXX-rank-1`
- `week-XXX-rank-2`
- `week-XXX-rank-3`
