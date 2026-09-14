# Experiment 060 — K8 cost-context robustness and specificity

## Question

Experiment 059 found history-generated prefix contexts that causally reduce the scan depth needed to enable the same local transformation field `T`.

Is this a fragile one-history effect, or is the cost reduction carried by a reusable context pattern?

## Robustness sweep

Use the same strict comparison as Experiment 059:

- same physical start;
- same first window value;
- same shared field `T`;
- different first-closure depth;
- equal-budget histories differing only in input order.

Sweep key widths 3, 4, 5, and 6 with six-window physical capacity, 32 deterministic backgrounds, both stateless scheduler orientations, and the same event budget.

For every strict case, copy only the cheaper history's additional prefix context into the expensive history while leaving the identical first window untouched.

## Robustness result

### key width 3

- start comparisons: **27,648**
- strict cost-difference cases: **159**
- causal restoration of cheap closure: **159/159**
- one-bit break destroys restoration: **159/159**

### key width 4

- start comparisons: **36,864**
- strict cases: **34**
- causal restoration: **34/34**
- one-bit break destroys restoration: **34/34**

### key width 5

- start comparisons: **46,080**
- strict cases: **5**
- causal restoration: **5/5**
- one-bit break destroys restoration: **5/5**

### key width 6

- start comparisons: **55,296**
- strict cases: **0**

The strict effect therefore survives widths 3 through 5 in this sample, while becoming rare enough to disappear at width 6 under the current density and background budget.

## Cross-history context specificity

The stronger control asks whether the cheaper donor must be the original trajectory.

For each strict case, take prefix contexts from **other strict cases with the same cheap closure depth** and transplant them into the recipient. Separate donors into:

1. exactly the same raw context-value sequence;
2. a different raw sequence of the same length.

### key width 3

- same-signature cross-history transplants: **820**
- successful cost restoration: **820/820 = 100%**
- different-signature transplants: **7,220**
- successful restoration: **220/7,220 = 3.05%**

### key width 4

- same-signature cross-history transplants: **48**
- successful restoration: **48/48 = 100%**
- different-signature transplants: **266**
- successful restoration: **8/266 = 3.01%**

## Interpretation

The cost reduction is not best described as a trajectory-specific hidden memory.

A more precise statement is:

> history can construct a reusable local context pattern that compiles access to a fixed transformation consequence into a shorter self-delimiting scan.

The same raw context pattern transfers the same cost reduction even when it arose in another history. Randomly substituting a different same-length context almost always fails.

This strengthens the Experiment 059 chain:

`history -> context pattern -> shorter operational access path`

without introducing a cache object, weight update, explicit macro instruction, or learned rule table.

## Important boundary

Exact recurrence of the same raw context sequence is partly trivial: under fixed deterministic K8 physics, the same local prefix produces the same XOR closure behavior.

The next nontrivial question is therefore **functional degeneracy**:

> can multiple *different* raw context patterns implement the same cost-compression role?

The ~3% successful different-signature controls show that such alternatives exist. The next experiment should identify and causally test those operational equivalence classes rather than celebrating exact-pattern recurrence.
