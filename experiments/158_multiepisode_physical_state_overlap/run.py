#!/usr/bin/env python3
"""Exp158: pretest physical-overlap and observer-score selection audit.

Strictly descriptive: all treatment states were created by external pulses.
No added learner/memory and no reinterpretation as endogenous learning.
"""
import argparse,csv,importlib.util,json,statistics
from pathlib import Path
from collections import Counter,defaultdict
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
s=importlib.util.spec_from_file_location('exp157',ROOT/'157_boundary_xor_multiepisode_gain_gate'/'run.py')
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
ARMS=('sham','L0','R24','LR','R0','L24','RL','simultaneous')


def assay(src=None):
    src=Path(src or ROOT/'157_boundary_xor_multiepisode_gain_gate'/'results/default.json')
    data=json.loads(src.read_text())
    assert data['experiment']==157
    parent_rows=defaultdict(list)
    for rec in data['contexts']:
        if rec['all_eight_arms']:parent_rows[rec['parent_id']].append(rec)
    assert len(parent_rows)==data['summary']['common_eight_arm']['parents']==111
    records=[]
    for pid,ctx in sorted(parent_rows.items()):
        assert len(ctx)==2
        state=ctx[0]['pretest_physics']
        for arm in ARMS:
            s=state[arm];assert s is not None
            records.append({'parent_id':pid,'arm':arm,'popcount':s[0],'occupied_windows':s[1]})
    features={}
    for arm in ('L0','R24','LR','R0','L24','RL','simultaneous'):
        diffs=[]
        for pid,ctx in sorted(parent_rows.items()):
            s=ctx[0]['pretest_physics'];base=s['sham'];a=s[arm]
            diffs.append((a[0]-base[0],a[1]-base[1]))
        ct=Counter(diffs)
        features[arm]={'parents':len(diffs),
                       'mean_popcount_difference':statistics.mean(x[0] for x in diffs),
                       'mean_occupied_window_difference':statistics.mean(x[1] for x in diffs),
                       'equal_popcount':sum(x[0]==0 for x in diffs),
                       'equal_occupied_windows':sum(x[1]==0 for x in diffs),
                       'equal_both':ct[(0,0)],
                       'min_popcount_diff':min(x[0] for x in diffs),
                       'max_popcount_diff':max(x[0] for x in diffs)}
    # Reconstruct full pretest physical states only; response outcomes are not
    # involved in identifying equal-state overlaps.
    parent_catalog=list(v.m.parents());assert len(parent_catalog)==130
    full_overlaps={a:0 for a in ARMS if a!='sham'}
    equal_examples=[]
    for pid in sorted(parent_rows):
        _,fr,o=parent_catalog[pid]
        lo=(min(o['support'])-1)%60;hi=(max(o['support'])+1)%60
        states={arm:v.v.evolve(fr,lo,hi,events) for arm,events in v.v.ARMS.items()}
        for arm in full_overlaps:
            if states[arm]==states['sham']:
                full_overlaps[arm]+=1;equal_examples.append([pid,arm])
    # Locally use all 157 saved XOR results with no re-fitting.
    probe_file=src.parent/'probes.csv'
    with probe_file.open(newline='') as f:probes=list(csv.DictReader(f))
    assert len(probes)==data['inventory']['response_records']
    by_parent=defaultdict(lambda:defaultdict(list))
    for r in probes:
        if int(r['parent_id']) not in parent_rows:continue
        by_parent[int(r['parent_id'])][r['arm']].append(r)
    endpoint={}
    for k in ('instant_affected_t1','instant_affected_t3','instant_affected_t6',
              'instant_affected_t24','instant_affected_t60','union_affected_sites'):
        d={arm:[] for arm in ARMS};diffs={arm:[] for arm in full_overlaps}
        for pid,rec in sorted(by_parent.items()):
            means={arm:statistics.mean(int(x[k]) for x in rec[arm]) for arm in ARMS}
            for arm,val in means.items():d[arm].append(val)
            for arm in diffs:diffs[arm].append(means[arm]-means['sham'])
        endpoint[k]={'means':{arm:statistics.mean(x) for arm,x in d.items()},
                      'contrasts':{arm:{'mean':statistics.mean(x),'positive':sum(z>0 for z in x),
                                       'negative':sum(z<0 for z in x),'tied':sum(z==0 for z in x)}
                                    for arm,x in diffs.items()}}
    # Microstate equality implies identical future for all test masks.
    for pid,arm in equal_examples:
        def extract(key):
            return sorted((int(r['test_side']),int(r['test_mask']),int(r['union_affected_sites']),int(r['reached_10']))
                          for r in by_parent[pid][key])
        assert extract('sham')==extract(arm)
    return {'experiment':158,'protocol':{'source':'frozen exp157 common-eligible 111 parents; selection before heldout XOR results',
                     'physics':'unchanged 104 kernel, scheduler-aligned t96 pretest states',
                     'features':'full-state identity; 4bit popcount and occupied windows are diagnostic proxies, not sufficient state matching',
                     'inference':'factorial differences are externally induced physical susceptibility, not learning'},
            'inventory':{'parents':len(parent_rows),'response_records_considered':sum(len(vv) for x in by_parent.values() for vv in x.values())},
            'baseline_physics':features,'exact_full_state_overlaps':full_overlaps,
            'equal_full_state_examples':equal_examples,'time_resolved_response':endpoint,
            'parent_feature_records':records}

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=None)
    p.add_argument('--output',type=Path,default=HERE/'results/default.json');a=p.parse_args()
    result=assay(a.source);a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('parent_feature_records','equal_full_state_examples')},indent=2,sort_keys=True))

if __name__=='__main__':main()
