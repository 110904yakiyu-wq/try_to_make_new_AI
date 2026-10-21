#!/usr/bin/env python3
"""Exp162: cross-parent transfer of externally supervised decoding.

All task labels, training, and readout are OBSERVER-side. Physics is the
unchanged 104/139 deterministic kernel. No target-parent labelled examples
are used by shared readouts. Sham differences use label-free calibration.
"""
import argparse
import importlib.util
import json
import statistics
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('exp161', ROOT/'161_split_decoder_audit'/'run.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)
old = e.old
physics = e.physics
N_GROUPS = 5
N_PERMUTATIONS = 5
BOOTSTRAP = 5000
SEED = 1622026
MODES = ('raw', 'sham_delta')
METHODS = ('linear', 'rbf')
MEASURES = ('transfer', 'within')


def state_matrix(parent_rows):
    """Compute paired 225-sequence readouts + no-input control for each G0 parent."""
    tensors = {'raw': [], 'sham_delta': []}
    seeds = []
    for seed, frame, orbit in parent_rows:
        lo = (min(orbit['support']) - 1) % 60
        hi = (max(orbit['support']) + 1) % 60
        assert frame[lo] == frame[hi] == 0 and lo != hi
        sham = bytes(frame)
        for tick in range(old.END_TICK):
            sham = physics.step(sham, tick % 3)
        sbits = np.asarray(old.bit_features(sham), dtype=np.float64)
        states = np.asarray([old.bit_features(old.evolve(frame, lo, hi, a, b))
                             for a in e.ALL for b in e.ALL], dtype=np.float64)
        assert states.shape == (225,240)
        tensors['raw'].append(states)
        tensors['sham_delta'].append(states - sbits)
        seeds.append(list(seed))
    return {k: np.stack(v) for k,v in tensors.items()}, seeds


def parent_fold_assignment(parent_rows):
    """Keep *phase-aware autonomous orbit classes* wholly in one fold.

    A parent can have a distinct start frame but be on the same phase-aware
    cycle as another. Splitting these two seeds would leak a physics class.
    Classes and fold loads are computed WITHOUT probe labels/outcomes.
    """
    classes = {}
    for pid, (_, _, orbit) in enumerate(parent_rows):
        canonical = min((((orbit['phase'] + i) % 3, bytes(frame))
                         for i, frame in enumerate(orbit['cycle'])))
        classes.setdefault(canonical, []).append(pid)
    groups = sorted(classes.values(), key=lambda ids: (-len(ids), ids[0]))
    assignment = [-1] * len(parent_rows)
    loads = [0] * N_GROUPS
    for cluster in groups:
        group = min(range(N_GROUPS), key=lambda g:(loads[g],g))
        for pid in cluster:
            assignment[pid] = group
        loads[group] += len(cluster)
    assert all(group in range(N_GROUPS) for group in assignment)
    assert all(len({assignment[i] for i in cluster}) == 1 for cluster in groups)
    return assignment, groups


def predict_many(method, train, test, ycolumns):
    """Share kernel Gram matrices over true and permuted labels.

    Algebraically identical to Exp161 predict on each ycolumn, but avoids
    reconstructing the same train/test kernels for six label vectors.
    """
    ycolumns = np.asarray(ycolumns, dtype=np.float64)
    assert ycolumns.ndim == 2 and ycolumns.shape[0] == len(train)
    if method == 'linear':
        center = train.mean(axis=0)
        tr = train - center
        te = test - center
        k = tr @ tr.T
        cross = te @ tr.T
    else:
        assert method == 'rbf'
        D = e.distance_squared(train,train)
        upper = D[np.triu_indices(len(D), k=1)]
        positive = upper[upper > 0]
        median = float(np.median(positive)) if len(positive) else 1.0
        k = np.exp(-D / median)
        cross = np.exp(-e.distance_squared(test, train) / median)
    coeff = np.linalg.solve(k + e.RIDGE_ALPHA * np.eye(len(train)),
                             ycolumns - ycolumns.mean(axis=0,keepdims=True))
    scores = ycolumns.mean(axis=0,keepdims=True) + cross @ coeff
    return (scores >= 0.5).astype(np.int8)


def compute(max_parents=130, max_folds=12, bootstrap=BOOTSTRAP):
    assert N_GROUPS * 2 <= max_parents <= 130
    assert 1 <= max_folds <= len(e.partitions())
    parents = list(physics.parents())
    assert len(parents) == 130
    X, seeds = state_matrix(parents[:max_parents])
    splits = e.partitions()[:max_folds]
    assignments, orbit_classes = parent_fold_assignment(parents[:max_parents])
    assert set(assignments) == set(range(N_GROUPS))
    y = np.asarray([old.label(a,b) for a in e.ALL for b in e.ALL], dtype=np.float64)
    records = []
    folds = []
    for sid,(train_masks, test_masks) in enumerate(splits):
        ti,vi = e.selected_indices(train_masks),e.selected_indices(test_masks)
        tr_y,te_y = y[ti],y[vi]
        assert len(ti)==64 and len(vi)==49 and set(tr_y)==set(te_y)=={0.,1.}
        for group in range(N_GROUPS):
            target = np.asarray([i for i,g in enumerate(assignments) if g == group], dtype=int)
            source = np.asarray([i for i,g in enumerate(assignments) if g != group], dtype=int)
            assert len(set(source)&set(target))==0
            assert len(source)+len(target)==max_parents
            # The SINGLE shared supervised model sees 64 input-pair prototype
            # responses: each is an average over source parents, never targets.
            folds.append({'split_id':sid, 'parent_group_id':group,
                          'source_parent_count':len(source), 'target_parent_count':len(target)})
            for mode in MODES:
                protos = X[mode][source][:,ti,:].mean(axis=0)
                test_features = X[mode][target][:,vi,:]
                flat = test_features.reshape((-1,240))
                for method in METHODS:
                    # Fixed seed, independent of targets and ground-truth heldout responses.
                    rngs = [np.random.default_rng(SEED+sid*10000+group*1000+perm)
                            for perm in range(N_PERMUTATIONS)]
                    columns = np.column_stack([tr_y]+[tr_y[r.permutation(len(tr_y))] for r in rngs])
                    predicted = predict_many(method,protos,flat,columns).reshape((len(target),len(vi),1+N_PERMUTATIONS))
                    transferred = predicted[:,:,0]
                    transfer_ba=[old.balanced_accuracy(te_y,p) for p in transferred]
                    shuffle_ba=[statistics.mean(old.balanced_accuracy(te_y,predicted[j,:,i])
                                                for i in range(1,1+N_PERMUTATIONS))
                                for j in range(len(target))]
                    for j,pid in enumerate(target):
                        within=e.predict(method,X[mode][pid,ti,:],X[mode][pid,vi,:],tr_y)
                        within_ba=old.balanced_accuracy(te_y,within)
                        records.append({
                            'parent_id':int(pid),'seed':seeds[pid], 'parent_group_id':group,
                            'split_id':sid,'mode':mode,'method':method,
                            'transfer_ba':transfer_ba[j],
                            'within_ba':within_ba,
                            'transfer_minus_within':transfer_ba[j]-within_ba,
                            'shuffled_transfer_ba':shuffle_ba[j],
                            'transfer_minus_shuffled':transfer_ba[j]-shuffle_ba[j],
                        })
    # Equal parent, equal split; same 130 parent IDs repeat in all folds.
    keys=('transfer_ba','within_ba','transfer_minus_within',
          'shuffled_transfer_ba','transfer_minus_shuffled')
    summaries={}
    for mode in MODES:
        for method in METHODS:
            key=f'{mode}_{method}'
            subset=[x for x in records if x['mode']==mode and x['method']==method]
            assert len(subset)==max_parents*max_folds
            means={k:statistics.mean(x[k] for x in subset) for k in keys}
            parent_value=np.empty((max_parents,len(keys)),dtype=float)
            for pid in range(max_parents):
                arr=[r for r in subset if r['parent_id']==pid]
                assert len(arr)==max_folds
                parent_value[pid,:]=[statistics.mean(r[k] for r in arr) for k in keys]
            random=np.random.default_rng(SEED+MODES.index(mode)*10+METHODS.index(method))
            indices=random.integers(max_parents,size=(bootstrap,max_parents))
            cis={k:list(map(float,np.quantile(parent_value[indices,i].mean(axis=1),[.025,.975])))
                 for i,k in enumerate(keys)}
            by_split=[{'split_id':sid,**{k:statistics.mean(r[k] for r in subset if r['split_id']==sid)
                                for k in keys}}
                      for sid in range(max_folds)]
            summaries[key]={'means':means,'parent_cluster_percentile_95pct':cis,
                            'per_split':by_split,
                            'transfer_above_chance_parent_bootstrap':cis['transfer_ba'][0]>.5,
                            'transfer_better_than_within_parent_bootstrap':cis['transfer_minus_within'][0]>0}
    return {
        'experiment':162,
        'protocol':{
            'physics':'Unchanged original G0 130-parent 60x4bit phase0 three-scheduler 104/139 deterministic kernel',
            'input':'Left original boundary XOR a at t0, right original boundary XOR b at t24, terminal readout at t96; a,b in 1..15',
            'task':'External parity-of-popcount XOR over two inputs; labels never injected into kernel',
            'raw_split':'Exactly Exp161 12 predeclared disjoint train/heldout partitions; no heldout raw mask in decoder training',
            'parent_split':'Five parent groups from label-free phase-aware autonomous orbit equivalence classes; greedy class-balanced split by class size desc, min parent ID, group minimum load; no equivalent cycles cross source/evaluation, no labelled target examples',
            'modalities':{'raw':'240 terminal raw bits','sham_delta':'240 signed difference of terminal raw bits from same parent no-input tick96 counterfactual, label-free target calibration'},
            'decoder':'Same pretrained-in-spec Exp161 linear dual ridge or RBF kernel ridge, fixed alpha=1 and training-only RBF median gamma, threshold=0.5',
            'comparators':'Within-parent trained on same 64 mask-pair examples (uses labelled target-parent examples), plus shuffled source-prototype train labels',
            'estimand':'Heldout novel-parent and novel-mask balanced accuracy of common external decoder vs within-parent external decoder, equal parent and split weights',
            'uncertainty':'5000 whole-parent bootstrap, conditional on 12 correlated fixed mask splits and fixed five parent groups; descriptive, not independent population sample',
            'limits':'Pooled templates train on 104 labelled source parents but only 64 averaged prototypes; can erase parent-specific information. Sham subtraction is target-side label-free calibration, not strict no-touch zero-shot.',
            'science':'No reward, learning, decoder or objective is implemented in the physical kernel; externally fitted readouts do not demonstrate internal learning.'},
        'inventory':{'parents':max_parents,'parent_groups':N_GROUPS,'raw_mask_splits':max_folds,
                     'physical_two_input_trajectories':max_parents*225,
                     'physical_sham_trajectories':max_parents, 'phase_aware_orbit_classes':len(orbit_classes),
                     'repeated_orbit_classes':sum(len(ids)>1 for ids in orbit_classes),
                     'parent_split_model_measurements':len(records),
                     'measurements_per_mode_method':max_parents*max_folds,
                     'source_train_pairs_per_parent':64,'heldout_pairs_per_parent':49,
                     'frozen_label_permutations_per_shared_fit':N_PERMUTATIONS},
        'orbit_classes_with_multiple_seeds':[ids for ids in orbit_classes if len(ids)>1],
        'parent_groups':[{'group':g,'parent_ids':[i for i,k in enumerate(assignments) if k==g]}
                         for g in range(N_GROUPS)],
        'raw_mask_partitions':[{'split_id':i,'train_masks':list(tr),'heldout_masks':list(te)}
                               for i,(tr,te) in enumerate(splits)],
        'fold_group_records':folds,
        'summary':summaries,'parent_split_records':records,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-parents',type=int,default=130)
    parser.add_argument('--max-folds',type=int,default=12)
    parser.add_argument('--bootstrap',type=int,default=BOOTSTRAP)
    parser.add_argument('--output',type=Path,default=HERE/'results/default.json')
    args=parser.parse_args()
    result=compute(args.max_parents,args.max_folds,args.bootstrap)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'inventory':result['inventory'],'summary':result['summary']},indent=2,sort_keys=True))

if __name__=='__main__':main()
