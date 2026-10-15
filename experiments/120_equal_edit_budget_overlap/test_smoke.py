#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('exp120',P/'run.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
d=json.loads((P/'results/default.json').read_text())
assert d['experiment']==120 and d['inventory']['parents']==20 and len(d['patch_records'])==57
assert sum(x['examined_assignments'] for x in d['patch_records'])==193774
for w,n,states,parents in [(1,3,3,2),(2,5,10,4),(3,7,15,5)]:
 s=d['summary'][str(w)]['eligibility']['same_distance_mask_full']
 assert s=={'patches':n,'parents':parents,'states_per_patch_sum':states}
for x in d['patch_records']:
 a=[x['pool_counts'][q] for q in v.TIERS]
 assert a==sorted(a,reverse=True)
 assert 0<=x['raw_distance_proposals']<=x['examined_assignments']
print('exp120 smoke: PASS')
