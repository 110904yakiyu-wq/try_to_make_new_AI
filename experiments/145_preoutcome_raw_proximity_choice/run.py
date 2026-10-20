#!/usr/bin/env python3
"""Exp145: pre-outcome raw-bit proximity selection among 1000-budget eligible controls.
All raw selection criteria use ONLY autonomous phase0 G0 / control microstates.
The held-out 30 material responses are loaded separately after selections.
"""
import argparse, csv, json, statistics
from collections import defaultdict, Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
CONTROLS=ROOT/'142_all_control_choice_sensitivity/results/eligible_states.csv'
G0STATES=ROOT/'140_extended_matched_spread/results/selected_states.csv'
OUTCOMES=ROOT/'142_all_control_choice_sensitivity/results/per_control.csv'
G0PROBES=ROOT/'140_extended_matched_spread/results/probes.csv'
RULES=('first','min_raw_bit_distance','max_raw_bit_distance','median_raw_bit_distance','min_popcount_difference')

def read(path):
 with open(path,newline='',encoding='utf-8') as f:return list(csv.DictReader(f))

def metrics(a,b):
 assert len(a)==len(b)==60 and all(0<=i<=15 for i in a+b)
 return {'raw_bit_distance':sum((x^y).bit_count() for x,y in zip(a,b)),
 'raw_window_distance':sum(x!=y for x,y in zip(a,b)),
 'popcount_difference':abs(sum(x.bit_count() for x in a)-sum(x.bit_count() for x in b)),
 'and_difference':abs(sum((a[i]&a[(i+1)%60]).bit_count() for i in range(60))-
                      sum((b[i]&b[(i+1)%60]).bit_count() for i in range(60)))}

def select(candidates,rule):
 if rule=='first':return min(candidates,key=lambda c:c['attempt'])
 if rule=='min_raw_bit_distance':return min(candidates,key=lambda c:(c['raw_bit_distance'],c['raw_window_distance'],c['attempt']))
 if rule=='max_raw_bit_distance':return min(candidates,key=lambda c:(-c['raw_bit_distance'],-c['raw_window_distance'],c['attempt']))
 if rule=='median_raw_bit_distance':return sorted(candidates,key=lambda c:(c['raw_bit_distance'],c['raw_window_distance'],c['attempt']))[(len(candidates)-1)//2]
 if rule=='min_popcount_difference':return min(candidates,key=lambda c:(c['popcount_difference'],c['and_difference'],c['raw_bit_distance'],c['attempt']))
 raise ValueError(rule)

def assay(controls=CONTROLS,g0_states=G0STATES,outcomes=OUTCOMES,g0probes=G0PROBES):
 frames={int(q['parent_id']):bytes.fromhex(q['frame_hex']) for q in read(g0_states) if int(q['arm'])==0}
 assert len(frames)==113
 ctrl=defaultdict(list)
 for r in read(controls):
  pid=int(r['parent_id']);a=bytes.fromhex(r['frame_hex']); assert pid in frames
  vals=metrics(a,frames[pid]);ctrl[pid].append({'parent_id':pid,'attempt':int(r['attempt']),**vals})
 assert len(ctrl)==113 and sum(map(len,ctrl.values()))==970
 outcomes={(int(q['parent_id']),int(q['attempt'])):q for q in read(outcomes)}
 assert len(outcomes)==970
 probes=read(g0probes)
 assert len(probes)==6780
 truth=defaultdict(dict)
 for q in probes:
  if int(q['arm'])!=0:continue
  key=(int(q['side']),int(q['raw']));pid=int(q['parent_id']);assert key not in truth[pid]
  truth[pid][key]=q
 assert len(truth)==113 and all(len(q)==30 for q in truth.values())
 audit=[]
 for pid,candidates in sorted(ctrl.items()):
  for c in candidates:
   x=outcomes[(pid,c['attempt'])]
   for th in (10,60):
    c[f'yes{th}']=int(x[f'yes{th}']);c[f'unknown{th}']=int(x[f'unknown{th}'])
  row={'parent_id':pid,'controls':len(candidates), 'raw_distance_min':min(x['raw_bit_distance'] for x in candidates),
       'raw_distance_max':max(x['raw_bit_distance'] for x in candidates),
       'G0_yes10':sum(int(q['first10'])>=0 for q in truth[pid].values()),
       'G0_yes60':sum(int(q['first60'])>=0 for q in truth[pid].values()),
       'G0_unknown60':sum(int(q['first60'])<0 and int(q['recurrence'])<0 for q in truth[pid].values()),
       'selected':{}}
  for rule in RULES:
   chosen=select(candidates,rule)
   row['selected'][rule]={k:chosen[k] for k in ('attempt','raw_bit_distance','raw_window_distance','popcount_difference','and_difference','yes10','unknown10','yes60','unknown60')}
  audit.append(row)
 assert len(audit)==113 and sum(q['G0_yes10'] for q in audit)==326 and sum(q['G0_yes60'] for q in audit)==240
 summary={}
 for cohort,rs in [('all113',audit),('old55',[q for q in audit if q['selected']['first']['attempt']<=100]),('new58',[q for q in audit if q['selected']['first']['attempt']>100])]:
  assert len(rs)=={'all113':113,'old55':55,'new58':58}[cohort]
  results={}
  for rule in RULES:
   x={'parents':len(rs),'control_states_selected':len(rs),'selected_distance_mean':statistics.mean(q['selected'][rule]['raw_bit_distance'] for q in rs),
      'different_from_first':sum(q['selected'][rule]['attempt']!=q['selected']['first']['attempt'] for q in rs),
      'selected_exact_G0_microstate':sum(q['selected'][rule]['raw_bit_distance']==0 for q in rs)}
   for th in (10,60):
    g=sum(q[f'G0_yes{th}'] for q in rs);gu=sum(q.get(f'G0_unknown{th}',0) for q in rs)
    b=sum(q['selected'][rule][f'yes{th}'] for q in rs);bu=sum(q['selected'][rule][f'unknown{th}'] for q in rs)
    n=30*len(rs)
    x[f'spread{th}']={'G0_yes':g,'G0_unknown':gu,'control_yes':b,'control_unknown':bu,
                     'lower_delta_count':g-b-bu,'upper_delta_count':g+gu-b,
                     'lower_delta_fraction':(g-b-bu)/n,'upper_delta_fraction':(g+gu-b)/n}
   results[rule]=x
  summary[cohort]=results
 assert summary['all113']['first']['spread10']['control_yes']==765
 assert summary['all113']['first']['spread60']['control_yes']==634
 return {'experiment':145,'design':{'controls':'Exp139 970 fully preintervention eligible states over 113 parents',
  'selection':'deterministic phase0 raw distance/bit popcount only, without material response labels',
  'outcome':'frozen Exp140 G0 and Exp142 eligible control spread10/spread60, 50k or exact recurrence',
  'uncertainty':'no 60-position threshold crossing and no recurrence is right-censored',
  'independence':'113 parent clusters; 30 probes repeated within each'},'summary':summary,'parent_records':audit}

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'results/default.json');args=p.parse_args()
 d=assay();args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
 print(json.dumps({'experiment':145,'summary':d['summary']},sort_keys=True,indent=2))
if __name__=='__main__':main()
