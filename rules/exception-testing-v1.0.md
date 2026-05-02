# exception-testing-v1.0

## Purpose

Exception testing verifies that Prompt Vote Lab fails safely when inputs, generated files, or workflow state are invalid.

Mock success is not enough. The automation must also stop correctly when expected boundaries are violated.

## Required exception classes

The project should test these failure classes without calling model APIs:

- no prompt beats the no-change baseline
- implementation modifies files outside `lab/`
- implementation includes external scripts or CDN resources
- implementation uses forbidden browser APIs
- implementation produces no `lab/` changes
- public root page loses the `./lab/` link
- public root page loses the no-change baseline explanation
- support wording claims merge, adoption, or control can be bought
- terminal-state labels conflict

## Expected behavior

For unsafe implementation output:

```text
FAIL safety-check
NO merge
NO report claiming success
```

For no eligible prompt:

```text
PASS workflow
NO implementation PR
NO API call
record vote summary
```

For public documentation or LP problems:

```text
FAIL static-site-check
NO publish confidence
```

## API usage

Exception tests must not call OpenAI or any other paid model API.

## Rationale

The workflow should be trusted only after both success paths and failure paths are tested.

A system that succeeds on a happy path but fails open on exceptions is not safe enough for autonomous weekly operation.
