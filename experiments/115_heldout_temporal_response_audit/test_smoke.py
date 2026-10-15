#!/usr/bin/env python3
"""Reproducibility and non-leakage checks for Experiment 115."""
import importlib.util
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('exp115',HERE/'run.py')
x=importlib.util.module_from_spec(spec);spec.loader.exec_module(x)
result=json.loads((HERE/'results/default.json').read_text(encoding='utf-8'))
assert result['experiment']==115
assert result['inventory']['parents']==20
assert len(result['patch_records'])==57
assert tuple(result['inventory'][f'width{w}_donor_mask_pass'] for w in (1,2,3))==(35,16,20)
assert tuple(result['inventory'][f'width{w}_feature_eligible'] for w in (1,2,3))==(23,14,20)
assert tuple(result['inventory'][f'width{w}_t1_eligible'] for w in (1,2,3))==(12,9,20)
assert tuple(result['inventory'][f'width{w}_t1t3_eligible'] for w in (1,2,3))==(0,0,0)
assert sum(result['inventory'][f'width{w}_t1_nulls'] for w in (1,2,3))==440
assert tuple(result['summary'][str(w)]['physical']['null_microstates'] for w in (1,2,3))==(33,59,414)
assert x.TRAIN==(1,7,15)
assert len(x.TEST)==12 and not(set(x.TRAIN)&set(x.TEST))
assert x.TIMES==(1,3,6,12,24)
assert result['summary']==x.aggregate(result['patch_records'])
assert all(set(r['eligible'])==set(x.GATES) for r in result['patch_records'])
assert all(r['pool_sizes']['train_t1_t3']<=r['pool_sizes']['train_t1']<=r['pool_sizes']['physical'] for r in result['patch_records'])
assert all(r['eligible']['train_t1']==(r['pool_sizes']['train_t1']>0) for r in result['patch_records'])
assert all(0<=r['donor_metrics'][str(t)]['jaccard']<=1 for r in result['patch_records'] for t in (6,12,24))
assert all(0<=r['null_metrics'][gate][str(t)]['jaccard']<=1 for r in result['patch_records'] for gate in x.GATES if r['eligible'][gate] for t in (6,12,24))
# Reconstruct a frozen control without testing material outcomes, then validate
# at least one genuinely distinct full-feature-matched raw null.
reference=json.loads((HERE.parent/'112_probe_discrimination_audit/results/default.json').read_text(encoding='utf-8'))
assert len(reference['parent_records'])==20
catalog=list(x.m.parents('left'))
p=reference['parent_records'][0]
seed,g0,orb=catalog[p['parent_id']]
assert list(seed)==p['seed']
ctrl=x.reference_control(p['parent_id'],g0,orb,p['control_match_attempt'])
mask=x.first_mask(g0)
assert x.first_mask(ctrl)==mask==frozenset(p['first_mask'])
for width in (1,2,3):
    for patch in x.changed_patches(g0,ctrl,orb['support'],width):
        trans=x.replace(ctrl,g0,patch)
        if x.first_mask(trans)!=mask:continue
        nulls=list(x.exact_physical_nulls(ctrl,g0,patch,mask,x.features(trans)))
        for candidate in nulls:
            assert candidate!=trans
            assert x.first_mask(candidate)==mask
            assert x.features(candidate)==x.features(trans)
            assert all(candidate[i]!=ctrl[i] for i in patch)
            assert all(candidate[i] in range(1,16) for i in patch)
            assert all(candidate[i]==ctrl[i] for i in range(x.m.SIZE) if i not in patch)
        if nulls:break
    else:continue
    break
else:raise AssertionError('no real physical alternative found in first pair')
print('exp115 smoke: PASS')
