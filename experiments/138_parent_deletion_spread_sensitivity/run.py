#!/usr/bin/env python3
"""Exp138: worst-case parent deletions on frozen exact spread records.
Sensitivity envelope only. Not a parent sampling model or a hypothesis test.
"""
import argparse,csv,json
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'130_spread_threshold_robustness/results/probes.csv'

def endpoint(rows,threshold):
    statuses={a:Counter('yes' if r[f'first{threshold}']>=0 else 'no' if r['recurrence']>=0 else 'unknown' for r in rows if r['arm']==a) for a in (0,1)}
    a,b=statuses[0],statuses[1]
    return (a['yes']-b['yes']-b['unknown'], a['yes']+a['unknown']-b['yes'])

def assay(source=SOURCE):
    with Path(source).open(newline='',encoding='utf-8') as f:
        rows=[{k:int(v) for k,v in x.items()} for x in csv.DictReader(f)]
    by_parent=defaultdict(list)
    for r in rows:by_parent[r['parent_id']].append(r)
    assert len(by_parent)==55 and all(len(r)==60 for r in by_parent.values())
    results={'experiment':138,'source':'frozen Exp130 records','notes':'Exact extremal deletion over 55 eligible parent clusters. Deletion chosen post-outcome is a sensitivity stress test only.','endpoints':{}}
    for k in (10,60):
        vals={pid:endpoint(p,k) for pid,p in by_parent.items()}
        assert all(-30<=lo<=hi<=30 for lo,hi in vals.values())
        loall=sum(x[0] for x in vals.values());hiall=sum(x[1] for x in vals.values())
        # To make retained difference as large as possible after k deletions,
        # retain the 55-k parents with highest parent-specific upper bounds.
        lo_sorted=sorted((x[0] for x in vals.values()))
        hi_sorted=sorted((x[1] for x in vals.values()),reverse=True)
        envelopes={}
        for deleted in range(0,55):
            retained=55-deleted
            worst_lower=sum(lo_sorted[:retained])/(30*retained)
            worst_upper=sum(hi_sorted[:retained])/(30*retained)
            envelopes[str(deleted)]={'retained_parents':retained,'lower_fraction_over_all_retained_subsets':worst_lower,'upper_fraction_over_all_retained_subsets':worst_upper,'guaranteed_negative_after_any_deletions':worst_upper<0}
        first_k=next((i for i,q in envelopes.items() if q['upper_fraction_over_all_retained_subsets']>=0),None)
        results['endpoints'][str(k)]={'full_lower':loall/1650,'full_upper':hiall/1650,
            'parent_strict_g0_advantage':sum(lo>0 for lo,hi in vals.values()),
            'parent_strict_control_advantage':sum(hi<0 for lo,hi in vals.values()),
            'parent_tied_or_unknown':sum(lo<=0<=hi for lo,hi in vals.values()),
            'parent_bounds':{str(pid):{'lower':lo,'upper':hi} for pid,(lo,hi) in sorted(vals.items())},
            'smallest_deleted_parents_for_sign_not_guaranteed':int(first_k) if first_k is not None else None,
            'envelopes':envelopes}
    assert results['endpoints']['10']['full_lower']==-280/1650
    assert results['endpoints']['60']['full_lower']==-253/1650
    assert results['endpoints']['60']['full_upper']==-252/1650
    return results

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=SOURCE);ap.add_argument('--output',type=Path,default=HERE/'results/default.json');args=ap.parse_args()
    data=assay(args.source);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:{t:v[t] for t in ('full_lower','full_upper','parent_strict_g0_advantage','parent_strict_control_advantage','parent_tied_or_unknown','smallest_deleted_parents_for_sign_not_guaranteed')} for k,v in data['endpoints'].items()},indent=2,sort_keys=True))
if __name__=='__main__':main()
