# Prompt Vote Lab public results export

Generated at: `2026-05-09T09:44:56+00:00`

This file is a raw results surface for participants. It does not score prompts or recommend improvements.

## Summary

| metric | value |
| --- | --- |
| issue_count | 12 |
| open_issue_count | 2 |
| blocked_issue_count | 2 |
| clear_issue_count | 5 |
| authorized_canary_issue_count | 1 |
| pr_count | 100 |
| open_pr_count | 0 |
| merged_pr_count | 97 |
| workflow_run_count | 100 |
| run_record_count | 20 |

## Recent Issues

| # | state | +1 | labels | title |
| --- | --- | --- | --- | --- |
| 195 | OPEN | 0 | issue-safety:clear, issue-safety:runtime-detected, issue-safety:submission-detected, normal-candidate, prompt-proposal, week:2026-W20 | [Prompt][Rank 2]: Add an evidence map for reviewing weekly runs |
| 196 | OPEN | 0 | issue-safety:clear, issue-safety:submission-detected, normal-candidate, prompt-proposal, week:2026-W20 | [Prompt][Rank 3]: Add a participant decision card for weekly run review |
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
| 207 | MERGED | 2 | 47/0 | Allow comparison runs from request PRs |
| 206 | MERGED | 1 | 7/0 | Request comparison run for Issue 195 rank 2 |
| 205 | MERGED | 2 | 3/2 | Fix comparison safety check base |
| 204 | MERGED | 2 | 66/2 | Allow comparison run request files |
| 203 | MERGED | 2 | 94/20 | Allow comparison runs from Issue comments |
| 202 | MERGED | 2 | 47/0 | Add lab evidence navigation |
| 201 | MERGED | 2 | 20/4 | Auto-run public results export after main pushes |
| 200 | MERGED | 5 | 645/6 | Add history page generator |
| 197 | MERGED | 4 | 529/0 | Add comparison dashboard generator |
| 198 | MERGED | 2 | 54/3 | Auto-build comparison dashboards during public export |
| 199 | MERGED | 2 | 260/0 | Add comparison Issue run workflow |
| 194 | MERGED | 2 | 50/4 | Add comparison run metadata inputs |
| 166 | MERGED | 4 | 452/123 | Harden fixed Issue instruction sanitizer |
| 168 | MERGED | 7 | 562/4 | Add Issue safety feedback gates |
| 165 | MERGED | 2 | 19/0 | Run Codex fixed Issue instruction canary |
| 175 | MERGED | 9 | 896/14 | Add public results export for participant analysis |
| 167 | MERGED | 2 | 310/8 | Record 009 hostile Issue sanitizer results |
| 192 | MERGED | 3 | 41/19 | Run Codex fixed Issue instruction canary |
| 185 | MERGED | 1 | 210/0 | Record second clear Issue run |
| 178 | MERGED | 3 | 177/13 | Ignore negated safety constraints in Issue scanner |
| 169 | MERGED | 6 | 264/7 | Gate blocked Issues before agent execution |
| 172 | MERGED | 2 | 21/17 | Preserve Issue safety phase labels |
| 171 | MERGED | 3 | 98/10 | Add manual Issue safety rescan |
| 174 | MERGED | 7 | 630/19 | Record authorized canary result and usable ops |
| 173 | MERGED | 3 | 176/3 | Run Codex fixed Issue instruction canary |
| 176 | MERGED | 7 | 655/15 | Add redacted raw agent run bundles |
| 180 | MERGED | 4 | 300/1 | Record clear Issue run and expand public agent bundle logs |
| 179 | MERGED | 3 | 33/14 | Run Codex fixed Issue instruction canary |
| 182 | MERGED | 7 | 869/14 | Add weekly Issue finalizer |
| 181 | MERGED | 2 | 258/16 | Update public results snapshot after clear Issue run |

## Recent Workflow Runs

| id | workflow | event | status | conclusion | title |
| --- | --- | --- | --- | --- | --- |
| 25598013730 | Terminal State Report | pull_request | completed | skipped | Allow comparison runs from request PRs |
| 25598013728 | Public Results Export | push | in_progress |  | Allow comparison runs from request PRs (#207) |
| 25598013386 | pages-build-deployment | dynamic | queued |  | pages build and deployment |
| 25593582772 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25593576392 | Public Results Export | schedule | completed | success | Public Results Export |
| 25593533491 | GitHub Pages Smoke Check | schedule | completed | failure | GitHub Pages Smoke Check |
| 25572378585 | Script Check | pull_request | completed | success | Allow comparison runs from request PRs |
| 25572378580 | Lab PR Scope Check | pull_request | completed | success | Allow comparison runs from request PRs |
| 25569438080 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25569417723 | Terminal State Report | pull_request | completed | skipped | Request comparison run for Issue 195 rank 2 |
| 25569417718 | Codex Comparison Issue Run | push | completed | failure | Request comparison run for Issue 195 rank 2 (#206) |
| 25569417713 | Public Results Export | push | completed | success | Request comparison run for Issue 195 rank 2 (#206) |
| 25569417125 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25569285896 | Lab PR Scope Check | pull_request | completed | success | Request comparison run for Issue 195 rank 2 |
| 25567694917 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25567680631 | Public Results Export | push | completed | success | Request comparison run for issue 195 rank 2 |
| 25567680613 | Codex Comparison Issue Run | push | completed | failure | Request comparison run for issue 195 rank 2 |
| 25567679424 | pages-build-deployment | dynamic | completed | cancelled | pages build and deployment |
| 25567579202 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25567566033 | Terminal State Report | pull_request | completed | skipped | Fix comparison safety check base |
| 25567565972 | Public Results Export | push | completed | success | Fix comparison safety check base (#205) |
| 25567565059 | pages-build-deployment | dynamic | completed | cancelled | pages build and deployment |
| 25567484270 | Lab PR Scope Check | pull_request | completed | success | Fix comparison safety check base |
| 25567484235 | Script Check | pull_request | completed | success | Fix comparison safety check base |
| 25566686968 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25566668292 | Public Results Export | push | completed | success | Allow comparison run request files (#204) |
| 25566668180 | Terminal State Report | pull_request | completed | skipped | Allow comparison run request files |
| 25566667573 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25566523718 | Script Check | pull_request | completed | success | Allow comparison run request files |
| 25566523702 | Lab PR Scope Check | pull_request | completed | success | Allow comparison run request files |

## Raw JSON

See `public-results.json` in the same export artifact or committed data snapshot.
