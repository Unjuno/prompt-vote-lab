# Prompt Vote Lab

Prompt Vote Lab is a public experiment for observing vibe coding.

People propose prompts, vote on them, and an AI coding agent implements ranked prompt candidates inside a constrained `lab/` directory.

The goal is not only to generate UI. The goal is to study the gap between collective expectation and AI-implemented reality.

Each run records:

- the voted prompt
- vote count
- candidate rank
- selection rule
- AI execution constraints
- PR diff
- safety checks
- merge/reject decision
- expectation gap classification

## Current scope

The AI agent may edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

The AI agent must not edit:

- `.github/`
- `rules/`
- `runs/`
- `docs/`
- `run-packages/`
- backend files
- config/secrets
- files outside `lab/`

## Weekly loop

1. People propose prompts as GitHub issues.
2. People vote with GitHub reactions.
3. Candidates are ranked by the vote result.
4. Rank 1 is the normal weekly run candidate.
5. Rank 2 and rank 3 may be executed as support-unlocked comparison runs.
6. The AI agent modifies only `lab/` and opens a PR.
7. Safety checks run.
8. The maintainer reviews and merges/rejects.
9. The result is recorded in `runs/week-XXX.md`.

## Ranked candidates

Prompt Vote Lab uses ranked candidates, not a single permanent winner.

- `rank-1`: normal weekly run and default mainline candidate
- `rank-2`: optional support-unlocked comparison run
- `rank-3`: optional support-unlocked comparison run

## Merge policy

Voting rank has priority.

Rank 1 is the default merge candidate. Rank 2 and rank 3 are comparison candidates.

If rank 1 does not pass review, the default result is no merge for that weekly vote. Rank 2 and rank 3 are not automatically promoted.

See `rules/merge-policy-v1.0.md`.

## Support-unlocked runs

Support may unlock additional comparison runs for rank 2 and rank 3 during the weekly run window.

Initial thresholds:

- rank 2 unlock: 5 USD weekly support
- rank 3 unlock: 10 USD total weekly support

Support unlocks additional experiment runs only. It does not guarantee merge, does not grant specification control, and does not bypass safety checks.

See `rules/support-unlocked-runs-v1.0.md`.

## GitHub Pages

This repository is designed to work with GitHub Pages as a static site.

Recommended Pages source:

- Branch: `main`
- Folder: `/`

Useful paths after Pages is enabled:

- `/lab/` — current lab UI
- `/runs/week-001.md` — run log template
- `/rules/static-ui-v1.0.md` — implementation rule profile

## License

This project is licensed under the Apache License 2.0.
