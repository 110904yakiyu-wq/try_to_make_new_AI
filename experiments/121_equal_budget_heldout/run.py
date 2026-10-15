#!/usr/bin/env python3
"""Exp121: heldout test of pre-response equal-edit-budget and distance nulls."""
import argparse,importlib.util,itertools,json,statistics
from collections import defaultdict,Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('exp117',ROOT/'117_probe_split_robustness'/'run.py')
f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f);e=f.e
TRAIN=f.indices(f.FOLDS[0]);TEST=f.indices([v for v in range(1,16) if v not in f.FOLDS[0]])

def hd(a,b):return sum((x^y).bit_count() for x,y in zip(a,b))

def equal_budget_pool(ctrl,g0,patch,donor,parent):
    changed=tuple(i for i,(a,b) in enumerate(zip(ctrl,g0)) if a!=b)
    replacements=[i for i in changed if i not in patch]
    site_sets={tuple(sorted([i for i in patch if i!=drop]+[external]))
                for drop in patch for external in replacements}
    needed=hd(ctrl,g0)-hd(donor,g0)
    mask=e.first_mask(donor); feat=e.features(donor)
    states=set()
    for sites in sorted(site_sets):
        alternatives=[[( (ctrl[pos]^g0[pos]).bit_count()-(v^g0[pos]).bit_count(),v)
                       for v in range(1,16) if v!=ctrl[pos]] for pos in sites]
        for combo in itertools.product(*alternatives):
            if sum(q[0] for q in combo)!=needed:continue
            candidate=bytearray(ctrl)
            for pos,(_,val) in zip(sites,combo):candidate[pos]=val
            state=bytes(candidate)
            if e.first_mask(state)==mask and e.features(state)==feat:
                assert hd(state,g0)==hd(donor,g0)
                assert sum(x!=y for x,y in zip(state,ctrl))==len(patch)
                states.add(state)
    return sorted(states)

def summarize(rows):
    out={}
    for width in e.WIDTHS:
        relevant=[r for r in rows if r['width']==width];groups=defaultdict(list)
        for q in relevant:groups[q['pid']].append(q)
        parent=[]
        for pid,recs in sorted(groups.items()):
            row={'parent_id':pid,'patches':len(recs),'eligible_equal_budget_microstates':sum(q['equal_budget_candidates'] for q in recs)}
            for tick in (6,12,24):
                for metric in ('jaccard','exact'):
                    col=f'{tick}_{metric}'
                    for item in ('donor','equal_budget','fixed_patch'):
                        row[col+'_'+item]=statistics.mean(q[item][str(tick)][metric] for q in recs)
                    row[col+'_donor_minus_equal_budget']=row[col+'_donor']-row[col+'_equal_budget']
                    row[col+'_donor_minus_fixed_patch']=row[col+'_donor']-row[col+'_fixed_patch']
            parent.append(row)
        ans={'eligible_patches':len(relevant),'eligible_parents':len(parent),
             'total_equal_budget_states':sum(q['equal_budget_candidates'] for q in relevant),
             'parent_details':parent}
        for tick in (6,12,24):
            for metric in ('jaccard','exact'):
                col=f'{tick}_{metric}'
                for contrast in ('donor_minus_equal_budget','donor_minus_fixed_patch'):
                    values=[r[col+'_'+contrast] for r in parent]
                    ans[col+'_'+contrast+'_mean']=statistics.mean(values) if values else None
                    ans[col+'_'+contrast+'_wins']=sum(v>1e-12 for v in values)
                    ans[col+'_'+contrast+'_losses']=sum(v< -1e-12 for v in values)
                    ans[col+'_'+contrast+'_ties']=sum(abs(v)<=1e-12 for v in values)
        out[str(width)]=ans
    return out

def assay(ref_file,census_file,max_parents=None):
    ref=json.loads(Path(ref_file).read_text());audit=json.loads(Path(census_file).read_text());assert len(ref['parent_records'])==20 and audit['experiment']==120
    loc={(q['parent_id'],q['width'],tuple(q['original_patch'])):q for q in audit['patch_records']}
    catalog=list(e.m.parents('left'));rows=[];inv=Counter()
    for j,refp in enumerate(ref['parent_records']):
        if max_parents is not None and j>=max_parents:break
        pid=refp['parent_id'];_,g0,parent=catalog[pid]
        ctrl=e.reference_control(pid,g0,parent,refp['control_match_attempt']);mask=e.first_mask(g0)
        assert mask==e.first_mask(ctrl)
        left,right=(min(parent['support'])-1,max(parent['support'])+1)
        gp=f.panel(g0,left,right);inv['parents']+=1
        for width in e.WIDTHS:
            for patch in e.changed_patches(g0,ctrl,parent['support'],width):
                donor=e.replace(ctrl,g0,patch)
                if e.first_mask(donor)!=mask:continue
                case=loc.get((pid,width,tuple(patch)))
                if case is None:continue
                candidate=equal_budget_pool(ctrl,g0,patch,donor,parent)
                assert len(candidate)==case['pool_counts']['same_distance_mask_full']
                if not candidate:continue
                old=list(e.exact_physical_nulls(ctrl,g0,patch,mask,e.features(donor)))
                assert old
                dp=f.panel(donor,left,right)
                def pick(pool):return min(pool,key=lambda st:(f.hd(f.panel(st,left,right),dp,TRAIN),st))
                new=pick(candidate);baseline=pick(old)
                def measure(st):return f.heldout(f.panel(st,left,right),gp,TEST)
                rows.append({'pid':pid,'width':width,'patch':list(patch),
                             'equal_budget_candidates':len(candidate),'original_fixed_patch_candidates':len(old),
                             'raw_distance_donor_to_G0':hd(donor,g0),'equal_budget_nearest_train_distance':f.hd(f.panel(new,left,right),dp,TRAIN),
                             'fixed_patch_nearest_train_distance':f.hd(f.panel(baseline,left,right),dp,TRAIN),
                             'donor':measure(donor),'equal_budget':measure(new),'fixed_patch':measure(baseline)})
                inv[f'width{width}_patches']+=1;inv[f'width{width}_equal_budget_states']+=len(candidate)
    result={'experiment':121,'protocol':{'physics':'unchanged 104 and frozen 112 G0 matched cohort',
        'null':'Exp120 equal number edited occupied 4-bit windows, same raw Hamming distance to original G0, first step mask/popcount/neighbor AND/bit flips',
        'eligibility':'census frozen by Exp120 before any injected response evaluation, one-for-one site exchanges only',
        'old_comparator':'original 113 exact feature null at same patch contexts, nearest on same train probes',
        'train':'raw(1,7,15) times both sides, response masks at tick1 and tick3; prechosen closest Hamming',
        'test':'other 12 raw values × two sides; response-mask Jaccard and exact at t6,12,24 against original G0',
        'independence':'parent is independent unit, patch/null dependent; small eligible support',
        'boundary':'equal edit count and raw distance does not match full spatial edit layout; cannot isolate temporal causation'},
        'inventory':dict(sorted(inv.items())),'summary':summarize(rows),'patch_records':rows}
    f.panel.cache_clear();return result

def main():
 a=argparse.ArgumentParser();a.add_argument('--reference',type=Path,default=ROOT/'112_probe_discrimination_audit/results/default.json');a.add_argument('--census',type=Path,default=ROOT/'120_equal_edit_budget_overlap/results/default.json');a.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json');a.add_argument('--max-parents',type=int,default=None);args=a.parse_args()
 if args.max_parents is not None and args.max_parents<1:a.error('positive max-parents')
 r=assay(args.reference,args.census,args.max_parents);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'inventory':r['inventory'],'summary':{w:{k:v for k,v in s.items() if k!='parent_details'} for w,s in r['summary'].items()}},sort_keys=True,indent=2))
if __name__=='__main__':main()
