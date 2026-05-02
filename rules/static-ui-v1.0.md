# static-ui-v1.0

## Purpose

This rule profile constrains AI coding-agent runs to a small static UI experiment.

The goal is to let the agent implement the voted prompt while keeping the blast radius small enough for public review.

## Boundary principle

The boundary is based on edit scope, external dependency, network behavior, and unsafe runtime behavior.

It is not based on forbidding normal code structure or browser-local interactivity.

The agent may create ordinary JavaScript functions, helper functions, event handlers, small classes, constants, and local modules inside the existing `lab/app.js` file when that makes the implementation clearer.

`new Function(...)` is allowed only as a controlled local mechanism. It must not execute user-provided or externally loaded strings.

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

JavaScript may be used for browser-local UI behavior.

Allowed examples:

- named functions
- arrow functions
- small helper functions
- small classes
- constants
- event handlers
- DOM updates
- local state with `localStorage` or `sessionStorage`
- browser-local structured state with `IndexedDB`
- JSON export/import implemented locally
- client-side filtering, sorting, grouping, and rendering
- static simulation or game-state logic that does not contact a server
- controlled `new Function(...)` for fixed local expressions or static repository-authored logic

Do not use:

- `fetch`
- `XMLHttpRequest`
- `WebSocket`
- `EventSource`
- `eval`
- `document.cookie`
- external scripts
- external APIs
- trackers
- login forms
- payment forms
- password fields

## Controlled `new Function(...)` rule

`new Function(...)` is allowed only when all of the following are true:

- the function body is fixed by repository code
- the function body is not assembled from user input
- the function body is not assembled from URL parameters, URL hash, form fields, imported JSON, `localStorage`, `sessionStorage`, or `IndexedDB`
- the generated function does not access network APIs, cookies, credentials, secrets, or external scripts
- the use is small enough to review in a PR

Forbidden examples:

```js
new Function(userText)
new Function(location.hash.slice(1))
new Function(localStorage.getItem('rule'))
new Function(importedJson.expression)
```

Allowed pattern example:

```js
const calculateScore = new Function('votes', 'baseline', 'return Math.max(0, votes - baseline);');
```

Prefer ordinary functions when they are sufficient.

## Cookie rule

Cookies remain blocked in this policy version.

Reason:

```text
Cookies are not just a browser-local data store.
They are normally attached to HTTP requests for the origin.
```

For static lab storage, prefer:

- `localStorage`
- `sessionStorage`
- `IndexedDB`
- local JSON export/import

A future policy may allow narrowly scoped non-sensitive cookies, but this version does not.

## If the voted prompt asks for forbidden behavior

Do not implement the forbidden part.

Instead, create the nearest safe static UI prototype and report which parts were ignored.

## Output required

After editing, report:

1. Files changed
2. Summary of changes
3. Manual test steps
4. Unsafe or unsupported parts ignored
