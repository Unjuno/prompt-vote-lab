# Support policy

Support helps Prompt Vote Lab open additional comparison runs for the current weekly vote.

Support is not a purchase of success, adoption, merge, maintenance, review, support work, or specification control.

## Supported one-time tiers

- 5 USD: Support Rank 2 Comparison Run
- 10 USD: Support Rank 3 Comparison Run

There is no general support tier.

## Weekly thresholds

- rank 2 comparison run: 5 USD total weekly support
- rank 3 comparison run: 10 USD total weekly support

The 10 USD threshold is total weekly support, not 5 USD plus 10 USD.

## Scope

Support applies to the current weekly vote only.

Old weekly candidates are not automatically reopened.

Support does not create a request channel, paid review obligation, delivery promise, support obligation, merge right, or specification-control right.

## No-change baseline interaction

Support does not override the no-change baseline.

Additional comparison runs can only happen after the weekly candidate set has passed the baseline rule.

Current implementation rule:

```text
1. A virtual no-change baseline candidate is inserted into the weekly candidate set.
2. Candidates are sorted by vote count.
3. If the no-change baseline ranks first, no implementation candidates are eligible.
4. If a real prompt ranks first, the weekly candidate set has passed the baseline rule.
5. Rank 1 is then eligible for the normal weekly implementation run.
6. If weekly support is at least 5 USD, rank 2 is eligible as a support-unlocked comparison run.
7. If weekly support is at least 10 USD, rank 3 is eligible as a support-unlocked comparison run.
```

Rank 2 and rank 3 do not independently need to exceed 20 votes after the candidate set has passed the baseline rule.

Example:

```text
no-change baseline: 20 votes
rank 1 prompt: 25 votes
rank 2 prompt: 12 votes
rank 3 prompt: 8 votes
weekly support: 10 USD
eligible implementation ranks: 1, 2, 3
```

Counterexample:

```text
no-change baseline: 20 votes
rank 1 prompt: 18 votes
rank 2 prompt: 12 votes
rank 3 prompt: 8 votes
weekly support: 10 USD
eligible implementation ranks: none
```

Reason:

```text
Support unlocks additional comparison runs only after the prompt candidate set beats the no-change baseline. It does not buy an implementation run when the baseline wins.
```

## Safety

All support-unlocked runs still follow:

- static UI rules
- agent-run policy
- fixed implementation model policy
- safety checks
- PR-only implementation flow
- merge policy
- manual adoption
