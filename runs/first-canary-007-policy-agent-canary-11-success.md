# first-canary-007 policy-agent canary 11 success

## Status

PASS, evidence-only.

## Fixed conditions

```text
canary_id: first-canary-007
run_number: 11
source_issue: none / issue_number=0
result_pr: #272 Run Codex policy-enforced agent canary
runner: codex-cli-policy-enforced-agent-container
model: gpt-5.4-nano
attempts_per_candidate: 1
retry_policy: none
fallback_policy: none
auto_merge_policy: disabled
sandbox_mode: docker-mounted-workdir-only
execution_mode: policy-enforced Codex CLI agent direct edit
container_work_root: /work
container_runtime_root: /codex-runtime
diagnostics_root: /diagnostics
repo_root_mounted: false
visible_work_files: lab/index.html, lab/style.css, lab/app.js
final_writable_files: lab/index.html, lab/style.css, lab/app.js
manual_review: required
```

## Purpose

This canary verified the current canonical Docker/Codex implementation-agent path after the public evidence pipeline was hardened.

It specifically checked that the policy-agent workflow can proceed through:

```text
Codex container execution
-> changed-file guard
-> safety-check
-> static-site-check
-> public bundle build
-> public bundle enrichment
-> public bundle verifier
-> public bundle Gitleaks scan
-> public bundle upload
-> uploaded bundle download
-> uploaded bundle verifier
-> uploaded bundle Gitleaks scan
-> diagnostics upload
-> public log upload
-> PR creation
```

This canary did not test automatic vote-winner selection.

## Observed result

The workflow completed far enough to create PR #272.

```text
PR: #272 Run Codex policy-enforced agent canary
branch: codex-policy-agent-canary-007-11
head_sha: ff170d5372fb87088ad805547e888e673fcc9c40
base_sha: 062e20bc8d6a06223c29a59e552608f0b60dcfc1
changed_files: lab/index.html
additions: 2
deletions: 0
mergeable: true
```

The PR body records these public evidence artifacts:

```text
codex-policy-agent-canary-public-bundle-11
codex-policy-agent-canary-diagnostics-11
codex-policy-agent-canary-public-log-11
```

The PR body also records these diagnostics reports as expected inside the diagnostics artifact:

```text
public-agent-run-bundle-verification.json
public-agent-run-bundle-gitleaks.json
public-agent-run-bundle-uploaded-verification.json
public-agent-run-bundle-uploaded-gitleaks.json
```

## Implemented lab result

The Codex run made a minimal canary-marker edit to `lab/index.html`.

```text
- added a meta tag: codex-canary=seventh-bounded-codex-implementation-agent-canary-7
- added a visible pill: Bounded Codex implementation-agent canary #7
```

This visible lab diff is not adopted as a product feature by this run record. It is only evidence that the canonical policy-agent path can create a constrained PR after the hardened public evidence checks.

## Diagnostics summary

The workflow reached PR creation after the following gates, because those gates occur before the PR creation step:

```text
policy-enforced container runner completed
changed-file guard passed
safety-check passed
static-site-check passed
public bundle pre-upload verifier passed
public bundle pre-upload Gitleaks scan passed
uploaded public bundle verifier passed
uploaded public bundle Gitleaks scan passed
```

The preceding failed run #10 failed at `verify_public_agent_run_bundle.py` because the custom OpenAI-key regex treated the ordinary path-like string `task-static-ui-v1.0.md` as an `sk-*` token. PR #271 fixed that false positive by requiring `sk-` not to be preceded by an alphanumeric character.

## Access-log interpretation

This record does not claim a full OS-level file access audit.

The relevant evidence is the workflow/container boundary and public diagnostics pipeline:

```text
- repository root is not mounted into the Codex editing container
- only the prepared `/work` directory is mounted read/write
- `/work` contains only the allowed lab files
- final copyback is restricted to lab/index.html, lab/style.css, lab/app.js
- public bundle evidence is sanitized, verified, scanned, uploaded, downloaded, and verified/scanned again
```

## Checks passed

```text
policy-enforced container runner completed before PR creation
changed-file guard passed before PR creation
safety-check passed before PR creation
static-site-check passed before PR creation
public bundle content verification passed before PR creation
public bundle Gitleaks scan passed before PR creation
uploaded public bundle verification passed before PR creation
uploaded public bundle Gitleaks scan passed before PR creation
```

## Interpretation

This is the first successful `first-canary-007` run after the evidence pipeline added:

```text
- observation-summary.md/json
- sanitized/ public diagnostics
- reasoning-traces/ public traces
- public bundle verifier
- uploaded artifact re-download verifier
- Gitleaks scan before upload
- Gitleaks scan after artifact download
- actionlint-protected workflow checks
```

The successful run supports these claims:

```text
- The canonical Docker/Codex policy-agent path can still create a PR under current main.
- The public evidence bundle can pass the custom verifier after the false-positive fix.
- The generated public bundle can pass Gitleaks scanning.
- The uploaded-and-downloaded artifact can pass the same verifier and Gitleaks scan before diagnostics upload and PR creation.
```

## Not proven

This single run does not prove:

```text
- automatic vote-winner selection
- repeated-run stability
- fixed GitHub Issue ingestion
- hostile prompt-injection resistance
- full OS-level file access tracing
- long-term artifact availability after retention expiry
- that the canary-marker UI diff should be merged into the live lab
```

## Current classification

```text
first-canary-007: canonical Docker/Codex policy-agent path verified after public bundle hardening
first-canary-009: successful fixed GitHub Issue instruction-packet agent candidate
weekly-auto-run: still not migrated to canonical Docker/Codex path
```

## Recommended next step

Treat PR #272 as evidence-only unless there is a specific reason to adopt the visible canary marker into `main`.

Then proceed to the next production-hardening step:

```text
1. Close or annotate #272 as evidence-only.
2. Migrate weekly-auto-run away from the legacy Python SDK implementation path only after deciding the fixed Issue / selected prompt ingestion route.
3. Run a fixed-Issue or selected-prompt canary through the same public bundle verifier + Gitleaks pipeline.
```
