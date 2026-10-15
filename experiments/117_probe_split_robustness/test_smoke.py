#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('exp117',H/'run.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
d=json.loads((H/'results/default.json').read_text())
assert d['experiment']==117
assert d['inventory']=={'parents':20,'qualified_by_width':{'1':23,'2':14,'3':20},'qualified_patches':57,'total_physical_null_states':506}
assert len(d['patch_records'])==57
assert m.aggregate(d['patch_records'])==d['summary']
assert sorted(q for fold in m.FOLDS for q in fold)==list(range(1,16))
for w in (1,2,3):
  a=d['summary'][str(w)];base=a['0']
  assert all(a[str(i)]['parents']==base['parents'] and a[str(i)]['patches']==base['patches'] for i in range(5))
  assert all(len(a[str(i)]['heldout_raw_values'])==12 for i in range(5))
  assert all(-1<=a[str(i)]['24_jaccard_diff']<=1 for i in range(5))
  assert a['across_folds']['n_parents']==base['parents']
# Fold zero exactly repeats 116 nearest-1 result using raw(1,7,15).
prev=json.loads((H.parent/'116_approximate_response_matching/results/default.json').read_text())
for w in (1,2,3):
 assert abs(d['summary'][str(w)]['0']['24_jaccard_diff']-prev['summary'][str(w)]['nearest1']['24_jaccard_diff'])<1e-12
print('exp117 smoke: PASS')
