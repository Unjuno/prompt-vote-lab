# Public agent run bundle

## Purpose

Prompt Vote Lab is an experiment where prompts influence agent behavior.

Participants need inspectable behavior evidence, not only final results.

The public agent run bundle exposes a redacted raw evidence bundle for canonical Docker/Codex policy-agent runs and fixed-Issue agent runs.

## Core rule

```text
Primary evidence: redacted raw files
Secondary evidence: index and manifest
Model-written summary: not primary evidence
```

Do not replace raw evidence with a model-written summary.

Summaries can hide failure modes, reflect prompt or model bias, and make participants miss important behavior.

## What is published

The bundle publishes allowlisted raw diagnostic files after secret-pattern redaction.

Examples:

```text
codex-events.jsonl
codex-last-message.txt
codex-exit-code.txt
policy-agent-container-exit-code.txt
policy-agent-diff.patch
policy-agent-diff-name-only.txt
policy-agent-copied-files.txt
issue-instruction-container-exit-code.txt
issue-instruction-diff.patch
issue-instruction-diff-name-only.txt
issue-instruction-copied-files.txt
git-diff.patch
git-diff-stat.txt
git-diff-name-only.txt
check-results.json
failure-summary.json
artifact-manifest.json
file-hashes-before.json
file-hashes-after.json
credential-presence-check.txt
policy-allowed-paths.json
policy-denied-access.txt
task-write-test-exit-code.txt
issue-execution-gate.json
issue-execution-gate.md
runtime-issue-safety-scan.json
runtime-issue-safety-comment.md
source-issue.raw.json
task-run-manifest.json
task-allowed-files.json
task-execution-policy.md
task-selected-issue.json
task-raw-issue-body.md
task-issue-safety-analysis.json
task-instruction-brief.md
task-selected-prompt.md
task-static-ui-v1.0.md
task-agent-run-policy-v1.0.md
task-file-hashes.json
task-visible-files.txt
task-visible-files-container.txt
task-visible-files-container-after.txt
container-visible-files-before.txt
container-visible-files-after.txt
```

The exact allowlist is enforced by `scripts/build_public_agent_run_bundle.py`.

## Why policy-agent files are included

The canonical Docker/Codex policy-agent run must publish enough evidence to let participants verify that the runner edited prepared lab files rather than the repository root.

These files provide that linkage:

```text
policy-agent-container-exit-code.txt
policy-agent-diff-name-only.txt
policy-agent-diff.patch
policy-agent-copied-files.txt
policy-allowed-paths.json
policy-denied-access.txt
container-visible-files-before.txt
container-visible-files-after.txt
```

The uploaded artifact name for this canonical policy-agent public bundle begins with:

```text
codex-policy-agent-canary-public-bundle-
```

## Why runtime scan and execution-gate files are included

The public bundle must let participants connect prompt text to execution behavior.

These files provide that linkage:

```text
source-issue.raw.json
runtime-issue-safety-scan.json
runtime-issue-safety-comment.md
issue-execution-gate.json
issue-execution-gate.md
```

Without them, a participant can see the diff and Codex events but cannot independently verify whether the Issue was clear, blocked, authorized, or stopped before execution.

## What is omitted

The bundle omits diagnostics that are more likely to contain credentials, package-manager noise, login flow details, raw stderr, or environment details.

Examples:

```text
codex-login-stdout.txt
codex-login-stderr.txt
codex-stderr.txt
codex-stdout.txt
policy-agent-container-stdout.txt
policy-agent-container-stderr.txt
issue-instruction-container-stdout.txt
issue-instruction-container-stderr.txt
npm-install-codex.txt
npm-install-codex-stderr.txt
policy-container-mounts.txt
container-runtime-files-after.txt
container-runtime-dirs-before.txt
```

These remain internal diagnostics unless a later manual review explicitly promotes a file class.

## Redaction

The builder redacts common secret-like patterns before publishing allowlisted raw files.

Examples:

```text
OpenAI-style secret keys
GitHub token-like strings
GitHub fine-grained personal access token-like strings
Authorization bearer tokens
OPENAI_API_KEY assignments
GITHUB_TOKEN assignments
GH_TOKEN assignments
```

Redaction is a safety net, not a proof that all secrets are impossible.

Therefore the allowlist remains narrow.

## Bundle structure

Each bundle contains:

```text
index.json
README.md
raw/<allowlisted-file>
```

`index.json` is a manifest and quick index. It is not a replacement for `raw/`.

`README.md` is a human navigation file. It is not an interpretation layer.

## 007 policy-agent workflow integration

The canonical policy-agent workflow builds the bundle after diagnostics collection:

```text
Collect diagnostics artifact
→ Build redacted public agent run bundle
→ Upload redacted public agent run bundle
→ Upload internal diagnostics artifact
```

The uploaded artifact name begins with:

```text
codex-policy-agent-canary-public-bundle-
```

## 009 workflow integration

The fixed-Issue 009 workflow builds the bundle after diagnostics collection:

```text
Collect diagnostics artifact
→ Build redacted public agent run bundle
→ Upload redacted public agent run bundle
```

The uploaded artifact name begins with:

```text
codex-fixed-issue-public-agent-run-bundle-
```

## Participant use

Participants can inspect the bundle to analyze:

```text
what the agent saw
what task packet was generated
which unsafe categories were detected
which files were visible
which files changed
what diff was produced
whether forbidden files changed
whether the task mount was read-only
whether the repository root was withheld from /work
what final agent message was produced
how many JSONL events were emitted
whether runtime scan was clear/blocked/review
whether the execution gate allowed or stopped the run
which source Issue generated the task packet
```

The project does not automatically explain or score these observations.

## Non-goals

Do not add these to the public bundle without a separate review:

```text
raw Actions logs
raw container stderr
raw login stdout/stderr
full package-manager install logs
secrets
private data
payment identifiers
automatic prompt advice
model-written causal explanation
```

## Schema

Current schema:

```text
prompt-vote-lab-public-agent-run-bundle-v1
```

Breaking changes should use a new schema version.
