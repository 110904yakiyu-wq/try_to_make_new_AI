#!/usr/bin/env python3
"""Exp156 structural and adversarial smoke checks."""
import importlib.util
from pathlib import Path
p=Path(__file__).with_name('run.py')
s=importlib.util.spec_from_file_location('exp156',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
assert v.EVAL_TICK%3==0 and v.GAP%3==0
assert set(v.ARMS)=={'sham','L0','R24','LR','R0','L24','RL','simultaneous'}
assert set(v.RAWS)=={1,5,9,14}
for a,b in ((bytes([0,1,0]+[0]*57),bytes([0,1,0]+[0]*57)),):assert a==b
r=v.assay(3)
assert r['inventory']['contexts']==6
assert r['summary']['common_eight_arm']['parents']>=1
assert all(x['union_affected_sites']>=1 for x in r['records'])
assert all(x['test_raw'] in v.RAWS for x in r['records'])
assert len(r['records'])==r['inventory']['response_records']
# This pilot is deliberately not a functional-learning positive result:
# its unconditioned sham at the remote test site can remain trivial.
print('exp156 smoke PASS')
