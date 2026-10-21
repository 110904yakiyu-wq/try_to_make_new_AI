#!/usr/bin/env python3
"""Exp161: frozen multi-split and matched-readout audit of Exp160.

Split definitions, two decoder families and primary contrasts were fixed
before first Exp161 outcomes. Shuffled-label negative controls and joint-axis
sensitivity were added after the first run, and are labeled exploratory.
Observers only: NO physical learning or kernel modification.
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
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('exp160', ROOT / '160_sequence_transduction_gate' / 'run.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
physics = old.physics
ALL = tuple(range(1, 16))
FOLDS = 12
SEED = 1612026
RIDGE_ALPHA = 1.0
BSTRAP = 5000
SHUFFLES = 5
METHODS = ('linear', 'rbf')
SOURCES = ('terminal', 'input_only')
CHANCE = 0.5


def partitions():
    # Parity balanced training subsets: exactly 4 of the 8 odd-popcount raw
    # values and 4 of the 7 even-popcount raw values in each of 12 folds.
    odd = [v for v in ALL if v.bit_count() % 2]
    even = [v for v in ALL if not v.bit_count() % 2]
    first = tuple(sorted(old.TRAIN))
    assert len(first) == 8
    seen = {first}
    out = [first]
    rng = random.Random(SEED)
    while len(out) < FOLDS:
        tr = tuple(sorted(rng.sample(odd, 4) + rng.sample(even, 4)))
        if tr in seen:
            continue
        seen.add(tr)
        out.append(tr)
    return tuple((train, tuple(x for x in ALL if x not in train)) for train in out)


def distance_squared(A, B):
    # Binary feature arrays, so squared Euclidean = Hamming distance.
    asq = (A * A).sum(axis=1)[:, None]
    bsq = (B * B).sum(axis=1)[None, :]
    return np.maximum(asq + bsq - 2 * (A @ B.T), 0)


def predict(method, x_train, x_test, y_train):
    if method == 'linear':
        return old.ridge_predictions(x_train, x_test, y_train, alpha=RIDGE_ALPHA)
    assert method == 'rbf'
    # Median computed on *training features only*, not on heldout outcomes.
    D = distance_squared(x_train, x_train)
    nonzero = D[np.triu_indices(len(D), k=1)]
    positive = nonzero[nonzero > 0]
    median = float(np.median(positive)) if len(positive) else 1.0
    train_kernel = np.exp(-D / median)
    test_kernel = np.exp(-distance_squared(x_test, x_train) / median)
    yy = np.asarray(y_train, dtype=np.float64)
    coeff = np.linalg.solve(train_kernel + RIDGE_ALPHA * np.eye(len(yy)), yy - yy.mean())
    scores = yy.mean() + test_kernel @ coeff
    return (scores >= 0.5).astype(np.int8)


def selected_indices(raws):
    return np.asarray([((a - 1) * 15 + (b - 1)) for a, b in itertools.product(raws, repeat=2)], dtype=np.intp)


def summarize(rows, npartitions, nparents):
    keys = [f'{src}_{method}_ba' for src in SOURCES for method in METHODS]
    keys += [f'terminal_minus_input_{m}' for m in METHODS]
    keys += ['terminal_rbf_shuffled_ba', 'terminal_rbf_minus_shuffled']
    fold_rows = []
    for fold in range(npartitions):
        rs = [r for r in rows if r['fold_id'] == fold]
        assert len(rs) == nparents
        fold_rows.append({'fold_id': fold,
                          **{k: statistics.mean(x[k] for x in rs) for k in keys},
                          'cross_label_collisions_parents': sum(x['heldout_cross_label_state_collisions'] > 0 for x in rs)})
    parent_rows = []
    for pid in range(nparents):
        rs = [r for r in rows if r['parent_id'] == pid]
        assert len(rs) == npartitions
        parent_rows.append({'parent_id': pid, **{k: statistics.mean(x[k] for x in rs) for k in keys}})
    means = {k: statistics.mean(x[k] for x in parent_rows) for k in keys}
    parent_matrix = np.asarray([[p[k] for k in keys] for p in parent_rows], dtype=np.float64)
    bootstrap = np.random.default_rng(SEED)
    samples = bootstrap.integers(nparents, size=(BSTRAP, nparents))
    replicate_means = parent_matrix[samples].mean(axis=1)
    intervals = {key: [float(v) for v in np.quantile(replicate_means[:, i], [0.025, 0.975])]
                 for i, key in enumerate(keys)}
    # Two-axis stress test: jointly resample parents and the finite set of
    # researcher-selected splits. Because splits share mask values, these are
    # *descriptive sensitivity intervals*, not formal independent-fold CIs.
    cube = np.empty((nparents, npartitions, len(keys)), dtype=np.float64)
    for r in rows:
        cube[r['parent_id'], r['fold_id'], :] = [r[k] for k in keys]
    rng2 = np.random.default_rng(SEED + 1)
    joint = np.empty((BSTRAP, len(keys)), dtype=np.float64)
    for begin in range(0, BSTRAP, 250):
        take = min(250, BSTRAP - begin)
        pi = rng2.integers(nparents, size=(take, nparents))
        fi = rng2.integers(npartitions, size=(take, npartitions))
        joint[begin:begin + take, :] = cube[pi[:, :, None], fi[:, None, :], :].mean(axis=(1,2))
    two_axis_intervals = {k: [float(x) for x in np.quantile(joint[:,i], [0.025,0.975])]
                          for i,k in enumerate(keys)}
    fold_ranges = {key: [min(x[key] for x in fold_rows), max(x[key] for x in fold_rows)] for key in keys}
    # Leave one fixed split out; checks whether a particular split dominates the sign.
    leave_one_out = {m: ([statistics.mean(x[f'terminal_minus_input_{m}'] for x in fold_rows if x['fold_id'] != omit)
                          for omit in range(npartitions)] if npartitions > 1 else [float('nan')]) for m in METHODS}
    return {
        'mean_parent_fold_balanced_accuracy': means,
        'parent_cluster_bootstrap_95pct': intervals,
        'joint_parent_split_resampling_95pct_descriptive': two_axis_intervals,
        'per_fold': fold_rows,
        'per_fold_ranges': fold_ranges,
        'leave_one_fold_out_terminal_minus_input': {m: [min(v), max(v)] for m, v in leave_one_out.items()},
        'gates': {m: {
            'terminal_above_chance_at_parent_bootstrap_95pct': intervals[f'terminal_{m}_ba'][0] > CHANCE,
            'terminal_minus_input_positive_at_parent_bootstrap_95pct': intervals[f'terminal_minus_input_{m}'][0] > 0,
            'all_fold_terminal_means_above_chance': all(f[f'terminal_{m}_ba'] > CHANCE for f in fold_rows),
            'all_fold_advantages_positive': all(f[f'terminal_minus_input_{m}'] > 0 for f in fold_rows),
        } for m in METHODS},
        'heldout_cross_label_collisions_parent_folds': sum(r['heldout_cross_label_state_collisions'] > 0 for r in rows),
        'independence_note': 'folds reuse physical inputs and parents; parent bootstrap conditions on these 12 folds, and fold ranges are descriptive, not 12 independent confirmations',
        'parity_oracle_accuracy': 1.0,
    }


def assay(max_parents=130, max_folds=FOLDS):
    assert 1 <= max_parents <= 130 and 1 <= max_folds <= FOLDS
    parents = list(physics.parents())
    assert len(parents) == 130
    folds = partitions()[:max_folds]
    rows = []
    for pid, (seed, frame, orbit) in enumerate(parents[:max_parents]):
        left = (min(orbit['support']) - 1) % 60
        right = (max(orbit['support']) + 1) % 60
        assert not frame[left] and not frame[right] and left != right
        state = [old.evolve(frame, left, right, a, b) for a, b in itertools.product(ALL, repeat=2)]
        assert len(state) == 225
        feature = {
            'terminal': np.asarray([old.bit_features(s) for s in state], dtype=np.float64),
            'input_only': np.asarray([old.bit_features(bytes([a, b])) for a, b in itertools.product(ALL, repeat=2)], dtype=np.float64),
        }
        target = np.asarray([old.label(a,b) for a,b in itertools.product(ALL, repeat=2)], dtype=np.float64)
        for fid, (tr, te) in enumerate(folds):
            ti, vi = selected_indices(tr), selected_indices(te)
            ty, vy = target[ti], target[vi]
            assert len(ti)==64 and len(vi)==49
            assert Counter(ty) == Counter({0.0:32, 1.0:32})
            assert Counter(vy) == Counter({0.0:25, 1.0:24})
            assert set(tr).isdisjoint(te)
            row = {'parent_id': pid, 'seed': list(seed), 'fold_id': fid,
                   'heldout_cross_label_state_collisions': old.collision_count([state[i] for i in vi], vy)}
            for src in SOURCES:
                for method in METHODS:
                    pred = predict(method, feature[src][ti], feature[src][vi], ty)
                    row[f'{src}_{method}_ba'] = old.balanced_accuracy(vy, pred)
            for method in METHODS:
                row[f'terminal_minus_input_{method}'] = row[f'terminal_{method}_ba'] - row[f'input_only_{method}_ba']
            # Negative-control supervised labels shuffled BEFORE fitting, without
            # altering physical trajectories or ground-truth heldout labels.
            rng = random.Random(SEED + pid * 100000 + fid * 1000)
            shuf_acc = []
            for _ in range(SHUFFLES):
                idx = list(range(len(ty)))
                rng.shuffle(idx)
                shuf_acc.append(old.balanced_accuracy(vy, predict('rbf', feature['terminal'][ti],
                                                                     feature['terminal'][vi], ty[idx])))
            row['terminal_rbf_shuffled_ba'] = statistics.mean(shuf_acc)
            row['terminal_rbf_minus_shuffled'] = row['terminal_rbf_ba'] - row['terminal_rbf_shuffled_ba']
            rows.append(row)
    return {
        'experiment': 161,
        'protocol': {
            'physics': 'unchanged 104/139 60x4 bit three phase deterministic kernel, same initial 130 G0 parents as 160',
            'sequence': 'left ORIGINAL boundary XOR a tick0, right ORIGINAL boundary XOR b tick24, phase0 output tick96',
            'task': 'XOR of popcount parity of a and b (external observer task)',
            'partition_generation': 'fold0 exactly exp160; remaining folds deterministic random.Random(1612026) sample 4 odd- and 4 even-parity raw masks; distinct folds, outcome blind',
            'readout': 'parent-specific, trained only on train raw pairs; external linear dual ridge or RBF Gaussian dual kernel ridge; alpha=1 and threshold=0.5 fixed; RBF bandwidth=median positive training pairwise squared distance',
            'compare': 'same two decoders separately fitted to terminal 240-bit state and literal input 8 bits',
            'oracle': 'exact input popcount parity XOR is an algebraic observer and attains 100% by task definition, not an empirical learner',
            'negative_control': 'five seeded training-label permutations for terminal RBF per parent/fold, heldout targets intact; added after initial Exp161 run',
            'primary': 'terminal heldout balanced accuracy and same-decoder terminal-minus-input differences averaged equally over parent and split',
            'uncertainty': 'fixed-fold whole-parent cluster bootstrap (primary) and post-first-run joint parent/split resampling (exploratory), 5000 replicates each; split dependence prevents classical independent-fold CI interpretation',
            'caveat': 'no reward, learner or goal in physical kernel; external decoders are supervised; folds dependent, not 12 independent trials'},
        'folds': [{'fold_id': i, 'train_masks': list(tr), 'heldout_masks': list(te)} for i, (tr,te) in enumerate(folds)],
        'inventory': {'parents': max_parents, 'folds': len(folds), 'raw_pairs_per_parent_cached': 225,
                      'physical_trajectories': max_parents*225, 'train_pairs_per_parent_fold': 64,
                      'heldout_pairs_per_parent_fold': 49, 'parent_fold_records': len(rows),
                      'parent_fold_model_fits': len(rows)*(len(SOURCES)*len(METHODS)+SHUFFLES)},
        'summary': summarize(rows, len(folds), max_parents), 'parent_fold_records': rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-parents', type=int, default=130)
    ap.add_argument('--max-folds', type=int, default=FOLDS)
    ap.add_argument('--output', type=Path, default=HERE / 'results/default.json')
    args = ap.parse_args()
    result = assay(args.max_parents, args.max_folds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({'inventory': result['inventory'], 'summary': result['summary']}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
