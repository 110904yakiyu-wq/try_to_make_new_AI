# Experiment 015 — dynamical feature audit

## Question

Experiment 014 found that simple local truth-table descriptors explain little of the remote history-dependent response geometry. Are dynamical properties of the fixed CA rule more informative?

## Observer-side dynamical measures

For every ECA rule, use deterministic pseudo-random binary backgrounds and introduce a one-bit perturbation. Measure:

- final damage mass
- peak damage mass
- time-integrated damage mass
- maximum propagation radius
- fraction of perturbations still alive at the final horizon

Also measure a simple nonlinear perturbation-interaction term. For two initial bit flips `p` and `q`, compare the joint perturbation with the XOR sum of the two individual perturbations after the same evolution horizon. Affine/additive behavior gives zero interaction under this assay.

These are observer metrics only. None are supplied to the CA as objectives.

## Default budget

Remote-geometry score uses the same budget as Experiment 012.

Dynamical assay:

- ring size: 128
- horizon: 32
- trials per rule: 32
- same deterministic random trial set for all 256 rules
- two-perturbation separation: 7 cells

## Result

The dynamical measures are more associated with the Experiment-012 untrained-probe geometry score than the simple local descriptors from Experiment 014.

Approximate correlations:

- final damage mass: Pearson 0.416, Spearman 0.494
- integrated damage: Pearson 0.373, Spearman 0.482
- propagation radius: Pearson 0.360, Spearman 0.459
- nonlinear perturbation interaction: Pearson 0.410, Spearman 0.522

For comparison, the strongest simple local statistic tested in Experiment 014 was average Boolean sensitivity, with Spearman only ~0.295.

## Interpretation

Transport and nonlinear interaction appear relevant, but are far from sufficient explanations. A correlation around 0.5 leaves substantial unexplained structure.

The observation is compatible with the idea that useful history dependence needs at least two things:

1. consequences of local history must remain dynamically available or propagate,
2. histories/interventions must be able to interact nonlinearly rather than simply superpose.

However, stronger damage is not monotonically equivalent to stronger response geometry. Some highly spreading rules are mediocre on the target observable, while some sparse-propagation rules score very highly.

The next step should therefore study **structured transport**, not generic chaos: which perturbations remain distinguishable, how they collide, and whether the low-dimensional response modes correspond to persistent dynamical channels or domains.

Damage spreading and Lyapunov-style analyses are established CA tools; this experiment uses them only as explanatory observer measurements, not as a novel metric.
