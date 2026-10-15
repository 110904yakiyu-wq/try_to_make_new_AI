#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('exp125',P/'run.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
d=json.loads((P/'results/default.json').read_text())
assert d['experiment']==125 and len(d['parent_records'])==55
assert m.analyze(d['parent_records'])==d['summary']
a=d['summary']
assert a['G0']=={'connected':1486,'censored':143,'fragmented':17,'static':4}
assert a['control']=={'connected':1215,'censored':398,'fragmented':30,'static':7}
assert (a['lower_bound_connected_difference'],a['upper_bound_connected_difference'])==(-127,414)
assert (a['parent_robust_positive'],a['parent_robust_negative'],a['parent_indeterminate'])==(11,1,43)
for x in d['parent_records']:
 assert x['lower_delta']<=x['observed_delta']<=x['upper_delta']
 assert sum(x['G0'].values())==sum(x['control'].values())==30
print('exp125 smoke: PASS')
