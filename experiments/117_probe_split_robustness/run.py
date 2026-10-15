#!/usr/bin/env python3
"""Exp117: rotate predeclared 3-value train folds; nearest early physical null.

Each fold keeps 12 raw values, on both support boundaries, held out.
Fold comparison is paired and descriptive, NOT five independent experiments.
"""
import argparse,importlib.util,json,statistics
from pathlib import Path
from functools import lru_cache
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('exp116',ROOT/'116_approximate_response_matching'/'run.py')
f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f)
e=f.e
FOLDS=((1,7,15),(2,8,14),(3,9,13),(4,10,12),(5,6,11))
assert sorted(z for fold in FOLDS for z in fold)==list(range(1,16))

@lru_cache(maxsize=128000)
def panel(state,left,right):
    return tuple(e.masked_response(state,pos,raw) for pos in (left,right) for raw in range(1,16))

def indices(values):return tuple(side*15+raw-1 for side in (0,1) for raw in values)

def hd(panel_a,panel_b,ix):
    return sum((panel_a[j][t]^panel_b[j][t]).bit_count() for j in ix for t in (1,3))

def heldout(a,original,ix):
    return {str(t):{'jaccard':statistics.mean(e.jaccard(a[j][t],original[j][t]) for j in ix),
                    'exact':statistics.mean(a[j][t]==original[j][t] for j in ix)} for t in (6,12,24)}

def aggregate(rows):
    out={}
    for width in e.WIDTHS:
        out[str(width)]={}
        for fold_index,values in enumerate(FOLDS):
            cur=[r['folds'][str(fold_index)] for r in rows if r['width']==width]
            groups=defaultdict(list)
            for x in cur:groups[x['parent_id']].append(x)
            per=[]
            for pid,rs in sorted(groups.items()):
                obj={'parent_id':pid,'patches':len(rs)}
                for tick in (6,12,24):
                    for metric in ('jaccard','exact'):
                        k=f'{tick}_{metric}'
                        obj[k+'_donor']=statistics.mean(r['donor'][str(tick)][metric] for r in rs)
                        obj[k+'_null']=statistics.mean(r['nearest'][str(tick)][metric] for r in rs)
                        obj[k+'_diff']=obj[k+'_donor']-obj[k+'_null']
                per.append(obj)
            agg={'train_raw_values':list(values),'heldout_raw_values':[j for j in range(1,16) if j not in values],
                 'parents':len(per),'patches':len(cur),'parent_details':per,
                 'median_nearest_early_distance':statistics.median(r['nearest_distance'] for r in cur) if cur else None}
            for tick in (6,12,24):
                for metric in ('jaccard','exact'):
                    k=f'{tick}_{metric}'
                    diff=[v[k+'_diff'] for v in per]
                    agg[k+'_diff']=statistics.mean(diff) if diff else None
                    agg[k+'_donor']=statistics.mean(v[k+'_donor'] for v in per) if per else None
                    agg[k+'_null']=statistics.mean(v[k+'_null'] for v in per) if per else None
                    agg[k+'_wins']=sum(x>1e-12 for x in diff)
                    agg[k+'_losses']=sum(x< -1e-12 for x in diff)
                    agg[k+'_ties']=sum(abs(x)<=1e-12 for x in diff)
            out[str(width)][str(fold_index)]=agg
        # Aggregate parent-level results across fold, not independent fold samples.
        first=out[str(width)]['0']['parent_details']
        ps=[]
        for pid in [v['parent_id'] for v in first]:
            measurements=[next(x for x in out[str(width)][str(i)]['parent_details'] if x['parent_id']==pid)
                          for i in range(len(FOLDS))]
            ps.append({'parent_id':pid,'24_jaccard_mean_diff':statistics.mean(x['24_jaccard_diff'] for x in measurements),
                       '24_jaccard_min_diff':min(x['24_jaccard_diff'] for x in measurements),
                       '24_jaccard_max_diff':max(x['24_jaccard_diff'] for x in measurements)})
        out[str(width)]['across_folds']={'n_parents':len(ps),'mean_parent_fold_difference':statistics.mean(x['24_jaccard_mean_diff'] for x in ps) if ps else None,
            'parents_positive_all_folds':sum(x['24_jaccard_min_diff']>1e-12 for x in ps),
            'parents_negative_all_folds':sum(x['24_jaccard_max_diff']< -1e-12 for x in ps),
            'parent_details':ps}
    return out

def assay(reference,max_parents=None):
    d=json.loads(Path(reference).read_text(encoding='utf-8'))
    assert d['experiment']==112 and len(d['parent_records'])==20
    catalog=list(e.m.parents('left'));assert len(catalog)==130
    rows=[]
    for k,entry in enumerate(d['parent_records']):
        if max_parents is not None and k>=max_parents:break
        pid=entry['parent_id'];pair,donor,parent=catalog[pid]
        ctrl=e.reference_control(pid,donor,parent,entry['control_match_attempt'])
        common=e.first_mask(donor);assert common==e.first_mask(ctrl)
        sites=(min(parent['support'])-1,max(parent['support'])+1)
        orig_panel=panel(donor,*sites)
        for width in e.WIDTHS:
            for patch in e.changed_patches(donor,ctrl,parent['support'],width):
                original=e.replace(ctrl,donor,patch)
                if e.first_mask(original)!=common:continue
                pool=list(e.exact_physical_nulls(ctrl,donor,patch,common,e.features(original)))
                if not pool:continue
                trans_panel=panel(original,*sites)
                pools=[panel(state,*sites) for state in pool]
                fold_data={}
                for i,train_values in enumerate(FOLDS):
                    train_idx=indices(train_values)
                    test_idx=indices([raw for raw in range(1,16) if raw not in train_values])
                    scored=[(hd(p,trans_panel,train_idx),state,j) for j,(state,p) in enumerate(zip(pool,pools))]
                    best=min(scored,key=lambda z:(z[0],z[1]))
                    selected=pools[best[2]]
                    fold_data[str(i)]={'parent_id':pid,'nearest_distance':best[0],
                                       'nearest_null_index':best[2],
                                       'donor':heldout(trans_panel,orig_panel,test_idx),
                                       'nearest':heldout(selected,orig_panel,test_idx)}
                rows.append({'parent_id':pid,'width':width,'patch':list(patch),'control_pool_size':len(pool),'folds':fold_data})
    r={'experiment':117,'protocol':{
        'physics':'frozen 104 60-window, CENTER=30 phase0 left',
        'physical_nuisance':'113 strongest exact physical-null feature tier, donor identity excluded',
        'cohort':'frozen 112 first-mask 20 parent pairs; 57 feature-eligible patches',
        'folds':[list(v) for v in FOLDS],
        'train':'3 raw values on each of two support sides, positions at ticks 1 and 3, minimum integer Hamming to transplanted frame',
        'test':'the other 12 raw values on each side, positions at ticks 6, 12 and 24; Jaccard/exact vs original G0',
        'selection':'null microstate determined without using any heldout raw values or outcomes; lexicographic ties',
        'independence':'folds and nulls share parents; parent is aggregation unit; no independent fold-based p-value',
        'limitations':'not matched full future state and not identification of organizational causality'},
       'inventory':{'parents':min(20,max_parents) if max_parents else 20,'qualified_patches':len(rows),
                    'qualified_by_width':{str(w):sum(x['width']==w for x in rows) for w in e.WIDTHS},
                    'total_physical_null_states':sum(x['control_pool_size'] for x in rows)},
       'summary':aggregate(rows),'patch_records':rows}
    panel.cache_clear();return r

def main():
    a=argparse.ArgumentParser();a.add_argument('--reference',type=Path,default=ROOT/'112_probe_discrimination_audit/results/default.json');a.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json');a.add_argument('--max-parents',type=int,default=None);z=a.parse_args()
    if z.max_parents is not None and z.max_parents<1:a.error('max-parents positive')
    obj=assay(z.reference,z.max_parents);z.output.parent.mkdir(parents=True,exist_ok=True)
    z.output.write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'inventory':obj['inventory'],'summary':{w:{g:{k:v for k,v in dd.items() if k!='parent_details'} for g,dd in rr.items()} for w,rr in obj['summary'].items()}},indent=2,sort_keys=True))
if __name__=='__main__':main()
