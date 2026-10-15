#!/usr/bin/env python3
"""Experiment 115: preoutcome early-response-equivalent physical nulls.

No new kernel. Train: 6 probes (1,7,15 left/right), response masks at
phase-consistent ticks 1 and 3; holdout: other 24 probes, ticks 6,12,24.
Comparison is retrospective and within a postselected 20-pair cohort.
"""
import argparse
import importlib.util
import itertools
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'108_cycle_union_geometry_match'/'run.py'
spec=importlib.util.spec_from_file_location('exp108',SRC)
v=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
m=v.m
TRAIN=(1,7,15)
TEST=tuple(x for x in range(1,16) if x not in TRAIN)
TIMES=(1,3,6,12,24)
WIDTHS=(1,2,3)
GATES=('physical','train_t1','train_t1_t3')


def first_mask(state):
    nxt=m.step(state,0,'left')
    return frozenset(i for i,(a,b) in enumerate(zip(state,nxt)) if a!=b)


def features(state):
    nxt=m.step(state,0,'left');n=len(state)
    return (sum(x.bit_count() for x in state),
            sum((state[i]&state[(i+1)%n]).bit_count() for i in range(n)),
            sum((a^b).bit_count() for a,b in zip(state,nxt)))


def changed_patches(donor,recipient,support,width):
    altered={i for i,(a,b) in enumerate(zip(donor,recipient)) if a!=b}
    return sorted({tuple((start+j)%m.SIZE for j in range(width))
       for start in support if all((start+j)%m.SIZE in altered for j in range(width))})


def replace(recipient,source,patch):
    buf=bytearray(recipient)
    for i in patch:buf[i]=source[i]
    return bytes(buf)


def exact_physical_nulls(recipient,donor,patch,mask,goal_features):
    """Same 113 strongest tier; entire legal finite alternative pool."""
    choices=[tuple(x for x in range(1,16) if x!=recipient[pos]) for pos in patch]
    for values in itertools.product(*choices):
        if all(val==donor[pos] for pos,val in zip(patch,values)):continue
        buf=bytearray(recipient)
        for pos,val in zip(patch,values):buf[pos]=val
        state=bytes(buf)
        if first_mask(state)!=mask:continue
        if features(state)!=goal_features:continue
        yield state


def masked_response(base,site,raw):
    assert base[site]==0
    baseline=base
    injected=bytearray(base);injected[site]=raw;injected=bytes(injected)
    out={}
    for tick in range(1,max(TIMES)+1):
        baseline=m.step(baseline,(tick-1)%3,'left')
        injected=m.step(injected,(tick-1)%3,'left')
        if tick in TIMES:
            out[tick]=sum(1<<i for i,(a,b) in enumerate(zip(baseline,injected)) if a!=b)
    return out


@lru_cache(maxsize=100000)
def response_panel(frame,left,right,kind):
    if kind=='train': vals=TRAIN
    elif kind=='test': vals=TEST
    else:raise ValueError(kind)
    return tuple(masked_response(frame,pos,raw) for pos in (left,right) for raw in vals)


def masks_equal(panel_a,panel_b,ticks):
    return all(pa[t]==pb[t] for pa,pb in zip(panel_a,panel_b) for t in ticks)


def jaccard(a,b):
    n=(a|b).bit_count()
    return (a&b).bit_count()/n if n else 1.0


def heldout_metrics(candidate,g0,sites):
    a=response_panel(candidate,*sites,'test')
    b=response_panel(g0,*sites,'test')
    out={}
    for tick in (6,12,24):
        out[str(tick)]={'jaccard':statistics.mean(jaccard(x[tick],y[tick]) for x,y in zip(a,b)),
                        'exact':statistics.mean(x[tick]==y[tick] for x,y in zip(a,b))}
    return out


def reference_control(pid,donor,parent,nth):
    rng=random.Random(3_000_000+pid*300_000+nth-1)
    candidate=bytes(rng.randrange(1,16) if x else 0 for x in donor)
    orb=m.orbit(candidate,phase=0,direction='left',max_ticks=500)
    assert orb['status']=='cycle' and orb['active']
    assert orb['period']==parent['period'] and orb['support']==parent['support']
    phase0=[f for j,f in enumerate(orb['cycle']) if (orb['phase']+j)%3==0]
    ctrl=max(phase0,key=lambda f:sum(bool(x) for x in f))
    assert all(bool(a)==bool(b) for a,b in zip(ctrl,donor))
    return ctrl


def class_label(frame,site,raw):
    mut=bytearray(frame);assert mut[site]==0;mut[site]=raw
    r=m.orbit(bytes(mut),phase=0,direction='left',max_ticks=500)
    if r['status']!='cycle':return 'censored'
    if not r['active']:return 'static'
    remaining=set(r['support']);cc=0
    while remaining:
        cc+=1;stack=[remaining.pop()]
        while stack:
            x=stack.pop()
            for z in ((x-1)%m.SIZE,(x+1)%m.SIZE):
                if z in remaining:remaining.remove(z);stack.append(z)
    return 'connected' if cc==1 else 'fragmented'


def classify_heldout(frame,sites,keys):
    return tuple(class_label(frame,sites[0] if side=='left' else sites[1],raw) for side,raw,_ in keys)


def aggregate(records):
    out={}
    for width in WIDTHS:
        out[str(width)]={}
        for gate in GATES:
            eligible=[x for x in records if x['width']==width and x['eligible'][gate]]
            groups=defaultdict(list)
            for r in eligible:groups[r['parent_id']].append(r)
            rows=[]
            for pid,items in sorted(groups.items()):
                parent={'parent_id':pid,'patches':len(items),
                        'null_microstates':sum(x['pool_sizes'][gate] for x in items)}
                for tick in (6,12,24):
                    s=str(tick)
                    for metric in ('jaccard','exact'):
                        a=statistics.mean(x['donor_metrics'][s][metric] for x in items)
                        b=statistics.mean(x['null_metrics'][gate][s][metric] for x in items)
                        parent[f'{s}_{metric}_donor']=a
                        parent[f'{s}_{metric}_null']=b
                        parent[f'{s}_{metric}_difference']=a-b
                # Class outcomes only on frozen resolved, reference-discordant HELD-OUT probes.
                citems=[x for x in items if x['class_informative']>0]
                parent['class_evaluable_patches']=len(citems)
                if citems:
                    parent['class_donor_confirmed']=statistics.mean(x['class_donor_confirmed']/x['class_informative'] for x in citems)
                    parent['class_null_confirmed']=statistics.mean(x['class_null_confirmed'][gate]/x['class_informative'] for x in citems)
                    parent['class_donor_censored']=sum(x['class_donor_censored'] for x in citems)
                    parent['class_null_censored']=sum(x['class_null_censored'][gate] for x in citems)
                rows.append(parent)
            row={'eligible_patches':len(eligible),'eligible_parents':len(rows),
                 'null_microstates':sum(x['pool_sizes'][gate] for x in eligible),
                 'parent_details':rows,
                 'class_informative_parents':sum(p['class_evaluable_patches']>0 for p in rows),
                 'class_informative_patches':sum(p['class_evaluable_patches'] for p in rows)}
            for tick in (6,12,24):
                for metric in ('jaccard','exact'):
                    s=str(tick);k=f'{s}_{metric}'
                    row[k+'_donor']=statistics.mean(p[k+'_donor'] for p in rows) if rows else None
                    row[k+'_null']=statistics.mean(p[k+'_null'] for p in rows) if rows else None
                    diff=[p[k+'_difference'] for p in rows]
                    row[k+'_diff']=statistics.mean(diff) if diff else None
                    row[k+'_wins']=sum(x>1e-12 for x in diff)
                    row[k+'_losses']=sum(x< -1e-12 for x in diff)
                    row[k+'_ties']=sum(abs(x)<=1e-12 for x in diff)
            class_rows=[p for p in rows if p['class_evaluable_patches']]
            row['class_parent_donor']=statistics.mean(x['class_donor_confirmed'] for x in class_rows) if class_rows else None
            row['class_parent_null']=statistics.mean(x['class_null_confirmed'] for x in class_rows) if class_rows else None
            row['class_parent_diff']=(row['class_parent_donor']-row['class_parent_null']) if class_rows else None
            row['class_donor_censored_applications']=sum(x['class_donor_censored'] for x in class_rows)
            row['class_null_censored_candidate_applications']=sum(x['class_null_censored'] for x in class_rows)
            out[str(width)][gate]=row
    return out


def assay(reference_path,max_parents=None):
    ref=json.loads(Path(reference_path).read_text(encoding='utf-8'))
    assert ref['experiment']==112 and ref['parameters']['attempts']==100 and ref['parameters']['ticks']==500
    assert ref['inventory']['equal_first_mask_pairs']==20
    roster={x['parent_id']:x for x in ref['parent_records']}
    assert len(roster)==20
    parent_catalog=list(m.parents('left'))
    assert len(parent_catalog)==130 and m.CENTER==30 and m.SIZE==60
    inventory=Counter();records=[];meta=[]
    for pid,entry in sorted(roster.items()):
        if max_parents is not None and len(meta)>=max_parents:break
        pair,donor,parent=parent_catalog[pid]
        assert list(pair)==entry['seed'] and sorted(parent['support'])==entry['union_support']
        ctrl=reference_control(pid,donor,parent,entry['control_match_attempt'])
        mask=first_mask(donor)
        assert mask==first_mask(ctrl)==frozenset(entry['first_mask'])
        sites=(min(parent['support'])-1,max(parent['support'])+1)
        train_ref=response_panel(donor,*sites,'train')
        inventory['parents']+=1
        # Retrospectively known class-contrast inputs, used ONLY as reporting denominator.
        informative=[]
        for j,row in enumerate(entry['probes']):
            if j%15+1 in TRAIN:continue
            cls_a,cls_b=row[0],row[3]
            if cls_a!='censored' and cls_b!='censored' and cls_a!=cls_b:
                informative.append(('left' if j<15 else 'right',j%15+1,cls_a))
        meta.append({'parent_id':pid,'seed':list(pair),'original_control_attempt':entry['control_match_attempt'],
                     'heldout_resolved_discordant_reference_probes':len(informative)})
        for width in WIDTHS:
            for patch in changed_patches(donor,ctrl,parent['support'],width):
                transplanted=replace(ctrl,donor,patch)
                if first_mask(transplanted)!=mask:continue
                inventory[f'width{width}_donor_mask_pass']+=1
                feature=features(transplanted)
                pool=list(exact_physical_nulls(ctrl,donor,patch,mask,feature))
                if not pool:continue
                inventory[f'width{width}_feature_eligible']+=1
                inv_train=response_panel(transplanted,*sites,'train')
                null_train=[response_panel(candidate,*sites,'train') for candidate in pool]
                groups={'physical':pool,
                        'train_t1':[cand for cand,sig in zip(pool,null_train) if masks_equal(sig,inv_train,(1,))],
                        'train_t1_t3':[cand for cand,sig in zip(pool,null_train) if masks_equal(sig,inv_train,(1,3))]}
                inventory[f'width{width}_t1_eligible']+=bool(groups['train_t1'])
                inventory[f'width{width}_t1t3_eligible']+=bool(groups['train_t1_t3'])
                inventory[f'width{width}_t1_nulls']+=len(groups['train_t1'])
                inventory[f'width{width}_t1t3_nulls']+=len(groups['train_t1_t3'])
                donor_metrics=heldout_metrics(transplanted,donor,sites)
                null_metrics={}
                for gate,states in groups.items():
                    if not states:continue
                    observed=[heldout_metrics(cand,donor,sites) for cand in states]
                    null_metrics[gate]={str(t):{metric:statistics.mean(x[str(t)][metric] for x in observed)
                                                     for metric in ('jaccard','exact')}
                                         for t in (6,12,24)}
                row={'parent_id':pid,'width':width,'patch':list(patch),
                     'pool_sizes':{k:len(st) for k,st in groups.items()},
                     'eligible':{k:bool(st) for k,st in groups.items()},
                     'train_equals_g0_t1':masks_equal(inv_train,train_ref,(1,)),
                     'train_equals_g0_t1t3':masks_equal(inv_train,train_ref,(1,3)),
                     'donor_metrics':donor_metrics,'null_metrics':null_metrics,
                     'class_informative':len(informative),'class_donor_confirmed':0,
                     'class_donor_censored':0,'class_null_confirmed':{},'class_null_censored':{}}
                if informative:
                    donor_labels=classify_heldout(transplanted,sites,informative)
                    row['class_donor_confirmed']=sum(x==y[2] for x,y in zip(donor_labels,informative))
                    row['class_donor_censored']=sum(x=='censored' for x in donor_labels)
                    for gate,states in groups.items():
                        if not states:continue
                        labeled=[classify_heldout(x,sites,informative) for x in states]
                        row['class_null_confirmed'][gate]=statistics.mean(sum(x==key[2] for x,key in zip(lbl,informative)) for lbl in labeled)
                        row['class_null_censored'][gate]=sum(x=='censored' for lbl in labeled for x in lbl)
                records.append(row)
    result={'experiment':115,'protocol':{
        'kernel':'frozen 104 on 60 4-bit windows, center 30, phase 0, left rotation',
        'cohort':'frozen 112 20 pairs, exact 108 geometry and first tick mask',
        'null':'exact 113 strongest feature tier, exclude exact donor-patch identity',
        'train':'2 sides x raw(1,7,15); responses versus own baseline at ticks 1 and 3',
        'heldout':'2 sides x remaining 12 raw values; exact position-mask Jaccard and equality at ticks 6,12,24',
        'gates':list(GATES),'selection':'training signatures and unperturbed physical features only',
        'class':'retrospective resolved reference class disagreements on heldout probe keys; 500 tick, censor separate',
        'independence':'20 parent-pair clusters, equal-parent means; candidate assignments and probes not independent',
        'status':'descriptive diagnostic, no causal attribution to organizational autonomy'},
        'inventory':dict(sorted(inventory.items())),'parent_records':meta,
        'summary':aggregate(records),'patch_records':records}
    response_panel.cache_clear()
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--reference',type=Path,default=ROOT/'112_probe_discrimination_audit/results/default.json')
    ap.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json')
    ap.add_argument('--max-parents',type=int,default=None)
    args=ap.parse_args()
    if args.max_parents is not None and args.max_parents<1:ap.error('positive max-parents required')
    result=assay(args.reference,args.max_parents)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
    compact={'inventory':result['inventory'],
             'summary':{w:{g:{k:v for k,v in a.items() if k!='parent_details'} for g,a in row.items()}
                        for w,row in result['summary'].items()}}
    print(json.dumps(compact,sort_keys=True,indent=2))

if __name__=='__main__':main()
