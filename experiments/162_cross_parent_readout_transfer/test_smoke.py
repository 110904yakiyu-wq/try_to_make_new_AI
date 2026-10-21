#!/usr/bin/env python3
"""Exp162 deterministic kernel, masked split, zero-target-label and readout audits."""
from importlib import util
from pathlib import Path
import numpy as np

f=Path(__file__).with_name('run.py')
s=util.spec_from_file_location('exp162',f)
e=util.module_from_spec(s)
s.loader.exec_module(e)
assert e.N_GROUPS==5
assert e.e.partitions()[0][0]==tuple(sorted(e.old.TRAIN))
assert len(list(e.physics.parents()))==130
parents=list(e.physics.parents())
assign,classes=e.parent_fold_assignment(parents)
assert len(classes)==126
assert sum(len(cluster)>1 for cluster in classes)==4
assert all(len({assign[i] for i in cluster})==1 for cluster in classes)
assert max(assign.count(group) for group in range(5))-min(assign.count(group) for group in range(5))<=1
assert e.physics.SIZE==60 and e.physics.CENTER==30
rng=np.random.default_rng(314)
for method in e.METHODS:
    x=rng.integers(0,2,size=(64,240)).astype(float)
    t=rng.integers(0,2,size=(10,240)).astype(float)
    y=rng.integers(0,2,size=(64,4)).astype(float)
    expected=np.stack([e.e.predict(method,x,t,y[:,i]) for i in range(4)],axis=1)
    observed=e.predict_many(method,x,t,y)
    assert np.array_equal(expected,observed)

r=e.compute(10,1,100)
assert r['inventory']['physical_two_input_trajectories']==2250
assert r['inventory']['physical_sham_trajectories']==10
assert r['inventory']['parent_split_model_measurements']==40
assert len(r['parent_groups'])==5
assert set(i for group in r['parent_groups'] for i in group['parent_ids'])==set(range(10))
assert all(x['source_parent_count']>=7 and x['target_parent_count']>=1 for x in r['fold_group_records'])
assert all(0<=x['transfer_ba']<=1 and 0<=x['within_ba']<=1 for x in r['parent_split_records'])
assert all(set(x['train_masks']).isdisjoint(x['heldout_masks']) for x in r['raw_mask_partitions'])
# Both modalities differ only by a constant sham vector for each parent;
# in-parent ridge and RBF are translation invariant.
for method in e.METHODS:
    raw={x['parent_id']:x for x in r['parent_split_records'] if x['mode']=='raw' and x['method']==method}
    delta={x['parent_id']:x for x in r['parent_split_records'] if x['mode']=='sham_delta' and x['method']==method}
    assert all(abs(raw[i]['within_ba']-delta[i]['within_ba'])<1e-12 for i in raw)
# First Exp161 split regression, recorded before Exp162 was run.
ref={0:(.5441666666666667,.6291666666666667),
     1:(.45166666666666666,.7533333333333333),
     2:(.4691666666666666,.6525000000000001),
     3:(.4933333333333333,.53),
     4:(.5116666666666667,.47)}
for pid,(lin,rbf) in ref.items():
    linear=next(x for x in r['parent_split_records'] if x['parent_id']==pid and x['mode']=='raw' and x['method']=='linear')
    nonlinear=next(x for x in r['parent_split_records'] if x['parent_id']==pid and x['mode']=='raw' and x['method']=='rbf')
    assert abs(linear['within_ba']-lin)<1e-12
    assert abs(nonlinear['within_ba']-rbf)<1e-12
print('exp162 smoke PASS')
