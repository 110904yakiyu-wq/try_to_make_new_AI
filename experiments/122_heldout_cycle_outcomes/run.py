#!/usr/bin/env python3
"""Exp122: direct heldout cycle/censoring outcomes for Exp121 equal-edit nulls.

A 500-tick censor is unresolved, not death, adaptation failure, etc.
"""
import argparse,importlib.util,json,statistics
from pathlib import Path
from collections import defaultdict,Counter
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('exp121',ROOT/'121_equal_budget_heldout'/'run.py')
f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f);e=f.e
EXCLUDED=(1,7,15);TEST=tuple(x for x in range(1,16) if x not in EXCLUDED)
CLASS=('connected','fragmented','static','censored')

def label(frame,site,raw):
    # Historical Exp115 classifier matches resolved component logic.
    return e.class_label(frame,site,raw)

def classify_panel(frame,sites):
    return [label(frame,pos,raw) for pos in sites for raw in TEST]

def tally_panel(labels):return {x:labels.count(x) for x in CLASS}

def summarize(rows):
    res={}
    for width in e.WIDTHS:
        rr=[r for r in rows if r['width']==width];group=defaultdict(list)
        for r in rr:group[r['pid']].append(r)
        parents=[]
        for pid,entries in sorted(group.items()):
            a={'parent_id':pid,'patches':len(entries)}
            for arm in ('G0_reference','recipient_reference','transplant','equal_edit_null','fixed_patch_null'):
                for cls in CLASS:
                    a[f'{arm}_{cls}']=statistics.mean(row[arm][cls]/24 for row in entries)
            for cls in ('connected','censored'):
                a[f'donor_minus_equal_{cls}']=a[f'transplant_{cls}']-a[f'equal_edit_null_{cls}']
                a[f'donor_minus_fixed_{cls}']=a[f'transplant_{cls}']-a[f'fixed_patch_null_{cls}']
            parents.append(a)
        agg={'patches':len(rr),'parents':len(parents),'parent_details':parents}
        for cls in ('connected','censored'):
            for name in ('donor_minus_equal','donor_minus_fixed'):
                vec=[p[f'{name}_{cls}'] for p in parents]
                agg[f'{name}_{cls}_mean']=statistics.mean(vec) if vec else None
                agg[f'{name}_{cls}_wins']=sum(q>1e-12 for q in vec)
                agg[f'{name}_{cls}_losses']=sum(q< -1e-12 for q in vec)
                agg[f'{name}_{cls}_ties']=sum(abs(q)<=1e-12 for q in vec)
            for arm in ('G0_reference','recipient_reference','transplant','equal_edit_null','fixed_patch_null'):
                agg[f'{arm}_{cls}_mean']=statistics.mean(p[f'{arm}_{cls}'] for p in parents) if parents else None
        res[str(width)]=agg
    return res

def assay(ref_file,census_file,pretested_file,max_parents=None):
    ref=json.loads(Path(ref_file).read_text());census=json.loads(Path(census_file).read_text());before=json.loads(Path(pretested_file).read_text())
    assert ref['experiment']==112 and census['experiment']==120 and before['experiment']==121
    catalog=list(e.m.parents('left'))
    expected={(p['pid'],p['width'],tuple(p['patch'])):p for p in before['patch_records']}
    rows=[];invt=Counter()
    for j,p in enumerate(ref['parent_records']):
        if max_parents is not None and j>=max_parents:break
        pid=p['parent_id'];_,g0,parent=catalog[pid]
        ctrl=e.reference_control(pid,g0,parent,p['control_match_attempt'])
        mask=e.first_mask(g0);assert mask==e.first_mask(ctrl)
        sites=(min(parent['support'])-1,max(parent['support'])+1)
        invt['parents']+=1
        for width in e.WIDTHS:
            for patch in e.changed_patches(g0,ctrl,parent['support'],width):
                key=(pid,width,tuple(patch))
                if key not in expected:continue
                donor=e.replace(ctrl,g0,patch)
                pool=f.equal_budget_pool(ctrl,g0,patch,donor,parent)
                if not pool:raise AssertionError('Exp121 eligible patch disappeared')
                old=list(e.exact_physical_nulls(ctrl,g0,patch,mask,e.features(donor)))
                donor_panel=f.f.panel(donor,*sites)
                def nearest(pool):return min(pool,key=lambda z:(f.f.hd(f.f.panel(z,*sites),donor_panel,f.TRAIN),z))
                chosen=nearest(pool);baseline=nearest(old)
                anchor=expected[key]
                assert len(pool)==anchor['equal_budget_candidates']
                assert f.f.hd(f.f.panel(chosen,*sites),donor_panel,f.TRAIN)==anchor['equal_budget_nearest_train_distance']
                names={'G0_reference':g0,'recipient_reference':ctrl,'transplant':donor,'equal_edit_null':chosen,'fixed_patch_null':baseline}
                scores={arm:tally_panel(classify_panel(frame,sites)) for arm,frame in names.items()}
                rows.append({'pid':pid,'width':width,'patch':list(patch),**scores})
                invt[f'w{width}_patches']+=1
    assert max_parents is not None or len(rows)==15
    result={'experiment':122,'protocol':{'cohort':'120/121 identical 15 eligible patch contexts in 112 frozen parent cohort',
        'controls':'one-for-one equal-window edit budget and raw distance plus matched first step physics, selection frozen 121 preresponse early train',
        'trained_values':'left/right raw 1,7,15 at tick1/tick3',
        'heldout_values':'left/right all nonzero raw values excluding 1,7,15; 24 probes per patch',
        'evaluation':'500 tick exact first recurrence (microstate,next scheduler phase): connected/fragmented/static or censored',
        'censored':'no recurrent key seen within horizon, NOT a negative lifetime/reproduction outcome',
        'inference':'not an autonomous survival or organization-specific causality estimate; parent-weighted'},
        'inventory':dict(sorted(invt.items())),'summary':summarize(rows),'patch_records':rows}
    f.f.panel.cache_clear();return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--reference',type=Path,default=ROOT/'112_probe_discrimination_audit/results/default.json');p.add_argument('--census',type=Path,default=ROOT/'120_equal_edit_budget_overlap/results/default.json');p.add_argument('--pretested',type=Path,default=ROOT/'121_equal_budget_heldout/results/default.json');p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json');p.add_argument('--max-parents',type=int,default=None);a=p.parse_args()
 if a.max_parents is not None and a.max_parents<1:p.error('positive max-parents')
 result=assay(a.reference,a.census,a.pretested,a.max_parents);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'inventory':result['inventory'],'summary':{w:{k:v for k,v in r.items() if k!='parent_details'} for w,r in result['summary'].items()}},sort_keys=True,indent=2))
if __name__=='__main__':main()
