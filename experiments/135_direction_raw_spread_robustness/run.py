#!/usr/bin/env python3
"""Exp135: raw-value and side stratification of exact finite-state spread certificates.
No new simulation; all 3300 trajectories are frozen Experiment 130 records.
"""
import argparse, csv, json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'130_spread_threshold_robustness/results/probes.csv'

def load(path):
    with Path(path).open(newline='',encoding='utf-8') as f:
        rows=[{key:int(v) for key,v in r.items()} for r in csv.DictReader(f)]
    keys=[(r['parent_id'],r['arm'],r['side'],r['raw']) for r in rows]
    assert len(rows)==len(set(keys))==3300
    assert len({r['parent_id'] for r in rows})==55
    for pid in {r['parent_id'] for r in rows}:
        assert {(r['arm'],r['side'],r['raw']) for r in rows if r['parent_id']==pid}=={(a,s,v) for a in (0,1) for s in (0,1) for v in range(1,16)}
    return rows

def cls(r,k):
    t=r[f'first{k}']
    if t>=0:
        assert t<=50000
        return 'yes'
    return 'no' if r['recurrence']>=0 else 'unknown'

def evaluate(rows,k):
    a,b=(Counter(cls(r,k) for r in rows if r['arm']==arm) for arm in (0,1))
    n=sum(a.values())
    assert n==sum(b.values())
    lo=a['yes']-b['yes']-b['unknown']
    hi=a['yes']+a['unknown']-b['yes']
    return {'paired_conditions':n,'G0':dict(a),'control':dict(b),'difference_lower':lo/n,'difference_upper':hi/n,'numerator_lower':lo,'numerator_upper':hi,'negative_sign_identified':hi<0}

def assay(path=SOURCE):
    rows=load(path)
    result={'experiment':135,'data_source':'Experiment 130 unchanged individual probes','matched_parents':55,'input_sha_git_blob':'9ac5ca7e81fddd11d205248d9995f6cc2a8efd5e','status':'reanalysis only; not independent experimental evidence', 'thresholds':{}}
    for k in (10,60):
        grp={'overall':evaluate(rows,k),'by_side':{('left' if s==0 else 'right'):evaluate([r for r in rows if r['side']==s],k) for s in (0,1)},'by_raw':{str(v):evaluate([r for r in rows if r['raw']==v],k) for v in range(1,16)}}
        assert all(v['negative_sign_identified'] for v in list(grp['by_side'].values())+list(grp['by_raw'].values()))
        result['thresholds'][str(k)]=grp
    assert result['thresholds']['10']['overall']['numerator_lower']==-280
    assert result['thresholds']['60']['overall']['numerator_lower']==-253
    assert result['thresholds']['60']['overall']['numerator_upper']==-252
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=SOURCE);p.add_argument('--output',type=Path,default=HERE/'results/default.json');a=p.parse_args()
    z=assay(a.source);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(z,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k: {'overall':v['overall'],'by_side':v['by_side']} for k,v in z['thresholds'].items()},indent=2,sort_keys=True))
if __name__=='__main__':main()
