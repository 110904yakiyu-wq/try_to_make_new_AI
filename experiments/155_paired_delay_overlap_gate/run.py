#!/usr/bin/env python3
"""Exp155: paired fixed-context delay effect, correcting Exp151 attrition.

No new trajectories or treatment fitting. Pair exact parent + train-side contexts
available at BOTH delays to avoid compositional changes in delayed comparisons.
"""
import argparse,csv,json,statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'151_experience_heldout_response_gate/results'
ARMS=('pulse7','pulse11');METRICS=('union_affected_sites','reached_10','reached_30')

def read(path):
 with Path(path).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))

def assay(probes,eligibility):
 viable={(int(r['parent_id']),int(r['train_side']),int(r['delay'])) for r in eligibility if r['eligible']=='True'}
 assert len(viable)==447
 common=sorted({(pid,side) for pid,side,delay in viable if (pid,side,24) in viable and (pid,side,96) in viable})
 assert len(common)==215
 accepted={(pid,side,delay) for pid,side in common for delay in (24,96)}
 data=defaultdict(lambda:defaultdict(list))
 for r in probes:
  key=(int(r['parent_id']),int(r['train_side']),int(r['delay']))
  if key in accepted:data[key][r['arm']].append(r)
 assert len(data)==430
 result={}
 for arm in ARMS:
  out={}
  for metric in METRICS:
   parent=defaultdict(lambda:defaultdict(list))
   for pid,side in common:
    for delay in (24,96):
     q=data[(pid,side,delay)]
     assert set(q)=={'sham','pulse7','pulse11'}
     assert len(q[arm])==len(q['sham'])==4
     def mean(names):
      vals=[float(x[metric] == "True") if x[metric] in ("True", "False") else float(x[metric]) for x in q[names]]
      return statistics.mean(vals)
     parent[pid][delay].append(mean(arm)-mean('sham'))
   a=[statistics.mean(r[24]) for r in parent.values()]
   b=[statistics.mean(r[96]) for r in parent.values()]
   ds=[y-x for x,y in zip(a,b)]
   out[metric]={'paired_parents':len(parent),'delay24_parent_mean_difference':statistics.mean(a),
                'delay96_parent_mean_difference':statistics.mean(b),
                'delay96_minus_24':statistics.mean(ds),
                'parents_delta_greater':sum(x>0 for x in ds),
                'parents_delta_smaller':sum(x<0 for x in ds),
                'parents_delta_equal':sum(x==0 for x in ds)}
  result[arm]=out
 return {'experiment':155,'protocol':{
         'source':'Exp151 frozen deterministic response and pretest-eligibility CSV',
         'fixed_cohort':'same parent and same training direction eligible at both delay24 and delay96',
         'outcomes':'parent-equal-weight pulse-versus-sham causal-response footprint and reach>=10/30',
         'design':'observational repeated-time comparison; not a retention, forgetting or memory mechanism estimator',
         'censor':'exclusion only on the pretest no-overwrite gate; never treat excluded as negative'},
         'inventory':{'all_parent_direction_contexts':260,'eligible_24':228,'eligible_96':219,
                      'shared_eligible_contexts':len(common),
                      'shared_parent_clusters':len(set(pid for pid,side in common)),
                      'per_arm_test_records_over_both_times':len(common)*2*4},
         'results':result}

def main():
 p=argparse.ArgumentParser();p.add_argument('--probes',type=Path,default=SOURCE/'probes.csv');p.add_argument('--eligibility',type=Path,default=SOURCE/'eligibility.csv');p.add_argument('--output',type=Path,default=HERE/'results/default.json');a=p.parse_args()
 r=assay(read(a.probes),read(a.eligibility));a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':main()
