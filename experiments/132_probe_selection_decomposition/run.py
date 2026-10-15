#!/usr/bin/env python3
"""Experiment 132: separate parent-selection and probe-selection in Experiment 131.

No new trajectory evaluation, physics, intervention, or control optimization.
Observational decomposition of fixed G0-control difference under selected
physical feature equality. This is not an estimate of mediation.
"""
from pathlib import Path
from collections import Counter,defaultdict
import csv,json,statistics,argparse
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'131_feature_conditioned_spread_audit/results/paired_features.csv'
TIERS=('all','popcount','pop_and','pop_and_flips','first_changed_mask')
THRESHOLDS=(10,20,30,40,50,60)

def tier_selected(row,tier):
    return all(row[f'{name}_equal']==1 for name in
          {'all':(), 'popcount':('popcount',), 'pop_and':('popcount','and'),
           'pop_and_flips':('popcount','and','flips'),
           'first_changed_mask':('popcount','and','flips','first_mask')}[tier])

def load():
    with SOURCE.open(newline='') as f:raw=list(csv.DictReader(f))
    assert len(raw)==1650
    for r in raw:
        for key in ('parent_id','side','raw','popcount_equal','and_equal','flips_equal','first_mask_equal'):
            r[key]=int(r[key])
    return raw

def bounds(rows,k):
    if not rows:return None
    g=Counter(x[f'g0_K{k}'] for x in rows)
    c=Counter(x[f'control_K{k}'] for x in rows)
    n=len(rows)
    return {'n':n,'g0':dict(sorted(g.items())),'control':dict(sorted(c.items())),
            'lower_fraction':(g['yes']-c['yes']-c['unknown'])/n,
            'upper_fraction':(g['yes']+g['unknown']-c['yes'])/n}

def parent_equal(rows,k):
    by=defaultdict(list)
    for r in rows:by[r['parent_id']].append(r)
    arr=[bounds(q,k) for q in by.values()]
    return {'parents':len(by),
            'lower_fraction':statistics.mean(x['lower_fraction'] for x in arr),
            'upper_fraction':statistics.mean(x['upper_fraction'] for x in arr)} if arr else None

def analyze(rows):
    parent_all=defaultdict(list)
    for row in rows:parent_all[row['parent_id']].append(row)
    assert len(parent_all)==55 and all(len(x)==30 for x in parent_all.values())
    result={}
    for tier in TIERS:
        eligible=[r for r in rows if tier_selected(r,tier)]
        parent_set={r['parent_id'] for r in eligible}
        same_parents=[r for r in rows if r['parent_id'] in parent_set]
        excluded=[r for r in same_parents if not tier_selected(r,tier)]
        assert len(eligible)+len(excluded)==len(same_parents)
        groups={'full_55_parent_cohort':rows,
                'same_eligible_parents_all_30':same_parents,
                'feature_eligible_probes':eligible,
                'same_parents_feature_ineligible_probes':excluded}
        result[tier]={ 'eligible_parents':len(parent_set), 'eligible_parent_ids':sorted(parent_set),
          'components':{group:{'probes':len(part),'parents':len({q['parent_id'] for q in part}),
             'by_threshold':{str(k):{'pooled':bounds(part,k),'parent_equal':parent_equal(part,k)} for k in THRESHOLDS}}
             for group,part in groups.items()}}
        for k in THRESHOLDS:
            # The pooled difference on identical parent population is exactly a
            # probe-count weighted average of eligible and excluded differences.
            e=bounds(eligible,k);u=bounds(excluded,k);a=bounds(same_parents,k)
            if u:
                frac=e['n']/a['n']
                for v in ('lower_fraction','upper_fraction'):
                    assert abs(a[v]-(frac*e[v]+(1-frac)*u[v]))<1e-12
            else:assert a==e
    return {'experiment':132,'protocol':{
        'data':'read-only Experiment131 fixed 1650 G0-control probe-feature paired rows',
        'design':'partition all 55 parents into those eligible for feature stratum, and within these parents partition eligible vs ineligible probes',
        'endpoint':'ever-union-reaches-K conditional bounds at 50k; no censor-as-negative',
        'scientific_status':'deterministic sampling-composition accounting, not causal adjustment/mediation/significance',
        'thresholds':list(THRESHOLDS),'tiers':list(TIERS)},'decomposition':result}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'results/default.json');args=ap.parse_args()
    ans=analyze(load());args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(ans,sort_keys=True,indent=2)+'\n')
    for tier,rr in ans['decomposition'].items():
        print(tier,rr['eligible_parents'],'parents')
        for group,z in rr['components'].items():
            b10=z['by_threshold']['10']['pooled'];b60=z['by_threshold']['60']['pooled']
            print(group,z['probes'],'K10',None if b10 is None else [b10['lower_fraction'],b10['upper_fraction']],
                  'K60',None if b60 is None else [b60['lower_fraction'],b60['upper_fraction']])
if __name__=='__main__':main()
