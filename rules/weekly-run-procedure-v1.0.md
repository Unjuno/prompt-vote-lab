# weekly-run-procedure-v1.0

## Purpose

This procedure defines the weekly human-in-the-loop process.

Automation may prepare implementation runs and reports. The maintainer decides whether to merge.

## 1. Collect prompts

- Prompt proposals are submitted as GitHub issues.
- Valid proposals should use the `prompt-proposal` label.
- Unsafe or out-of-scope prompts may be labeled `unsafe`, `invalid`, or `out-of-scope`.

## 2. Count votes

- Use GitHub reactions as the initial voting signal.
- The initial vote signal is advisory and public.
- Apply `rules/selection-v1.0.md` before running the agent.

## 3. Select or skip

Run the agent only if the top prompt passes:

```text
top_prompt_votes >= no_change_baseline + required_margin
```

and:

```text
total_votes >= minimum_total_votes
```

If no prompt passes, write a no-run weekly log.

## 4. Run implementation

- Start a fresh implementation session.
- Use `rules/static-ui-v1.0.md`.
- The agent may edit only `lab/`.
- The agent must create a PR. It must not push directly to `main`.

## 5. Check safety

Minimum checks:

- Only `lab/` changed.
- No external network calls.
- No cookie access.
- No `eval` or `new Function`.
- No external scripts.
- Browser display check passes.

## 6. Review result

Classify the result as one of:

- Hit
- Partial
- Misread
- Overbuild
- Underbuild
- Rule conflict
- Unsafe
- Rejected

## 7. Decide

The maintainer decides:

- merge
- close
- request revision

Result votes and reactions are advisory only.

## 8. Log

Write or update `runs/week-XXX.md` with:

- selected issue
- vote count
- selection rule
- rule profile
- changed files
- safety check
- merge/reject decision
- expectation gap
- rule change for next run
