# Experiment 065 — CPU-work-coupled K8 audit

## Motivation

Experiments 059–064 measured access cost, but the substrate itself was still granted a fixed **number of events**. A depth-2 closure and a depth-6 closure therefore had the same physical opportunity to execute.

This experiment makes finite CPU work part of the dynamics.

## Physical change

Replace the fixed event count with a fixed work budget.

- candidate starts are scanned sequentially;
- every prefix window read consumes one unit;
- every rewritten window consumes one unit;
- execution stops when the work budget is exhausted;
- there is no reward, utility, learner, or retained scheduler state.

Thus short closures can physically receive more execution opportunities within the same CPU budget.

## Result

Key width 3, 16 backgrounds:

- work budget 24: matching cheaper **33**, mismatching cheaper **26**
- work budget 48: matching **38**, mismatching **37**
- work budget 96: matching **38**, mismatching **20**
- strict A/B cross-over: **0** for all three budgets

A 32-background confirmation at work budget 96 gave:

- A-probe: matching **47**, mismatching **24**, equal **90**
- B-probe: matching **34**, mismatching **32**, equal **46**
- total non-tied: matching **81**, mismatching **56**
- strict cross-over: **0**

The apparent aggregate tilt is not uniform across complement pairs. At the same 32-background condition, match/mismatch totals by the four A representatives were approximately:

- `000`: 16 / 13
- `001`: 13 / 14
- `010`: 18 / 16
- `011`: 34 / 13

So much of the aggregate effect is concentrated in one value family rather than being a generic experience-specific effect.

## Interpretation

Making computational cost physically consequential is conceptually cleaner than treating access cost as a pure observer metric, but **resource coupling alone does not produce robust experience-specific compilation** in K8.

The weak aggregate bias at high budget is insufficient because:

- no strict pairwise cross-over appears;
- the effect is strongly value-family dependent;
- a parameter sweep over work budgets would make post-hoc selection easy.

The next audit therefore shifts from repetition to consequences of perturbation and recovery, while retaining an operational rather than purely bit-state readout.
