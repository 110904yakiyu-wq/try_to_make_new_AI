"""Exp143: deterministic cumulative eligibility-and-spread by proposal budget.
No post-response parent inclusion; a budget includes a parent iff its first
pre-response eligible attempt <= B. Frozen selected control is unchanged.
"""
import csv,json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'140_extended_matched_spread/results/probes.csv'
ROSTER=HERE.parent/'139_extended_control_budget/results/default.json'
OLD=HERE.parent/'137_matching_budget_sensitivity/results/default.json'
BUDGETS=(1,2,5,10,25,50,75,100,150,200,300,400,500,750,1000)

def bounds(rows,k):
 a=Counter('yes' if q[f'first{k}']>=0 else 'unknown' if q['recurrence']<0 else 'no' for q in rows if q['arm']==0)
 b=Counter('yes' if q[f'first{k}']>=0 else 'unknown' if q['recurrence']<0 else 'no' for q in rows if q['arm']==1)
 n=sum(a.values());assert n==sum(b.values())
 if not n:return None
 return {'n_per_arm':n,'G0_yes':a['yes'],'control_yes':b['yes'],'G0_unknown':a['unknown'],'control_unknown':b['unknown'],
         'lower_delta':a['yes']-b['yes']-b['unknown'], 'upper_delta':a['yes']+a['unknown']-b['yes'],
         'lower_rate':(a['yes']-b['yes']-b['unknown'])/n, 'upper_rate':(a['yes']+a['unknown']-b['yes'])/n}

def assay(probes=SOURCE,roster=ROSTER,legacy=OLD):
 with open(probes,newline='') as f:rows=[{k:int(v) for k,v in r.items()} for r in csv.DictReader(f)]
 meta=json.loads(Path(roster).read_text());assert len(meta['parent_records'])==130
 attempts={q['parent_id']:q['first_eligible_attempt'] for q in meta['parent_records'] if q['first_eligible_attempt'] is not None}
 assert len(attempts)==113 and len(rows)==6780
 result={'experiment':143,'contract':{'selection':'first acceptable pre-response control under budget B, B<=1000','parent_family':'frozen 130 G0 catalog',
 'outcomes':'exact reused Experiment140 50000-tick spread records; no resimulation',
 'censor':'unknown if no recurrence and no event by horizon',
 'limitations':'budget sweep is nested cohorts of correlated parents, not 15 new independent experiments'},'budgets':{}}
 for B in BUDGETS:
  valid={pid for pid,a in attempts.items() if a<=B}
  sub=[r for r in rows if r['parent_id'] in valid]
  assert len(sub)==len(valid)*60
  result['budgets'][str(B)]={'parents':len(valid),'spread10':bounds(sub,10),'spread60':bounds(sub,60)}
 assert result['budgets']['100']['parents']==55 and result['budgets']['1000']['parents']==113
 if Path(legacy).exists():
  old=json.loads(Path(legacy).read_text())
  for B in (1,2,5,10,25,50,75,100):
   assert result['budgets'][str(B)]['parents']==old['budget_results'][str(B)]['eligible_parents']
   for th in (10,60):
    a=result['budgets'][str(B)][f'spread{th}']
    b=old['budget_results'][str(B)][f'spread{th}']
    assert a['lower_delta']==b['lower_delta'] and a['upper_delta']==b['upper_delta'],(B,th)
 return result
if __name__=='__main__':
 x=assay();(HERE/'results/default.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
 (HERE/'results/default.txt').write_text(json.dumps(x['budgets'],indent=2,sort_keys=True)+'\n')
 print('exp143 budgets:',[(b,r['parents'],round(r['spread10']['upper_rate']*100,2)) for b,r in x['budgets'].items()])
