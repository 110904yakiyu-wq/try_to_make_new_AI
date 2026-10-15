#!/usr/bin/env python3
"""Exp134: account for variability over ALL ex-ante eligible on-cycle controls.

Counterfactual *choice envelopes* use outcome-adaptive min/max only as
mathematical sensitivity bounds, never as deployable selection or significance.
"""
from pathlib import Path
from collections import defaultdict, Counter
import json,csv,statistics,argparse
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
REF133=ROOT/'133_eligible_control_multiplicity/results/default.json'
REF130=ROOT/'130_spread_threshold_robustness/results/probes.csv'
ALTS=HERE/'results/probes.csv'
KEYS=(10,60)

def read_csv(path):
    with Path(path).open(newline='') as f:
        return [{k:int(v) for k,v in x.items()} for x in csv.DictReader(f)]

def event(row,k):
    first=row[f'first{k}']
    if first>=0:return 'yes'
    if row['recurrence']>=0:return 'no'
    return 'unknown'

def counts(rs,k):
    c=Counter(event(x,k) for x in rs)
    return {'yes':c['yes'],'no':c['no'],'unknown':c['unknown']}

def limits(c,denom):
    return [c['yes']/denom,(c['yes']+c['unknown'])/denom]

def assay(reference,baseline,alternative):
    source=json.loads(Path(reference).read_text())
    assert source['experiment']==133 and source['summary']['eligible_parents']==55
    parents={x['parent_id']:x for x in source['parent_records'] if x['num_eligible_candidates']}
    base=read_csv(baseline);alt=read_csv(alternative)
    assert len(base)==3300 and len(alt)==960
    groups=defaultdict(list)
    for row in base:
        key=(row['parent_id'],0 if row['arm']==0 else 1)
        if key[1]==1:
            key=(row['parent_id'],parents[row['parent_id']]['accepted_attempts'][0])
        groups[key].append(row)
    for row in alt:
        assert row['attempt'] in parents[row['parent_id']]['accepted_attempts'][1:]
        groups[(row['parent_id'],row['attempt'])].append(row)
    assert len(groups)==55+87
    assert all(len(v)==30 for v in groups.values())
    parent_details=[]
    for pid,ref in sorted(parents.items()):
        g0=groups[(pid,0)]
        attempts=ref['accepted_attempts']
        options=[groups[(pid,a)] for a in attempts]
        parent_details.append({'parent_id':pid,'seed':ref['seed'],'candidate_attempts':attempts,
          'num_candidates':len(attempts),'endpoints':{
           str(k):{'G0':counts(g0,k),'controls':[{'attempt':a,'count':counts(rs,k)} for a,rs in zip(attempts,options)]}
           for k in KEYS}})
    outcomes={}
    for k in KEYS:
        original=[];choice_mean=[];envelope=[]
        varied=0;sign_change=0
        for p in parent_details:
            t=p['endpoints'][str(k)];a=limits(t['G0'],30)
            ctrls=[limits(x['count'],30) for x in t['controls']]
            # Event-rate difference G0 - control; uncertain arm bounds propagate.
            variants=[[a[0]-c[1],a[1]-c[0]] for c in ctrls]
            original.append(variants[0]);choice_mean.append([statistics.mean(q[i] for q in variants) for i in (0,1)])
            envelope.append([min(q[0] for q in variants),max(q[1] for q in variants)])
            if len(ctrls)>1:
                varied+=len({tuple(c) for c in ctrls})>1
                sign_change+=min(q[0] for q in variants)<0 and max(q[1] for q in variants)>0
        outcomes[str(k)]={
            'original_first_choice_bounds':[statistics.mean(v[0] for v in original),statistics.mean(v[1] for v in original)],
            'within_parent_uniform_candidate_mean_bounds':[statistics.mean(v[0] for v in choice_mean),statistics.mean(v[1] for v in choice_mean)],
            'arbitrary_per_parent_choice_sensitivity_envelope':[statistics.mean(v[0] for v in envelope),statistics.mean(v[1] for v in envelope)],
            'multi_candidate_parents_with_control_outcome_variation':varied,
            'multi_candidate_parents_with_both_strict_signs_possible':sign_change,
            'original_guaranteed_g0_positive_parents':sum(q[0]>0 for q in original),
            'original_guaranteed_control_positive_parents':sum(q[1]<0 for q in original),
            'any_choice_can_g0_win_parents':sum(q[1]>0 for q in envelope),
            'any_choice_can_control_win_parents':sum(q[0]<0 for q in envelope)}
    return {'experiment':134,'protocol':{
      'physics':'unchanged 104/108 phase0 left rotation, 60 four-bit windows',
      'same_cohort':'55 G0 parents with exact on-cycle support/period/phase0 occupancy matching in up to 100 attempts',
      'control_pool':'87 distinct eligible controls, including the 55 historical first accepted and 32 additional from exp133; selection precedes all material outcomes',
      'probe':'30 fixed raw material inputs per parent and each accepted control, both boundaries raw1..15',
      'horizon':50000,
      'observation':'ever union reaches 10 or 60 positions; recurrence certifies never after full microstate+next scheduler-phase repeat',
      'candidate_average':'uniform average over all accepted candidates within each parent, then equal parent weight (a specified sensitivity estimand, not a random population)',
      'choice_envelope':'min/max per parent across eligible controls computed retrospectively from outcomes; NOT a legitimate performance-optimized selector',
      'interpretation':'same 55 parent clusters, not 87 independent controls; not an organization-specific mechanism or statistical replication'},
      'summary':{'parent_count':len(parent_details),'control_microstates':sum(x['num_candidates'] for x in parent_details),
         'parents_with_multiple_eligible':sum(x['num_candidates']>1 for x in parent_details),'extra_control_probe_rows':len(alt),
         'endpoints':outcomes},'parent_records':parent_details}

def main():
    z=argparse.ArgumentParser();z.add_argument('--reference',type=Path,default=REF133)
    z.add_argument('--baseline',type=Path,default=REF130);z.add_argument('--alternatives',type=Path,default=ALTS)
    z.add_argument('--output',type=Path,default=HERE/'results/default.json');a=z.parse_args()
    res=assay(a.reference,a.baseline,a.alternatives);a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(res,sort_keys=True,indent=2)+'\n')
    print(json.dumps(res['summary'],sort_keys=True,indent=2))
if __name__=='__main__':main()
