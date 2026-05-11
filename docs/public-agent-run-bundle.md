# Public agent run bundle

## Purpose

Prompt Vote Lab is an experiment where prompts influence agent behavior.

Participants need inspectable behavior evidence, not only final results.

The public agent run bundle exposes:

```text
redacted raw evidence
sanitized diagnostic logs
sanitized reasoning / CoT-like trace artifacts
agent observation summaries
reasoning-to-behavior hypotheses
```

for canonical Docker/Codex policy-agent runs and fixed-Issue agent runs.

## Core rule

```text
Primary evidence: redacted raw files, sanitized logs, and sanitized exposed reasoning traces
Secondary evidence: observation summary, reasoning-to-behavior hypotheses, index, and manifest
Model-written summary: not primary evidence
```

Do not replace raw evidence with a model-written summary.

Summaries can hide failure modes, reflect prompt or model bias, and make participants miss important behavior.

If a run artifact exposes reasoning / CoT-like trace text, Prompt Vote Lab treats that trace as experimental evidence after sanitizer replacement.

## What is published as raw evidence

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

## What is published as sanitized diagnostics

Some logs are useful for prompt improvement but too noisy or risky to publish as raw evidence. These are published after sanitizer replacement under `sanitized/`.

Examples:

```text
sanitized/codex-login-stdout.txt
sanitized/codex-login-stderr.txt
sanitized/codex-stderr.txt
sanitized/codex-stdout.txt
sanitized/policy-agent-container-stdout.txt
sanitized/policy-agent-container-stderr.txt
sanitized/issue-instruction-container-stdout.txt
sanitized/issue-instruction-container-stderr.txt
sanitized/npm-install-codex.txt
sanitized/npm-install-codex-stderr.txt
sanitized/policy-container-mounts.txt
sanitized/container-runtime-files-after.txt
sanitized/container-runtime-dirs-before.txt
```

The sanitizer replaces token-like, environment-like, and path-like strings before publication.

Examples:

```text
[REDACTED_SECRET]
[REDACTED_RUNNER_WORKDIR]
[REDACTED_RUNNER_TEMP]
[REDACTED_TMP_PATH]
[REDACTED_GITHUB_WORKSPACE]
```

Sanitization is a best-effort publication guard. If a real token is discovered in a public artifact, rotate it and treat it as an incident.

## What is published as reasoning / CoT-like trace evidence

If the run creates reasoning-like artifacts that are visible to the workflow, they are published after sanitizer replacement under `reasoning-traces/`.

Examples:

```text
reasoning-traces/codex-events.jsonl
reasoning-traces/codex-last-message.txt
reasoning-traces/codex-stdout.txt
reasoning-traces/codex-stderr.txt
reasoning-traces/policy-agent-container-stdout.txt
reasoning-traces/policy-agent-container-stderr.txt
reasoning-traces/issue-instruction-container-stdout.txt
reasoning-traces/issue-instruction-container-stderr.txt
```

This is not a proxy-only policy. Exposed reasoning / CoT-like traces are evaluation targets.

If provider-private reasoning exists but is not exposed to the workflow, the bundle records:

```text
unexposed_provider_private_cot_available = unknown
unexposed_provider_private_cot_published = false
```

The project does not pretend unavailable provider-private internals are observable. It does publish exposed reasoning traces that exist in run artifacts.

## Agent observation summary

The enriched bundle contains:

```text
observation-summary.md
observation-summary.json
```

These files summarize:

```text
path model
/work, /task, and /codex-runtime roles
whether the repository root was mounted
visible files before and after
changed files
copied-back files
additions and deletions by file
hashes before and after
sanitized logs and redaction counts
reasoning-traces/ files and redaction counts
reasoning-like term counts
reasoning-to-behavior hypotheses
agent final action summary
known evidence limits
```

The observation summary is a navigation index over evidence. It does not replace the published reasoning traces.

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

## Redaction

The builder and enrichment step redact common secret-like patterns before publishing allowlisted, sanitized, or reasoning-trace files.

Examples:

```text
OpenAI-style secret keys
GitHub token-like strings
GitHub fine-grained personal access token-like strings
Authorization bearer tokens
OPENAI_API_KEY assignments
GITHUB_TOKEN assignments
GH_TOKEN assignments
runner workspace paths
temporary directory paths
GitHub workspace paths
```

Redaction is a safety net, not a proof that all secrets are impossible.

## Bundle structure

Each enriched bundle contains:

```text
index.json
README.md
observation-summary.md
observation-summary.json
raw/<allowlisted-file>
sanitized/<sanitized-file>
reasoning-traces/<sanitized-reasoning-trace-file>
```

`index.json` is a manifest and quick index. It is not a replacement for `raw/`, `sanitized/`, or `reasoning-traces/`.

`README.md` is a human navigation file. It is not an interpretation layer.

## 007 policy-agent workflow integration

The canonical policy-agent workflow builds and enriches the bundle after diagnostics collection:

```text
Collect diagnostics artifact
→ Build redacted public agent run bundle
→ Enrich public agent run bundle with sanitized logs and reasoning traces
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
what reasoning / CoT-like traces were exposed
whether reasoning traces mention copy, interaction, style, or scope terms
what stdout/stderr/install logs looked like after sanitization
whether runtime scan was clear/blocked/review
whether the execution gate allowed or stopped the run
which source Issue generated the task packet
```

The project does not automatically explain or score these observations as truth. It records hypotheses for participant review.

## Non-goals

Do not publish these without sanitizer or separate review:

```text
unsanitized raw Actions logs
unsanitized raw container stderr
unsanitized login stdout/stderr
unsanitized full package-manager install logs
unredacted exposed reasoning traces
secrets
private data
payment identifiers
automatic prompt advice
model-written causal explanation as primary evidence
```

Provider-private reasoning that is not exposed to the workflow is not claimed to be available.

## Schema

Current raw bundle schema:

```text
prompt-vote-lab-public-agent-run-bundle-v1
```

Current observation summary schema:

```text
prompt-vote-lab-agent-observation-summary-v1
```

Breaking changes should use a new schema version.
