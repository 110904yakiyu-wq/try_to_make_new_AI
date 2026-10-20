#!/usr/bin/env python3
"""Experiment 156: externally scheduled two-episode history, heldout response.

No reward/learner/memory objective in the physics. Finite observer-locality score.
Compare factorial difference-in-differences with sham and one-pulse histories;
exclude only via pretest site occupancy and pulse placement feasibility.
"""
import argparse, csv, importlib.util, json, statistics
from pathlib import Path
from collections import defaultdict
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
s=importlib.util.spec_from_file_location('exp151',ROOT/'151_experience_heldout_response_gate'/'run.py')
v=importlib.util.module_from_spec(s);s.loader.exec_module(v);m=v.m
assert m.SIZE==60 and m.CENTER==30
EVAL_TICK=96
GAP=24
RAWS=(1,5,9,14)  # disjoint from training pulses 7/11
ARMS={
 'sham':(),
 'L0':((0,'L',7),),
 'R24':((24,'R',11),),
 'LR':((0,'L',7),(24,'R',11)),
 'R0':((0,'R',11),),
 'L24':((24,'L',7),),
 'RL':((0,'R',11),(24,'L',7)),
 'simultaneous':((0,'L',7),(0,'R',11)),
}
ORDER_SETS={'LR':('sham','L0','R24','LR'),
            'RL':('sham','R0','L24','RL')}


def evolve(frame,left,right,events,end=EVAL_TICK):
    state=bytearray(frame)
    schedule=defaultdict(list)
    for time,side,raw in events:
        schedule[time].append((left if side=='L' else right,raw))
    for t in range(end):
        if t in schedule:
            for pos,raw in schedule[t]:
                if state[pos]!=0:return None
                state[pos]=raw
        state=bytearray(m.step(state,t%3))
    return bytes(state)


def summarize_context(rows,arms):
    pairs=defaultdict(lambda:defaultdict(list))
    for row in rows:
        pairs[row['parent_id']][row['arm']].append(row)
    # All contexts supplied have complete arm-wise raw panels; parent-level
    # pooling gives equal parent weights rather than pseudo-replicated probes.
    parents=[]
    for pid,rec in sorted(pairs.items()):
        if any(x not in rec for x in arms):continue
        means={x:statistics.mean(z['union_affected_sites'] for z in rec[x]) for x in arms}
        spread={x:statistics.mean(z['reached_10'] for z in rec[x]) for x in arms}
        parents.append({'parent_id':pid,'means':means,'spread':spread})
    result={'parents':len(parents),'contexts':len(set((x['parent_id'],x['test_side']) for x in rows)),
            'records':len(rows)}
    if not parents:return result
    result['mean_affected_sites_by_arm']={a:statistics.mean(x['means'][a] for x in parents) for a in arms}
    result['mean_ever10_by_arm']={a:statistics.mean(x['spread'][a] for x in parents) for a in arms}
    if 'LR' in arms or 'RL' in arms:
        for full,one0,one24 in (('LR','L0','R24'),('RL','R0','L24')):
            if full not in arms:continue
            vals=[x['means'][full]-x['means'][one0]-x['means'][one24]+x['means']['sham'] for x in parents]
            d=[x['means'][full]-x['means']['sham'] for x in parents]
            result['synergy_'+full]={'mean':statistics.mean(vals),
                    'positive':sum(z>0 for z in vals),'negative':sum(z<0 for z in vals),'tied':sum(z==0 for z in vals)}
            result['full_minus_sham_'+full]={'mean':statistics.mean(d),
                    'positive':sum(z>0 for z in d),'negative':sum(z<0 for z in d),'tied':sum(z==0 for z in d)}
    return result


def assay(max_parents=130):
    assert 1<=max_parents<=130
    parents=list(m.parents());assert len(parents)==130
    contexts=[];rows=[];cache={}
    for pid,(seed,frame,orbit) in enumerate(parents[:max_parents]):
        lo=(min(orbit['support'])-1)%60;hi=(max(orbit['support'])+1)%60
        assert frame[lo]==frame[hi]==0 and lo!=hi
        states={arm:evolve(frame,lo,hi,events) for arm,events in ARMS.items()}
        for test_side,site in ((0,(lo-2)%60),(1,(hi+2)%60)):
            if site in (lo,hi):continue
            eligible={arm:(state is not None and state[site]==0) for arm,state in states.items()}
            both={k:all(eligible[a] for a in ar) for k,ar in ORDER_SETS.items()}
            all_arms=all(eligible.values())
            contexts.append({'parent_id':pid,'seed':list(seed),'test_side':test_side,
                            'test_site':site,'feasible':{a:states[a] is not None for a in ARMS},
                            'eligible':eligible,'LR_four_arm':both['LR'],'RL_four_arm':both['RL'],
                            'all_eight_arms':all_arms,
                            'pretest_physics':{a:None if states[a] is None else
                                [sum(z.bit_count() for z in states[a]),sum(bool(z) for z in states[a])]
                                for a in ARMS}})
            for a,ok in eligible.items():
                if not ok:continue
                for raw in RAWS:
                    key=(states[a],site,raw)
                    if key not in cache:cache[key]=v.response(states[a],site,raw)
                    score=cache[key]
                    rows.append({'parent_id':pid,'test_side':test_side,'arm':a,'test_raw':raw,
                                 'union_affected_sites':score['union_affected_sites'],
                                 'reached_10':int(score['reached_10']),
                                 'reached_30':int(score['reached_30'])})
    main={}
    for order,names in ORDER_SETS.items():
        ctx={(x['parent_id'],x['test_side']) for x in contexts if x[order+'_four_arm']}
        subset=[r for r in rows if (r['parent_id'],r['test_side']) in ctx and r['arm'] in names]
        main[order]=summarize_context(subset,names)
        main[order]['eligible_contexts']=len(ctx)
    common={(x['parent_id'],x['test_side']) for x in contexts if x['all_eight_arms']}
    subset=[r for r in rows if (r['parent_id'],r['test_side']) in common]
    main['common_eight_arm']=summarize_context(subset,tuple(ARMS))
    main['common_eight_arm']['eligible_contexts']=len(common)
    return {'experiment':156,
       'protocol':{'physics':'unchanged frozen 104/139 60-window 4-bit left-rotation three-phase kernel',
        'experiences':'boundary raw7 on left and raw11 on right, 0/24 phase-aligned external event times',
        'arms':{k:list(v) for k,v in ARMS.items()},
        'evaluation':'all arms time96 phase0, original two outer test locations and heldout raw1/5/9/14; observer difference from each arm own autonomous baseline over60 ticks',
        'eligibility':'pretest occupancy and no-overwrite feasibility; four-arm factorial and eight-arm common subsets separately',
        'utility':'lower affected-site union is observer-designated locality, not internal reward',
        'independence':'parent clusters; repeated test positions, raw values and multiple arms within parent',
        'claims':'experiences are externally scheduled, no learning or internal goal is assumed'},
       'inventory':{'catalog_parents':130,'processed_parents':max_parents,'contexts':len(contexts),
                    'unique_response_microstates':len(cache),'response_records':len(rows)},
       'summary':main,'contexts':contexts,'records':rows}


def main():
    p=argparse.ArgumentParser();p.add_argument('--max-parents',type=int,default=130)
    p.add_argument('--output',type=Path,default=HERE/'results/default.json')
    p.add_argument('--csv',type=Path,default=HERE/'results/probes.csv')
    a=p.parse_args();r=assay(a.max_parents)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    small={k:v for k,v in r.items() if k!='records'}
    a.output.write_text(json.dumps(small,sort_keys=True,indent=2)+'\n')
    columns=('parent_id','test_side','arm','test_raw','union_affected_sites','reached_10','reached_30')
    with a.csv.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns,lineterminator='\n');w.writeheader();w.writerows(r['records'])
    print(json.dumps({'inventory':r['inventory'],'summary':r['summary']},indent=2,sort_keys=True))

if __name__=='__main__':main()
