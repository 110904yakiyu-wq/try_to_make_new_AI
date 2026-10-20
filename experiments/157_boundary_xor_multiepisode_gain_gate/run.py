#!/usr/bin/env python3
"""Exp157: same multi-episode histories as 156; informative XOR heldout probes.

Unlike adding raw material to an unoccupied distant site, XOR-ing an
independent bit at the *original support boundary* is always well defined,
so matched cohorts are selected only by TRAIN intervention feasibility.
No training via the observer's performance criterion.
"""
import argparse, csv, importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
spec=importlib.util.spec_from_file_location('exp156',ROOT/'156_multiepisode_heldout_gain_gate'/'run.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);m=v.m
MASKS=(1,2,4,8)
TICKS=60


def xor_response(state,site,mask):
    assert mask in MASKS and len(state)==60 and 0<=site<60
    base=bytes(state);test=bytearray(state);test[site]^=mask;test=bytes(test)
    union=0;instant=[]
    for tick in range(1,TICKS+1):
        base=m.step(base,(tick-1)%3);test=m.step(test,(tick-1)%3)
        changed=sum((1<<i) for i,(a,b) in enumerate(zip(base,test)) if a!=b)
        union |= changed
        if tick in (1,3,6,24,60):instant.append(changed.bit_count())
    return {'union_affected_sites':union.bit_count(),'reached_10':int(union.bit_count()>=10),
            'reached_30':int(union.bit_count()>=30),'instant_affected_sites':instant}


def assay(max_parents=130):
    assert 1<=max_parents<=130
    parents=list(m.parents());assert len(parents)==130
    contexts=[];records=[];memo={}
    for pid,(seed,frame,o) in enumerate(parents[:max_parents]):
        lo=(min(o['support'])-1)%60;hi=(max(o['support'])+1)%60
        states={a:v.evolve(frame,lo,hi,ev) for a,ev in v.ARMS.items()}
        feasible={a:states[a] is not None for a in v.ARMS}
        gates={k:all(feasible[a] for a in names) for k,names in v.ORDER_SETS.items()}
        for test_side,site in ((0,lo),(1,hi)):
            contexts.append({'parent_id':pid,'seed':list(seed),'test_side':test_side,'test_site':site,
                             'feasible':feasible,'LR_four_arm':gates['LR'],'RL_four_arm':gates['RL'],
                             'all_eight_arms':all(feasible.values()),
                             'pretest_physics':{a:None if states[a] is None else
                                [sum(t.bit_count() for t in states[a]),sum(bool(t) for t in states[a]),states[a][site]]
                                 for a in v.ARMS}})
            for arm,valid in feasible.items():
                if not valid:continue
                for mask in MASKS:
                    key=(states[arm],site,mask)
                    if key not in memo:memo[key]=xor_response(states[arm],site,mask)
                    response=memo[key]
                    records.append({'parent_id':pid,'test_side':test_side,'arm':arm,'test_mask':mask,
                       'union_affected_sites':response['union_affected_sites'],
                       'reached_10':response['reached_10'],'reached_30':response['reached_30'],
                       'instant_affected_t1':response['instant_affected_sites'][0],
                       'instant_affected_t3':response['instant_affected_sites'][1],
                       'instant_affected_t6':response['instant_affected_sites'][2],
                       'instant_affected_t24':response['instant_affected_sites'][3],
                       'instant_affected_t60':response['instant_affected_sites'][4]})
    summary={}
    for order,arms in v.ORDER_SETS.items():
        allowed={(q['parent_id'],q['test_side']) for q in contexts if q[order+'_four_arm']}
        subset=[r for r in records if (r['parent_id'],r['test_side']) in allowed and r['arm'] in arms]
        summary[order]=v.summarize_context(subset,arms)
        summary[order]['eligible_contexts']=len(allowed)
    common={(q['parent_id'],q['test_side']) for q in contexts if q['all_eight_arms']}
    subset=[r for r in records if (r['parent_id'],r['test_side']) in common]
    summary['common_eight_arm']=v.summarize_context(subset,tuple(v.ARMS))
    summary['common_eight_arm']['eligible_contexts']=len(common)
    return {'experiment':157,'protocol':{
     'physics':'unchanged 60 window 4bit three-phase local kernel, CENTER30, left rotation',
     'experience':'externally scripted sham/single/two ordered/simultaneous raw7 left, raw11 right at t0 or t24',
     'test':'bit XOR masks 1,2,4,8 at ORIGINAL left/right union-support boundary positions, t96 phase0; same mask applied to each arm, irrespective of occupancy',
     'metric':'union of physical window locations causally changed by XOR relative to each arm own no-test trajectory over 60 ticks',
     'eligibility':'no overwrite for training injections only; no post-treatment test-site occupancy filter',
     'estimand':'observer-defined locality and factorial interaction, not internal reward, learning, or causal effect independent of physical state',
     'unit':'original parent cluster; correlated sides, masks and schedules'},
     'inventory':{'catalog_parents':130,'parents_processed':max_parents,'contexts':len(contexts),
                  'response_records':len(records),'unique_test_microstates':len(memo)},
     'summary':summary,'contexts':contexts,'records':records}


def main():
    p=argparse.ArgumentParser();p.add_argument('--max-parents',type=int,default=130)
    p.add_argument('--output',type=Path,default=HERE/'results/default.json')
    p.add_argument('--csv',type=Path,default=HERE/'results/probes.csv')
    a=p.parse_args();r=assay(a.max_parents)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps({k:x for k,x in r.items() if k!='records'},sort_keys=True,indent=2)+'\n')
    fields=tuple(r['records'][0])
    with a.csv.open('w',newline='') as f:
        w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader();w.writerows(r['records'])
    print(json.dumps({'inventory':r['inventory'],'summary':r['summary']},indent=2,sort_keys=True))

if __name__=='__main__':main()
