# Contributor Credit Specification

## Purpose

Prompt Vote Lab may show a public contributor summary for accepted prompt authors.

This is not user tracking. It is a public credit record derived only from public GitHub contribution data and weekly experiment logs.

## Allowed data

The contributor summary may use:

- GitHub login
- public issue number
- public issue title
- public issue URL
- selected week id
- accepted/merged status
- count of accepted prompts

## Disallowed data

Do not collect or display:

- IP address
- device information
- location
- private email
- browser fingerprint
- session identifiers
- vote-by-vote personal behavior timelines
- private analytics data

## Credit rule

A contributor receives accepted-prompt credit only if all conditions are true:

1. a valid weekly snapshot exists
2. `decision = "selected"`
3. the contributor authored the selected issue
4. the weekly run log records an accepted result

Initial accepted result statuses:

- `merged`

Future policies may add more accepted statuses, but they must be documented before use.

## No credit cases

A contributor does not receive accepted-prompt credit if:

- no prompt passed the selection rule
- the selected implementation PR was rejected
- the run was invalidated
- the issue was selected only in a corrected snapshot that was not used for implementation
- the author information is unavailable

## Canonical files

Machine-readable summary:

```text
data/contributors.json
```

Human-readable summary:

```text
docs/contributors.md
```

These files are generated or maintained outside `lab/`.

## Contributors JSON schema

```json
{
  "schema_version": "contributors-v1.0",
  "generated_at": "2026-05-11T00:10:00+09:00",
  "contributors": [
    {
      "login": "Unjuno",
      "accepted_prompts": 2,
      "selected_issues": [3, 8],
      "weeks": ["001", "004"],
      "last_accepted_at": "2026-06-01T00:00:00+09:00"
    }
  ]
}
```

## Display guidance

Use neutral wording:

- `Accepted prompt contributors`
- `Accepted prompts`
- `Selected issues`

Avoid wording that suggests behavioral surveillance:

- `tracked users`
- `user behavior ranking`
- `voter profile`

## Anti-gaming note

Contributor credit can encourage spam if over-emphasized.

Initial display should be small and factual:

```text
Accepted prompt contributors
1. Unjuno — 2 accepted prompts
2. example-user — 1 accepted prompt
```

Do not add prizes, badges, or aggressive ranking mechanics until spam controls exist.

## Privacy note

All displayed contributor information must be derived from public GitHub artifacts already visible in the repository context.
