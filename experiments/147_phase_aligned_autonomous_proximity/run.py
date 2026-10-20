#!/usr/bin/env python3
"""Experiment147: select matched controls using only the *no-material* orbit
geometry of G0 and each autonomous control at phase-aligned early ticks.
Holdout endpoints are frozen, unseen by the selection function.
"""
import argparse,csv,json,statistics,sys
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'139_extended_control_budget'))
import core
TIMES=(0,1,3,6,12)
RULES={'raw0':(0,), 'phase0_3':(0,3), 'phase0_3_6':(0,3,6),
       'phase0_1_3_6_12':(0,1,3,6,12), 'phase3_6_12':(3,6,12)}

def read(p):
 with open(p,newline='',encoding='utf-8') as f:return list(csv.DictReader(f))

def trace(s):
 assert len(s)==60 and all(v<16 for v in s)
 out={0:bytes(s)}
 for t in range(1,max(TIMES)+1):
  s=core.step(s,(t-1)%3)
  if t in TIMES:out[t]=s
 return out

def rawmetrics(a,b):
 return (sum((x^y).bit_count() for x,y in zip(a,b)),sum(x!=y for x,y in zip(a,b)))

def selected(cs,ticks):
 return min(cs,key=lambda x:(sum(x['distances'][str(t)] for t in ticks), x['distances']['0'], x['window_distance0'],x['attempt']))

def assay():
 frames={int(q['parent_id']):bytes.fromhex(q['frame_hex']) for q in read(ROOT/'140_extended_matched_spread/results/selected_states.csv') if q['arm']=='0'}
 controls=read(ROOT/'142_all_control_choice_sensitivity/results/eligible_states.csv')
 outcomes={(int(q['parent_id']),int(q['attempt'])):q for q in read(ROOT/'142_all_control_choice_sensitivity/results/per_control.csv')}
 probeG=defaultdict(dict)
 for q in read(ROOT/'140_extended_matched_spread/results/probes.csv'):
  if q['arm']=='0':
   key=int(q['parent_id']);pr=(int(q['side']),int(q['raw']));assert pr not in probeG[key]
   probeG[key][pr]=q
 assert len(frames)==len(probeG)==113 and len(outcomes)==len(controls)==970
 G={pid:trace(s) for pid,s in frames.items()}
 candidates=defaultdict(list)
 for q in controls:
  pid=int(q['parent_id']);att=int(q['attempt']);s=bytes.fromhex(q['frame_hex']);o=outcomes[pid,att]
  t=trace(s);dist={str(k):rawmetrics(t[k],G[pid][k])[0] for k in TIMES}
  wd=rawmetrics(s,frames[pid])[1]
  candidates[pid].append({'attempt':att,'distances':dist,'window_distance0':wd,
      'yes10':int(o['yes10']),'yes60':int(o['yes60']),'unknown60':int(o['unknown60'])})
 assert len(candidates)==113
 records=[]
 for pid,cs in sorted(candidates.items()):
  assert len(probeG[pid])==30
  r={'parent_id':pid,'control_candidates':len(cs),
     'G0_yes10':sum(int(x['first10'])>=0 for x in probeG[pid].values()),
     'G0_yes60':sum(int(x['first60'])>=0 for x in probeG[pid].values()),
     'G0_unknown60':sum(int(x['first60'])<0 and int(x['recurrence'])<0 for x in probeG[pid].values()),
     'choice':{}}
  for rule,ticks in RULES.items():
   x=selected(cs,ticks)
   r['choice'][rule]={'attempt':x['attempt'],'training_distance':sum(x['distances'][str(t)] for t in ticks),
       'bit_distance0':x['distances']['0'],'window_distance0':x['window_distance0'],
       'yes10':x['yes10'],'yes60':x['yes60'],'unknown60':x['unknown60']}
  records.append(r)
 summary={}
 for group,rr in [('all113',records),('old55',[r for r in records if min(q['attempt'] for q in candidates[r['parent_id']])<=100]),('new58',[r for r in records if min(q['attempt'] for q in candidates[r['parent_id']])>100])]:
  assert len(rr)=={'all113':113,'old55':55,'new58':58}[group]
  rrsummary={}
  for rule in RULES:
   o={'parents':len(rr),'selected_control_raw_distance_mean':statistics.mean(r['choice'][rule]['bit_distance0'] for r in rr),
      'changed_vs_raw0':sum(r['choice'][rule]['attempt']!=r['choice']['raw0']['attempt'] for r in rr),
      'training_distance_mean':statistics.mean(r['choice'][rule]['training_distance'] for r in rr)}
   for th in (10,60):
    g=sum(r[f'G0_yes{th}'] for r in rr);gu=sum(r.get(f'G0_unknown{th}',0) for r in rr)
    b=sum(r['choice'][rule][f'yes{th}'] for r in rr);bu=sum(r['choice'][rule].get(f'unknown{th}',0) for r in rr)
    n=len(rr)*30
    o[f'spread{th}']={'G0_yes':g,'control_yes':b,'G0_unknown':gu,'control_unknown':bu,
                     'lower_difference':(g-b-bu)/n,'upper_difference':(g+gu-b)/n}
   rrsummary[rule]=o
  summary[group]=rrsummary
 assert summary['all113']['raw0']['spread10']['control_yes']==615
 assert summary['all113']['raw0']['spread60']['control_yes']==476
 return {'experiment':147,'design':{'physics':'unchanged Exp104/139 three-phase left-rotated 60x4bit kernel',
  'eligibility':'frozen 970 autonomous pre-material exact period/union support/phase0 occupancy matched controls',
  'selection':'phase-aligned no-injection microstates at fixed ticks; fully preoutcome',
  'times':list(TIMES),'rules':{k:list(v) for k,v in RULES.items()},
  'holdout':'all 30 injected side/raw material responses, 50000 tick spread10/60 from Exp140/142',
  'independence':'113 matched parent clusters, many dependent controls/probes',
  'censoring':'unseen spread60 and no exact recurrence is unknown'},
  'summary':summary,'parent_records':records}

def main():
 a=argparse.ArgumentParser();a.add_argument('--output',type=Path,default=HERE/'results/default.json');args=a.parse_args()
 result=assay();args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 print(json.dumps({'experiment':result['experiment'],'summary':result['summary']},indent=2,sort_keys=True))
if __name__=='__main__':main()
