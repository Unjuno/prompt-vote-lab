# Canary log policy

This document defines what canary runs should collect, publish, and withhold.

The goal is to make the experiment useful as a prompt-design game: users inspect run evidence, identify failure modes, and design the next prompt or runner variant. The logging policy must therefore preserve useful failure evidence without leaking secrets or raw private reasoning.

## Scope

This policy applies to Codex canaries and future implementation-agent canaries.

It does not change model, prompt, retry, fallback, sandbox, or file-scope conditions for an existing canary ID.

## Principle

```text
Collect thick internal artifacts.
Publish only redacted durable summaries.
Never publish secrets, raw environment dumps, or raw private chain-of-thought.
```

Tool failures are valuable evidence and should be preserved internally. A failed file-write, failed command, sandbox error, or malformed output can be more useful than a successful run when designing the next prompt.

## Required internal artifacts

When available, each canary run should upload an internal artifact bundle containing:

```text
codex-events.jsonl
codex-last-message.txt
codex-stderr.txt
codex-stdout.txt
git-status-before.txt
git-status-after.txt
git-diff-name-only.txt
git-diff-stat.txt
git-diff.patch
file-hashes-before.json
file-hashes-after.json
check-results.json
failure-summary.json
artifact-manifest.json
```

If a file is unavailable, the artifact manifest should record it as missing instead of silently omitting it.

## Useful failure evidence

The following evidence is explicitly useful and should be kept in the internal artifact bundle when available:

```text
tool error excerpts
sandbox errors
command exit codes
failed file paths
failed write/read operation summaries
invalid JSON or invalid patch summaries
check failure summaries
changed-file guard output
```

Known useful example:

```text
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
Failed to read file to update lab/index.html
Failed to write file /tmp/pvll_test_codex.txt
```

This kind of evidence showed that a previous `no changes` result was not model refusal; Codex reached the edit step but the local sandbox helper failed.

## Public run log

The durable public log may include:

```text
canary_id
status
model
fixed_parameter_summary
runner_mode
sandbox_mode
visible_files
allowed_final_changed_files
changed_files
diff_stat
file_hashes_before_after
check_results
failure_step
failure_type
redacted_error_summary
artifact_names
workflow_run_number
branch
base_sha
pr_number_if_created
```

The public log should summarize raw errors, not dump full raw logs.

## Forbidden public content

Do not publish:

```text
API keys
repository secrets
raw environment variables
raw private chain-of-thought
unreviewed raw Codex JSONL
unreviewed raw stderr
unreviewed raw stdout
full prompt if it contains operational secrets
full file contents unless manually reviewed
private tokens
```

## Raw private reasoning policy

Raw private chain-of-thought is not a canary artifact.

Allowed substitutes:

```text
rationale summary
action summary
changed-file explanation
declared non-changes
constraint checklist
```

The prompt may ask Codex for a short rationale summary, but it must not ask for raw hidden reasoning.

## Failure taxonomy

Use the following failure types where possible:

```text
auth_failure
model_access_failure
prompt_delivery_failure
sandbox_failure
no_changes
invalid_json
invalid_patch
forbidden_changed_file
safety_check_failure
static_site_check_failure
pr_creation_failure
artifact_upload_failure
unknown_failure
```

## Prompt-design game loop

The intended loop is:

```text
1. Run one fixed canary attempt.
2. Save thick internal artifacts.
3. Publish a redacted summary.
4. User inspects artifacts.
5. User designs the next prompt or a new canary variant.
6. If any fixed parameter changes, use a new canary ID.
```

Do not silently mutate an existing canary ID to make it pass.

## Minimum acceptance for a canary run

A canary run is not useful unless it records at least:

```text
status
canary_id
model
runner_mode
failure_step or success_step
changed_files or explicit no_changes
check_results or check_not_reached
artifact_manifest
```

## Diagnostics collector status

A common diagnostics collector exists:

```text
scripts/collect_canary_diagnostics.py
```

It should favor collecting evidence over hiding failures, while keeping the public/private boundary intact.

Future work should consolidate common schema expectations across canary families and the canonical selected-prompt runner without rewriting historical evidence labels.