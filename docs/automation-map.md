# Automation map

This document maps Prompt Vote Lab automation boundaries.

## Automated

- package weekly candidates
- run rank-1 implementation
- run support-unlocked rank-2 and rank-3 implementations
- create implementation PRs
- run safety checks
- create run logs
- classify final expectation gap
- create and publish blog reports
- create Hacker News drafts

## Not automated

- merge into `main`
- weaken safety rules to accept a failed implementation PR
- submit posts to Hacker News
- maintainer emergency decisions

## Main workflows

| Workflow | Status | Purpose |
|---|---|---|
| `create-run-package.yml` | implemented | Manually create a run package PR |
| `codex-lab-run.yml` | implemented | Run `gpt-5-nano` against `lab/` and open a PR |
| `safety-check.yml` | implemented | Check lab implementation PRs |
| `weekly-vote-run.yml` | not implemented | Count votes and select ranks |
| `support-check.yml` | not implemented | Check weekly support thresholds |
| `blog-report.yml` | not implemented | Publish weekly report |

## Data flow

```text
GitHub Issues
→ GitHub reactions
→ weekly ranking
→ implementation model
→ implementation PR
→ safety check
→ run log
→ evaluation model
→ blog report
```
