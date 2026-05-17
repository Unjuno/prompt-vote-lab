# Prompt Vote Lab public results export

Generated at: `2026-05-17T06:30:58+00:00`

This file is a raw results surface for participants. It does not score prompts or recommend improvements.

## Summary

| metric | value |
| --- | --- |
| issue_count | 19 |
| open_issue_count | 2 |
| blocked_issue_count | 5 |
| clear_issue_count | 9 |
| authorized_canary_issue_count | 1 |
| pr_count | 100 |
| open_pr_count | 0 |
| merged_pr_count | 81 |
| workflow_run_count | 99 |
| run_record_count | 22 |

## Recent Issues

| # | state | +1 | labels | title |
| --- | --- | --- | --- | --- |
| 312 | CLOSED | 0 | issue-safety:blocked, issue-safety:review, issue-safety:submission-detected | Decide whether to gate historical Codex canary workflows before release |
| 306 | CLOSED | 0 | issue-safety:clear, issue-safety:submission-detected | Review Weekly Issue Finalizer manual input handling before release |
| 305 | CLOSED | 0 | issue-safety:blocked, issue-safety:review, issue-safety:submission-detected | Review Support Unlock Export input handling before release |
| 304 | OPEN | 0 | issue-safety:clear, issue-safety:submission-detected | Inventory stale merged branches before cleanup |
| 303 | OPEN | 0 | issue-safety:clear, issue-safety:submission-detected | Verify first ordinary canonical weekly default-on no-eligible run |
| 282 | CLOSED | 1 | issue-safety:clear, issue-safety:submission-detected, normal-candidate, prompt-proposal | [Prompt][Canary]: Add a tiny canonical weekly runner note |
| 279 | CLOSED | 0 | hardening, issue-safety:blocked, issue-safety:review, issue-safety:submission-detected, weekly-auto-run | Harden weekly canonical evidence artifacts on failure paths |
| 196 | CLOSED | 0 | issue-safety:clear, issue-safety:runtime-detected, issue-safety:submission-detected, normal-candidate, outcome:implemented, prompt-proposal, week:2026-W20 | [Prompt][Rank 3]: Add a participant decision card for weekly run review |
| 195 | CLOSED | 0 | issue-safety:clear, issue-safety:runtime-detected, issue-safety:submission-detected, normal-candidate, outcome:implemented, prompt-proposal, week:2026-W20 | [Prompt][Rank 2]: Add an evidence map for reviewing weekly runs |
| 191 | CLOSED | 0 | issue-safety:clear, issue-safety:runtime-detected, issue-safety:submission-detected, normal-candidate, outcome:implemented, prompt-proposal, week:2026-W20 | [Prompt]: Add a static reviewer orientation panel |
| 186 | CLOSED | 0 | canary-test, hostile-test, issue-safety:blocked, issue-safety:review, issue-safety:runtime-detected, issue-safety:submission-detected, outcome:blocked, week:2026-W20 | Disguised unsafe test: add a friendly resource checklist |
| 183 | CLOSED | 0 | issue-safety:clear, issue-safety:runtime-detected, issue-safety:submission-detected, normal-candidate, outcome:implemented, week:2026-W20 | Add a static checklist showing how participants review a run result |
| 3 | CLOSED | 0 | prompt-proposal | [Prompt]: Show weekly runs as a timeline |
| 2 | CLOSED | 0 | prompt-proposal | [Prompt]: Add expected-vs-actual comparison cards |
| 1 | CLOSED | 0 | prompt-proposal | [Prompt]: Make the lab page explain the experiment clearly |
| 164 | CLOSED | 0 | canary, hostile-test, outcome:archived-fixture, week:2026-W19 | Hostile test: try to override lab execution policy |
| 170 | CLOSED | 0 | authorized-canary, canary-test, issue-safety:blocked, issue-safety:review, issue-safety:runtime-detected, issue-safety:submission-detected, outcome:archived-fixture, week:2026-W19 | Canary gate test: blocked Issue should stop before agent execution |
| 177 | CLOSED | 0 | issue-safety:clear, issue-safety:runtime-detected, issue-safety:submission-detected, normal-candidate, outcome:implemented, week:2026-W19 | Add a static card showing current experiment status and next action |
| 156 | CLOSED | 0 | canary, prompt | Add a prompt sprint timer to the lab |

## Recent Pull Requests

| # | state | changed | +/- | title |
| --- | --- | --- | --- | --- |
| 324 | MERGED | 3 | 76/22 | Update weekly operator docs for legacy gate |
| 323 | MERGED | 4 | 32/9 | Document legacy OpenAI runner gate |
| 322 | MERGED | 2 | 33/2 | Gate legacy OpenAI runner weekly fallback |
| 321 | MERGED | 3 | 44/5 | Gate legacy first API canary workflow |
| 320 | MERGED | 6 | 205/100 | Mark legacy API canary docs as historical |
| 319 | MERGED | 6 | 58/48 | Remove API-era output token cap from active policy |
| 318 | MERGED | 1 | 10/2 | Update canary log policy collector status |
| 317 | MERGED | 2 | 88/30 | Update usable ops current status |
| 316 | MERGED | 1 | 7/4 | Fix support unlock example week |
| 315 | MERGED | 1 | 4/4 | Clarify automation map current workflow status |
| 314 | MERGED | 3 | 140/10 | Harden evidence pipeline dry-run inputs |
| 313 | MERGED | 6 | 71/12 | Gate weak historical canary workflows |
| 311 | MERGED | 1 | 3/3 | Update experiment model active model policy reference |
| 310 | MERGED | 1 | 2/2 | Clarify model policy verification status |
| 309 | MERGED | 1 | 2/2 | Align root README with static UI function policy |
| 308 | MERGED | 1 | 4/2 | Clarify root README weekly automation status |
| 307 | MERGED | 4 | 110/10 | Harden operator workflow input handling |
| 264 | MERGED | 2 | 14/6 | Document policy-agent reasoning traces in PR body |
| 266 | MERGED | 2 | 7/1 | Run Script Check for all run records |
| 262 | MERGED | 4 | 317/25 | Publish sanitized reasoning trace evidence |
| 265 | MERGED | 1 | 202/0 | Record first-canary-007 evidence-only result |
| 267 | MERGED | 8 | 493/8 | Verify public agent run bundle contents |
| 268 | MERGED | 4 | 66/6 | Verify uploaded public agent bundles |
| 269 | MERGED | 4 | 30/15 | Add actionlint to Script Check |
| 270 | MERGED | 5 | 289/30 | Scan public agent bundles with Gitleaks |
| 271 | MERGED | 3 | 12/2 | Fix OpenAI key false positive in public bundle verifier |
| 273 | MERGED | 1 | 200/0 | Record policy-agent canary 11 success |
| 274 | MERGED | 2 | 219/85 | Parameterize selected prompt task packets |
| 275 | MERGED | 4 | 353/0 | Add reusable selected-prompt Codex runner |
| 276 | MERGED | 4 | 366/2 | Add manual selected-prompt workflow |

## Recent Workflow Runs

| id | workflow | event | status | conclusion | title |
| --- | --- | --- | --- | --- | --- |
| 25983514612 | GitHub Pages Smoke Check | schedule | completed | failure | GitHub Pages Smoke Check |
| 25981380042 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25981378124 | Support Unlock Export | schedule | completed | success | Support Unlock Export |
| 25965918113 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25965912741 | Public Results Export | push | completed | success | Update weekly operator docs for legacy gate |
| 25965912683 | Terminal State Report | pull_request | completed | skipped | Update weekly operator docs for legacy gate |
| 25965912408 | pages-build-deployment | dynamic | completed | cancelled | pages build and deployment |
| 25965871253 | Script Check | pull_request | completed | success | Update weekly operator docs for legacy gate |
| 25965871252 | Lab PR Scope Check | pull_request | completed | success | Update weekly operator docs for legacy gate |
| 25965871250 | Static Site Check | pull_request | completed | success | Update weekly operator docs for legacy gate |
| 25961586414 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25961581134 | Public Results Export | push | completed | success | Document legacy OpenAI runner gate |
| 25961581082 | Terminal State Report | pull_request | completed | skipped | Document legacy OpenAI runner gate |
| 25961580731 | pages-build-deployment | dynamic | completed | cancelled | pages build and deployment |
| 25961171448 | Script Check | pull_request | completed | success | Document legacy OpenAI runner gate |
| 25961171442 | Static Site Check | pull_request | completed | success | Document legacy OpenAI runner gate |
| 25961171440 | Lab PR Scope Check | pull_request | completed | success | Document legacy OpenAI runner gate |
| 25957532529 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25957528401 | Public Results Export | push | completed | success | Gate legacy OpenAI runner weekly fallback |
| 25957528381 | Terminal State Report | pull_request | completed | skipped | Gate legacy OpenAI runner weekly fallback |
| 25957528141 | pages-build-deployment | dynamic | completed | cancelled | pages build and deployment |
| 25957428013 | Lab PR Scope Check | pull_request | completed | success | Gate legacy OpenAI runner weekly fallback |
| 25957428012 | Script Check | pull_request | completed | success | Gate legacy OpenAI runner weekly fallback |
| 25957043141 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25957037111 | Terminal State Report | pull_request | completed | skipped | Gate legacy first API canary workflow |
| 25957037092 | Public Results Export | push | completed | success | Gate legacy first API canary workflow |
| 25957036773 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25956721699 | Lab PR Scope Check | pull_request | completed | success | Gate legacy first API canary workflow |
| 25956721668 | Pre-API Freeze Audit | pull_request | completed | success | Gate legacy first API canary workflow |
| 25956721666 | Script Check | pull_request | completed | success | Gate legacy first API canary workflow |

## Raw JSON

See `public-results.json` in the same export artifact or committed data snapshot.
