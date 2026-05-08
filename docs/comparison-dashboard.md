# Comparison dashboard

## Purpose

The comparison dashboard makes weekly rank-based experiment evidence readable without replacing GitHub as the source of truth.

GitHub Issues, PRs, commits, public agent run bundles, and `runs/` records remain the canonical evidence.

The dashboard is an index for participants.

## Public location

Generated dashboards should be written under:

```text
lab/comparisons/<week_id>/index.html
lab/comparisons/<week_id>/style.css
```

Rank outputs should live under:

```text
lab/comparisons/<week_id>/rank-1/
lab/comparisons/<week_id>/rank-2/
lab/comparisons/<week_id>/rank-3/
```

Each rank root should contain only the static prototype for that rank:

```text
index.html
style.css
app.js
```

## Evidence shown

The dashboard should show, per rank:

```text
rank
Issue number
Issue title
Issue state
vote count
safety scan status
runtime scan status
implementation PR
changed files
output root
run record path
decision
```

## Source data

The first implementation reads:

```text
data/public-results.json
```

It does not read raw diagnostics or private artifacts.

## Security boundary

The dashboard must not embed:

```text
raw Codex stdout/stderr
raw login logs
raw container logs
raw environment variables
secrets
payment data
private user data
iframes
external scripts
network calls
```

The page uses the same static-site posture as the lab:

```text
connect-src 'none'
frame-src 'none'
object-src 'none'
form-action 'none'
```

## Why Git history alone is insufficient

Git history is the evidence source, but it is not a participant interface.

Participants need a readable index that answers:

```text
which Issue was run
which PR was produced
which evidence bundle exists
which rank was adopted or rejected
where the run record lives
```

## Generator

Use:

```text
python scripts/build_comparison_dashboard.py \
  --public-results data/public-results.json \
  --week-id 2026-W20 \
  --out-dir lab/comparisons/2026-W20
```

This writes:

```text
index.html
style.css
```

## Current limitation

This generator creates the comparison index only.

Rank-specific implementation roots are still produced by comparison-run workflows or manual evidence PRs.
