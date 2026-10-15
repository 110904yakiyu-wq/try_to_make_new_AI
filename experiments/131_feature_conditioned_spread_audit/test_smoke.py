#!/usr/bin/env python3
"""Invariant and reproducibility tests for Experiment 131."""
import csv
import importlib.util
import json
import math
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('exp131',HERE/'run.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test():
    results=json.loads((HERE/'results/default.json').read_text())
    assert results['experiment']==131
    assert list(results['strata'])==sorted(m.TIERS), 'JSON sort-keys ordering expected'
    expected={'all':(1650,55),'popcount':(450,15),'pop_and':(168,14),
              'pop_and_flips':(126,10),'first_changed_mask':(102,6)}
    for tier,(n,p) in expected.items():
        entry=results['strata'][tier]
        assert (entry['eligible_probes'],entry['eligible_parents'])==(n,p)
    full=results['strata']['all']['endpoints']
    assert (full['10']['G0']['yes'],full['10']['control']['yes'])==(173,453)
    assert (full['60']['G0']['yes'],full['60']['control']['yes'])==(143,395)
    assert full['60']['control']['unknown']==1
    for tier in m.TIERS:
        a=results['strata'][tier]['endpoints']
        for k in m.THRESHOLDS:
            z=a[str(k)];n=results['strata'][tier]['eligible_probes']
            assert sum(z['G0'].values())==sum(z['control'].values())==n
            l,h=z['pooled_delta_bounds'];assert l<=h
            assert sum(z['parent_signs'].values())==results['strata'][tier]['eligible_parents']
    # Verify the local step independently against the frozen 127 reconstruction.
    spec2=importlib.util.spec_from_file_location('exp127_builder',m.ROOT/'127_censor_resolution_work_budget'/'build_states.py')
    b=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(b)
    states=m.load_states(m.STATES)
    for pid in list(states)[:10]:
        for base in states[pid][:2]:
            for site in (states[pid][2],states[pid][3]):
                for raw in (1,7,15):
                    x=bytearray(base);x[site]=raw
                    assert m.step(bytes(x))==b.step(bytes(x),0)
    # Individual probe CSV is lossless for equality bits and outcome labels.
    with (HERE/'results/paired_features.csv').open(newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==1650
    assert sum(int(x['popcount_equal']) for x in rows)==450
    assert sum(int(x['popcount_equal']) and int(x['and_equal']) for x in rows)==168
    assert sum(int(x['popcount_equal']) and int(x['and_equal']) and int(x['flips_equal']) for x in rows)==126
    assert sum(int(x['popcount_equal']) and int(x['and_equal']) and int(x['flips_equal']) and int(x['first_mask_equal']) for x in rows)==102
    assert sum(x['g0_K10']=='yes' for x in rows)==173
    assert sum(x['control_K10']=='yes' for x in rows)==453
    print('exp131 smoke: PASS')

if __name__=='__main__':test()
