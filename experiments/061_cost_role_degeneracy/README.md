# Experiment 061 — operational degeneracy of cost-compressing contexts

## Question

Experiment 060 showed that the same raw prefix-context pattern can reappear in another history and reproduce the same closure-cost reduction.

That exact-pattern result is partly trivial under deterministic K8 physics. A stronger question is:

> can *different* raw context patterns implement the same effective cost-compression role?

## Effective role

For a strict Experiment-059/060 case, define the observer-side role

`R = (first window value, shared field T, cheap closure depth)`.

Two contexts occupy the same role when they enable the same first-member transformation field after the same scan depth, even if the remaining raw prefix values are different.

This is an operational quotient, not a symbol stored by the substrate.

## Natural degeneracy

Using the Experiment-060 sweep with 32 deterministic backgrounds:

### key width 3

- strict cost-difference cases: **159**
- unique effective roles: **43**
- roles realized by multiple distinct raw signatures: **17/43**
- unique raw signatures: **78**
- maximum distinct raw signatures for one role: **7**

Role multiplicities:

- 26 roles have 1 raw signature
- 7 have 2
- 6 have 3
- 2 have 4
- 1 has 5
- 1 has 7

### key width 4

- strict cases: **34**
- unique effective roles: **22**
- multi-signature roles: **2/22**
- unique raw signatures: **25**
- maximum signatures per role: **3**

### key width 5

- strict cases: **5**
- unique effective roles: **5**
- multi-signature roles: **0** under this sample

As closure density decreases, naturally observed degeneracy also becomes rarer.

## Causal interchangeability test

For every recipient strict case, transplant a context from another case.

Two controls are separated:

1. **different raw signature, same effective role**;
2. **same closure depth, different effective role**.

### key width 3

- different-signature / same-role transplants: **220**
- successful restoration of recipient target role: **220/220 = 100%**
- same-depth / different-role transplants: **7,000**
- successful restoration: **0/7,000**

### key width 4

- different-signature / same-role transplants: **8**
- successful restoration: **8/8 = 100%**
- same-depth / different-role transplants: **258**
- successful restoration: **0/258**

### key width 5

No naturally observed alternative signature exists for the same role in this sample. The same-depth/different-role control succeeds **0/20** times.

## Interpretation

The useful result is not that the substrate contains symbols or explicit macros.

It is that multiple micro-contexts can fall into the same observer-defined operational equivalence class:

`different raw prefix -> same (first value, T, closure depth)`.

Those distinct micro-contexts are causally interchangeable for the measured access-cost role, while contexts from another role at the same depth are not.

This provides a concrete toy example of **many physical realizations, one effective accelerator role**.

It also weakens the temptation to identify cognition with one privileged internal representation. The effective role is an equivalence class induced by what the contexts make possible under a finite scan budget, not by shared bit identity.

## Boundary

The equivalence relation is observer-defined and follows directly from K8's closure/rewrite algebra once the role variables are chosen. This experiment does not show that K8 itself discovers the quotient.

The next nontrivial question is whether history changes the **accessibility landscape over these effective roles**: which accelerator classes recur, disappear, or become cheap to reconstruct during autonomous dynamics.
