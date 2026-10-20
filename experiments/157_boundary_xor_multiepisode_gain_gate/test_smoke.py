#!/usr/bin/env python3
"""Exp157 physical-regression and heldout-panel smoke checks."""
import importlib.util,json
from pathlib import Path
p=Path(__file__).with_name('run.py')
s=importlib.util.spec_from_file_location('exp157',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
r=v.assay(3)
assert r['inventory']['contexts']==6
assert len(r['records'])==r['inventory']['response_records']
assert r['summary']['common_eight_arm']['eligible_contexts']==6
assert {x['test_mask'] for x in r['records']}==set(v.MASKS)
# Directly reconstruct first-tick physical causal response without touching
# any summary code; consistency check against reference local kernel.
state=bytes([0]*30+[7,11]+[0]*28)
site=29;mask=1;test=bytearray(state);test[site]^=mask
base1=v.m.step(state,0);test1=v.m.step(test,0)
expected=sum(a!=b for a,b in zip(base1,test1))
assert v.xor_response(state,site,mask)['instant_affected_sites'][0]==expected
assert v.xor_response(state,site,mask)['union_affected_sites']>=expected
# Markov: the XOR response is deterministic for equal full states/phase.
assert v.xor_response(state,site,mask)==v.xor_response(bytes(state),site,mask)
print('exp157 smoke PASS')
