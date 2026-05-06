# Canary 007 policy feasibility pass

## Status

PASS.

## Scope

This records the feasibility smoke result for the planned policy-enforced agent canary.

This is not the full `first-canary-007` Codex run. It only verifies whether the GitHub-hosted runner can support the isolation primitives needed for a full 007 implementation.

## Workflow

```text
Canary 007 Policy Feasibility
```

## Observed summary

The uploaded feasibility artifact reported:

```json
{
  "container_write_test": true,
  "docker_available": true,
  "isolated_mount_has_lab_files": true,
  "recommendation": "Implement full 007 only after reviewing this artifact.",
  "strace_status": "strace_available=true",
  "unexpected_repo_paths_visible": false
}
```

## Container-visible files

The container saw the mounted isolated work directory and not the repository root.

Observed visible files:

```text
/work/container-id.txt
/work/container-write-test.txt
/work/lab/app.js
/work/lab/index.html
/work/lab/style.css
```

## Interpretation

The feasibility smoke supports proceeding to a full policy-enforced agent implementation.

Supported claims:

```text
- Docker is available on GitHub-hosted ubuntu-latest for this workflow.
- A container can run with a limited bind mount containing only prepared lab files.
- The mounted work directory is writable when the container runs as the host runner UID/GID.
- The repository root is not visible inside the container-mounted work directory.
- Host-side strace is available for file-access tracing experiments.
```

## Not yet proven

This smoke does not prove the following:

```text
- Codex CLI can run inside the container.
- Codex API communication works from the container.
- Codex file access can be fully traced inside the container.
- Network policy can be narrowed to only required API endpoints.
```

## Next valid step

Implement the full 007 workflow as a new canary:

```text
first-canary-007-policy-enforced-agent
```

Required design direction:

```text
- Run Codex inside a container.
- Mount only a prepared /work directory containing lab/index.html, lab/style.css, and lab/app.js.
- Do not mount the repository root into the container.
- Copy back only allowed files from /work/lab after the run.
- Upload diagnostics for mounts, file access, Codex events, stderr/stdout, diffs, and copied-back files.
- Keep manual review and auto-merge disabled.
```

## Rejected option

```text
Do not treat first-canary-006 as policy-enforced. It observed agent behavior, but did not enforce an OS-level repository access boundary.
```
