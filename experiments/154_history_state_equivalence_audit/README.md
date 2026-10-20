# Experiment 154 — History-state equivalence and deterministic future equality

Audit Experiment153's two differently ordered physical-input histories at their shared post-history tick72/phase0.

- Of 110 eligible test-site contexts, **46** have exactly equal **all 60 4-bit windows** after the two ordered histories, and **64** have unequal final states.
- On the 46 same-state contexts, the **184 heldout probes** produce exactly identical causal response metrics (location union size, event>=10, event>=30). No mismatches.
- For the 64 different-state contexts (256 heldout probes across 47 parents), the parent-mean difference in the response-union size between left-first and right-first is **−0.8723 positions**. Signs by parent: 18 left-higher, 26 right-higher, 3 tied.

The same-state result is an exact **Markov determinism control**: full microstate + scheduler phase + identical intervention determines the future. The independent sequences leave no special physical history tag. Distinct final states may differ in their later responses; this is expected under ordinary nonlinear dynamics.

This is a stratification by current physical microstate equality, not identification of learning or a separate temporally encoded high-level causal variable.

```sh
python experiments/154_history_state_equivalence_audit/run.py > experiments/154_history_state_equivalence_audit/results/default.txt
python experiments/154_history_state_equivalence_audit/test_smoke.py
```
