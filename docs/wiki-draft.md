# Wiki draft

This document is a copy-ready draft for the GitHub Wiki.

The repository should keep canonical rules and implementation documents in `docs/`, `rules/`, and `runs/`. The Wiki can be used later as a beginner-friendly navigation layer.

## Suggested Wiki pages

### Home

Prompt Vote Lab is a public experiment for observing how voted prompts behave when implemented by a constrained AI coding agent.

Participants propose prompts as GitHub Issues, vote with 👍 reactions, and review the resulting implementation PRs and reports.

Key links:

- Lab UI: `/lab/`
- Participation guide: `docs/how-to-participate.md`
- Experiment model: `docs/experiment-model.md`
- Support policy: `docs/support-policy.md`
- Automation map: `docs/automation-map.md`

### How to participate

1. Open a prompt proposal issue.
2. Write the exact prompt.
3. Describe the expected visible result.
4. Confirm it fits the static lab scope.
5. Vote on prompts with 👍 reactions.

### Weekly vote model

Each week includes real prompt candidates plus a virtual no-change baseline.

```text
No-change baseline: 20 virtual votes
```

If the baseline ranks first, no implementation run is created.

### Support model

Support may open additional comparison runs.

- 5 USD: Support Rank 2 Comparison Run
- 10 USD: Support Rank 3 Comparison Run
- 20 USD: Support the Experiment

Support does not guarantee success, adoption, merge, or specification control.

### Automation boundary

Automated:

- vote collection
- eligibility calculation
- implementation PR creation
- safety check
- report creation

Not automated:

- merge into `main`
- safety rule weakening
- Hacker News submission
- maintainer emergency decisions

## Recommendation

Do not make the Wiki the source of truth.

Use the Wiki as a readable index, and keep canonical rules in repo files.
