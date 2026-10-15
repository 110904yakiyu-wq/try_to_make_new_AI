#!/usr/bin/env python3
"""Exp133: enumerate all 100 pre-intervention exact-geometry eligible controls per original G0 parent.

No material injection or future outcome classification participates in null eligibility.
"""
import importlib.util,hashlib,json,random,argparse,statistics,time
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
spec=importlib.util.spec_from_file_location('frozen127', ROOT/'127_censor_resolution_work_budget'/'build_states.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def classify_candidates(index,frame,parent,attempts=100):
    matches=[]
    for attempt in range(attempts):
        rng=random.Random(3_000_000+index*300_000+attempt)
        cand=bytes(rng.randrange(1,16) if x else 0 for x in frame)
        o=m.orbit(cand,max_ticks=500)
        if o['status']!='cycle' or not o['active'] or o['period']!=parent['period'] or o['support']!=parent['support']:continue
        phase0=[fr for j,fr in enumerate(o['cycle']) if (o['phase']+j)%3==0]
        ctrl=max(phase0,key=lambda x:sum(bool(q) for q in x))
        if any(bool(a)!=bool(b) for a,b in zip(ctrl,frame)):continue
        matches.append((attempt+1,ctrl,o['period']))
    return matches

def assay(start=0,limit=130):
    manifest={pid:(a,b,attempt) for pid,a,b,attempt in m.MANIFEST}
    records=[];n=0;t0=time.monotonic()
    for pid,(seed,frame,parent) in enumerate(m.parents()):
        if pid>=limit:break
        if pid<start:continue
        x=classify_candidates(pid,frame,parent)
        expected=manifest.get(pid)
        assert (bool(x)==(expected is not None)),('eligibility mismatch',pid)
        if expected:
            assert x[0][0]==expected[2],('first match attempt mismatch',pid)
            assert seed==(expected[0],expected[1])
        unique={ctrl for _,ctrl,_ in x}
        records.append({'parent_id':pid,'seed':list(seed),'period':parent['period'],
                        'union_support':sorted(parent['support']),'num_eligible_candidates':len(x),
                        'num_unique_phase0_microstates':len(unique),'accepted_attempts':[a for a,_,_ in x],
                        'accepted_microstate_sha256':[hashlib.sha256(ctrl).hexdigest() for _,ctrl,_ in x]})
        n+=len(x)
    return {'experiment':133,'contract':{'parents':limit-start,'catalog_start':start,'catalog_stop':limit,'attempts':100,'kernel':'original finite-speed 104/108 phase0 left-rotation; size 60 center 30',
        'eligibility':'autonomous cycle period, exact cycle-union support positions, phase-zero instantaneous occupancy and scheduler phase',
        'selection':'No injected outcomes used; entire frozen attempt budget enumerated',
        'original_control':'first accepted exact candidate, independently compared to 127 frozen manifest'},
        'summary':{'parents_inspected':len(records),'eligible_parents':sum(bool(x['num_eligible_candidates']) for x in records),
        'parents_with_multiple_eligible':sum(x['num_eligible_candidates']>1 for x in records),
        'parents_with_multiple_distinct_controls':sum(x['num_unique_phase0_microstates']>1 for x in records),
        'total_accepted_candidates':n,
        'accepted_histogram':dict(sorted(Counter(x['num_eligible_candidates'] for x in records).items())),
        'unique_state_histogram':dict(sorted(Counter(x['num_unique_phase0_microstates'] for x in records).items()))},
        'parent_records':records}

def main():
    p=argparse.ArgumentParser();p.add_argument('--max-parents',type=int,default=130);p.add_argument('--start-parent',type=int,default=0)
    p.add_argument('--output',type=Path,default=HERE/'results/default.json')
    args=p.parse_args();r=assay(args.start_parent,args.max_parents)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps(r['summary'],sort_keys=True,indent=2))
if __name__=='__main__':main()
