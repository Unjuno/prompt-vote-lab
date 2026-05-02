# local-data-store-v1.0

## Purpose

This policy allows Prompt Vote Lab to keep structured experiment data without turning `lab/` into a backend application.

## Allowed data stores

Allowed as repository-managed data:

- Markdown run logs in `runs/`
- JSON or JSONL files in `data/`
- CSV files in `data/`
- generated SQLite files as workflow artifacts
- generated DuckDB files as workflow artifacts

## Source of truth

The source of truth must remain reviewable text files:

- `runs/*.md`
- `data/*.json`
- `data/*.jsonl`
- `data/*.csv`

Binary database files must not be the only source of truth.

## SQLite

SQLite is allowed for workflow-side indexing and local analysis.

Recommended use:

- build a SQLite database from `runs/` and `data/`
- query it in GitHub Actions or local scripts
- export reviewable Markdown, JSON, JSONL, or CSV

SQLite database files should normally be uploaded as workflow artifacts rather than committed to `main`.

## DuckDB

DuckDB is allowed for heavier analytics and aggregate reports.

Recommended use:

- scan JSONL, CSV, or Parquet-like analytical datasets
- generate aggregate reports
- compare many historical runs

DuckDB database files should normally be uploaded as workflow artifacts rather than committed to `main`.

## Browser runtime rule

The public root page and `lab/` must not connect to an external database or external API at runtime.

The lab must not load a database engine from a CDN.

If browser-side database querying is ever introduced, all runtime code and data must be local repository files, and a new policy version is required.

## Lab edit scope

Implementation runs still edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

Implementation runs must not directly edit canonical data files unless a future policy version explicitly allows it.

## Rationale

A database can help the experiment, but only if it improves recording and analysis without changing the implementation conditions.

External databases, hidden data sources, or CDN-hosted database engines would make results less reproducible and harder to compare.
