#!/usr/bin/env python3
"""Cluster-aware signed bounds across a frozen physical spread threshold family."""
import csv,json,collections,argparse
from pathlib import Path
ROOT=Path(__file__).parent;TH=(10,20,30,40,50,60);H=(500,2000,50000)

def label(row,k,h):
 t=row[f'first{k}'];re=row['recurrence']
 if 0<=t<=h:return 'yes'
 if re>=0 and re<=h:return 'certified_no'
 return 'unknown'

def analyze(rows):
 assert len(rows)==3300
 parent=collections.defaultdict(lambda:[collections.Counter(),collections.Counter()])
 results={}
 for k in TH:
  result={}
  for h in H:
   counts=[collections.Counter(),collections.Counter()]
   cluster=collections.defaultdict(lambda:[collections.Counter(),collections.Counter()])
   for r in rows:
    lab=label(r,k,h);counts[r['arm']][lab]+=1;cluster[r['parent_id']][r['arm']][lab]+=1
   g,c=counts;lower=g['yes']-c['yes']-c['unknown'];upper=g['yes']+g['unknown']-c['yes']
   parent_counter=collections.Counter()
   for p,(pg,pc) in cluster.items():
    lo=pg['yes']-pc['yes']-pc['unknown'];hi=pg['yes']+pg['unknown']-pc['yes']
    parent_counter['G0_greater']+=lo>0
    parent_counter['control_greater']+=hi<0
    parent_counter['undetermined_or_tied']+=lo<=0<=hi
   result[str(h)]={'G0':dict(g),'control':dict(c),'lower_count':lower,'upper_count':upper,
    'lower_fraction':lower/1650,'upper_fraction':upper/1650,'parent_bound_signs':dict(parent_counter)}
  results[str(k)]=result
 for k in TH:
  assert results[str(k)]['50000']['upper_count']<0, k
 assert results['10']['50000']['G0']['yes']==173
 assert results['10']['50000']['control']['yes']==453
 assert (results['60']['50000']['G0']['yes'],results['60']['50000']['control']['yes'])==(143,395)
 return {'experiment':130,'protocol':{
   'physics':'unchanged 104/108/127 ring and material probes',
   'thresholds':list(TH),'horizons':list(H),
   'event': 'ever touches at least K distinct physical window positions in historical nonzero union',
   'negative_certificate':'exact full-state plus next-phase recurrence before reaching K',
   'independence':'55 matched parent pairs; 30 correlated probes per arm',
   'endpoint_independence':'this post-hoc threshold family and previous 60-position endpoint share the same physical trajectories'},
   'results':results}

def main():
 a=argparse.ArgumentParser();a.add_argument('--csv',type=Path,default=ROOT/'results/probes.csv');a.add_argument('--output',type=Path,default=ROOT/'results/default.json');z=a.parse_args()
 with z.csv.open(newline='')as f:rows=[{k:int(v) for k,v in r.items()}for r in csv.DictReader(f)]
 result=analyze(rows);z.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 for t,v in result['results'].items():
  z=v['50000'];print('threshold',t,'G0',z['G0'],'control',z['control'],'lower',z['lower_fraction'],'upper',z['upper_fraction'],'parent signs',z['parent_bound_signs'])
if __name__=='__main__':main()
