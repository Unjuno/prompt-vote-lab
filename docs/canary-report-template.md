# Canary report template

## Metadata

```text
week:
prompt_issue:
implementation_pr:
model: gpt-5-nano
attempts: 1
```

## Input prompt

```
<prompt text>
```

## Output summary

```text
What changed:

Files touched:

Diff size:
```

## Safety checks

```text
static-site-check: PASS/FAIL
safety-check: PASS/FAIL
```

## Evaluation

```text
Outcome: PASS / PARTIAL / FAIL / UNSAFE / UNCERTAIN
Reason:

Hit / Partial / Misread / Overbuild / Underbuild / Unsafe / Unknown
```

## Observations

```text
- what worked
- what failed
- unexpected behavior
```

## Decision

```text
STOP / CONTINUE
```

## Next step (if CONTINUE)

```text
explicit next instruction
```
