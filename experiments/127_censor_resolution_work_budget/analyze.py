#!/usr/bin/env python3
"""Aggregate exact-horizon persistence bounds without treating censoring as failure."""
import csv, json, collections, argparse
from pathlib import Path
HORIZONS=(500,1000,2000,4000,8000,16000,32000,50000)
CLASSES={-1:'censored',0:'static',1:'connected',2:'fragmented'}

def analyze(csv_path):
 with open(csv_path,newline='') as f: rows=[{k:int(v) for k,v in r.items()} for r in csv.DictReader(f)]
 assert len(rows)==3300 and len({(r['pid'],r['arm'],r['side'],r['raw']) for r in rows})==3300
 assert len({r['pid'] for r in rows})==55
 assert len({(r['pid'],r['arm'],r['side'],r['raw']) for r in rows})==3300
 aggregate={};parent_rows=[];previous=None
 for h in HORIZONS:
  counts=[collections.Counter(),collections.Counter()]
  parents=collections.defaultdict(lambda:[collections.Counter(),collections.Counter()])
  for r in rows:
   label=CLASSES[r['class']] if 0<=r['recurrence']<=h else 'censored'
   counts[r['arm']][label]+=1;parents[r['pid']][r['arm']][label]+=1
  assert sum(counts[0].values())==sum(counts[1].values())==1650
  g,c=counts
  lower=g['connected']-c['connected']-c['censored']
  upper=g['connected']+g['censored']-c['connected']
  positive=negative=ambiguous=0
  details=[]
  for pid,(p0,p1) in sorted(parents.items()):
   lo=p0['connected']-p1['connected']-p1['censored']
   hi=p0['connected']+p0['censored']-p1['connected']
   positive+=lo>0;negative+=hi<0;ambiguous+=lo<=0<=hi
   details.append({'parent_id':pid,'G0':dict(p0),'control':dict(p1),'lower':lo,'upper':hi})
  # CPU work measured in exact kernel state transitions of each unique initial microstate.
  unique={}
  for r in rows:
   key=(r['pid'],r['arm'],r['side'],r['raw'])
   if r['cache_hit']==0:unique[key]=r['recurrence']
  assert len(unique)==3270
  work=sum(min(n if n>=0 else h,h) for n in unique.values())
  agg={'horizon':h,'G0':dict(sorted(g.items())),'control':dict(sorted(c.items())),
    'observed_confirmed_difference':g['connected']-c['connected'],
    'lower_delta_count':lower,'upper_delta_count':upper,
    'lower_rate':lower/1650,'upper_rate':upper/1650,
    'robust_G0_parents':positive,'robust_control_parents':negative,'sign_indeterminate_parents':ambiguous,
    'unique_orbit_steps_cumulative':work}
  if previous is not None:
   agg['additional_orbit_steps']=work-previous['unique_orbit_steps_cumulative']
   agg['newly_resolved_G0']=previous['G0']['censored']-g['censored']
   agg['newly_resolved_control']=previous['control']['censored']-c['censored']
   agg['gain_rate_bound_width']= (previous['upper_delta_count']-previous['lower_delta_count']-(upper-lower))/1650
  aggregate[str(h)]=agg
  if h==50000:parent_rows=details
  previous=agg
 # preserve strict expected historical validation
 v=aggregate['500'];w=aggregate['2000']
 assert (v['G0']['connected'],v['control']['connected'],v['G0']['censored'],v['control']['censored'])==(1486,1215,143,398)
 assert (w['G0']['connected'],w['control']['connected'],w['G0']['censored'],w['control']['censored'])==(1486,1218,143,395)
 assert (v['robust_G0_parents'],v['robust_control_parents'],v['sign_indeterminate_parents'])==(11,1,43)
 return {'experiment':127,'horizons':list(HORIZONS),'reference':'Exp126 full 55-pair frozen roster, 30 material probes per parent per arm',
 'physics':'exact 104/108 left-rotation phase0 three-phase 60x4-bit updates; C++ port checked against 125/126 results at 500 and 2000',
 'max_horizon':50000,'cohort_size':55,'observations_each_arm':1650,'distinct_initial_states':3270,
 'censoring':'right-censored until full-state and next-phase exact recurrence; no assumptions on eventual fate',
 'aggregate':aggregate,'parent_records_at_max_horizon':parent_rows}

def main():
 root=Path(__file__).parent
 p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,default=root/'results/probes.csv');p.add_argument('--output',type=Path,default=root/'results/default.json');z=p.parse_args()
 result=analyze(z.csv)
 z.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 for h,r in result['aggregate'].items():
  print(h,'G0',r['G0']['connected'],'C',r['control']['connected'],'G0cens',r['G0']['censored'],'Ccens',r['control']['censored'],'bounds',f"[{r['lower_rate']:.3%},{r['upper_rate']:.3%}]",'signs',r['robust_G0_parents'],r['robust_control_parents'],r['sign_indeterminate_parents'],'kernel_work',r['unique_orbit_steps_cumulative'])
if __name__=='__main__':main()
