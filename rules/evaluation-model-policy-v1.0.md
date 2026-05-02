# evaluation-model-policy-v1.0

## Purpose

This policy separates the implementation model from the evaluation and blog-writing model.

Prompt Vote Lab evaluates prompt candidates under a fixed implementation condition. The model used to implement `lab/` should remain fixed during a comparison period.

The blog and evaluation model may be stronger, because it does not change the implementation result. It only analyzes the recorded outcome.

## Implementation model

The implementation model is used to modify:

- `lab/index.html`
- `lab/style.css`
- `lab/app.js`

The implementation model must be fixed for rank-1, rank-2, and rank-3 candidates in the same weekly vote.

This keeps the prompt comparison fair.

## Evaluation model

The evaluation model is used for:

- weekly analysis drafts
- expectation-gap classification assistance
- Hacker News summary drafts
- comparison notes between rank-1, rank-2, and rank-3
- rule-change recommendations

The evaluation model may be stronger than the implementation model.

## Boundary

The evaluation model must not modify `lab/`.

The evaluation model must not decide merge automatically.

The evaluation model may suggest classifications, but the maintainer makes the final decision.

## Required inputs for evaluation

Use only recorded project data:

- selected prompt
- candidate rank
- vote count
- implementation PR
- changed files
- diff summary
- safety-check result
- maintainer decision
- reviewer notes
- run log

If data is missing, write `unrecorded`.

Do not invent missing facts.

## Model changes

The evaluation model should also be versioned.

If the evaluation model changes, record it in the weekly log.

Example:

```text
implementation_model_policy: model-policy-v1.0
evaluation_model_policy: evaluation-model-policy-v1.0
implementation_model: low-cost fixed model
evaluation_model: stronger analysis model
```

## Rationale

Using a low-cost fixed implementation model makes prompt comparison fair.

Using a stronger evaluation model improves analysis quality without changing the generated implementation.

This separates the experiment from the commentary about the experiment.
