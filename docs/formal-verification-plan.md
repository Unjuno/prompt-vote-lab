# Formal Verification Plan

## Purpose

Prompt Vote Lab can use Lean to verify small decision procedures used by the experiment.

Formal verification is not a substitute for system logs, API logs, or maintainer review. It only verifies defined logic under explicit assumptions.

## What Lean can verify

Lean can verify:

- the selection predicate matches the written rule
- `selected` implies both threshold conditions
- `no_run` follows when either threshold condition fails
- top-three extraction preserves sorted order under a defined comparator
- tie-breaking is deterministic
- snapshot decision fields are consistent with candidate votes

## What Lean cannot verify

Lean cannot verify:

- GitHub returned complete reaction data
- public reactions reflect sincere preferences
- the AI-generated UI is useful
- HN readers will respond well
- a model provider will keep behavior unchanged
- a workflow runner will never fail

These require operational logs and review, not proof alone.

## Core variables

| Symbol | Meaning | Unit | Definition | Domain | Type |
|---|---|---:|---|---|---|
| `v_i` | votes for prompt `i` | votes | public `+1` reaction count | natural number | scalar |
| `B` | no-change baseline | votes | initial value `5` | natural number | scalar |
| `M` | required margin | votes | initial value `2` | natural number | scalar |
| `T` | minimum total votes | votes | initial value `5` | natural number | scalar |
| `V` | total votes | votes | sum of candidate votes | natural number | scalar |
| `v_max` | top prompt votes | votes | maximum candidate vote count | natural number | scalar |
| `S` | selected decision | none | Boolean predicate | true/false | proposition |

## Selection rule

```text
S iff (v_max >= B + M) and (V >= T)
```

Unit check:

```text
v_max: votes
B + M: votes + votes = votes
v_max >= B + M compares votes with votes

V: votes
T: votes
V >= T compares votes with votes
```

## Minimal Lean target

```lean
namespace PromptVoteLab

def selected
  (topVotes baseline margin totalVotes minTotal : Nat) : Bool :=
  topVotes >= baseline + margin && totalVotes >= minTotal

theorem selected_true_iff
  (topVotes baseline margin totalVotes minTotal : Nat) :
  selected topVotes baseline margin totalVotes minTotal = true ↔
    topVotes >= baseline + margin ∧ totalVotes >= minTotal := by
  unfold selected
  simp

end PromptVoteLab
```

## Top-three verification target

Define a candidate as:

```lean
structure Candidate where
  issue : Nat
  votes : Nat
```

Comparator policy:

1. higher votes rank first
2. lower issue number wins ties

Target properties:

- sorted output is ordered by comparator
- top-three length is at most three
- if input is non-empty, first output element is maximal under comparator
- equal input data produces equal output data

## Snapshot consistency target

Given a generated snapshot:

- `top_prompt_votes` must equal the first top prompt vote count
- `selected_issue` must equal the first top prompt issue when `decision = selected`
- `selected_issue` must be absent/null when `decision = no_run`
- `decision = selected` iff selection rule is true

## Proof boundary

The proof assumes the input candidate list is already parsed correctly.

Parsing JSON, calling GitHub APIs, and writing files are outside the Lean proof boundary.

## Implementation path

Recommended future files:

```text
formal/PromptVoteLab/Selection.lean
formal/PromptVoteLab/Ranking.lean
formal/PromptVoteLab/Snapshot.lean
formal/lakefile.lean
```

## Validation path

Run proof checks before real API execution:

```text
lake build
```

The repository should not require Lean for ordinary static UI edits, but formal checks should run for changes to selection or snapshot logic.
