#!/usr/bin/env python3
"""Exp124 read-only stratification of 122 heldout material outcomes by 123 no-material recurrence.

Post-treatment conditioning (on another physics-derived state measurement)
changes population, it does not identify mediation or causal effects.
"""
import argparse,json,statistics
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
STRATA=('both_connected','both_censored','mixed_resolved','other')

def label(a,b):
 if a['class']=='connected' and b['class']=='connected' and not a['censored_500'] and not b['censored_500']:return 'both_connected'
 if a['censored_500'] and b['censored_500']:return 'both_censored'
 if not a['censored_500'] and not b['censored_500'] and a['class']!=b['class']:return 'mixed_resolved'
 return 'other'

def assay(a_file,b_file):
 A=json.loads(Path(a_file).read_text());B=json.loads(Path(b_file).read_text());assert A['experiment']==123 and B['experiment']==122
 b={(x['pid'],x['width'],tuple(x['patch'])):x for x in B['patch_records']}
 rows=[]
 for x in A['patch_records']:
  y=b.get((x['pid'],x['width'],tuple(x['patch'])))
  if y is None:raise AssertionError('cohort mismatch')
  stratum=label(x['transplant'],x['equal_edit_null'])
  rows.append({'parent_id':x['pid'],'width':x['width'],'patch':x['patch'],'stratum':stratum,
     'post_connected_diff':(y['transplant']['connected']-y['equal_edit_null']['connected'])/24,
     'post_censor_diff':(y['transplant']['censored']-y['equal_edit_null']['censored'])/24,
     'autonomous_G0_class':x['transplant']['class'],
     'autonomous_null_class':x['equal_edit_null']['class']})
 summary={}
 for width in (1,2,3):
  summary[str(width)]={}
  for s in STRATA:
   rr=[r for r in rows if r['width']==width and r['stratum']==s]
   grp=defaultdict(list)
   for r in rr:grp[r['parent_id']].append(r)
   parents=[]
   for pid,recs in sorted(grp.items()):
    parents.append({'parent_id':pid,'patches':len(recs),
      'connected_difference':statistics.mean(x['post_connected_diff'] for x in recs),
      'censor_difference':statistics.mean(x['post_censor_diff'] for x in recs)})
   summary[str(width)][s]={'patches':len(rr),'parents':len(parents),
       'mean_connected_difference':statistics.mean(x['connected_difference'] for x in parents) if parents else None,
       'mean_censor_difference':statistics.mean(x['censor_difference'] for x in parents) if parents else None,
       'parent_connected_wins':sum(x['connected_difference']>1e-12 for x in parents),
       'parent_connected_losses':sum(x['connected_difference']<-1e-12 for x in parents),
       'parent_connected_ties':sum(abs(x['connected_difference'])<=1e-12 for x in parents),
       'parent_details':parents}
 return {'experiment':124,'protocol':{'inputs':'read-only exact frozen 122 and 123 JSON results; no simulation or physics revisions',
   'stratification':'autonomous pre-material 500-tick state class for donor and equal-edit null',
   'post_measure':'heldout material 500-tick cycle-connected and right-censored rates',
   'independence':'parent unit, not 15 independent patch trials',
   'strict_warning':'subset conditioning on baseline orbit outcome is selection, NOT causal mediation identification'},
   'summary':summary,'patch_records':rows}

def main():
 p=argparse.ArgumentParser();p.add_argument('--material',type=Path,default=ROOT/'122_heldout_cycle_outcomes/results/default.json');p.add_argument('--autonomous',type=Path,default=ROOT/'123_autonomous_viability_control/results/default.json');p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json');z=p.parse_args()
 r=assay(z.autonomous,z.material);z.output.parent.mkdir(parents=True,exist_ok=True);z.output.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'summary':{w:{s:{k:v for k,v in q.items() if k!='parent_details'} for s,q in d.items()} for w,d in r['summary'].items()}},sort_keys=True,indent=2))
if __name__=='__main__':main()
