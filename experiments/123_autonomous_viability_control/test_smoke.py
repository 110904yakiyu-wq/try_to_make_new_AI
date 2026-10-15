#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('exp123',P/'run.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
d=json.loads((P/'results/default.json').read_text())
assert d['experiment']==123 and d['inventory']['parents']==20 and len(d['patch_records'])==15
assert v.aggregate(d['patch_records'])==d['summary']
for w,n in [(1,3),(2,5),(3,7)]:assert d['inventory'][f'w{w}_patches']==n
for q in d['patch_records']:
 for name in v.ARMS:
  state=q[name]
  assert state['censored_2000']<=state['censored_500']
  assert state['recurrence_tick'] is None or state['recurrence_tick']<=2000
  assert state['censored_500']==(state['recurrence_tick'] is None or state['recurrence_tick']>500)
assert d['summary']['3']['transplant_censored_500_mean']==0.4
print('exp123 smoke: PASS')
