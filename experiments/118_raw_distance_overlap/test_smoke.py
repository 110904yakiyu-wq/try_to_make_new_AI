#!/usr/bin/env python3
"""Exp118 strict combinatorial positivity/counterfactual smoke audit."""
import importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('exp118',H/'run.py');x=importlib.util.module_from_spec(s);s.loader.exec_module(x)
d=json.loads((H/'results/default.json').read_text())
assert d['experiment']==118
assert d['inventory']['parents']==20
assert len(d['patch_records'])==57
assert sum(q['null_count'] for q in d['patch_records'])==506
assert set(map(int,d['raw_gap_histogram']))=={2,4,6,8,10}
for q in d['patch_records']:
    assert q['min_extra_raw_hamming']>=2
    assert all(q['qualifying_unique_state_counts'][k] >= q['qualifying_unique_state_counts'][j] for k,j in zip(x.TIERS,x.TIERS[1:]))
    assert all(z not in q['patch'] for z in q['compensating_positions'])
for w,counts in [(1,(23,33,10,17)),(2,(14,59,9,21)),(3,(20,414,9,35))]:
    a=d['summary'][str(w)]
    assert a['physical_patches']==counts[0] and a['matched_physical_nulls']==counts[1]
    assert a['same_patch_raw_distance_overlap']==0
    assert a['compensated']['raw_distance_mask_full']['patches_with_any']==counts[2]
    assert a['compensated']['raw_distance_mask_full']['total_unique_per_patch']==counts[3]
print('exp118 smoke: PASS')
