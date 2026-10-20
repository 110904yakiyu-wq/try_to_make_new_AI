#!/usr/bin/env python3
"""Exp160 zero-leakage, deterministic physical and decoder protocol checks."""
import importlib.util
from pathlib import Path

import numpy as np

p = Path(__file__).with_name('run.py')
spec = importlib.util.spec_from_file_location('exp160', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

assert len(m.TRAIN) == 8 and len(m.HELDOUT) == 7
assert not (set(m.TRAIN) & set(m.HELDOUT))
assert m.label(3, 5) == 0  # even / even
assert m.label(7, 3) == 1  # odd / even
assert m.label(7, 11) == 0  # odd / odd
parents = list(m.physics.parents())
assert len(parents) == 130
seed, frame, orbit = parents[0]
lo = (min(orbit['support'])-1) % 60
hi = (max(orbit['support'])+1) % 60
assert m.evolve(frame,lo,hi,1,3) == m.evolve(frame,lo,hi,1,3)
X,Y,S = m.matrices(frame,lo,hi,m.TRAIN)
assert X['terminal'].shape == (64,240)
assert X['input_only'].shape == (64,8)
assert X['counts'].shape == (64,2)
assert set(Y) == {0.0,1.0}
assert 0 <= m.balanced_accuracy(Y,m.ridge_predictions(X['terminal'],X['terminal'],Y)) <= 1
r=m.assay(2)
assert r['inventory']['processed_parents']==2
assert r['inventory']['physical_trajectories']==226
assert len(r['parent_records'])==2
assert all(0<=v['terminal_balanced_accuracy']<=1 for v in r['parent_records'])
print('exp160 smoke PASS')
