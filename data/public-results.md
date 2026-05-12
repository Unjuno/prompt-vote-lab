# Prompt Vote Lab public results export

Generated at: `2026-05-12T09:02:14+00:00`

This file is a raw results surface for participants. It does not score prompts or recommend improvements.

## Summary

| metric | value |
| --- | --- |
| issue_count | 12 |
| open_issue_count | 0 |
| blocked_issue_count | 2 |
| clear_issue_count | 5 |
| authorized_canary_issue_count | 1 |
| pr_count | 100 |
| open_pr_count | 0 |
| merged_pr_count | 85 |
| workflow_run_count | 98 |
| run_record_count | 21 |

## Recent Issues

| # | state | +1 | labels | title |
| --- | --- | --- | --- | --- |
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
| 271 | MERGED | 3 | 12/2 | Fix OpenAI key false positive in public bundle verifier |
| 270 | MERGED | 5 | 289/30 | Scan public agent bundles with Gitleaks |
| 269 | MERGED | 4 | 30/15 | Add actionlint to Script Check |
| 268 | MERGED | 4 | 66/6 | Verify uploaded public agent bundles |
| 267 | MERGED | 8 | 493/8 | Verify public agent run bundle contents |
| 266 | MERGED | 2 | 7/1 | Run Script Check for all run records |
| 265 | MERGED | 1 | 202/0 | Record first-canary-007 evidence-only result |
| 263 | CLOSED | 1 | 1/0 | Run Codex policy-enforced agent canary |
| 264 | MERGED | 2 | 14/6 | Document policy-agent reasoning traces in PR body |
| 262 | MERGED | 4 | 317/25 | Publish sanitized reasoning trace evidence |
| 261 | MERGED | 6 | 648/52 | Expand public agent observation logs |
| 260 | MERGED | 6 | 185/4 | Publish redacted policy-agent public bundle |
| 259 | MERGED | 2 | 110/249 | Document canonical Docker Codex runner |
| 258 | CLOSED | 2 | 27/0 | Run fixed first canary |
| 249 | MERGED | 1 | 3/3 | Fix root prompt template links |
| 250 | CLOSED | 8 | 463/21 | Add live previews for rank outputs |
| 253 | MERGED | 1 | 10/1 | Update generated dashboard live output contract |
| 252 | CLOSED | 3 | 380/0 | Add W20 rank 1 live output snapshot |
| 251 | MERGED | 2 | 22/7 | Generate live output links in comparison dashboards |
| 254 | MERGED | 3 | 380/0 | Add W20 rank 1 live output snapshot |
| 256 | MERGED | 2 | 69/9 | Fix history adopted rank inference |
| 255 | MERGED | 3 | 292/0 | Add W19 rank 1 live output snapshot |
| 257 | MERGED | 2 | 54/7 | Add live preview hub to lab page |
| 201 | MERGED | 2 | 20/4 | Auto-run public results export after main pushes |
| 203 | MERGED | 2 | 94/20 | Allow comparison runs from Issue comments |
| 202 | MERGED | 2 | 47/0 | Add lab evidence navigation |
| 205 | MERGED | 2 | 3/2 | Fix comparison safety check base |
| 204 | MERGED | 2 | 66/2 | Allow comparison run request files |
| 206 | MERGED | 1 | 7/0 | Request comparison run for Issue 195 rank 2 |
| 209 | MERGED | 2 | 44/93 | Simplify comparison workflow and detect new rank files |

## Recent Workflow Runs

| id | workflow | event | status | conclusion | title |
| --- | --- | --- | --- | --- | --- |
| 25724466429 | Terminal State Report | pull_request | completed | skipped | Fix OpenAI key false positive in public bundle verifier |
| 25724034333 | Lab PR Scope Check | pull_request | completed | success | Fix OpenAI key false positive in public bundle verifier |
| 25724034331 | Script Check | pull_request | completed | success | Fix OpenAI key false positive in public bundle verifier |
| 25718461471 | Codex Policy Agent Canary Run | workflow_dispatch | completed | failure | Codex Policy Agent Canary Run |
| 25718214991 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25718201613 | Terminal State Report | pull_request | completed | skipped | Scan public agent bundles with Gitleaks |
| 25718201576 | Public Results Export | push | completed | success | Scan public agent bundles with Gitleaks (#270) |
| 25718201000 | pages-build-deployment | dynamic | completed | cancelled | pages build and deployment |
| 25717773526 | Script Check | pull_request | completed | success | Scan public agent bundles with Gitleaks |
| 25717773502 | Lab PR Scope Check | pull_request | completed | success | Scan public agent bundles with Gitleaks |
| 25717327783 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25717316218 | Public Results Export | schedule | completed | success | Public Results Export |
| 25717244415 | GitHub Pages Smoke Check | schedule | completed | failure | GitHub Pages Smoke Check |
| 25714507921 | pages-build-deployment | dynamic | completed | success | pages build and deployment |
| 25714495705 | Public Results Export | push | completed | success | Add actionlint to Script Check (#269) |
| 25714495666 | Terminal State Report | pull_request | completed | skipped | Add actionlint to Script Check |
| 25714495158 | pages-build-deployment | dynamic | completed | cancelled | pages build and deployment |
| 25714427077 | Pre-API Freeze Audit | pull_request | completed | success | Add actionlint to Script Check |
| 25714427060 | Select Eligible Test | pull_request | completed | success | Add actionlint to Script Check |
| 25714427055 | Implementation Preflight Test | pull_request | completed | success | Add actionlint to Script Check |
| 25714427052 | Script Check | pull_request | completed | success | Add actionlint to Script Check |
| 25714427050 | Lab PR Scope Check | pull_request | completed | success | Add actionlint to Script Check |
| 25714172383 | Script Check | pull_request | completed | failure | Add actionlint to Script Check |
| 25714172382 | Pre-API Freeze Audit | pull_request | completed | success | Add actionlint to Script Check |
| 25714172381 | Implementation Preflight Test | pull_request | completed | success | Add actionlint to Script Check |
| 25714172380 | Lab PR Scope Check | pull_request | completed | success | Add actionlint to Script Check |
| 25714172377 | Select Eligible Test | pull_request | completed | success | Add actionlint to Script Check |
| 25713643434 | Script Check | pull_request | completed | failure | Add actionlint to Script Check |
| 25713643423 | Lab PR Scope Check | pull_request | completed | success | Add actionlint to Script Check |
| 25712668692 | pages-build-deployment | dynamic | completed | success | pages build and deployment |

## Raw JSON

See `public-results.json` in the same export artifact or committed data snapshot.
