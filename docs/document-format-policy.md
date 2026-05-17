# Document format policy

This document defines the documentation format policy for participant-facing and maintainer-facing documents.

## Current decision

Use Markdown files with the `.md` extension for public documentation.

Do not convert participant-facing docs to `.mdx` yet.

```text
current documentation format: .md
mdx adoption status: not approved
build-system requirement for mdx: not present
```

## Reason

Prompt Vote Lab is currently a GitHub-native static experiment.

The current public explanation layer is designed around:

```text
GitHub-rendered Markdown
GitHub Pages static files
plain repository review
no documentation build step
no React documentation runtime
no MDX compiler
```

MDX is useful when documentation needs embedded JSX components, imports, exports, or a framework build step.

That is not the current requirement.

## Why not MDX now

Do not introduce `.mdx` now because it would add new moving parts:

```text
MDX compiler
JSX runtime or framework integration
build pipeline
component policy
additional security review for embedded interactive components
additional local preview path
```

Those costs do not match the current release goal.

The current release goal is:

```text
static public explanation
clear participant journey
canonical runner evidence
manual review
auto-merge disabled
ordinary default-on weekly observation
```

MDX does not help those release blockers.

## Approved documentation format

Use `.md` for:

```text
participant guide
how to participate
operator runbook
release readiness review
root folder audit
script dependency map
workflow family map
canonical runner evidence guide
support policy
run and evidence explanations
```

Use plain HTML only for public pages that must render directly on GitHub Pages without Markdown rendering ambiguity, such as:

```text
/index.html
/lab/index.html
```

## When MDX can be reconsidered

MDX can be reconsidered only after a separate proposal records:

```text
chosen static site framework or build system
MDX compiler and dependency policy
component allowlist
security review for embedded components
preview workflow
GitHub Pages deployment path
migration plan from existing .md docs
rollback path
```

Until then, `.mdx` is not an accepted format for user-facing project docs.

## Rule

```text
If a document is meant to be readable in GitHub's repository UI, keep it .md.
If a document is meant to be rendered by the current GitHub Pages static layer, use .html or existing generated pages.
If a document needs MDX, first add a build-system proposal and security review.
```

## Current answer

For this repository today:

```text
Use .md, not .mdx.
```