#!/usr/bin/env python3
"""Exp137: read-only reconstruction of control-proposal budget sensitivity.
All selection uses autonomous pre-response eligibility in frozen Exp133.
The retained control is always the FIRST eligible within the budget, hence
its response is the same as the frozen Exp130 first-choice control.
"""
import argparse,csv,json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROSTER=HERE.parent/'133_eligible_control_multiplicity/results/default.json'
PROBES=HERE.parent/'130_spread_threshold_robustness/results/probes.csv'
BUDGETS=(1,2,5,10,25,50,75,100)

def bound(rows,k):
    n=len(rows)//2
    a=Counter('yes' if r[f'first{k}']>=0 else 'no' if r['recurrence']>=0 else 'unknown' for r in rows if r['arm']==0)
    b=Counter('yes' if r[f'first{k}']>=0 else 'no' if r['recurrence']>=0 else 'unknown' for r in rows if r['arm']==1)
    assert sum(a.values())==sum(b.values())==n
    lo=a['yes']-b['yes']-b['unknown'];hi=a['yes']+a['unknown']-b['yes']
    return {'n':n,'g0_yes':a['yes'],'ctrl_yes':b['yes'],'g0_unknown':a['unknown'],'ctrl_unknown':b['unknown'],
            'lower_delta':lo,'upper_delta':hi,'lower_rate':lo/n if n else None,'upper_rate':hi/n if n else None,
            'negative_identified':hi<0 if n else None}

def assay(roster=ROSTER,probes=PROBES):
    source=json.loads(Path(roster).read_text(encoding='utf-8'))
    assert source['summary']['eligible_parents']==55
    with Path(probes).open(newline='',encoding='utf-8') as f:rows=[{key:int(v) for key,v in q.items()} for q in csv.DictReader(f)]
    assert len(rows)==3300
    result={'experiment':137,'nature':'budget sensitivity reanalysis, no new controls or interventions',
            'protocol':'100 historical attempts per parent are frozen; budgets select first accepted attempt if within budget',
            'match_ratio_base':55/130,'budget_results':{}}
    prev=set()
    for B in BUDGETS:
        eligible={r['parent_id'] for r in source['parent_records'] if r['accepted_attempts'] and r['accepted_attempts'][0]<=B}
        assert prev.issubset(eligible);prev=eligible
        sub=[r for r in rows if r['parent_id'] in eligible]
        assert len(sub)==len(eligible)*60
        counts=Counter(r['num_eligible_candidates']>1 for r in source['parent_records'] if r['parent_id'] in eligible)
        result['budget_results'][str(B)]={'eligible_parents':len(eligible),'eligible_rate':len(eligible)/130,
                 'multiple_controls_available_within_100':counts[True],
                 'spread10':bound(sub,10) if eligible else None,'spread60':bound(sub,60) if eligible else None}
    assert result['budget_results']['100']['eligible_parents']==55
    assert result['budget_results']['100']['spread10']['lower_delta']==-280
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--roster',type=Path,default=ROSTER);ap.add_argument('--probes',type=Path,default=PROBES);ap.add_argument('--output',type=Path,default=HERE/'results/default.json');a=ap.parse_args()
    out=assay(a.roster,a.probes);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'budgets':{k:{'eligible':v['eligible_parents'],'spread10':v['spread10'],'spread60':v['spread60']} for k,v in out['budget_results'].items()}},sort_keys=True,indent=2))
if __name__=='__main__':main()
