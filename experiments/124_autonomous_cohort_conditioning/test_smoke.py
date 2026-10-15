#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('exp124',P/'run.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
d=json.loads((P/'results/default.json').read_text())
assert d['experiment']==124 and len(d['patch_records'])==15
for w,n in [(1,3),(2,5),(3,7)]:
 assert sum(q['patches'] for q in d['summary'][str(w)].values())==n
assert d['summary']['3']['both_connected']['patches']==3
assert d['summary']['3']['both_connected']['parents']==2
assert abs(d['summary']['3']['both_connected']['mean_connected_difference']-1/48)<1e-12
assert d['summary']['3']['mixed_resolved']['patches']==1
for x in d['patch_records']:
 assert x['stratum'] in v.STRATA
 assert -1<=x['post_connected_diff']<=1
print('exp124 smoke: PASS')
