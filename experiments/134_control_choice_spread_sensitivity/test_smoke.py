#!/usr/bin/env python3
"""Exp134: exact candidate/probe integrity and Python-vs-C++ trace spot checks."""
from pathlib import Path
import csv,json,hashlib,importlib.util
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
s=importlib.util.spec_from_file_location('frozen127',ROOT/'127_censor_resolution_work_budget'/'build_states.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
ref=json.loads((ROOT/'133_eligible_control_multiplicity/results/default.json').read_text())
with (HERE/'results/alternative_controls.csv').open(newline='') as f:controls=list(csv.DictReader(f))
with (HERE/'results/probes.csv').open(newline='') as f:probes=list(csv.DictReader(f))
res=json.loads((HERE/'results/default.json').read_text())
assert (len(controls),len(probes))==(32,960)
assert (res['summary']['control_microstates'],res['summary']['parents_with_multiple_eligible'])==(87,22)
manifest={p['parent_id']:p for p in ref['parent_records']}
for c in controls:
    pid=int(c['parent_id']);state=bytes.fromhex(c['phase0_60_window_hex'])
    assert len(state)==60 and hashlib.sha256(state).hexdigest()==c['sha256']
    assert int(c['attempt']) in manifest[pid]['accepted_attempts'][1:]
    assert state[int(c['left'])]==state[int(c['right'])]==0
assert {(int(x['parent_id']),int(x['attempt'])) for x in controls}=={(int(x['parent_id']),int(x['attempt'])) for x in probes}
for k in ('10','60'):
    endpoint=res['summary']['endpoints'][k]
    assert endpoint['arbitrary_per_parent_choice_sensitivity_envelope'][1]<0
    assert endpoint['multi_candidate_parents_with_control_outcome_variation']==20
assert abs(res['summary']['endpoints']['10']['original_first_choice_bounds'][0]+280/1650)<1e-12
assert abs(res['summary']['endpoints']['60']['original_first_choice_bounds'][0]+253/1650)<1e-12
lookup={(int(x['parent_id']),int(x['attempt']),int(x['side']),int(x['raw'])):x for x in probes}
checkcount=0
for c in controls[:8]:
    pid=int(c['parent_id']);attempt=int(c['attempt']);base=bytes.fromhex(c['phase0_60_window_hex'])
    for side in (0,1):
        pos=int(c['left'] if side==0 else c['right'])
        for raw in (1,2,7,15):
            injected=bytearray(base);injected[pos]=raw;state=bytes(injected)
            seen={(state,0):0};covered={i for i,v in enumerate(state) if v}
            first10=0 if len(covered)>=10 else -1
            first60=0 if len(covered)>=60 else -1
            recurrence=-1
            if first60<0:
                for tick in range(1,501):
                    state=m.step(state,(tick-1)%3)
                    covered.update(i for i,v in enumerate(state) if v)
                    if first10<0 and len(covered)>=10:first10=tick
                    if first60<0 and len(covered)>=60:first60=tick
                    if first60>=0:break
                    key=(state,tick%3)
                    if key in seen:recurrence=tick;break
                    seen[key]=tick
            result=lookup[(pid,attempt,side,raw)]
            assert int(result['first10'])==first10 or (first10==-1 and int(result['first10'])>500)
            assert int(result['first60'])==first60 or (first60==-1 and int(result['first60'])>500)
            if recurrence>=0:assert int(result['recurrence'])==recurrence
            checkcount+=1
assert checkcount==64
print('exp134 smoke: PASS, independent Python traces checked:',checkcount)
