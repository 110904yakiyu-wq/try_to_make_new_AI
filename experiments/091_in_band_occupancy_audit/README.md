# Experiment 091 — in-band causal occupancy audit

## Question

Experiment 090 showed that parallel K8 sits between two bad symmetric extremes:

- compose all overlapping rewrite demands -> high churn;
- reject contested demands -> frozen medium.

Can temporary execution rights be represented in the same raw ring without owner IDs, priority tables, or a scheduler-side memory?

## Variant A: active raw claims

For every current K8 candidate, compute a width-bit fingerprint from its own current closure:

`fingerprint = rotl(field XOR first_value XOR arity)`.

The candidate writes that fingerprint into the immediately preceding width-bit window as an in-band claim. If the old preceding window already equals the fingerprint, the candidate may also execute its K8 rewrite.

All claim and rewrite deltas are XOR-composed. There is no external owner table.

### Result

The claim traffic becomes another source of churn.

For width 4, 16 seeds, 200 sweeps:

- candidate events/sweep: **22.23**;
- executed events/sweep: **1.36**;
- changed bits/sweep: **21.30 / 48**;
- operational-role Jaccard: **0.025**.

This is essentially the same churn regime as parallel K8.

## Variant B: passive self-token gating

To remove claim traffic, a candidate executes only when the preceding raw window already equals its current fingerprint. A successful event writes the same fingerprint immediately after its closure, so execution can in principle propagate its own temporary token.

No candidate writes a claim unless it actually executes.

### Result

Churn disappears, but activity does not self-sustain.

Across 32 random seeds and 500 sweeps:

- width 3: 31/32 seeds execute at least once, **0/32** remain active in the final 50 sweeps;
- width 4: 27/32 execute at least once, **0/32** remain active;
- width 5: 17/32 execute at least once, **0/32** remain active.

Mean executions per sweep fall to 0.083, 0.010, and 0.002 respectively.

## Interpretation

Putting occupancy state into the same medium is not by itself sufficient.

Two minimal implementations reproduce the earlier freeze/churn tension:

- continuously writing claims turns arbitration itself into high-density traffic;
- requiring an exact in-band handshake makes causal chains too brittle to reproduce themselves.

The result argues against adding a tuned handshake threshold or privileged token symbol.

More importantly, it exposes another hidden assumption in K8: a closure can read a long prefix atomically. Before adding richer occupancy machinery, that nonlocal atomic read should be audited directly.
