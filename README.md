# Prompt Vote Lab

Prompt Vote Lab is a public experiment for observing vibe coding.

People propose prompts, vote on them, and an AI coding agent implements the winning prompt inside a constrained `lab/` directory.

The goal is not only to generate UI. The goal is to study the gap between collective expectation and AI-implemented reality.

Each run records:

- the voted prompt
- vote count
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
- backend files
- config/secrets
- files outside `lab/`

## Weekly loop

1. People propose prompts as GitHub issues.
2. People vote with GitHub reactions.
3. The maintainer applies `rules/selection-v1.0.md`.
4. If a prompt passes the no-change baseline, a lab run is created.
5. The AI agent modifies only `lab/` and opens a PR.
6. Safety checks run.
7. The maintainer reviews and merges/rejects.
8. The result is recorded in `runs/week-XXX.md`.

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
