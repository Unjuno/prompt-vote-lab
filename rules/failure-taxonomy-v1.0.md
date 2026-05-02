# failure-taxonomy-v1.0

This taxonomy classifies the gap between a voted prompt and the AI-implemented result.

## Labels

### Hit

The result matches the expectation and is safe to merge.

### Partial

The result is useful but incomplete.

### Misread

The agent misunderstood the prompt or optimized for the wrong goal.

### Overbuild

The agent added more UI, logic, or complexity than needed.

### Underbuild

The agent produced a result that is too weak, shallow, or incomplete.

### Rule conflict

The prompt required behavior that conflicts with the active rule profile.

Example: a prompt asks for backend behavior while `static-ui-v1.0` allows only static UI changes.

### Unsafe

The result violates a safety rule.

Examples:

- changed files outside `lab/`
- added network calls
- added cookie access
- added `eval` or `new Function`
- added external scripts

### Rejected

The result should not be merged.

This may include unsafe, broken, or irrelevant output.

## Required weekly note

Each run log should record:

- expected result before implementation
- actual result after implementation
- classification label
- reviewer note
- rule change for next run, if any
