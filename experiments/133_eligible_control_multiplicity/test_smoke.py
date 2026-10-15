#!/usr/bin/env python3
"""Frozen-eligibility integrity checks for Experiment 133."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'results/default.json').read_text())
assert r['experiment']==133
s=r['summary']
assert (s['parents_inspected'],s['eligible_parents'],s['parents_with_multiple_eligible'],s['total_accepted_candidates'])==(130,55,22,87)
assert s['accepted_histogram']=={'0':75,'1':33,'2':16,'3':3,'4':2,'5':1}
assert len(r['parent_records'])==130
assert [p['parent_id'] for p in r['parent_records']]==list(range(130))
from collections import Counter
assert len({(p['parent_id'],p['seed'][0],p['seed'][1]) for p in r['parent_records']})==130
for rec in r['parent_records']:
    n=rec['num_eligible_candidates']
    assert n==len(rec['accepted_attempts'])==len(rec['accepted_microstate_sha256'])
    assert 0<=n<=5 and n==rec['num_unique_phase0_microstates']
    assert rec['accepted_attempts']==sorted(set(rec['accepted_attempts']))
    assert all(1<=x<=100 for x in rec['accepted_attempts'])
    assert len(set(rec['accepted_microstate_sha256']))==n
print('exp133 smoke: PASS')
