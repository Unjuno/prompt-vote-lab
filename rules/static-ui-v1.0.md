# static-ui-v1.0

## Purpose

This rule profile constrains AI coding-agent runs to a small static UI experiment.

The goal is to let the agent implement the voted prompt while keeping the blast radius small enough for public review.

## Editable scope

The agent may edit only files under `lab/`.

Expected editable files:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

## Forbidden files and directories

The agent must not edit, create, delete, or depend on:

- `.github/`
- `rules/`
- `runs/`
- `docs/`
- `.gitignore`
- `README.md`
- `LICENSE`
- any file outside `lab/`
- backend files
- database files
- payment or webhook files
- authentication or session files
- server configuration files
- `.env` or secret files
- dependency files

## JavaScript constraints

JavaScript may be used only for local UI behavior.

Do not use:

- `fetch`
- `XMLHttpRequest`
- `WebSocket`
- `EventSource`
- `eval`
- `new Function`
- `document.cookie`
- external scripts
- external APIs
- trackers
- login forms
- payment forms
- password fields

## If the voted prompt asks for forbidden behavior

Do not implement the forbidden part.

Instead, create the nearest safe static UI prototype and report which parts were ignored.

## Output required

After editing, report:

1. Files changed
2. Summary of changes
3. Manual test steps
4. Unsafe or unsupported parts ignored
