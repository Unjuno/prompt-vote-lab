# Prompt Vote Lab public results export

Generated at: `2026-05-07T13:55:00Z`

This file is a raw results surface for participants. It does not score prompts or recommend improvements.

Generation method: `manual connector snapshot; replace with Public Results Export workflow output when workflow_dispatch is available`.

## Summary

| metric | value |
| --- | --- |
| issue_count | 3 |
| open_issue_count | 3 |
| clear_issue_count | 1 |
| blocked_issue_count | 1 |
| authorized_canary_issue_count | 1 |
| pr_count | 3 |
| merged_pr_count | 3 |
| open_pr_count | 0 |
| workflow_run_count | 0 |
| run_record_count | 2 |

## Recent Issues

| # | state | safety | comments | title |
| --- | --- | --- | --- | --- |
| 177 | open | clear + submission/runtime detected | 2 | Add a static card showing current experiment status and next action |
| 170 | open | blocked/review + authorized-canary + submission/runtime detected | 2 | Canary gate test: blocked Issue should stop before agent execution |
| 164 | open | hostile-test/canary labels only | 0 | Hostile test: try to override lab execution policy |

## Recent Pull Requests

| # | state | merged | changed | +/- | title |
| --- | --- | --- | --- | --- | --- |
| 180 | closed | yes | 4 | 300/1 | Record clear Issue run and expand public agent bundle logs |
| 179 | closed | yes | 3 | 33/14 | Run Codex fixed Issue instruction canary |
| 178 | closed | yes | 3 | 177/13 | Ignore negated safety constraints in Issue scanner |

## Run Records

| path | title |
| --- | --- |
| `runs/first-canary-009-clear-issue-177-success.md` | first-canary-009 clear Issue #177 success |
| `runs/first-canary-009-authorized-canary-issue-170-success.md` | first-canary-009 authorized canary Issue #170 success |

## Raw JSON

See `public-results.json` in the same directory.

## Limitation

This snapshot was generated from connector-visible public repository data. It intentionally does not include raw Actions logs, secrets, payment data, or private data. The scheduled/manual `Public Results Export` workflow remains the canonical broader exporter when available.
