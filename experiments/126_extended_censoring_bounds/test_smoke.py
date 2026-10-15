#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('exp126',P/'run.py');x=importlib.util.module_from_spec(spec);spec.loader.exec_module(x)
d=json.loads((P/'results/default.json').read_text());s=d['summary']
assert d['experiment']==126 and len(d['parent_records'])==55
assert s['G0_newly_resolved']==0 and s['control_newly_resolved']==3
assert s['memoized_orbit_calls']=={'orbit2000_unique':532,'orbit500_unique':3270}
assert s['horizon2000']==x.bound(d['parent_records'],'2000')
assert s['horizon500']==x.bound(d['parent_records'],'500')
for key in ('horizon500','horizon2000'):
 dct=s[key]
 assert sum(dct['G0'].values())==sum(dct['control'].values())==1650
 assert dct['lower_rate_delta']<=dct['observed_rate_delta']<=dct['upper_rate_delta']
 assert dct['parent_robust_sign']=={'positive':11,'negative':1,'indeterminate':43}
print('exp126 smoke: PASS')
