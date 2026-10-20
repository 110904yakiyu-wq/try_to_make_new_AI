#!/usr/bin/env python3
"""Exp151: does a *single prior external pulse* alter heldout causal response?

No learner, optimization, rewards, or new kernel primitives. Every response
compares heldout-injected vs no-heldout trajectories of its OWN prior state.
This is a functional susceptibility pilot, NOT a test proving learning.
"""
import argparse
import csv
import csv
import importlib.util
import json
import statistics
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CORE = ROOT / '139_extended_control_budget' / 'core.py'
spec = importlib.util.spec_from_file_location('exp139_physics', CORE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
assert m.SIZE == 60 and m.CENTER == 30

DELAYS = (24, 96)                # divisible by scheduler period three
TRAIN_VALUES = (0, 7, 11)      # 0: sham; raw7 and raw11: same popcount=3
TEST_RAW = (1, 5, 9, 14)       # never used for conditioning or control selection
TRACE_HORIZON = 60
SAMPLE_TIMES = (6, 24, 60)
ARMS = {0: 'sham', 7: 'pulse7', 11: 'pulse11'}


def evolve(start, n):
    state = bytes(start)
    for tick in range(n):
        state = m.step(state, tick % 3)
    return state


def response(frame, site, raw, horizon=TRACE_HORIZON):
    """Physical difference from OWN time- and phase-aligned no-test trajectory."""
    if frame[site]:
        raise ValueError('Cannot inject raw material into occupied site')
    base = bytes(frame)
    test = bytearray(frame)
    test[site] = raw
    test = bytes(test)
    union = 0
    trajectory = {}
    for tick in range(1, horizon+1):
        phase = (tick-1) % 3
        base = m.step(base, phase)
        test = m.step(test, phase)
        mask = sum(1 << i for i,(a,b) in enumerate(zip(base,test)) if a != b)
        union |= mask
        if tick in SAMPLE_TIMES:
            trajectory[str(tick)] = {'affected_sites': mask.bit_count(),
                                     'bit_difference': sum((a^b).bit_count() for a,b in zip(base,test)),
                                     'union_affected_sites': union.bit_count()}
    return {'union_affected_sites': union.bit_count(),
            'reached_10': union.bit_count() >= 10,
            'reached_30': union.bit_count() >= 30,
            'samples':trajectory}


def summary(rows):
    # Equal-weight parent groups, not independent probes; two sides and two
    # delays are repeated measures within the same original G0 parent.
    out = {}
    for delay in DELAYS:
        subset = [r for r in rows if r['delay'] == delay]
        for endpoint in ('union_affected_sites','reached_10','reached_30'):
            parent_data = defaultdict(lambda: defaultdict(list))
            for item in subset:
                parent_data[item['parent_id']][item['arm']].append(float(item[endpoint]))
            valid = {pid:arms for pid,arms in parent_data.items() if all(name in arms for name in ARMS.values())}
            means = {name:statistics.mean(statistics.mean(v[name]) for v in valid.values()) if valid else None for name in ARMS.values()}
            contrast = {}
            for treatment in ('pulse7','pulse11'):
                diffs = [statistics.mean(v[treatment])-statistics.mean(v['sham']) for v in valid.values()]
                contrast[treatment+'-sham'] = {'mean':statistics.mean(diffs) if diffs else None,
                                              'parent_positive':sum(x>0 for x in diffs),
                                              'parent_negative':sum(x<0 for x in diffs),
                                              'parent_tied':sum(x==0 for x in diffs)}
            diffs = [statistics.mean(v['pulse7'])-statistics.mean(v['pulse11']) for v in valid.values()]
            contrast['pulse7-pulse11'] = {'mean':statistics.mean(diffs) if diffs else None,
                                         'parent_positive':sum(x>0 for x in diffs),
                                         'parent_negative':sum(x<0 for x in diffs),
                                         'parent_tied':sum(x==0 for x in diffs)}
            out[f'{delay}:{endpoint}']={'eligible_parent_clusters':len(valid),
                                     'eligible_side_contexts':len({(r['parent_id'],r['train_side']) for r in subset}),
                                     'heldout_records_per_arm':len(subset)//3,
                                     'arm_means':means,'contrasts':contrast}
    return out


def assay(limit=130):
    assert 1<=limit<=130
    parents = list(m.parents())
    assert len(parents)==130
    out = []
    eligibility=[]
    for pid,(seed,frame,orbit) in enumerate(parents[:limit]):
        support = sorted(orbit['support'])
        left = (support[0]-1)%m.SIZE
        right = (support[-1]+1)%m.SIZE
        assert left!=right and not frame[left] and not frame[right]
        for train_side,train_site,test_site in ((0,left,right),(1,right,left)):
            for delay in DELAYS:
                states={raw:evolve(bytes(bytearray(frame[:train_site])+bytes([raw])+frame[train_site+1:]) if raw else frame,delay)
                        for raw in TRAIN_VALUES}
                eligible=all(s[test_site]==0 for s in states.values())
                eligibility.append({'parent_id':pid,'train_side':train_side,'delay':delay,
                                    'eligible':eligible,
                                    'occupied_test_site_by_arm':{ARMS[r]:states[r][test_site]!=0 for r in TRAIN_VALUES},
                                    'same_full_state_sham_pulse7':states[0]==states[7],
                                    'same_full_state_pulse7_pulse11':states[7]==states[11],
                                    'physical_bits_before_test':{ARMS[r]:sum(x.bit_count() for x in states[r]) for r in TRAIN_VALUES},
                                    'occupied_windows_before_test':{ARMS[r]:sum(bool(x) for x in states[r]) for r in TRAIN_VALUES}})
                if not eligible:
                    continue
                for raw in TEST_RAW:
                    for train_raw in TRAIN_VALUES:
                        resp=response(states[train_raw],test_site,raw)
                        out.append({'parent_id':pid,'seed':list(seed),'train_side':train_side,'delay':delay,
                                    'train_raw':train_raw,'arm':ARMS[train_raw],
                                    'test_side':1-train_side,'test_raw':raw,**resp})
    assert len(eligibility)==4*limit
    assert len(out)==sum(x['eligible'] for x in eligibility)*len(TEST_RAW)*len(TRAIN_VALUES)
    return {'experiment':151,'protocol':{'kernel':'unchanged 60x4bit phase0 left rotation 3-scheduler 104/139',
                   'parents':'original G0 parent catalog; no matched-control filter',
                   'train':'one externally introduced raw pulse on original cycle-union boundary; sham=0, equal-popcount raw7 or raw11',
                   'timing':'start from G0 phase0; wait 24 or 96 ticks; then test starts from phase0',
                   'test':'opposite original boundary x raw (1,5,9,14), never train raw values',
                   'test_site':'must be empty before injecting for ALL three arms, pretest eligibility',
                   'metric':'union over 60 ticks of physical positions changed vs each arm own no-test, phase-identical orbit',
                   'primary':'parent-average pulse7-sham contrast in union affected sites; pulse11 same-popcount specificity negative control',
                   'censor':'finite-window causal response, not asymptotic cycle or survival; no censor substitution',
                   'scope':'a single external pulse is not learning, and lower response spread is only observer-defined utility'},
            'inventory':{'catalog_parents':len(parents),'processed_parents':limit,
                        'context_count':len(eligibility),'eligible_contexts':sum(x['eligible'] for x in eligibility),
                        'ineligible_contexts':sum(not x['eligible'] for x in eligibility),
                        'per_arm_probe_records':len(out)//3,'total_response_records':len(out)},
            'summary':summary(out),'eligibility_records':eligibility,'probe_records':out}


def write_csv(path, rows, keys):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n')
        w.writeheader()
        for x in rows:w.writerow(x)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=HERE/'results/default.json')
    ap.add_argument('--probes',type=Path,default=HERE/'results/probes.csv')
    ap.add_argument('--eligibility',type=Path,default=HERE/'results/eligibility.csv')
    ap.add_argument('--max-parents',type=int,default=130)
    args=ap.parse_args()
    result=assay(args.max_parents)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    # Summary metadata in JSON; lossless row observations in CSV to avoid
    # duplicating bulky per-tick trajectories in two serialized formats.
    summary={k:v for k,v in result.items() if k not in ('eligibility_records','probe_records')}
    args.output.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    keys=['parent_id','seed_a','seed_b','train_side','delay','train_raw','arm',
          'test_side','test_raw','union_affected_sites','reached_10','reached_30']
    keys+=['affected_sites_t'+str(t) for t in SAMPLE_TIMES]
    keys+=['bit_difference_t'+str(t) for t in SAMPLE_TIMES]
    keys+=['union_affected_sites_t'+str(t) for t in SAMPLE_TIMES]
    flattened=[]
    for row in result['probe_records']:
        x={k:row[k] for k in keys if k in row}
        x['seed_a'],x['seed_b']=row['seed']
        for t in SAMPLE_TIMES:
            y=row['samples'][str(t)]
            for key in ('affected_sites','bit_difference','union_affected_sites'):
                x[f'{key}_t{t}']=y[key]
        flattened.append(x)
    write_csv(args.probes,flattened,keys)
    ek=['parent_id','train_side','delay','eligible','same_full_state_sham_pulse7','same_full_state_pulse7_pulse11']
    for field in ('occupied_test_site_by_arm','physical_bits_before_test','occupied_windows_before_test'):
        ek += [field+'_'+arm for arm in ARMS.values()]
    ers=[]
    for row in result['eligibility_records']:
        x={k:row[k] for k in ek if k in row}
        for field in ('occupied_test_site_by_arm','physical_bits_before_test','occupied_windows_before_test'):
            for arm in ARMS.values(): x[field+'_'+arm]=row[field][arm]
        ers.append(x)
    write_csv(args.eligibility,ers,ek)
    print(json.dumps({'inventory':result['inventory'],'summary':result['summary']},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
