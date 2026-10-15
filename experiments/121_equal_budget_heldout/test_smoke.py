#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('exp121',P/'run.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
d=json.loads((P/'results/default.json').read_text())
assert d['experiment']==121 and d['inventory']['parents']==20 and len(d['patch_records'])==15
assert v.summarize(d['patch_records'])==d['summary']
for w,n,pool,parents in [(1,3,3,2),(2,5,10,4),(3,7,15,5)]:
 assert d['inventory'][f'width{w}_patches']==n
 assert d['inventory'][f'width{w}_equal_budget_states']==pool
 assert d['summary'][str(w)]['eligible_parents']==parents
for x in d['patch_records']:
 assert x['equal_budget_candidates']>0 and x['original_fixed_patch_candidates']>0
 assert x['raw_distance_donor_to_G0']>=0
 for key in ('donor','equal_budget','fixed_patch'):
  for t in ('6','12','24'):
   assert 0<=x[key][t]['jaccard']<=1 and 0<=x[key][t]['exact']<=1
print('exp121 smoke: PASS')
