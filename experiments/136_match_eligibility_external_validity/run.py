#!/usr/bin/env python3
"""Exp136: denominator and support audit; bounds for missing counterfactuals.
Read-only audit of historical Exp130 3300 rows and Exp133 130 G0 records.
A 100-draw unmatched parent is not proven to have no eligible null globally.
"""
import argparse,csv,json
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
CSV=HERE.parent/'130_spread_threshold_robustness/results/probes.csv'
REFERENCE=HERE.parent/'133_eligible_control_multiplicity/results/default.json'

def bound(rows,k):
    n=len(rows)//2
    assert n>0 and sum(r['arm']==0 for r in rows)==sum(r['arm']==1 for r in rows)==n
    counts={arm:Counter(('yes' if r[f'first{k}']>=0 else 'no' if r['recurrence']>=0 else 'unknown') for r in rows if r['arm']==arm) for arm in (0,1)}
    a,b=counts[0],counts[1]
    return {'n':n,'g0_yes':a['yes'],'control_yes':b['yes'],'g0_unknown':a['unknown'],'control_unknown':b['unknown'],
            'lower_count':a['yes']-b['yes']-b['unknown'],
            'upper_count':a['yes']+a['unknown']-b['yes']}

def assay(csv_path=CSV,ref_path=REFERENCE):
    source=json.loads(ref_path.read_text(encoding='utf-8'))
    parents=source['parent_records']
    assert len(parents)==130
    with csv_path.open(newline='',encoding='utf-8') as f:
        rows=[{k:int(v) for k,v in x.items()} for x in csv.DictReader(f)]
    assert len(rows)==3300
    roster={x['parent_id'] for x in parents if x['num_eligible_candidates']>0}
    assert len(roster)==55 and {r['parent_id'] for r in rows}==roster
    features=lambda p:{'period':p['period'],'union_support_size':len(p['union_support']),
        'seed_bitcount':sum(x.bit_count() for x in p['seed'])}
    group=defaultdict(lambda:{'total':0,'eligible':0,'eligible_control_count':0})
    for p in parents:
        for key,value in features(p).items():
            k=f'{key}:{value}'
            group[k]['total']+=1
            group[k]['eligible']+=int(p['num_eligible_candidates']>0)
            group[k]['eligible_control_count']+=p['num_eligible_candidates']
    for v in group.values():v['eligibility_rate']=v['eligible']/v['total']
    sub={}
    for k in (10,60):
        sampled=bound(rows,k)
        unmatched=(len(parents)-len(roster))*30
        all_n=len(parents)*30
        low=sampled['lower_count']-unmatched
        up=sampled['upper_count']+unmatched
        s={str(x):bound([r for r in rows if features(next(p for p in parents if p['parent_id']==r['parent_id']))['period']==x],k) for x in sorted({p['period'] for p in parents if p['parent_id'] in roster})}
        sub[str(k)]={'matched_55':sampled,'hypothetical_unmatched_parent_probe_rows_per_arm':unmatched,
         'all130_hypothetical_lower_count':low,'all130_hypothetical_upper_count':up,
         'all130_hypothetical_lower_fraction':low/all_n,'all130_hypothetical_upper_fraction':up/all_n,
         'matched_by_period':s}
    result={'experiment':136,'parent_count':130,'eligible_count':55,'unmatched_at_100_attempts':75,
            'eligibility_fraction':55/130,'note':'All130 contrasts are hypothetical arithmetic envelopes only; for 75 unmatched G0 there is no defined selected counterpart under original 100-attempt matching protocol.',
            'assumptions':'Hypothetically complete 75 pairs with arbitrary binary per-probe outcomes; no finite horizon censor-as-failure assumption.',
            'strata':dict(sorted(group.items())),'spread_bounds':sub}
    assert sub['10']['all130_hypothetical_lower_count']==-2530
    assert sub['10']['all130_hypothetical_upper_count']==1970
    assert sub['60']['all130_hypothetical_lower_count']==-2503
    assert sub['60']['all130_hypothetical_upper_count']==1998
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--probes',type=Path,default=CSV);p.add_argument('--roster',type=Path,default=REFERENCE);p.add_argument('--output',type=Path,default=HERE/'results/default.json');a=p.parse_args()
    out=assay(a.probes,a.roster);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'eligibility_fraction':out['eligibility_fraction'],'spread_bounds':out['spread_bounds']},indent=2,sort_keys=True))
if __name__=='__main__':main()
