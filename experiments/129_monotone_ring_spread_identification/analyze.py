#!/usr/bin/env python3
"""Sharp finite-population partial-identification intervals for monotone spread."""
import csv,json,collections,statistics,argparse
from pathlib import Path
ROOT=Path(__file__).parent
HORIZONS=(100,250,500,1000,2000,50000)

def classify(r,h):
 full=r['first_full_ring_tick'];no=r['proven_never_full_ring_tick']
 if full>=0 and full<=h:return 'ever_full'
 if no>=0 and no<=h:return 'never_full_certified'
 return 'unresolved'

def summarize(rows):
 assert len(rows)==3300 and len(set(x['parent_id'] for x in rows))==55
 out={}
 for h in HORIZONS:
  counts=[collections.Counter(),collections.Counter()];clusters=collections.defaultdict(lambda:[collections.Counter(),collections.Counter()])
  for r in rows:
   cat=classify(r,h);counts[r['arm']][cat]+=1;clusters[r['parent_id']][r['arm']][cat]+=1
  a,b=counts;lo=a['ever_full']-b['ever_full']-b['unresolved'];hi=a['ever_full']+a['unresolved']-b['ever_full']
  parent_positive=parent_negative=parent_ambig=0
  details=[]
  for pid,(x,y) in sorted(clusters.items()):
   l=x['ever_full']-y['ever_full']-y['unresolved'];u=x['ever_full']+x['unresolved']-y['ever_full']
   parent_positive+=l>0;parent_negative+=u<0;parent_ambig+=l<=0<=u
   details.append({'parent_id':pid,'G0':dict(x),'control':dict(y),'lower_difference':l,'upper_difference':u})
  out[str(h)]={'G0':dict(sorted(a.items())),'control':dict(sorted(b.items())),
     'lower_count_difference':lo,'upper_count_difference':hi,
     'lower_rate_difference':lo/1650,'upper_rate_difference':hi/1650,
     'G0_spreads_more_guaranteed_parents':parent_positive,
     'control_spreads_more_guaranteed_parents':parent_negative,
     'parent_sign_indeterminate':parent_ambig}
  if h==50000:parent_records=details
 # Exact independent regression to Experiment127 and Experiment128 subcohort.
 z=out['50000']
 assert z['G0']['ever_full']==143 and z['G0']['never_full_certified']==1507 and z['G0'].get('unresolved',0)==0
 assert z['control']['ever_full']==395 and z['control']['never_full_certified']==1254 and z['control']['unresolved']==1
 assert out['500']['G0']['ever_full']==129 and out['500']['control']['ever_full']==369
 return {'experiment':129,'population':'55 frozen exact-autonomous-matched G0/control pairs, 30 material probes per arm',
 'endpoint':'Ever visits all 60 ring positions by a nonzero raw window value, cumulative historical union. NOT eventual recurrent connected-cycle class.',
 'certification':'ever_full if visited all 60 positions, never_full if complete full-state+next-phase recurrence was detected first with no full historical spread; otherwise right-censored',
 'horizon_bounds':out,'parent_records_at_max_horizon':parent_records,
 'metadata':{'reference':'Experiment127 recurrence CSV and frozen phase0 parent/control states','max_ticks':50000,'n_parents':55,'n_per_arm':1650,'unique_initial_states':3270}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,default=ROOT/'results/probes.csv');p.add_argument('--output',type=Path,default=ROOT/'results/default.json');a=p.parse_args()
 with a.csv.open(newline='')as f:r=[{k:int(v) for k,v in row.items()}for row in csv.DictReader(f)]
 result=summarize(r);a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 for h,z in result['horizon_bounds'].items():
  print(h,'G0',z['G0'],'control',z['control'],'lower upper',z['lower_rate_difference'],z['upper_rate_difference'],'parent signs',z['G0_spreads_more_guaranteed_parents'],z['control_spreads_more_guaranteed_parents'],z['parent_sign_indeterminate'])
if __name__=='__main__':main()
