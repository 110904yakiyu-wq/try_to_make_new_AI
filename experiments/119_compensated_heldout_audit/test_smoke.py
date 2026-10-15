#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('exp119',H/'run.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
d=json.loads((H/'results/default.json').read_text())
assert d['experiment']==119 and d['inventory']['parents']==20 and len(d['patch_records'])==28
assert m.stats(d['patch_records'])==d['summary']
for w,k,p in [(1,17,10),(2,21,9),(3,35,9)]:
 assert d['inventory'][f'w{w}_compensated_states']==k
 assert d['inventory'][f'w{w}_matched_patches']==p
for row in d['patch_records']:
 assert row['compensated_pool']>0
 for t in (6,12,24):
  for metric in ('jaccard','exact'):
   assert all(0<=row[name][str(t)][metric]<=1 for name in ('donor','uncompensated_nearest','compensated_nearest'))
print('exp119 smoke: PASS')
