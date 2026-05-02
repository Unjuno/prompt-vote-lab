# public-site-v1.0

## Purpose

This policy separates the public explanation page from the experimental lab target.

## Public root page

The root page is:

```text
index.html
```

It explains:

- what Prompt Vote Lab is
- how voting works
- the no-change baseline
- support-unlocked comparison runs
- where documentation lives
- how to open the lab

The root page is not edited by implementation model runs.

## Lab page

The lab page is:

```text
lab/
```

It is the constrained implementation target edited by accepted prompt runs.

The lab starts as a minimal placeholder before the first accepted run.

## Rule

Do not use `lab/` as the landing page for project explanation.

Do not use `index.html` as the implementation target.

## Rationale

The project needs two surfaces:

1. A stable explanation surface for participants.
2. A mutable experiment surface for AI implementation runs.

Keeping them separate prevents the first lab run from starting from an already-polished landing page.
