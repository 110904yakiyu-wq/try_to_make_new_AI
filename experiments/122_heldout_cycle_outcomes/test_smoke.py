#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('exp122',P/'run.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
d=json.loads((P/'results/default.json').read_text())
assert d['experiment']==122 and d['inventory']['parents']==20 and len(d['patch_records'])==15
assert v.summarize(d['patch_records'])==d['summary']
for w,n,parents in [(1,3,2),(2,5,4),(3,7,5)]:
 assert d['inventory'][f'w{w}_patches']==n and d['summary'][str(w)]['parents']==parents
for x in d['patch_records']:
 for name in ('G0_reference','recipient_reference','transplant','equal_edit_null','fixed_patch_null'):
  assert sum(x[name][cls] for cls in v.CLASS)==24
  assert all(isinstance(x[name][cls],int) and x[name][cls]>=0 for cls in v.CLASS)
print('exp122 smoke: PASS')
