#!/usr/bin/env python3
"""Experiment 131: pre-outcome physical-feature strata for monotone spread.

This is a *descriptive matched-subset* audit, not a causal mediation estimate.
Only features of the injected initial state and its unperturbed first update
are used for eligibility. No future spread outcome is used for selection.
"""
from __future__ import annotations
import argparse
import csv
import json
import statistics
import struct
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATES = ROOT / '127_censor_resolution_work_budget' / 'states.bin'
REFERENCE = ROOT / '130_spread_threshold_robustness' / 'results' / 'probes.csv'
HERE = Path(__file__).resolve().parent
TIERS = ('all', 'popcount', 'pop_and', 'pop_and_flips', 'first_changed_mask')
THRESHOLDS = (10,20,30,40,50,60)


def rotate(x):
    return ((x<<1)&15)|(x>>3)


def step(state, phase=0):
    out=bytearray(state)
    for j in range(20):
        a=(phase+3*j)%60;b=(a+1)%60;c=(a+2)%60
        x,y,z=state[a],state[b],state[c]
        out[a]=x^rotate(y&z)
        out[b]=y^rotate(x&z)
        out[c]=z^rotate(x&y)
    return bytes(out)


def features(initial):
    nxt=step(initial)
    return {
      'popcount':sum(x.bit_count() for x in initial),
      'neighbor_and':sum((initial[i]&initial[(i+1)%60]).bit_count() for i in range(60)),
      'first_flips':sum((a^b).bit_count() for a,b in zip(initial,nxt)),
      'first_changed_mask':sum(1<<i for i,(a,b) in enumerate(zip(initial,nxt)) if a!=b),
    }


def load_states(path):
    blob=Path(path).read_bytes()
    assert len(blob)==55*124
    out={}
    for k in range(0,len(blob),124):
        pid,attempt,left,right=struct.unpack('<BBBB',blob[k:k+4])
        g=blob[k+4:k+64];c=blob[k+64:k+124]
        assert pid not in out and all(x<16 for x in g+c)
        out[pid]=(g,c,left,right,attempt)
    assert len(out)==55
    return out


def read_pairs(path):
    with Path(path).open(newline='') as f:
        data=list(csv.DictReader(f))
    assert len(data)==3300
    grouped=defaultdict(dict)
    for x in data:
        row={key:int(v) for key,v in x.items()}
        key=(row['parent_id'],row['side'],row['raw'])
        assert row['arm'] not in grouped[key]
        grouped[key][row['arm']]=row
    assert len(grouped)==1650 and all(set(x)=={0,1} for x in grouped.values())
    return grouped


def label(rec,k):
    hit=rec[f'first{k}']
    if 0<=hit<=50000:return 'yes'
    if 0<=rec['recurrence']<=50000:return 'no'
    return 'unknown'


def pair_bounds(pair,k):
    a=label(pair[0],k);b=label(pair[1],k)
    # Potentially eventual Bernoulli outcomes for censored status.
    alo,ahi=(1,1) if a=='yes' else ((0,0) if a=='no' else (0,1))
    blo,bhi=(1,1) if b=='yes' else ((0,0) if b=='no' else (0,1))
    return alo-bhi,ahi-blo,a,b


def analyze(states,grouped):
    pairs=[]
    for (pid,side,raw), arms in sorted(grouped.items()):
        g,c,left,right,attempt=states[pid]
        site=left if side==0 else right
        assert g[site]==c[site]==0
        vectors=[]
        for state in (g,c):
            buf=bytearray(state);buf[site]=raw
            vectors.append(features(bytes(buf)))
        same={
          'all':True,
          'popcount':vectors[0]['popcount']==vectors[1]['popcount'],
        }
        same['pop_and']=same['popcount'] and vectors[0]['neighbor_and']==vectors[1]['neighbor_and']
        same['pop_and_flips']=same['pop_and'] and vectors[0]['first_flips']==vectors[1]['first_flips']
        same['first_changed_mask']=same['pop_and_flips'] and vectors[0]['first_changed_mask']==vectors[1]['first_changed_mask']
        pairs.append({'parent_id':pid,'side':side,'raw':raw,'tiers':same,
                      'g0_features':vectors[0],'control_features':vectors[1],
                      'status':{str(k):{'g0':label(arms[0],k),'control':label(arms[1],k)} for k in THRESHOLDS}})
    out={}
    for tier in TIERS:
        selected=[p for p in pairs if p['tiers'][tier]]
        cluster=defaultdict(list)
        for p in selected:cluster[p['parent_id']].append(p)
        sub={'eligible_probes':len(selected),'eligible_parents':len(cluster),
             'parent_probe_histogram':dict(sorted(Counter(len(v) for v in cluster.values()).items())),'endpoints':{}}
        for k in THRESHOLDS:
            arm_counts={'G0':Counter(),'control':Counter()}
            sums=[];parent_sign=Counter();pair_sign=Counter()
            for pid,items in sorted(cluster.items()):
                lo=hi=0
                for p in items:
                    a=p['status'][str(k)]['g0'];b=p['status'][str(k)]['control']
                    arm_counts['G0'][a]+=1;arm_counts['control'][b]+=1
                    al,ah=(1,1) if a=='yes' else ((0,0) if a=='no' else (0,1))
                    bl,bh=(1,1) if b=='yes' else ((0,0) if b=='no' else (0,1))
                    low=al-bh;high=ah-bl
                    lo+=low;hi+=high
                    pair_sign['G0_certain']+=low>0
                    pair_sign['control_certain']+=high<0
                    pair_sign['unidentified_or_tied']+=low<=0<=high
                sums.append((lo/len(items),hi/len(items)))
                parent_sign['G0_certain']+=lo>0
                parent_sign['control_certain']+=hi<0
                parent_sign['unidentified_or_tied']+=lo<=0<=hi
            total=len(selected)
            g=arm_counts['G0'];c=arm_counts['control']
            # Partial-identification for pooled and parent-equal estimands.
            low=g['yes']-c['yes']-c['unknown'];high=g['yes']+g['unknown']-c['yes']
            sub['endpoints'][str(k)]={
               'G0':dict(sorted(g.items())),'control':dict(sorted(c.items())),
               'pooled_delta_bounds':[low/total,high/total] if total else None,
               'parent_equal_delta_bounds':[statistics.mean(a for a,b in sums),statistics.mean(b for a,b in sums)] if sums else None,
               'parent_signs':dict(parent_sign),'probe_signs':dict(pair_sign)}
        out[tier]=sub
    return {'experiment':131,'protocol':{
            'cohort':'frozen 55 exact 108-matched parent pairs; 1650 paired probes, initial states from 127',
            'physical_kernel':'original 104/108 60-window phase0, left rotation; no new rules',
            'conditions':list(TIERS),
            'matching':'nested exact equality of post-injection initial popcount, neighbor AND, autonomous first-step Hamming flips and first-step changed-site mask',
            'event':'eventual cumulative union ever reaches K; only exact recurrence certifies absence by 50k',
            'thresholds':list(THRESHOLDS),'horizon':50000,
            'selection':'physical variables at t=0 and t=1 only, no post-t1 outcome screening',
            'limitation':'selected physical strata may be biased and small; no causal identification or equal outcome sampling'},
            'strata':out,'pair_records':pairs}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--states',type=Path,default=STATES)
    ap.add_argument('--reference',type=Path,default=REFERENCE)
    ap.add_argument('--output',type=Path,default=HERE/'results'/'default.json')
    ap.add_argument('--csv',type=Path,default=HERE/'results'/'paired_features.csv')
    args=ap.parse_args()
    result=analyze(load_states(args.states),read_pairs(args.reference))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps({k:v for k,v in result.items() if k!='pair_records'},sort_keys=True,indent=2)+'\n')
    args.csv.parent.mkdir(parents=True,exist_ok=True)
    columns=['parent_id','side','raw','popcount_equal','and_equal','flips_equal','first_mask_equal',
             'g0_popcount','control_popcount','g0_neighbor_and','control_neighbor_and',
             'g0_first_flips','control_first_flips','g0_first_changed_mask','control_first_changed_mask']+\
             [f'{arm}_K{k}' for k in THRESHOLDS for arm in ('g0','control')]
    with args.csv.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=columns,lineterminator='\n');w.writeheader()
        for q in result['pair_records']:
            a={'parent_id':q['parent_id'],'side':q['side'],'raw':q['raw']}
            a.update({name+'_equal':int(q['g0_features'][key]==q['control_features'][key]) for name,key in
                      [('popcount','popcount'),('and','neighbor_and'),('flips','first_flips'),('first_mask','first_changed_mask')]})
            for arm,features in [('g0',q['g0_features']),('control',q['control_features'])]:
                for key,value in features.items():a[arm+'_'+key]=value
            for k in THRESHOLDS:
                for arm in ('g0','control'):a[arm+'_K'+str(k)]=q['status'][str(k)][arm]
            w.writerow(a)
    for tier,s in result['strata'].items():
        print(tier,'paired_probes',s['eligible_probes'],'parents',s['eligible_parents'])
        for k in (10,60):
            q=s['endpoints'][str(k)]
            print('  threshold',k,'G0',q['G0'],'control',q['control'],'pooled_bounds',q['pooled_delta_bounds'],'parent_equal_bounds',q['parent_equal_delta_bounds'],'parent_signs',q['parent_signs'])

if __name__=='__main__':main()
