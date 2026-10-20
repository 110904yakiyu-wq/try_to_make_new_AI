#!/usr/bin/env python3
"""Exp160: external-readout generalization on unseen two-symbol XOR sequences.

The frozen 139/104 physical kernel has NO learning, goals, labels, decoder or
memory register. Only the external ridge readout is fitted. No physical
trajectory or readout hyperparameter is selected by heldout performance.
"""
import argparse
import importlib.util
import itertools
import json
import random
import statistics
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CORE = HERE.parent / '139_extended_control_budget' / 'core.py'
spec = importlib.util.spec_from_file_location('exp139_physics', CORE)
physics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(physics)

TRAIN = (1, 2, 3, 5, 6, 7, 9, 11)
HELDOUT = (4, 8, 10, 12, 13, 14, 15)
FIRST_TICK, SECOND_TICK, END_TICK = 0, 24, 96
ALPHA = 1.0
SHUFFLES = 5
FEATURES = ('terminal', 'input_only', 'counts')
assert set(TRAIN).isdisjoint(HELDOUT)
assert set(TRAIN) | set(HELDOUT) == set(range(1, 16))
assert {v.bit_count() % 2 for v in TRAIN} == {0, 1}
assert {v.bit_count() % 2 for v in HELDOUT} == {0, 1}
assert END_TICK % 3 == SECOND_TICK % 3 == 0


def label(a, b):
    """Observer's prespecified two-input Boolean XOR-of-popcount-parities."""
    return (a.bit_count() ^ b.bit_count()) & 1


def evolve(frame, left, right, a, b):
    """At t=0 and t=24, externally XOR a 4-bit mask; kernel unchanged."""
    assert 1 <= a <= 15 and 1 <= b <= 15
    state = bytearray(frame)
    for tick in range(END_TICK):
        if tick == FIRST_TICK:
            state[left] ^= a
        if tick == SECOND_TICK:
            state[right] ^= b
        state = bytearray(physics.step(state, tick % 3))
    return bytes(state)


def bit_features(state):
    return [int(bool(value & (1 << bit))) for value in state for bit in range(4)]


def matrices(frame, left, right, tokens):
    states = []
    for a, b in itertools.product(tokens, repeat=2):
        states.append(evolve(frame, left, right, a, b))
    features = {
        'terminal': np.asarray([bit_features(s) for s in states], dtype=np.float64),
        'input_only': np.asarray([bit_features(bytes((a, b))) for a, b in itertools.product(tokens, repeat=2)], dtype=np.float64),
        'counts': np.asarray([[sum(v.bit_count() for v in s) / 240.0,
                               sum(v != 0 for v in s) / 60.0] for s in states], dtype=np.float64),
    }
    targets = np.asarray([label(a, b) for a, b in itertools.product(tokens, repeat=2)], dtype=np.float64)
    return features, targets, states


def ridge_predictions(train, test, y, alpha=ALPHA):
    """Frozen-alpha dual ridge with train-only centering and fixed 0.5 threshold."""
    center = train.mean(axis=0)
    tr = train - center
    te = test - center
    k = tr @ tr.T
    k.flat[::len(k) + 1] += alpha
    coeff = np.linalg.solve(k, y - y.mean())
    scores = y.mean() + (te @ tr.T) @ coeff
    return (scores >= 0.5).astype(np.int8)


def balanced_accuracy(truth, predicted):
    truth = np.asarray(truth, dtype=np.int8)
    pred = np.asarray(predicted, dtype=np.int8)
    assert set(truth) == {0, 1}
    return float((np.mean(pred[truth == 0] == 0) + np.mean(pred[truth == 1] == 1)) / 2)


def collision_count(states, targets):
    labels_by_state = {}
    for state, target in zip(states, targets):
        labels_by_state.setdefault(state, set()).add(int(target))
    return sum(len(classes) > 1 for classes in labels_by_state.values())


def assay(max_parents=130):
    assert 1 <= max_parents <= 130
    parents = list(physics.parents())
    assert len(parents) == 130
    records = []
    for pid, (seed, frame, orbit) in enumerate(parents[:max_parents]):
        left = (min(orbit['support']) - 1) % 60
        right = (max(orbit['support']) + 1) % 60
        assert frame[left] == frame[right] == 0 and left != right
        train_x, train_y, train_states = matrices(frame, left, right, TRAIN)
        test_x, test_y, test_states = matrices(frame, left, right, HELDOUT)
        assert len(train_y) == 64 and len(test_y) == 49
        scores = {}
        for feature in FEATURES:
            pred = ridge_predictions(train_x[feature], test_x[feature], train_y)
            scores[feature] = balanced_accuracy(test_y, pred)
        # A fixed, independently seeded label-permutation diagnostic.  The
        # physical features are intact; decoder receives meaningless mapping.
        rng = random.Random(160_000 + pid)
        shuf = []
        for _ in range(SHUFFLES):
            indices = list(range(len(train_y)))
            rng.shuffle(indices)
            fake_y = train_y[indices]
            shuf.append(balanced_accuracy(test_y,
                ridge_predictions(train_x['terminal'], test_x['terminal'], fake_y)))
        records.append({
            'parent_id': pid, 'seed': list(seed), 'original_support_size': len(orbit['support']),
            'train_label_count': dict(Counter(map(str, train_y.astype(int)))),
            'heldout_label_count': dict(Counter(map(str, test_y.astype(int)))),
            'terminal_balanced_accuracy': scores['terminal'],
            'input_only_balanced_accuracy': scores['input_only'],
            'counts_balanced_accuracy': scores['counts'],
            'shuffled_terminal_balanced_accuracy': statistics.mean(shuf),
            'terminal_minus_input': scores['terminal'] - scores['input_only'],
            'terminal_minus_counts': scores['terminal'] - scores['counts'],
            'heldout_terminal_cross_label_collisions': collision_count(test_states, test_y),
            'heldout_distinct_terminal_states': len(set(test_states)),
            'train_terminal_cross_label_collisions': collision_count(train_states, train_y),
        })
    keys = ('terminal_balanced_accuracy', 'input_only_balanced_accuracy',
            'counts_balanced_accuracy', 'shuffled_terminal_balanced_accuracy',
            'terminal_minus_input', 'terminal_minus_counts')
    result = {k: statistics.mean(row[k] for row in records) for k in keys}
    # Exploratory parent-cluster bootstrap; preserves within-parent correlations.
    # Diagnostics were specified after the first complete exploratory run;
    # they must not be represented as prospectively preregistered inference.
    bootstrap_rng = np.random.default_rng(1602026)
    indices = bootstrap_rng.integers(0, len(records), size=(10000, len(records)))
    result['parent_cluster_bootstrap_95pct'] = {}
    for key in keys:
        values = np.asarray([row[key] for row in records])
        means = values[indices].mean(axis=1)
        result['parent_cluster_bootstrap_95pct'][key] = [float(x) for x in np.quantile(means, [0.025, 0.975])]
    result['descriptive_function_gate'] = {
        'terminal_lower_bound_gt_chance': result['parent_cluster_bootstrap_95pct']['terminal_balanced_accuracy'][0] > 0.5,
        'terminal_minus_input_lower_bound_gt_zero': result['parent_cluster_bootstrap_95pct']['terminal_minus_input'][0] > 0,
        'status': 'exploratory_only_not_preregistered',
    }
    result.update({
        'parent_terminal_gt_input': sum(r['terminal_minus_input'] > 0 for r in records),
        'parent_terminal_lt_input': sum(r['terminal_minus_input'] < 0 for r in records),
        'parent_terminal_eq_input': sum(r['terminal_minus_input'] == 0 for r in records),
        'heldout_parents_with_cross_label_state_collision': sum(r['heldout_terminal_cross_label_collisions'] > 0 for r in records),
        'parents_terminal_above_chance': sum(r['terminal_balanced_accuracy'] > 0.5 for r in records),
        'parents_terminal_below_chance': sum(r['terminal_balanced_accuracy'] < 0.5 for r in records),
    })
    return {
        'experiment': 160,
        'protocol': {
            'physics': 'frozen 139/104 60x4-bit three-phase deterministic local kernel',
            'injection': 'external XOR mask a at ORIGINAL support left boundary at tick0; b at right boundary at tick24',
            'endpoint': 'full terminal microstate at tick96 with next phase0',
            'task': 'binary XOR of the parities of popcount(a) and popcount(b); observer label only',
            'train_masks': list(TRAIN), 'heldout_masks': list(HELDOUT),
            'split': 'disjoint raw masks for both time slots; full Cartesian product in each split',
            'readout': 'independent parent-specific, externally fitted dual linear ridge, alpha=1, train-only mean centering, threshold=0.5',
            'features': {'terminal': '240 raw state bits at t96', 'input_only': '8 literal input bits, no dynamics',
                         'counts': 'terminal total one-bits/240 and occupied-windows/60'},
            'primary': 'equal-parent mean heldout balanced accuracy terminal minus input_only',
            'null': 'five deterministic permutations of training labels per parent, terminal features unchanged',
            'uncertainty': 'exploratory 10000 resamples of whole parent clusters, seeded 1602026, percentile 95% CI; added after initial exploratory run',
            'unit': 'original G0 parent; 49 correlated heldout sequences per parent are not independent',
            'scientific_boundary': 'Only external readout is trained. No learning, reward, decoder, target, or online feedback is introduced into physical kernel.'},
        'inventory': {'catalog_parents': 130, 'processed_parents': len(records),
                      'train_sequences_per_parent': len(TRAIN) ** 2,
                      'heldout_sequences_per_parent': len(HELDOUT) ** 2,
                      'physical_trajectories': len(records) * (len(TRAIN) ** 2 + len(HELDOUT) ** 2)},
        'summary': result, 'parent_records': records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-parents', type=int, default=130)
    parser.add_argument('--output', type=Path, default=HERE/'results/default.json')
    args = parser.parse_args()
    result = assay(args.max_parents)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({'inventory': result['inventory'], 'summary': result['summary']}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
