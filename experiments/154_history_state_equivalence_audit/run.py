#!/usr/bin/env python3
"""Exp154: separate commutative history paths from distinct final microstates.

Uses pretest state identity from frozen Exp153, no additional simulation,
post-hoc equivalence classes are explanatory, NOT a new causal estimator.
"""
import argparse,csv,json,statistics
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'153_input_order_history_gate/results'

def analyze(meta,rows):
 contexts={(x['parent_id'],x['test_side']):x for x in meta['contexts']}
 paired=defaultdict(dict)
 for q in rows:
  key=(int(q['parent_id']),int(q['test_side']),int(q['test_raw']))
  paired[key][q['schedule']]=q
 assert len(paired)==len(contexts)*4
 audit=defaultdict(lambda:defaultdict(list));counts=Counter();fail=[]
 for key,arms in paired.items():
  pid,side,raw=key;ctx=contexts[(pid,side)]
  eq=ctx['left_equal_right']
  group='same_state' if eq else 'different_state'
  counts[group]+=1
  assert set(arms)=={'left_first','right_first','simultaneous'}
  for field in ('union_affected_sites','reached_10','reached_30'):
   a=float(arms['left_first'][field]);b=float(arms['right_first'][field]);c=float(arms['simultaneous'][field]);diff=a-b
   audit[group][(pid,field)].append(diff)
   if eq and (diff!=0 or a!=c):fail.append((key,field,diff,a-c))
 assert not fail,fail[:3]
 out={}
 for group in ('same_state','different_state'):
  parents=sorted({pid for pid,field in audit[group]})
  stats={}
  for field in ('union_affected_sites','reached_10','reached_30'):
   means=[statistics.mean(audit[group][(pid,field)]) for pid in parents]
   stats[field]={'parent_mean_left_minus_right':statistics.mean(means) if means else None,
                 'parents_left_higher':sum(x>0 for x in means),
                 'parents_right_higher':sum(x<0 for x in means),
                 'parent_ties':sum(x==0 for x in means)}
  out[group]={'eligible_site_contexts':sum(v['left_equal_right']==(group=='same_state') for v in contexts.values()),
              'paired_heldout_probes':counts[group],'distinct_parents':len(parents),'stats':stats}
 assert out['same_state']['eligible_site_contexts']==46
 assert out['different_state']['eligible_site_contexts']==64
 return {'experiment':154,'protocol':{
   'inputs':'frozen Exp153 physical states and heldout responses',
   'same_state':'exactly equal 60-window phase0 microstate at tick72 for ordered sequences',
   'future':'same raw heldout input at same site and same scheduler phase',
   'theorem':'same full microstate + phase + intervention implies identical deterministic future',
   'selection':'state identity defined pre-heldout, and group outcomes are descriptive only',
   'claims':'observed order effect does not establish adaptation, abstract memory, SELF, or learning'},
   'integrity':{'paired_probe_keys':len(paired),'same_state_future_mismatches':len(fail)},'results':out}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--reference',type=Path,default=SOURCE/'default.json');ap.add_argument('--probes',type=Path,default=SOURCE/'probes.csv');ap.add_argument('--output',type=Path,default=HERE/'results/default.json');a=ap.parse_args()
 meta=json.loads(a.reference.read_text(encoding='utf-8'))
 with a.probes.open(newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
 r=analyze(meta,rows);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':main()
