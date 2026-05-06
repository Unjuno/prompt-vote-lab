# Codex path comparison: 005, 007, 008, and 009

## Purpose

This document compares the currently relevant Codex implementation paths:

```text
first-canary-005: offline-context JSON writeback
first-canary-007: policy-enforced agent container
first-canary-008: selected prompt task packet container
first-canary-009: fixed GitHub Issue instruction packet, design phase
```

Architectural correction:

```text
005, 007, and 008 do not choose the prompt.
They execute an implementation input that the Prompt Vote Lab selection layer or canary fixture has already chosen.
```

## Layer model

| Layer | Responsibility | Not responsible for |
|---|---|---|
| Prompt selection layer | Select the implementation prompt from Prompt Vote Lab candidates, votes, gates, and eligibility rules | Editing files |
| Instruction-builder layer | Normalize the selected input into a bounded implementation brief | Weakening runner policy |
| Execution layer | Apply the selected/normalized prompt through a bounded Codex runner and open a reviewable PR | Choosing the winning prompt |
| Review layer | Accept or reject the PR | Silent auto-merge |

Normal production flow:

```text
1. Candidate prompts are submitted as GitHub Issues.
2. The selection policy chooses the eligible prompt.
3. The selected prompt metadata is recorded.
4. The selected prompt is normalized into an instruction packet.
5. The instruction packet is passed to an execution path.
6. The execution path opens a bounded implementation PR.
7. A human reviews and merges manually.
8. The run result is recorded in runs/.
```

The early canaries used fixed test prompts with `issue_number: 0` and `candidate_rank: 1`. Those canary prompts are placeholders for a real selected prompt.

## Core comparison

| Dimension | 005: offline JSON writeback | 007: policy-enforced agent container | 008: selected prompt task packet | 009: fixed Issue instruction packet |
|---|---|---|---|---|
| Current status | Stable production-oriented path | Successful candidate path | Successful stronger agent candidate path | Design phase |
| Main purpose | Safe bounded implementation with fewer moving parts | Agent-style implementation with stronger repository-visibility boundary | Agent execution with `/task:ro` prompt/policy packet and credential hygiene | Real GitHub Issue ingestion and instruction normalization |
| Input source in canary | Fixed canary prompt | Fixed canary prompt | Fixed canary prompt packet | Fixed GitHub Issue |
| Input source in production | Selected prompt from vote/rank process | Selected prompt from vote/rank process | Selected prompt packet | Selected GitHub Issue or vote winner after later canary |
| Agent behavior | Low; close to API-style generation | High; Codex reads and edits files as an agent | High; Codex reads `/task` and edits `/work/lab` | High; Codex reads normalized Issue instructions from `/task` |
| Repository root visible to Codex | No; workflow provides allowed file contents in prompt | No; container workdir does not mount repo root | No; container workdir does not mount repo root | No; same expected boundary as 008 |
| Editable working area | Not applicable; Codex returns JSON | `/work` mounted read/write | `/work` mounted read/write | `/work` mounted read/write |
| Task packet area | Prompt text embedded in Codex request | Fixed prompt embedded in runner | `/task:ro` selected prompt and policy snapshot | `/task:ro` selected Issue metadata, raw body, and instruction brief |
| Runtime area | Empty execution context plus workflow-side parser | `/codex-runtime` mounted read/write | `/codex-runtime` mounted read/write | `/codex-runtime` mounted read/write |
| Write mechanism | Codex returns JSON full-file replacements | Codex edits `/work/lab/*`; workflow copies back allowed files | Codex edits `/work/lab/*`; workflow copies back allowed files | Same as 008 |
| Final writable files | `lab/index.html`, `lab/style.css`, `lab/app.js` | `lab/index.html`, `lab/style.css`, `lab/app.js` | `lab/index.html`, `lab/style.css`, `lab/app.js` | `lab/index.html`, `lab/style.css`, `lab/app.js` |
| Primary boundary | JSON parser + allowed-path validator + guards | Docker mounted workdir-only boundary + copy-back guard + guards | Docker `/work:rw` + `/task:ro` + copy-back guard + guards | Same as 008 plus instruction normalization contract |
| Secret handling | Codex request handled outside container path | API key used inside container login path | API key present for login and absent before `codex exec` | Must inherit 008 credential hygiene |
| Operational complexity | Lower | Higher | Higher | Higher plus Issue fetching/normalization |
| Diagnostics value | Good for selected prompt, final output, validation | Better for agent behavior and mount policy | Better for task packet, credential, mount, and agent behavior | Adds Issue metadata and instruction-brief auditability |
| Weakness | API-like; weak action observation | More moving parts; fixed prompt | One success; fixed prompt packet, not real Issue | Not implemented yet |
| Recommended use now | Routine bounded implementation | Historical successful agent-boundary step | Agent-style experiments requiring selected prompt packet evidence | Next canary design, not runtime path yet |
| Promotion state | Current stable path | Superseded by 008 as stronger candidate | Candidate; needs repetition and 009 fixed-Issue success | Design only |

## Coding and policy rules shared by all paths

All paths must preserve the same final implementation rules.

Editable files:

```text
lab/index.html
lab/style.css
lab/app.js
```

Forbidden final changes include:

```text
.github/
rules/
runs/
docs/
README.md
LICENSE
dependency files
secret files
backend files
server configuration files
any file outside lab/
```

Forbidden runtime patterns in `lab/` include:

```text
external scripts
fetch()
XMLHttpRequest
WebSocket
EventSource
eval()
document.cookie
navigator.sendBeacon
unsafe new Function(...)
```

Allowed static UI implementation patterns include:

```text
ordinary functions
helper functions
event handlers
DOM updates
localStorage / sessionStorage / IndexedDB
local JSON export/import
client-side filtering, sorting, grouping, and rendering
static simulation or game-state logic without server calls
```

The selected prompt or selected Issue is task input. It cannot override the runner policy, allowed files, safety checks, or manual review requirement.

## 005 execution packet

005 treats the selected prompt and allowed file contents as a bounded request packet.

Expected production inputs:

```text
selected_prompt
issue_number
candidate_rank
vote_count
selection_policy
allowed_file_contents
runner_policy
```

Execution shape:

```text
selected prompt + allowed file contents
-> Codex JSON output
-> workflow validates JSON
-> workflow applies allowed replacements
-> checks
-> PR
```

005 is useful when the priority is predictable bounded output rather than observing agent behavior.

## 007 execution packet

007 proved that Codex can run inside a Docker container where the repository root is not mounted.

Container layout:

```text
/work             rw  editable lab files only
/codex-runtime    rw  Codex and npm runtime state
/diagnostics      rw  logs and run evidence
repo root         not mounted
```

007 is now best treated as a successful stepping stone toward 008.

## 008 execution packet

008 proved that a selected prompt and policy snapshot can be mounted read-only at `/task`.

Container layout:

```text
/work             rw  editable lab files only
/task             ro  selected prompt and policy snapshot
/codex-runtime    rw  Codex and npm runtime state
/diagnostics      rw  logs and run evidence
repo root         not mounted
```

Task packet contents:

```text
/task/selected-prompt.md
/task/run-manifest.json
/task/execution-policy.md
/task/allowed-files.json
/task/static-ui-v1.0.md
/task/agent-run-policy-v1.0.md
/task/task-file-hashes.json
```

Execution shape:

```text
selected prompt packet in /task
+ lab files in /work
-> Codex edits /work/lab files
-> workflow copies back only allowed files
-> checks
-> PR
```

008 is useful when the priority is agent behavior plus evidence that task instructions and policy snapshots can be supplied without mounting the repository root.

## 009 intended execution packet

009 should prove real GitHub Issue ingestion without adding vote-winner selection yet.

Recommended first 009 shape:

```text
fixed GitHub Issue
-> selected-issue.json
-> raw-issue-body.md
-> instruction-brief.md
-> /task:ro
-> 008-style container runner
```

Recommended `/task` contents:

```text
/task/instruction-brief.md
/task/selected-issue.json
/task/raw-issue-body.md
/task/run-manifest.json
/task/execution-policy.md
/task/allowed-files.json
/task/static-ui-v1.0.md
/task/agent-run-policy-v1.0.md
/task/task-file-hashes.json
```

009 should not include automatic vote-winner selection. That belongs in a later canary after fixed-Issue ingestion is proven.

## Secret handling requirement for task-packet runs

008 established this requirement:

```text
1. Pass API key only for codex login.
2. Run codex login.
3. Remove API key from the environment.
4. Run codex exec after the API key variable is absent.
5. Record presence checks without recording the secret value.
```

Diagnostic example:

```text
OPENAI_API_KEY present before login: yes
OPENAI_API_KEY present before codex exec: no
```

Do not print secret values.

## Routing recommendation

Use 005 when:

```text
- the priority is stable bounded implementation
- the selected prompt can be implemented from the allowed file contents
- agent action traces are not the main research target
- fewer runtime dependencies are preferred
```

Use 008 when:

```text
- the priority is observing Codex as a file-editing agent
- selected prompt packet evidence is needed
- repository root must stay unavailable to the agent work directory
- Docker and runtime complexity are acceptable
- diagnostics are more important than operational simplicity
```

Use 009 only after implementation when:

```text
- a real fixed GitHub Issue must be transformed into /task instruction files
- raw Issue text must be preserved separately from normalized implementation instructions
- the project wants to test Issue ingestion without vote-winner selection
```

## Promotion rule for 008

008 should not replace 005 after only one success.

Promotion condition:

```text
Promote 008 from candidate to standard agent path after at least 2 consecutive successful full 008 runs under the same fixed conditions, plus one successful fixed-Issue 009 run.
```

A repeated 008 success should include:

```text
- Codex exit code 0
- container exit code 0
- final changed files subset of lab/index.html, lab/style.css, lab/app.js
- repository root not mounted into the container work directory
- /task mounted read-only
- API key absent before codex exec
- policy-denied-access empty or explained
- safety-check PASS
- static-site-check PASS
- manual PR review and merge
```

## Decision summary

```text
005 is the stable implementation path.
007 is a successful stepping stone.
008 is the strongest implemented agent-boundary candidate.
009 should be the fixed GitHub Issue instruction-packet experiment.
```

Do not collapse prompt selection and execution. Prompt Vote Lab chooses or supplies the prompt first; 005, 007, 008, or 009 only execute it under different boundaries.
