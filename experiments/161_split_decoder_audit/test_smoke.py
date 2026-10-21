#!/usr/bin/env python3
"""Exp161 split/label/physics, non-leakage and exp160 parity-regression tests."""
import importlib.util
from pathlib import Path

p = Path(__file__).with_name('run.py')
spec = importlib.util.spec_from_file_location('exp161', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
folds = m.partitions()
assert len(folds) == 12 and len(set(x[0] for x in folds)) == 12
assert folds[0][0] == tuple(sorted(m.old.TRAIN))
for train, heldout in folds:
    assert len(train) == 8 and len(heldout) == 7
    assert not (set(train) & set(heldout))
    assert set(train) | set(heldout) == set(m.ALL)
    assert sum(x.bit_count()%2 for x in train)==4
    assert sum(x.bit_count()%2 for x in heldout)==4
# Distances are symmetric and nonnegative, no dependence on heldout labels.
import numpy as np
x=np.asarray([[0,1],[1,0],[1,1]],dtype=float)
assert np.array_equal(m.distance_squared(x,x),[[0,2,1],[2,0,1],[1,1,0]])
# Reproduce exp160 on the fixed first parent and original mask split.
r = m.assay(2,1)
assert r['inventory']['physical_trajectories']==450
assert len(r['parent_fold_records'])==2
baseline = m.old.assay(2)
for row in r['parent_fold_records']:
    prev=baseline['parent_records'][row['parent_id']]
    assert abs(row['terminal_linear_ba'] - prev['terminal_balanced_accuracy']) < 1e-12
    assert abs(row['input_only_linear_ba'] - prev['input_only_balanced_accuracy']) < 1e-12
assert r['summary']['parity_oracle_accuracy']==1.0
print('exp161 smoke PASS')
