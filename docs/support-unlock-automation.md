# Support unlock automation

Prompt Vote Lab support unlocks are automated as an anonymized weekly aggregate.

## Purpose

Support can unlock extra comparison runs for the current weekly vote:

- rank 2 unlock: 5 USD total weekly one-time support
- rank 3 unlock: 10 USD total weekly one-time support

Support does not buy votes, merge rights, success, adoption, maintenance, review, support work, delivery, or specification control.

## Privacy boundary

The public output must contain only aggregate unlock data.

Allowed public fields include:

- week id
- support total in cents/USD
- counted event count
- ignored event count
- rank 2 unlocked boolean
- rank 3 unlocked boolean
- threshold values
- source label
- generated timestamp

The public output must not contain sponsor names, sponsor logins, sponsor emails, individual payment events, or per-supporter amounts.

## Data source

The automation polls GitHub Sponsors activity through GitHub GraphQL.

The fetch step writes a temporary local payload under `tmp/`. The temporary payload is not committed.

The build step converts that temporary payload into:

```text
data/support-unlocks/<week-id>.json
```

Only the anonymized aggregate file is allowed to be committed.

## Operational token

The workflow needs a repository secret that can read the maintainer's GitHub Sponsors activity.

Expected secret name:

```text
SPONSORS_GRAPHQL_TOKEN
```

The token should use the least permissions that can read sponsorship activity for the maintainer account. Do not use a token with repository administration permissions.

## CI contract

Script Check must run:

```text
python scripts/test_build_support_unlocks.py
```

That test verifies:

- weekly totals are computed from fixture activity
- rank 2 unlocks at 5 USD
- rank 3 unlocks at 10 USD
- non-new, old, and recurring support events are ignored
- sponsor identities from the raw fixture are not present in the public output

## Failure mode

If the fetch step fails because the token is missing or lacks access, the workflow must fail visibly. It must not guess support totals and must not unlock comparison runs from stale data.
