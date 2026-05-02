# initial-lab-state-v1.0

## Purpose

This policy defines the initial state of `lab/` before the first accepted prompt run.

## Initial files

The lab starts with exactly three editable files:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

These files are intentionally minimal.

## Initial state rule

The initial lab may show a small placeholder explaining that the area is waiting for the first accepted prompt run.

It must not behave like a landing page for the whole project.

Project explanation belongs in:

- `README.md`
- `docs/`
- `rules/`
- GitHub Wiki as a navigation layer

## Allowed initial content

Allowed:

- project title
- short status text
- note that the area is the constrained implementation target
- local CSS
- no-op JavaScript

Not allowed:

- full project explanation
- participation guide
- support pitch
- current candidate list
- voting dashboard
- external scripts
- network calls
- forms
- login
- payment UI

## Rationale

`lab/` is the experimental surface modified by accepted implementation runs.

If `lab/` starts as a polished landing page, the first prompt run is no longer working from a clean baseline.

The baseline should be small enough that later changes are attributable to voted prompts.
