#!/usr/bin/env python3
"""Exp120: one-for-one site-exchange equal-edit-budget null feasibility.

All candidate selection on raw bit physics and unperturbed first step;
NO material-response or future-outcome probes in selection.
"""
import argparse,importlib.util,itertools,json,statistics
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('exp115',ROOT/'115_heldout_temporal_response_audit'/'run.py')
e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
TIERS=('same_raw_distance','same_distance_mask','same_distance_mask_popcount','same_distance_mask_popcount_and','same_distance_mask_full')

def d(a,b):return sum((x^y).bit_count() for x,y in zip(a,b))

def eligible_swap_pool(ctrl,g0,original_patch,trans,mutated_sites):
    """One-for-one exchanged edit-window support Q; 14**width alternatives."""
    goal_distance=d(trans,g0);goal_feature=e.features(trans);goal_mask=e.first_mask(trans)
    outside=[i for i in mutated_sites if i not in original_patch]
    subsets={tuple(sorted(tuple(x for x in original_patch if x!=drop)+(new,)))
             for drop in original_patch for new in outside}
    matches={key:set() for key in TIERS}
    count=0;raw_feasible=0
    # Compute required raw-Hamming reduction from ctrl instead of 60-position
    # distance for each enumerated microstate.
    ctrl_distance=d(ctrl,g0);target_reduction=ctrl_distance-goal_distance
    for q in sorted(subsets):
        choices=[tuple(v for v in range(1,16) if v!=ctrl[i]) for i in q]
        contrib=[tuple(((ctrl[i]^g0[i]).bit_count()-(v^g0[i]).bit_count(),v) for v in vv) for i,vv in zip(q,choices)]
        for pair in itertools.product(*contrib):
            count+=1
            if sum(z[0] for z in pair)!=target_reduction:continue
            raw_feasible+=1
            buf=bytearray(ctrl)
            for i,x in zip(q,pair):buf[i]=x[1]
            state=bytes(buf);matches[TIERS[0]].add(state)
            if e.first_mask(state)!=goal_mask:continue
            matches[TIERS[1]].add(state)
            feat=e.features(state)
            if feat[0]!=goal_feature[0]:continue
            matches[TIERS[2]].add(state)
            if feat[1]!=goal_feature[1]:continue
            matches[TIERS[3]].add(state)
            if feat[2]!=goal_feature[2]:continue
            matches[TIERS[4]].add(state)
    return {tier:len(v) for tier,v in matches.items()},len(subsets),count,raw_feasible

def assay(reference,max_parents=None):
    source=json.loads(Path(reference).read_text());assert source['experiment']==112 and len(source['parent_records'])==20
    parents=list(e.m.parents('left'));assert len(parents)==130
    rows=[];inv=Counter()
    for j,p in enumerate(source['parent_records']):
        if max_parents is not None and j>=max_parents:break
        pid=p['parent_id'];_,g0,parent=parents[pid]
        ctrl=e.reference_control(pid,g0,parent,p['control_match_attempt'])
        altered=tuple(i for i,(a,b) in enumerate(zip(ctrl,g0)) if a!=b)
        mask=e.first_mask(g0);assert mask==e.first_mask(ctrl)
        inv['parents']+=1
        for width in e.WIDTHS:
            for patch in e.changed_patches(g0,ctrl,parent['support'],width):
                trans=e.replace(ctrl,g0,patch)
                if e.first_mask(trans)!=mask:continue
                old_pool=list(e.exact_physical_nulls(ctrl,g0,patch,mask,e.features(trans)))
                if not old_pool:continue
                inv[f'w{width}_113_eligible_patches']+=1
                pool,swaps,proposals,raw_eligible=eligible_swap_pool(ctrl,g0,patch,trans,altered)
                inv[f'w{width}_swapped_site_sets']+=swaps
                inv[f'w{width}_candidate_states_examined']+=proposals
                inv[f'w{width}_raw_distance_proposals']+=raw_eligible
                for key,n in pool.items():inv[f'w{width}_{key}_patches']+=n>0
                rows.append({'parent_id':pid,'width':width,'original_patch':list(patch),'altered_site_count':len(altered),
                             'swapped_site_sets':swaps,'examined_assignments':proposals,
                             'raw_distance_proposals':raw_eligible,'donor_raw_distance':d(trans,g0),
                             'pool_counts':pool})
    summary={}
    for width in e.WIDTHS:
        rs=[r for r in rows if r['width']==width]
        summary[str(width)]={'original_contexts':len(rs),'parents':len({r['parent_id'] for r in rs}),
           'swapped_site_sets':sum(r['swapped_site_sets'] for r in rs),
           'states_examined':sum(r['examined_assignments'] for r in rs),
           'eligibility':{tier:{'patches':sum(bool(r['pool_counts'][tier]) for r in rs),
                     'parents':len({r['parent_id'] for r in rs if r['pool_counts'][tier]}),
                     'states_per_patch_sum':sum(r['pool_counts'][tier] for r in rs)} for tier in TIERS}}
    return {'experiment':120,'protocol':{'physics':'unchanged 104/108; same 112 20 matched G0 parents',
           'donor':'copy original G0 raw bits at each original contiguous patch',
           'null':'one-for-one swap of one edited window location with another originally differing G0/recipient position; exactly width changed occupied windows',
           'matching':'original donor to G0 global raw bit Hamming, then initial changed-site mask, popcount, adjacent AND, first-tick flips',
           'sampling':'exact enumerate 14**width assignments at each swapped edit-site set; all eligible are nonzero and differ from recipient at each edited site',
           'selection':'pre-response only, no material probes consulted; loss of support preserved',
           'scope':'only one edited-window exchange; not arbitrary equal-budget patch reshaping',
           'independence':'20 parent clusters; no inference from candidates as iid'},
           'inventory':dict(sorted(inv.items())),'summary':summary,'patch_records':rows}

def main():
 a=argparse.ArgumentParser();a.add_argument('--reference',type=Path,default=ROOT/'112_probe_discrimination_audit/results/default.json');a.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json');a.add_argument('--max-parents',type=int,default=None);z=a.parse_args()
 if z.max_parents is not None and z.max_parents<1:a.error('max-parents positive')
 r=assay(z.reference,z.max_parents);z.output.parent.mkdir(parents=True,exist_ok=True);z.output.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'inventory':r['inventory'],'summary':r['summary']},sort_keys=True,indent=2))
if __name__=='__main__':main()
