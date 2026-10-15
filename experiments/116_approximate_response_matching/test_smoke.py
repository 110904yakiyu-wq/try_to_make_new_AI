#!/usr/bin/env python3
"""Invariant audit for Experiment 116; deterministic small-case recomputation."""
import importlib.util,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('exp116',HERE/'run.py')
x=importlib.util.module_from_spec(spec);spec.loader.exec_module(x)
d=json.loads((HERE/'results/default.json').read_text())
assert d['experiment']==116
assert d['inventory']['parents']==20
assert len(d['patch_records'])==57
assert {(w,d['inventory'][f'width{w}_physical_eligible']) for w in (1,2,3)}=={(1,23),(2,14),(3,20)}
assert x.summarize(d['patch_records'])==d['summary']
assert sum(r['candidates'] for r in d['patch_records'])==506
for row in d['patch_records']:
  assert row['candidates']>0
  assert 0<row['min_train_hamming']<=row['mean_train_hamming']<=row['max_train_hamming']
  sizes=[row['pool_size'][q] for q in x.GATES]
  assert sizes[0]==row['candidates']
  assert sizes[1]==1 and sizes[2]==min(3,sizes[0])
  assert all(row['eligible'][q]==(row['pool_size'][q]>0) for q in x.GATES)
  assert row['pool_size']['t1']<=row['candidates']
  for lim in (4,8,16,32,64):
    assert row['pool_size'][f'd_le_{lim}']==row['threshold_counts'][str(lim)]
    assert 0<=row['pool_size'][f'd_le_{lim}']<=row['candidates']
  for g in x.GATES:
    if not row['eligible'][g]:continue
    for tick in (6,12,24):
      for metric in ('jaccard','exact'):
        assert 0<=row['donor'][str(tick)][metric]<=1
        assert 0<=row['null'][g][str(tick)][metric]<=1
assert d['summary']['2']['nearest1']['24_jaccard_diff']<0
assert d['summary']['3']['nearest1']['24_jaccard_diff']>0
print('exp116 smoke: PASS')
