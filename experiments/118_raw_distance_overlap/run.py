#!/usr/bin/env python3
"""Exp118: raw-Hamming positivity audit and one-site compensatory null census.

Selection uses states and immediate physics only; NO response outcomes observed.
The extra-site candidates are conditional on 113's original all-feature pool.
"""
import argparse,importlib.util,json,statistics
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('exp115',ROOT/'115_heldout_temporal_response_audit'/'run.py')
e=importlib.util.module_from_spec(s);s.loader.exec_module(e)
TIERS=('raw_distance','raw_distance_mask','raw_distance_mask_popcount','raw_distance_mask_popcount_and','raw_distance_mask_full')

def raw_distance(a,b):return sum((x^y).bit_count() for x,y in zip(a,b))

def assay(reference,max_parents=None):
    f=json.loads(Path(reference).read_text());assert f['experiment']==112 and len(f['parent_records'])==20
    catalog=list(e.m.parents('left'));assert len(catalog)==130
    record=[];inv=Counter();gap_hist=Counter()
    for j,ref in enumerate(f['parent_records']):
        if max_parents is not None and j>=max_parents:break
        pid=ref['parent_id'];_,g0,parent=catalog[pid]
        ctrl=e.reference_control(pid,g0,parent,ref['control_match_attempt'])
        mask=e.first_mask(g0);assert mask==e.first_mask(ctrl)
        inv['parents']+=1
        for width in e.WIDTHS:
            for patch in e.changed_patches(g0,ctrl,parent['support'],width):
                trans=e.replace(ctrl,g0,patch)
                if e.first_mask(trans)!=mask:continue
                pool=list(e.exact_physical_nulls(ctrl,g0,patch,mask,e.features(trans)))
                if not pool:continue
                inv[f'w{width}_physical_patches']+=1
                original_dist=raw_distance(trans,g0)
                gaps=[raw_distance(v,g0)-original_dist for v in pool]
                assert min(gaps)>=1, 'fatal raw-distance source identity invariant violated'
                gap_hist.update(gaps);inv[f'w{width}_null_microstates']+=len(pool)
                compensators=[i for i in sorted(parent['support']) if i not in patch and ctrl[i]!=g0[i]]
                tallies=Counter();parents={q:set() for q in TIERS}
                for candidate in pool:
                    for site in compensators:
                        for val in range(1,16):
                            if val==candidate[site]:continue
                            tmp=bytearray(candidate);tmp[site]=val;state=bytes(tmp)
                            if raw_distance(state,g0)!=original_dist:continue
                            tallies['raw_distance']+=1;parents['raw_distance'].add(state)
                            if e.first_mask(state)!=mask:continue
                            tallies['raw_distance_mask']+=1;parents['raw_distance_mask'].add(state)
                            ft=e.features(state);goal=e.features(trans)
                            if ft[0]!=goal[0]:continue
                            tallies['raw_distance_mask_popcount']+=1;parents['raw_distance_mask_popcount'].add(state)
                            if ft[1]!=goal[1]:continue
                            tallies['raw_distance_mask_popcount_and']+=1;parents['raw_distance_mask_popcount_and'].add(state)
                            if ft[2]!=goal[2]:continue
                            tallies['raw_distance_mask_full']+=1;parents['raw_distance_mask_full'].add(state)
                record.append({'parent_id':pid,'width':width,'patch':list(patch),
                               'baseline_raw_hamming_to_G0':original_dist,
                               'null_count':len(pool),
                               'min_extra_raw_hamming':min(gaps),'max_extra_raw_hamming':max(gaps),
                               'compensating_positions':compensators,
                               'qualifying_proposal_counts':dict(sorted(tallies.items())),
                               'qualifying_unique_state_counts':{tier:len(parents[tier]) for tier in TIERS}})
    summary={}
    for width in e.WIDTHS:
        rr=[r for r in record if r['width']==width]
        per={}
        for tier in TIERS:
            yes=[r for r in rr if r['qualifying_unique_state_counts'][tier]]
            per[tier]={'patches_with_any':len(yes),'parents_with_any':len({r['parent_id'] for r in yes}),
                        'total_unique_per_patch':sum(r['qualifying_unique_state_counts'][tier] for r in rr)}
        summary[str(width)]={'physical_patches':len(rr),'matched_physical_nulls':sum(r['null_count'] for r in rr),
                             'min_extra_raw_distance':min(r['min_extra_raw_hamming'] for r in rr) if rr else None,
                             'median_min_extra_distance':statistics.median(r['min_extra_raw_hamming'] for r in rr) if rr else None,
                             'same_patch_raw_distance_overlap':0,
                             'compensated':per}
    return {'experiment':118,'protocol':{'kernel':'unchanged 104',
        'null':'113 strongest-feature exact alternatives; source patch identity excluded',
        'cohort':'frozen 112 20 parents',
        'distance':'sum 4-bit XOR popcount across all 60 windows to original G0 reference',
        'physical_constraint':'same first mask, popcount, adjacent AND count, first autonomous Hamming flips',
        'compensation':'one more originally donor-vs-recipient-different site outside target patch, each of 14 alternate nonzero 4-bit values; no outcome inspected',
        'tiers':list(TIERS),
        'interpretation':'conditional one-extra-site feasibility, not proof of all possible compensated controls',
        'independence':'parent clusters; patches and candidates dependent'},
       'inventory':dict(sorted(inv.items())),'summary':summary,'raw_gap_histogram':dict(sorted(gap_hist.items())),
       'patch_records':record}

def main():
 a=argparse.ArgumentParser();a.add_argument('--reference',type=Path,default=ROOT/'112_probe_discrimination_audit/results/default.json');a.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json');a.add_argument('--max-parents',type=int,default=None);z=a.parse_args()
 if z.max_parents is not None and z.max_parents<1:a.error('max-parents positive')
 d=assay(z.reference,z.max_parents);z.output.parent.mkdir(parents=True,exist_ok=True);z.output.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'inventory':d['inventory'],'raw_gap_histogram':d['raw_gap_histogram'],'summary':d['summary']},sort_keys=True,indent=2))
if __name__=='__main__':main()
