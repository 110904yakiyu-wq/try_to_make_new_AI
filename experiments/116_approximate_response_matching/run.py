#!/usr/bin/env python3
"""Exp116: distance-conditioned physical-null assay with frozen train/test probes.

One of the predeclared hypotheses is that nearest early-trace physical nulls
reproduce heldout behavior as well as a genuine donor patch. Other direction
and class-based scores are exploratory. No source physics is modified.
"""
import argparse, importlib.util, json, statistics
from pathlib import Path
from collections import defaultdict, Counter
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'115_heldout_temporal_response_audit'/'run.py'
spec=importlib.util.spec_from_file_location('exp115',S)
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
THRESHOLDS=(0,1,2,4,8,16,32,64,128,256,512,1024)
TICKS=(1,3,6,12,24)
GATES=('all','nearest1','nearest3','t1','d_le_4','d_le_8','d_le_16','d_le_32','d_le_64')

def distance(a,b,times=(1,3)):
    return sum((x[t]^y[t]).bit_count() for x,y in zip(a,b) for t in times)

def score_heldout(candidate,donor,sites):
    return e.heldout_metrics(candidate,donor,sites)

def summarize(records):
    out={}
    for width in e.WIDTHS:
        out[str(width)]={}
        for gate in GATES:
            rows=[x for x in records if x['width']==width and x['eligible'][gate]]
            groups=defaultdict(list)
            for r in rows:groups[r['pid']].append(r)
            details=[]
            for pid,rr in sorted(groups.items()):
                d={'parent_id':pid,'patches':len(rr),'null_states':sum(x['pool_size'][gate] for x in rr)}
                for tick in (6,12,24):
                    for metric in ('jaccard','exact'):
                        k=f'{tick}_{metric}'
                        donor=statistics.mean(r['donor'][str(tick)][metric] for r in rr)
                        null=statistics.mean(r['null'][gate][str(tick)][metric] for r in rr)
                        d[k+'_donor']=donor;d[k+'_null']=null;d[k+'_difference']=donor-null
                details.append(d)
            result={'eligible_patches':len(rows),'eligible_parents':len(details),
                    'pool_microstates':sum(x['pool_size'][gate] for x in rows),
                    'parent_details':details}
            for tick in (6,12,24):
                for metric in ('jaccard','exact'):
                    key=f'{tick}_{metric}'
                    diffs=[d[key+'_difference'] for d in details]
                    result[key+'_donor']=statistics.mean(d[key+'_donor'] for d in details) if details else None
                    result[key+'_null']=statistics.mean(d[key+'_null'] for d in details) if details else None
                    result[key+'_diff']=statistics.mean(diffs) if details else None
                    result[key+'_wins']=sum(v>1e-12 for v in diffs)
                    result[key+'_losses']=sum(v< -1e-12 for v in diffs)
                    result[key+'_ties']=sum(abs(v)<=1e-12 for v in diffs)
            out[str(width)][gate]=result
    return out

def assay(reference,max_parents=None):
    reference=json.loads(Path(reference).read_text(encoding='utf-8'))
    assert reference['experiment']==112 and reference['parameters']['ticks']==500
    roster={x['parent_id']:x for x in reference['parent_records']}
    assert len(roster)==20
    catalog=list(e.m.parents('left'));assert len(catalog)==130
    inv=Counter();rows=[]
    for pid,ref in sorted(roster.items()):
        if max_parents is not None and inv['parents']>=max_parents:break
        pair,donor,parent=catalog[pid]
        ctrl=e.reference_control(pid,donor,parent,ref['control_match_attempt'])
        mask=e.first_mask(donor);assert mask==e.first_mask(ctrl)
        sites=(min(parent['support'])-1,max(parent['support'])+1)
        inv['parents']+=1
        for width in e.WIDTHS:
            for patch in e.changed_patches(donor,ctrl,parent['support'],width):
                trans=e.replace(ctrl,donor,patch)
                if e.first_mask(trans)!=mask:continue
                inv[f'width{width}_mask_pass']+=1
                pool=list(e.exact_physical_nulls(ctrl,donor,patch,mask,e.features(trans)))
                if not pool:continue
                inv[f'width{width}_physical_eligible']+=1
                train=e.response_panel(trans,*sites,'train')
                scores=[(distance(e.response_panel(state,*sites,'train'),train),state) for state in pool]
                scores.sort(key=lambda z:(z[0],z[1]))
                t1=[(d,s) for d,s in scores if distance(e.response_panel(s,*sites,'train'),train,(1,))==0]
                selected={'all':scores,'nearest1':scores[:1], 'nearest3':scores[:3],
                          't1':t1,'d_le_4':[x for x in scores if x[0]<=4],
                          'd_le_8':[x for x in scores if x[0]<=8],
                          'd_le_16':[x for x in scores if x[0]<=16],
                          'd_le_32':[x for x in scores if x[0]<=32],
                          'd_le_64':[x for x in scores if x[0]<=64]}
                hist={str(t):sum(d<=t for d,_ in scores) for t in THRESHOLDS}
                observed={state:score_heldout(state,donor,sites) for _,state in scores}
                null={}
                for gate,choices in selected.items():
                    if not choices:continue
                    null[gate]={str(t):{metric:statistics.mean(observed[state][str(t)][metric] for _,state in choices)
                                         for metric in ('jaccard','exact')} for t in (6,12,24)}
                    inv[f'width{width}_{gate}_patches']+=1
                rows.append({'pid':pid,'width':width,'patch':list(patch),'candidates':len(scores),
                             'min_train_hamming':scores[0][0],'mean_train_hamming':statistics.mean(x[0] for x in scores),
                             'max_train_hamming':scores[-1][0], 'threshold_counts':hist,
                             'pool_size':{g:len(v) for g,v in selected.items()},
                             'eligible':{g:bool(v) for g,v in selected.items()},
                             'donor':score_heldout(trans,donor,sites),'null':null})
    res={'experiment':116,'protocol':{'physics':'unchanged 104, SIZE=60 CENTER=30 left phase=0',
          'cohort':'frozen 112 20 parent pairs, 113 fully matched physical alternatives',
          'train':'6 probes left/right values 1,7,15; ticks 1 and 3; integer Hamming of response masks vs G0 patch transplant',
          'test':'24 disjoint raw-value probes; ticks 6,12,24, relative to original G0 parent',
          'controls':'all finite admissible bit states; deterministic nearest (lexicographic tie), nearest 3, exact tick1 and Hamming thresholds',
          'selection':'physical and train measurements only, never heldout outcomes',
          'independence':'parent-pair unit; repeated patches and candidate microstates nested',
          'interpretation':'observational restricted finite physics null; not organization-causal identification'},
         'inventory':dict(sorted(inv.items())),'summary':summarize(rows),'patch_records':rows}
    e.response_panel.cache_clear()
    return res

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--reference',type=Path,default=ROOT/'112_probe_discrimination_audit/results/default.json')
    ap.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json')
    ap.add_argument('--max-parents',type=int,default=None)
    args=ap.parse_args()
    if args.max_parents is not None and args.max_parents<1:ap.error('max-parents must be positive')
    data=assay(args.reference,args.max_parents)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'inventory':data['inventory'],'summary':{w:{g:{k:v for k,v in d.items() if k!='parent_details'} for g,d in r.items()} for w,r in data['summary'].items()}},indent=2,sort_keys=True))
if __name__=='__main__':main()
