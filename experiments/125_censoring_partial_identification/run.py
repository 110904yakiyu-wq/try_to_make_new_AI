#!/usr/bin/env python3
"""Experiment 125: exact parent-wise finite-time censoring bounds for Exp108.

For eventual connected-class indicator, resolved non-connected cycles are
known nonconnected; unresolved trajectories might later become connected
or not. No recensor-as-failure assumptions.
"""
import argparse,importlib.util,json,statistics
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'108_cycle_union_geometry_match'/'run.py'
spec=importlib.util.spec_from_file_location('exp108',SOURCE)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);m=v.m

def comps(support):
    remainder=set(support);n=0
    while remainder:
        n+=1;stack=[remainder.pop()]
        while stack:
            x=stack.pop()
            for y in ((x-1)%m.SIZE,(x+1)%m.SIZE):
                if y in remainder:remainder.remove(y);stack.append(y)
    return n

def classify(frame,pos,raw,ticks=500):
    new=bytearray(frame);assert new[pos]==0;new[pos]=raw
    outcome=m.orbit(new,phase=0,direction='left',max_ticks=ticks)
    if outcome['status']!='cycle':return 'censored'
    if not outcome['active']:return 'static'
    return 'connected' if comps(outcome['support'])==1 else 'fragmented'

def analyze(rows):
    total_a=Counter();total_c=Counter()
    for q in rows:
        total_a.update(q['G0']);total_c.update(q['control'])
    pairs=len(rows);denom=pairs*30
    observed=total_a['connected']-total_c['connected']
    min_possible=total_a['connected']-(total_c['connected']+total_c['censored'])
    max_possible=(total_a['connected']+total_a['censored'])-total_c['connected']
    pairs_robust_positive=sum(r['lower_delta']>0 for r in rows)
    pairs_robust_negative=sum(r['upper_delta']<0 for r in rows)
    pairs_possible_positive=sum(r['upper_delta']>0 for r in rows)
    pairs_possible_negative=sum(r['lower_delta']<0 for r in rows)
    return {'matched_parents':pairs,'material_conditions_each_arm':denom,
            'G0':dict(sorted(total_a.items())),'control':dict(sorted(total_c.items())),
            'observed_connected_difference':observed,'observed_fraction_difference':observed/denom,
            'lower_bound_connected_difference':min_possible,'upper_bound_connected_difference':max_possible,
            'lower_bound_fraction_difference':min_possible/denom,'upper_bound_fraction_difference':max_possible/denom,
            'parent_robust_positive':pairs_robust_positive,'parent_robust_negative':pairs_robust_negative,
            'parent_indeterminate':pairs-pairs_robust_positive-pairs_robust_negative,
            'parents_some_positive_possible':pairs_possible_positive,
            'parents_some_negative_possible':pairs_possible_negative}

def assay(ticks=500,attempts=100,max_parents=None):
    if ticks!=500 or attempts!=100:raise ValueError('Frozen Exp108 contract uses 500 ticks/100 attempts')
    parents=list(m.parents('left'));assert len(parents)==130 and m.CENTER==30
    rows=[];matched_n=0
    for pid,(pair,g0,parent) in enumerate(parents):
        if max_parents is not None and pid>=max_parents:break
        match=v.matched_control(pid,g0,parent,attempts)
        if match is None:continue
        ctrl,other,when=match;matched_n+=1
        assert parent['support']==other['support'] and parent['period']==other['period']
        assert all(bool(a)==bool(b) for a,b in zip(g0,ctrl))
        union=sorted(parent['support']);sites=(union[0]-1,union[-1]+1)
        ca=Counter();cb=Counter()
        for pos in sites:
            for raw in range(1,16):
                ca[classify(g0,pos,raw,ticks)]+=1
                cb[classify(ctrl,pos,raw,ticks)]+=1
        assert sum(ca.values())==sum(cb.values())==30
        lower=ca['connected']-cb['connected']-cb['censored']
        upper=ca['connected']+ca['censored']-cb['connected']
        assert lower<=ca['connected']-cb['connected']<=upper
        rows.append({'parent_id':pid,'seed':list(pair),'accepted_attempt':when,
                     'G0':dict(ca),'control':dict(cb),
                     'observed_delta':ca['connected']-cb['connected'],
                     'lower_delta':lower,'upper_delta':upper})
    result={'experiment':125,'protocol':{'physics':'unchanged 104 / 108 left direction three-phase phase0 CENTER30',
       'cohort':'all 130 G0 parents, 100 pre-material control proposals each, exact autonomous period/cycle-support/phase0 occupancy match (55 accepted)',
       'probe':'both support boundaries x raw 1..15, 30 per parent per arm, horizon500',
       'bounds':'asymptotic connected eventual class: proven connected lower, proven connected + censored upper; once recurrent cannot change without new perturbation',
       'identification':'no assumption on eventual classification for right-censored states; intervals are worst-case combinatorial bounds',
       'independence':'parent-level clusters; 1650 response probes not independent',
       'scope':'conditional 55 eligible matched parents; no claim about excluded 75'},
       'summary':analyze(rows),'parent_records':rows}
    if max_parents is None:
        s=result['summary']
        assert s['matched_parents']==55
        assert s['G0']['connected']==1486 and s['G0']['censored']==143
        assert s['control']['connected']==1215 and s['control']['censored']==398
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json');p.add_argument('--max-parents',type=int,default=None);a=p.parse_args()
    if a.max_parents is not None and a.max_parents<1:p.error('positive max-parents')
    r=assay(max_parents=a.max_parents);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'summary':r['summary']},sort_keys=True,indent=2))
if __name__=='__main__':main()
