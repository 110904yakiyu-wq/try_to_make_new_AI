#!/usr/bin/env python3
"""Experiment148: choose each autonomous control by predeclared six TRAIN raw probes'
phase-consistent early response masks; evaluate only the 24 disjoint held-out
raw probes' spread. Same frozen physical kernel and candidate eligibility.
"""
import argparse, csv, json, sys, statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'139_extended_control_budget'))
import core
TRAIN=(1,7,15)
HOLD=tuple(i for i in range(1,16) if i not in TRAIN)
TIMES=(1,3,6)
RULES={'first':(), 'raw_nearest':(), 'train_t1':(1,), 'train_t1_3':(1,3), 'train_t1_3_6':(1,3,6)}

def read(p):
 with open(p,newline='',encoding='utf-8') as f:return list(csv.DictReader(f))

def response_masks(s,site,raw):
 assert s[site]==0
 altered=bytearray(s);altered[site]=raw;altered=bytes(altered)
 baseline=bytes(s);out={}
 for tick in range(1,max(TIMES)+1):
  baseline=core.step(baseline,(tick-1)%3)
  altered=core.step(altered,(tick-1)%3)
  if tick in TIMES:
   out[tick]=sum(1<<i for i,(a,b) in enumerate(zip(baseline,altered)) if a!=b)
 return out

def signature(s,lo,hi):
 out={}
 for side,site in ((0,lo),(1,hi)):
  for raw in TRAIN:
   for tick,mask in response_masks(s,site,raw).items():out[(side,raw,tick)]=mask
 return out

def choose(rs,rule):
 if rule=='first':return min(rs,key=lambda x:x['attempt'])
 if rule=='raw_nearest':return min(rs,key=lambda x:(x['raw_hd'],x['window_hd'],x['attempt']))
 times=RULES[rule]
 return min(rs,key=lambda x:(sum(x['distances'][t] for t in times),x['raw_hd'],x['window_hd'],x['attempt']))

def assay():
 refs={}
 for r in read(ROOT/'140_extended_matched_spread/results/selected_states.csv'):
  if int(r['arm'])==0:
   pid=int(r['parent_id']);assert pid not in refs
   refs[pid]=(bytes.fromhex(r['frame_hex']),int(r['left']),int(r['right']),int(r['attempt']))
 assert len(refs)==113
 evals={(int(r['parent_id']),int(r['attempt']),int(r['side']),int(r['raw'])):r for r in read(ROOT/'142_all_control_choice_sensitivity/results/probes.csv') if int(r['raw']) in HOLD}
 assert len(evals)==970*24
 g0_eval={(int(r['parent_id']),int(r['side']),int(r['raw'])):r for r in read(ROOT/'140_extended_matched_spread/results/probes.csv') if int(r['arm'])==0 and int(r['raw']) in HOLD}
 assert len(g0_eval)==113*24
 g0sig={pid:signature(fr,lo,hi) for pid,(fr,lo,hi,_) in refs.items()}
 choices=defaultdict(list)
 for r in read(ROOT/'142_all_control_choice_sensitivity/results/eligible_states.csv'):
  pid=int(r['parent_id']);att=int(r['attempt']);s=bytes.fromhex(r['frame_hex']);g,lo,hi,refatt=refs[pid]
  assert int(r['left'])==lo and int(r['right'])==hi and s[lo]==s[hi]==0
  sig=signature(s,lo,hi);g0=g0sig[pid]
  distances={t:sum((mask^g0[side,raw,t]).bit_count() for (side,raw,j),mask in sig.items() if j==t) for t in TIMES}
  raw_hd=sum((a^b).bit_count() for a,b in zip(s,g));window_hd=sum(a!=b for a,b in zip(s,g))
  scores={}
  for th in (10,60):
   f=f'first{th}'
   rs=[evals[pid,att,side,raw] for side in (0,1) for raw in HOLD]
   scores[f'yes{th}']=sum(int(q[f])>=0 for q in rs)
   scores[f'unknown{th}']=sum(int(q[f])<0 and int(q['recurrence'])<0 for q in rs)
  choices[pid].append({'attempt':att,'raw_hd':raw_hd,'window_hd':window_hd,'distances':distances,**scores})
 assert len(choices)==113 and sum(map(len,choices.values()))==970
 parents=[]
 for pid,rs in sorted(choices.items()):
  chosen={}
  for rule in RULES:
   sel=choose(rs,rule)
   chosen[rule]={'attempt':sel['attempt'],'raw_hd':sel['raw_hd'],'window_hd':sel['window_hd'],
      'train_distance':sum(sel['distances'][t] for t in RULES[rule]) if RULES[rule] else None,
      'exact_train_response_t1_t3':sel['distances'][1]==sel['distances'][3]==0,
      'yes10':sel['yes10'],'unknown10':sel['unknown10'],'yes60':sel['yes60'],'unknown60':sel['unknown60']}
  G={}
  for th in (10,60):
   key=f'first{th}';rr=[g0_eval[pid,side,raw] for side in (0,1) for raw in HOLD]
   G[f'yes{th}']=sum(int(q[key])>=0 for q in rr)
   G[f'unknown{th}']=sum(int(q[key])<0 and int(q['recurrence'])<0 for q in rr)
  parents.append({'parent_id':pid,'first_attempt':refs[pid][3], 'G0':G, 'choices':chosen,'num_eligible_controls':len(rs)})
 assert len(parents)==113
 summary={}
 for name,rr in [('all113',parents),('old55',[r for r in parents if r['first_attempt']<=100]),('new58',[r for r in parents if r['first_attempt']>100])]:
  assert len(rr)=={'all113':113,'old55':55,'new58':58}[name]
  out={}
  for rule in RULES:
   d={'parents':len(rr),'heldout_probes_per_arm':len(rr)*24,
      'changed_choice_vs_first':sum(r['choices'][rule]['attempt']!=r['choices']['first']['attempt'] for r in rr),
      'mean_bitdistance0':statistics.mean(r['choices'][rule]['raw_hd'] for r in rr),
      'exact_training_t1_t3_parents':sum(r['choices'][rule]['exact_train_response_t1_t3'] for r in rr)}
   for th in (10,60):
    g=sum(r['G0'][f'yes{th}'] for r in rr);gu=sum(r['G0'][f'unknown{th}'] for r in rr)
    c=sum(r['choices'][rule][f'yes{th}'] for r in rr);cu=sum(r['choices'][rule][f'unknown{th}'] for r in rr)
    n=24*len(rr)
    d[f'spread{th}']={'G0_yes':g,'G0_unknown':gu,'control_yes':c,'control_unknown':cu,
        'lower_difference':(g-c-cu)/n,'upper_difference':(g+gu-c)/n}
   out[rule]=d
  summary[name]=out
 assert summary['all113']['first']['spread10']['control_yes']>0
 return {'experiment':148,'design':{'physics':'frozen 104/139, size60 4-bit phase0, no new primitive',
   'train':'left/right raw 1,7,15 (6 probes) at identical phase0 with own no-material counterfactual, response position masks at ticks 1,3,6',
   'test':'heldout left/right raw 2..14 excluding7 (24 probes) from frozen 140 G0 + 142 970-control material outcomes',
   'train_test_separation':'no test raw values or spread endpoint used to choose a control',
   'selection':'minimum summed train mask XOR-popcount; tie raw Hamming, differing windows, attempt',
   'censoring':'unresolved full spread without exact recurrence is unknown; nonarrival from recurrent state is certified no',
   'unit':'113 parent clusters'},'summary':summary,'parent_records':parents}

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'results/default.json');args=p.parse_args()
 r=assay();args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
 print(json.dumps({'experiment':148,'summary':r['summary']},sort_keys=True,indent=2))
if __name__=='__main__':main()
