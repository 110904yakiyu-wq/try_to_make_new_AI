# Experiment 085 — generic replication does not internalize E3-selected p3

## Question

Experiment 084 showed that E3 plus unbiased turnover can make period-3 organization appear and persist while E3 is present, but the organization disappears when E3 is removed.

A tempting next step is generic replication: whenever the medium already contains two adjacent copies of a block, copy that block forward once more.

This experiment asks whether such non-semantic replication is enough to internalize the E3-selected organization.

## Setup

- ring size: 120 symbols
- alphabet size: 8
- initial state: pure period-2
- one unbiased symbol replacement per sweep
- E3 active for sweeps 0..299, then removed
- observer: minimal p2 / p3 coverage

Two conditions are compared:

1. baseline repetition-extension dynamics from Experiment 084;
2. the same dynamics plus a generic block-replication sweep.

The replication rule has no p2/p3 label. For every detected `B B`, it proposes another copy of `B` immediately after it. Conflicting proposals are ignored.

## Result

Across 16 seeds, using the final 100 sweeps of the E3 phase and the final 100 sweeps after E3 removal:

### Baseline

- pre-removal p2: **90.035625**
- pre-removal p3: **9.047500**
- post-removal p2: **113.074375**
- post-removal p3: **0.000000**

### Generic replication

- pre-removal p2: **104.503125**
- pre-removal p3: **0.001250**
- post-removal p2: **112.595625**
- post-removal p3: **0.000000**

## Interpretation

Generic replication not only fails to retain the E3-selected p3 organization after E3 is removed; it almost completely suppresses p3 while E3 is still present.

The conservative explanation is that replication amplifies the substrate's existing nucleation prior. Period-2 structure is already easier to form and repair, so copying whatever is already repeated reinforces p2 rather than encoding environmental consequence.

Therefore:

`generic persistence / copying != consequence-sensitive retention`

This is a negative result and should remain one.

## Next question

Can retention be coupled to an actual **disturbance -> repair** episode rather than to mere presence or repetition?

The next audit should also test whether any apparent success depends on a trace geometry accidentally tuned to the organization being measured.