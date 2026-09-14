# Experiment 064 — minimal retention asymmetry audit

## Question

Experiment 063 showed that K8 history dependence is not experience-selective. Can one small, semantics-free retention asymmetry make repeated experience selectively cheaper?

Three generic physical variants were checked without reward, labels, counters, or a learner:

1. **field trace** — after an event, write the raw collective field `T` into the next unused aligned window;
2. **generic copy** — copy the first event output into the next unused window;
3. **recurrence-gated copy** — copy the first input only when the same value already occurs at least twice in the current self-delimited event.

All variants use the same Experiment-063 query: repeated A versus repeated B, then compare closure cost for the same A or B probe only when the operational transformation identity `(first value, T)` matches across histories.

## Result

16 backgrounds, key width 3:

### raw field trace

- matching experience cheaper: **36**
- mismatching experience cheaper: **37**
- strict A/B cross-over: **0**

### generic copy

- matching experience cheaper: **27**
- mismatching experience cheaper: **21**
- strict cross-over: **0**

A 32-background confirmation of generic copy gave **58 matching vs 45 mismatching**, still with **0 strict cross-over**. The imbalance is weak and not uniform across complement pairs.

### recurrence-gated copy

- matching experience cheaper: **28**
- mismatching experience cheaper: **25**
- strict cross-over: **0**

Key width 4 was too sparse to provide stronger evidence.

## Interpretation

These are negative results.

Simply leaving a trace, copying what was used, or conditionally copying a locally repeated value does not robustly turn K8 into an experience-specific compiler.

The project should not tune arbitrary trace formulas until one happens to work. The stronger missing issue is that **access cost is still mostly an observer metric rather than a consequence that controls continuation of the substrate itself**.

This motivates a separate resource/consequence audit rather than more retention-formula search.
