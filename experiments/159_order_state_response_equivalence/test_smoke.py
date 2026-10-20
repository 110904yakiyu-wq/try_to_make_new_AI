#!/usr/bin/env python3
"""Frozen physical-state equivalence and heldout response checks."""
import importlib.util
from pathlib import Path
p=Path(__file__).with_name('run.py');spec=importlib.util.spec_from_file_location('exp159',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
r=m.assay()
assert r['inventory']['both_orders_feasible_parents']==111
assert r['inventory']['same_current_state_parents']==24
assert r['inventory']['different_current_state_parents']==87
assert r['summary']['same_current_state_probes_identical']==24
assert r['summary']['same_current_state_probe_records']==192
assert all(x['heldout_XOR_mismatching_probes']==0 for x in r['parent_records'] if x['same_full_microstate'])
assert all(x['num_heldout_probes']==8 for x in r['parent_records'])
print('exp159 smoke PASS')
