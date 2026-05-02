# How to participate

Prompt Vote Lab uses GitHub as the public participation layer.

## Propose a prompt

Open a new prompt proposal issue:

```text
https://github.com/Unjuno/prompt-vote-lab/issues/new/choose
```

A proposal should include:

- the exact prompt
- the expected visible result
- confirmation that it fits the static `lab/` scope

## Vote

Vote with GitHub reactions on prompt proposal issues.

The default vote signal is:

```text
👍
```

Votes are treated as an advisory public ranking signal, not as a binding election.

## Review results

After a weekly run, review:

- the implementation PR
- the safety-check result
- the run log
- the blog report
- the expectation-gap classification

## Scope

The implementation model may edit only:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

The static lab page does not store submissions or votes directly.
