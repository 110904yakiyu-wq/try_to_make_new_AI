# Experiment 021 — operational distinguishability depth

## Motivation

Experiment 020 sampled a few future delays and asked whether two histories with the same current quotient later diverged.

A closer audit found an important complication: **exact-delay distinguishability is not monotone**. Two histories may be distinguishable at delay 3, indistinguishable again at delay 4, and distinguishable later.

Therefore an exact time offset should not be confused with a bisimulation/test depth.

## Two notions

### Exact-delay relation

At delay `d`, compare the same fixed operational quotient after exactly `d` autonomous CA steps.

The printed trajectory uses:

- `=` : one-shot and repeated histories have the same quotient at that exact delay
- `!` : the quotients differ at that exact delay

This relation may split and re-merge.

### Cumulative operational depth

For a pair of histories that have the same quotient at delay 0, define the observer-side first distinguishing depth as the smallest `d > 0` for which the exact-delay quotient differs.

Equivalently, histories are cumulatively equivalent through depth `D` only when they agree at **every** delay `0..D` under this fixed assay family.

This cumulative relation is monotone by construction: once a distinguishing delay exists, increasing the allowed depth cannot erase the fact that the histories were distinguishable within budget.

## Relation to prior work

This construction is conceptually close to finite approximants of bisimulation and bounded modal/testing equivalence, where greater modal/test depth can refine an earlier behavioral equivalence.

It is **not** claimed to be a new form of bisimulation. The local assay, probe vocabulary, and autonomous-delay construction used here are specific to this toy substrate.

See `docs/001-operational-equivalence-boundary.md`.

## Result

Exact-delay re-mergence is common.

Examples:

- Rule 98, train `000`: `====!=======!===`
- Rule 98, train `001`: `==!=!=!===!=!=!=`
- Rule 113, train `000`: `!!==!!==!!==!!==`
- Rule 129, train `111`: `=======!========`

Thus the quotient trajectory itself is dynamic and should not be summarized as "once split, always split".

For the representative rule set, the first cumulative distinguishing depth ranges from 1 to 8 under the default budget. Some histories remain indistinguishable through all 16 tested delays.

Notably:

- Rule 110: all eight eligible training histories remain indistinguishable through depth 16.
- Rule 129: six of eight remain indistinguishable through depth 16; one distinguishes at depth 1 and one at depth 8.
- Rule 126: only one of eight distinguishes, at depth 1.
- Rules 14, 113, and 142: every eligible history distinguishes at depth 1.

## Interpretation

The useful object is not a permanently fixed quotient at one time. It is a **resource-indexed family of operational equivalences**.

Increasing observation depth can expose historical differences that a shallower assay cannot see. This is classical in spirit; the hobby-project question remains whether the substrate can make deeper tests available to itself rather than relying on an external observer to enlarge the test family.
