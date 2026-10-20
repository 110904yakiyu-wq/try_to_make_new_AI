#!/usr/bin/env python3
"""Exp158 audit invariants over frozen 157 observations."""
import importlib.util,json
from pathlib import Path
p=Path(__file__).with_name('run.py');s=importlib.util.spec_from_file_location('exp158',p)
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
r=v.assay()
assert r['inventory']['parents']==111
assert r['inventory']['response_records_considered']==7104
assert r['baseline_physics']['LR']['equal_both']==0
assert r['baseline_physics']['RL']['equal_both']==0
assert all(n==0 for n in r['exact_full_state_overlaps'].values())
assert r['time_resolved_response']['union_affected_sites']['contrasts']['LR']['mean']>0
assert r['time_resolved_response']['instant_affected_t1']['contrasts']['LR']['mean'] < r['time_resolved_response']['instant_affected_t24']['contrasts']['LR']['mean']
print('exp158 smoke PASS')
