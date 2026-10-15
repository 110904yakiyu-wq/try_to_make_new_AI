# 026 — Full 55-parent 2000-tick extension does not identify eventual connected advantage

Experiment 126 extends **all 55** Experiment 108 exact-on-cycle geometry matched G0/control parents, not only the 20 first-step-mask-matched subset from 114, to 2000 ticks. Same fixed physical kernel, same 30 raw material boundary probes per pair. Recomputed 500 tick results exactly match Experiment 125 (G0 1486 connected,143 censored; control 1215 connected,398 censored). Only 500-censored injected states are reevaluated at 2000; cache by identical full state+phase0 to avoid duplicate CPU evaluation, without altering the number of observations.

2000 tick resolution adds **three control connected** orbits, no G0 resolutions. At horizon 2000 confirmed connected is G0=1486, control=1218; right censored G0=143, control=395. Observed finite-time confirmed rate difference +16.24 percentage points, but **worst-case eventual-rate interval is still [−7.70,+24.91] percentage points**. Parent bound signs unchanged: 11 guaranteed G0-positive, 1 control-positive, 43 inconclusive. The full finite-state Markov dynamics will eventually recur, but a large recurrence period/transient need not be found at 2000. Censor is uncertainty, not death/nonviability.

No evidence of an intrinsic self-maintenance motive, reproduction, heredity or learning. No historical claims or physical primitive changed. This result primarily establishes low information gain per extended CPU tick in this already selected population.

Authorities: `experiments/126_extended_censoring_bounds/`, frozen 125 reference, existing docs 010, 014, 025.
