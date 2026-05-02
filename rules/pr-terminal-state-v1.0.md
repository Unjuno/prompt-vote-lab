# pr-terminal-state-v1.0

## Purpose

This policy defines how Prompt Vote Lab records the terminal state of implementation PRs.

## Terminal states

Allowed terminal states:

- `merged`
- `rejected`
- `unsafe`
- `failed`
- `no-change`

## Labels

Use these labels on implementation PRs:

- `pvl:merged`
- `pvl:rejected`
- `pvl:unsafe`
- `pvl:failed`
- `pvl:no-change`

Only one terminal-state label should be present on a PR.

## Review boundary

The workflow may create PRs and draft reports automatically.

The maintainer still decides:

- merge
- reject
- unsafe
- failed

## Report trigger

After a terminal-state label is applied, a report workflow may create a deterministic report or an evaluation-model blog draft.

## Safety

A terminal-state label must not weaken safety rules.

A support-unlocked PR must follow the same terminal-state process as a normal rank-1 PR.
