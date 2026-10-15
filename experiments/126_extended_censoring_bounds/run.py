#!/usr/bin/env python3
"""Experiment 126: Exp125 full 55-parent horizon extension 500 -> 2000.

Only unresolved 500-tick states require additional 2000-tick orbit evaluation.
Cache by the exact (initial full microstate, phase0) input to avoid duplicate
calculations; count probes/parents independently for descriptive aggregation.
"""
import argparse,importlib.util,json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('exp125',ROOT/'125_censoring_partial_identification'/'run.py')
v=importlib.util.module_from_spec(s);s.loader.exec_module(v);m=v.m


def classify_state(state,horizon):
    o=m.orbit(state,phase=0,direction='left',max_ticks=horizon)
    if o['status']!='cycle':return 'censored'
    if not o['active']:return 'static'
    return 'connected' if v.comps(o['support'])==1 else 'fragmented'

def bound(records,field):
    g=Counter();c=Counter();robust=Counter()
    for r in records:
        a=Counter(r['G0_'+field]);b=Counter(r['control_'+field])
        g.update(a);c.update(b)
        lower=a['connected']-b['connected']-b['censored']
        upper=a['connected']+a['censored']-b['connected']
        robust['positive']+=lower>0
        robust['negative']+=upper<0
        robust['indeterminate']+=not (lower>0 or upper<0)
    n=len(records)*30
    return {'G0':dict(sorted(g.items())),'control':dict(sorted(c.items())),
            'n_per_arm':n,
            'observed_connected_delta':g['connected']-c['connected'],
            'observed_rate_delta':(g['connected']-c['connected'])/n,
            'lower_connected_delta':g['connected']-c['connected']-c['censored'],
            'upper_connected_delta':g['connected']+g['censored']-c['connected'],
            'lower_rate_delta':(g['connected']-c['connected']-c['censored'])/n,
            'upper_rate_delta':(g['connected']+g['censored']-c['connected'])/n,
            'parent_robust_sign':dict(robust)}

def assay(reference,max_parents=None):
    source=json.loads(Path(reference).read_text());assert source['experiment']==125
    prior={r['parent_id']:r for r in source['parent_records']}
    cohort=list(m.parents('left'));assert len(cohort)==130
    memo={};calls=Counter();records=[]
    def examine(frame,pos,raw):
        base=bytearray(frame);assert base[pos]==0;base[pos]=raw;state=bytes(base)
        if state not in memo:
            first=classify_state(state,500);calls['orbit500_unique']+=1
            if first=='censored':
                second=classify_state(state,2000);calls['orbit2000_unique']+=1
            else:second=first
            memo[state]=(first,second)
        return memo[state]
    for pid,(pair,g0,parent) in enumerate(cohort):
        if pid not in prior:continue
        if max_parents is not None and len(records)>=max_parents:break
        meta=prior[pid];assert meta['seed']==list(pair)
        ctrl,corbit,attempt=v.v.matched_control(pid,g0,parent,100)
        assert attempt==meta['accepted_attempt'] and corbit['support']==parent['support']
        lo,hi=min(parent['support'])-1,max(parent['support'])+1
        c0=[Counter(),Counter()];c2=[Counter(),Counter()];transition=Counter()
        for arm,frame in enumerate((g0,ctrl)):
            for pos in (lo,hi):
                for raw in range(1,16):
                    a,b=examine(frame,pos,raw)
                    c0[arm][a]+=1;c2[arm][b]+=1
                    transition[('G0' if arm==0 else 'control')+'_'+a+'_to_'+b]+=1
        assert all(c0[j]['connected']==meta['G0' if j==0 else 'control'].get('connected',0) for j in (0,1))
        assert all(c0[j]['censored']==meta['G0' if j==0 else 'control'].get('censored',0) for j in (0,1))
        records.append({'parent_id':pid,'seed':list(pair),'control_match_attempt':attempt,
             'G0_500':dict(c0[0]),'control_500':dict(c0[1]),
             'G0_2000':dict(c2[0]),'control_2000':dict(c2[1]),
             'G0_newly_resolved':c0[0]['censored']-c2[0]['censored'],
             'control_newly_resolved':c0[1]['censored']-c2[1]['censored'],
             'transition_histogram':dict(sorted(transition.items()))})
    r500=bound(records,'500');r2000=bound(records,'2000')
    summary={'cohort_parents':len(records),'horizon500':r500,'horizon2000':r2000,
       'G0_newly_resolved':sum(r['G0_newly_resolved'] for r in records),
       'control_newly_resolved':sum(r['control_newly_resolved'] for r in records),
       'memoized_orbit_calls':dict(sorted(calls.items()))}
    if max_parents is None:
        assert len(records)==55
        p=source['summary'];assert r500['G0']['connected']==p['G0']['connected']==1486
        assert r500['control']['connected']==p['control']['connected']==1215
        assert r500['G0']['censored']==143 and r500['control']['censored']==398
    return {'experiment':126,'protocol':{'physics':'unchanged 104 60 windows left rotation phase0 CENTER30',
           'cohort':'exactly 55 of 130 G0 parents with Exp108 pre-response exact cycle support matches, 30 material probes per parent',
           'horizons':[500,2000],
           'execution':'evaluate each probe at500; only 500-censored states reevaluated at2000; exact state cache avoids duplicates',
           'censor':'right-censored until recurrence observed, never counted as failed viability',
           'bounds':'nonparametric worst-case eventual connected class interval',
           'inference':'not evidence of reproduction, learning, permanent nonconvergence or a new physical mechanism'},
           'summary':summary,'parent_records':records}

def main():
 p=argparse.ArgumentParser();p.add_argument('--reference',type=Path,default=ROOT/'125_censoring_partial_identification/results/default.json');p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json');p.add_argument('--max-parents',type=int,default=None);z=p.parse_args()
 if z.max_parents is not None and z.max_parents<1:p.error('positive max-parents')
 r=assay(z.reference,z.max_parents);z.output.parent.mkdir(parents=True,exist_ok=True);z.output.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'summary':r['summary']},sort_keys=True,indent=2))
if __name__=='__main__':main()
