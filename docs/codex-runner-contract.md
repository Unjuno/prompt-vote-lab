# Codex runner contract

This document defines the Codex-based implementation-agent path.

## Current correction

The previous first canary used the OpenAI Responses API through `scripts/openai_lab_run.py` with `gpt-5-nano` and full-file JSON output.

That was not a Codex run.

It verified that the API secret and preflight path could reach a model call, but it did not verify the intended Codex implementation-agent path.

## Target runner

Use Codex CLI as the implementation agent.

Rationale:

- Codex is a coding agent, not only a text-to-JSON generator.
- The experiment should test coding-agent behavior under repository constraints.
- The runner should not force a custom patch DSL unless the experiment explicitly tests DSL-following.

## Fixed canary conditions

The first Codex canary is a controlled experiment. Do not change model or run parameters while debugging execution-path failures.

Fixed values:

```text
model: gpt-5.4-nano
candidate_rank: 1
issue_number: 0
vote_count: 0
week: first-canary-001
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
allowed_changed_files: lab/index.html, lab/style.css, lab/app.js
prompt_source: scripts/create_first_canary_candidate.py + inline workflow prompt
manual_review_required: true
```

Explicitly forbidden during this canary:

```text
changing the model
changing temperature or sampling parameters
adding fallback models
adding retries
changing the fixed prompt goal
expanding writable file scope
switching to a stronger model to make the run pass
accepting a run that changes non-lab files
```

Allowed changes while the runner is failing:

```text
fix Codex CLI argument syntax
fix authentication plumbing
fix stdin/prompt delivery
fix shell quoting
fix local diagnostic logging
fix changed-file detection
fix public redacted log generation
```

If a parameter must change, create a new canary ID instead of mutating `first-canary-001`.

## Required invariants

The Codex runner must preserve these invariants:

```text
attempts per candidate: 1
SDK/API retry: 0 or disabled by wrapper
fallback model: none
auto-merge: disabled
allowed changed files: lab/index.html, lab/style.css, lab/app.js
internal checks before PR: safety-check + static-site-check + changed-file guard
manual review before merge
```

## First step before paid Codex canary

Before running a paid Codex canary, run an API-free Codex CLI smoke workflow that only verifies:

```text
Codex package can be installed
codex binary is available
codex --version works
codex exec help text is reachable
```

This smoke workflow must not set `OPENAI_API_KEY` and must not run a prompt.

## Public log boundary

Public logs must contain experiment evidence, not raw secrets or raw model output.

Allowed public fields:

```text
provider
runner
model or configured model label
workflow
run_number
base_sha
branch
candidate_rank
issue_number
vote_count
attempt_count
retry_policy
fallback_policy
auto_merge_policy
max_output_tokens or Codex output budget label
changed_files
check_results
exit_code
failure_step
failure_type
redacted_error_summary
```

Forbidden public fields:

```text
API keys
raw environment
raw stderr
raw Codex rollout JSONL
full model output
full prompt if it contains private or operational secrets
unredacted stack traces
```

The raw GitHub Actions log may exist as an internal execution artifact, but the repository's durable public evidence should use redacted summaries.

## Codex logs

Codex CLI can create local session logs. Those logs are not automatically public evidence.

If used, publish only a redacted summary, hash, and file list unless the raw log has been manually reviewed.

## Stop rule

If the Codex runner cannot produce one lab-only PR with internal checks passing, stop and record the failure.

Do not fall back to `scripts/openai_lab_run.py` in the same run.
