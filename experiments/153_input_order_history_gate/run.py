#!/usr/bin/env python3
"""Exp153: two identical raw injections in different order; disjoint heldout test.

Order is an externally scripted history, NOT a stored instruction or learning.
Both chronological arms receive raw7 at left and raw11 at right exactly once.
Simultaneous control receives the same contents at tick 0. Test at phase0 t72.
"""
import argparse,csv,importlib.util,json,statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
spec=importlib.util.spec_from_file_location('exp151',ROOT/'151_experience_heldout_response_gate'/'run.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);m=v.m
SCHEDULES=('left_first','right_first','simultaneous')
RAWS=(1,5,9,14)
FIRST_GAP=24;END_TICK=72

def trajectory(frame,left,right,order):
 s=bytearray(frame)
 if order=='simultaneous':
  assert s[left]==s[right]==0
  s[left]=7;s[right]=11;events=[]
 else:
  first,second=((left,7),(right,11)) if order=='left_first' else ((right,11),(left,7))
  assert s[first[0]]==0
  s[first[0]]=first[1]
  events=[(FIRST_GAP,second)]
 for tick in range(END_TICK):
  if events and tick==events[0][0]:
   pos,raw=events[0][1]
   if s[pos]!=0:return None  # respect single-add/no-overwrite contract
   s[pos]=raw
  s=bytearray(m.step(s,tick%3))
 return bytes(s)

def summarize(rows,contexts):
 out={}
 for metric in ('union_affected_sites','reached_10','reached_30'):
  by_parent=defaultdict(lambda:defaultdict(list))
  for r in rows:by_parent[r['parent_id']][r['schedule']].append(float(r[metric]))
  assert all(set(x)==set(SCHEDULES) for x in by_parent.values())
  values={arm:statistics.mean(statistics.mean(rec[arm]) for rec in by_parent.values()) for arm in SCHEDULES}
  diff={}
  for a,b in (('left_first','right_first'),('left_first','simultaneous'),('right_first','simultaneous')):
   d=[statistics.mean(x[a])-statistics.mean(x[b]) for x in by_parent.values()]
   diff[a+'-'+b]={'mean':statistics.mean(d),'parent_a_higher':sum(x>0 for x in d),'parent_b_higher':sum(x<0 for x in d),'parent_tied':sum(x==0 for x in d)}
  out[metric]={'parent_count':len(by_parent),'per_arm_mean':values,'contrasts':diff}
 out['state_identity']={'both_ordered_states_same':sum(q['left_equal_right'] for q in contexts),
                       'all_three_same':sum(q['all_three_equal'] for q in contexts)}
 return out

def assay(limit=130):
 parents=list(m.parents());assert len(parents)==130
 out=[];contexts=[];eligible_parents=set();two_pulse_feasible=0
 for pid,(seed,frame,o) in enumerate(parents[:limit]):
  lo=(min(o['support'])-1)%60;hi=(max(o['support'])+1)%60
  sts={a:trajectory(frame,lo,hi,a) for a in SCHEDULES}
  if sts['left_first'] is None or sts['right_first'] is None:continue
  two_pulse_feasible+=1
  for test_side,site in ((0,(lo-2)%60),(1,(hi+2)%60)):
   if not all(sts[s][site]==0 for s in SCHEDULES):continue
   eligible_parents.add(pid)
   contexts.append({'parent_id':pid,'test_side':test_side,'site':site,
                    'left_equal_right':sts['left_first']==sts['right_first'],
                    'all_three_equal':len(set(sts.values()))==1,
                    'pretest_occupied_windows':{s:sum(bool(x) for x in sts[s]) for s in SCHEDULES},
                    'pretest_total_bits':{s:sum(x.bit_count() for x in sts[s]) for s in SCHEDULES}})
   for raw in RAWS:
    for schedule in SCHEDULES:
     score=v.response(sts[schedule],site,raw)
     out.append({'parent_id':pid,'seed':list(seed),'schedule':schedule,
                 'test_side':test_side,'test_raw':raw,
                 'union_affected_sites':score['union_affected_sites'],
                 'reached_10':int(score['reached_10']),'reached_30':int(score['reached_30'])})
 assert len(out)==len(contexts)*len(RAWS)*len(SCHEDULES)
 return {'experiment':153,'protocol':{'kernel':'unchanged Exp104 phase0 3-step scheduler; no learning primitive',
    'treatment':'equal input multiset {left:raw7,right:raw11}; chronological order left-first vs right-first at tick0/24',
    'control':'same raw values injected simultaneously at tick0; equal total material amount but different timing',
    'end':'all arms compared at common absolute tick72, scheduler phase0',
    'heldout':'original outer sites (left-2, right+2) only if unoccupied across all three arms; raw1,5,9,14',
    'metric':'60-tick time-integrated causal response positions versus own no-test future',
    'inference':'order sensitivity means ordinary nonlinear state dependence, not learning, optimization, or intrinsic memory'},
    'inventory':{'catalog_parents':130,'parents_evaluated':limit,'two_order_interventions_both_feasible':two_pulse_feasible,
                 'heldout_eligible_parents':len(eligible_parents),'heldout_eligible_side_contexts':len(contexts),
                 'observations_per_arm':len(out)//3},'summary':summarize(out,contexts),'contexts':contexts,'records':out}

def write(path,items,fields):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(items)

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'results/default.json');p.add_argument('--csv',type=Path,default=HERE/'results/probes.csv');p.add_argument('--max-parents',type=int,default=130);a=p.parse_args()
 r=assay(a.max_parents);a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps({k:v for k,v in r.items() if k!='records'},indent=2,sort_keys=True)+'\n')
 write(a.csv,[{k:x[k] for k in ('parent_id','schedule','test_side','test_raw','union_affected_sites','reached_10','reached_30')} for x in r['records']],('parent_id','schedule','test_side','test_raw','union_affected_sites','reached_10','reached_30'))
 print(json.dumps({'inventory':r['inventory'],'summary':r['summary']},indent=2,sort_keys=True))
if __name__=='__main__':main()
