# static-ui-v1.0

## Purpose

This rule profile constrains AI coding-agent runs to a small static UI experiment.

The goal is to let the agent implement the voted prompt while keeping the blast radius small enough for public review.

## Boundary principle

The boundary is based on edit scope, external dependency, network behavior, and unsafe runtime behavior.

It is not based on forbidding normal code structure.

The agent may create ordinary JavaScript functions, helper functions, event handlers, small classes, constants, and local modules inside the existing `lab/app.js` file when that makes the implementation clearer.

The forbidden item is the dynamic code constructor `new Function(...)`, not newly written helper functions.

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

JavaScript may be used for local UI behavior.

Allowed examples:

- named functions
- arrow functions
- small helper functions
- event handlers
- DOM updates
- local state with `localStorage` or `sessionStorage`
- JSON export/import implemented locally

Do not use:

- `fetch`
- `XMLHttpRequest`
- `WebSocket`
- `EventSource`
- `eval`
- `new Function(...)`
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
