# Codex path comparison: 005 vs 007

## Purpose

This document compares the two currently useful Codex implementation paths:

```text
first-canary-005: offline-context JSON writeback
first-canary-007: policy-enforced agent container
```

It also corrects an important architectural point:

```text
005 and 007 do not choose the prompt.
They execute a prompt that the Prompt Vote Lab selection layer has already chosen.
```

## Two-layer model

| Layer | Responsibility | Not responsible for |
|---|---|---|
| Prompt selection layer | Select the implementation prompt from Prompt Vote Lab candidates, votes, gates, and eligibility rules | Editing files |
| Execution layer | Apply the selected prompt through a bounded Codex runner and open a reviewable PR | Choosing the winning prompt |

Normal production flow:

```text
1. Candidate prompts are submitted as GitHub Issues.
2. The selection policy chooses the eligible prompt.
3. The selected prompt metadata is recorded.
4. The selected prompt is passed to an execution path.
5. The execution path opens a bounded implementation PR.
6. A human reviews and merges manually.
7. The run result is recorded in runs/.
```

The canaries used fixed test prompts with `issue_number: 0` and `candidate_rank: 1`. Those canary prompts are placeholders for a real selected prompt.

## Core comparison

| Dimension | 005: offline JSON writeback | 007: policy-enforced agent container |
|---|---|---|
| Current status | Stable production-oriented path | Successful candidate path |
| Main purpose | Safe bounded implementation with fewer moving parts | Agent-style implementation with stronger repository-visibility boundary |
| Prompt source in canary | Fixed canary prompt | Fixed canary prompt |
| Prompt source in production | Selected prompt from vote/rank process | Selected prompt from vote/rank process |
| Agent behavior | Low; close to API-style generation | High; Codex reads and edits files as an agent |
| Repository root visible to Codex | No; workflow provides allowed file contents in the prompt | No; container workdir does not mount repository root |
| Editable working area | Not applicable; Codex returns JSON | `/work` mounted read/write |
| Runtime area | Empty execution context plus workflow-side parser | `/codex-runtime` mounted read/write |
| Prompt packet area | Prompt text is embedded in the Codex request | Future 008 should add `/task:ro`; current 007 uses a fixed embedded prompt |
| Write mechanism | Codex returns JSON full-file replacements | Codex edits `/work/lab/*`; workflow copies back allowed files |
| Final writable files | `lab/index.html`, `lab/style.css`, `lab/app.js` | `lab/index.html`, `lab/style.css`, `lab/app.js` |
| Primary boundary | JSON parser + allowed-path validator + guards | Docker mounted workdir-only boundary + copy-back guard + guards |
| Operational complexity | Lower | Higher |
| Dependencies | Codex CLI, workflow JSON parser | Docker, Node image, npm install, Codex CLI, runtime mount |
| Diagnostics value | Good for selected prompt, final output, validation | Better for agent behavior, mount policy, runtime behavior |
| Weakness | API-like; weak action observation | More moving parts; one full success so far |
| Recommended use now | Routine bounded implementation | Agent-style experiments requiring stronger filesystem-boundary evidence |
| Promotion state | Current stable path | Candidate; needs repeated success |

## Coding and policy rules shared by both paths

Both 005 and 007 must preserve the same final implementation rules.

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

The selected prompt is task input. It cannot override the runner policy, allowed files, safety checks, or manual review requirement.

## 005 execution packet

005 can treat the selected prompt and allowed file contents as a bounded request packet.

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

Current 007 uses a fixed canary prompt and container-mounted lab files.

A production-grade successor should add a read-only task packet mount:

```text
/task:ro
```

Recommended `/task` contents:

```text
/task/selected-prompt.md
/task/run-manifest.json
/task/execution-policy.md
/task/allowed-files.json
/task/static-ui-v1.0.md
/task/agent-run-policy-v1.0.md
```

Recommended container layout:

```text
/work             rw  editable lab files only
/task             ro  selected prompt and policy snapshot
/codex-runtime    rw  Codex and npm runtime state
/diagnostics      rw  logs and run evidence
repo root         not mounted
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

007 is useful when the priority is agent behavior plus stronger evidence that repository files are not available in the agent work directory.

## Secret handling requirement for future task-packet runs

A future 008-style task-packet runner should avoid leaving the API key in the Codex execution environment.

Required shape:

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

Use 007 when:

```text
- the priority is observing Codex as a file-editing agent
- stronger repository-visibility boundary evidence is needed
- Docker and runtime complexity are acceptable
- diagnostics are more important than operational simplicity
```

Use a future 008 when:

```text
- a selected prompt packet must be mounted into the container as /task:ro
- policy snapshots should be available to Codex without mounting the repository root
- API key presence should be removed before codex exec
```

## Promotion rule for 007

007 should not replace 005 after only one success.

Promotion condition:

```text
Promote 007 from candidate to standard agent path after at least 2 consecutive successful full 007 runs under the same fixed conditions, with matching policy diagnostics.
```

A repeated 007 success should include:

```text
- Codex exit code 0
- container exit code 0
- final changed files subset of lab/index.html, lab/style.css, lab/app.js
- repository root not mounted into the container work directory
- container-visible work files limited to the prepared lab files plus expected runtime files
- policy-denied-access empty or explained
- safety-check PASS
- static-site-check PASS
- manual PR review and merge
```

## Decision summary

```text
005 is the stable implementation path.
007 is the stronger agent-boundary candidate.
008 should be the selected-prompt packet experiment.
```

Do not collapse prompt selection and execution. Prompt Vote Lab chooses the prompt first; 005, 007, or 008 only execute it under different boundaries.
