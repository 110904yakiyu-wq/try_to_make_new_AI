#!/usr/bin/env python3
"""Exp146: raw distance is not sufficient for matched-control response;
also audit exact autonomous orbit identity at phase0. No new input probes.
"""
import csv, json, math, statistics, sys
from collections import defaultdict, Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'139_extended_control_budget'))
import core

def read(path):
 with open(path,encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def canon(s):
 o=core.orbit(s,phase=0,max_ticks=500)
 assert o['status']=='cycle' and o['phase']==0
 return min(o['cycle'][i] for i in range(0,len(o['cycle']),3))

def assay():
 phases={int(q['parent_id']):bytes.fromhex(q['frame_hex']) for q in read(ROOT/'140_extended_matched_spread/results/selected_states.csv') if q['arm']=='0'}
 ctrls=read(ROOT/'142_all_control_choice_sensitivity/results/eligible_states.csv')
 results={(int(q['parent_id']),int(q['attempt'])):q for q in read(ROOT/'142_all_control_choice_sensitivity/results/per_control.csv')}
 assert len(phases)==113 and len(ctrls)==len(results)==970
 cg={pid:canon(fr) for pid,fr in phases.items()}
 grouped=defaultdict(list)
 for q in ctrls:
  pid=int(q['parent_id']);att=int(q['attempt']);fr=bytes.fromhex(q['frame_hex']);g=phases[pid]
  d=sum((a^b).bit_count() for a,b in zip(fr,g));wd=sum(a!=b for a,b in zip(fr,g));r=results[pid,att]
  same_orbit=canon(fr)==cg[pid]
  grouped[pid].append({'attempt':att,'raw_bit_distance':d,'raw_window_distance':wd,'same_microstate':fr==g,'same_autonomous_orbit':same_orbit,
                       'yes10':int(r['yes10']),'yes60':int(r['yes60']),'unknown60':int(r['unknown60'])})
 assert len(grouped)==113
 parents=[]
 for pid,rs in sorted(grouped.items()):
  near=min(rs,key=lambda r:(r['raw_bit_distance'],r['attempt']))
  far=min(rs,key=lambda r:(-r['raw_bit_distance'],r['attempt']))
  near_distinct=min((r for r in rs if r['raw_bit_distance']>0),key=lambda r:(r['raw_bit_distance'],r['attempt']))
  near_windows=min(rs,key=lambda r:(r['raw_bit_distance'],r['raw_window_distance'],r['attempt']))
  far_windows=min(rs,key=lambda r:(-r['raw_bit_distance'],-r['raw_window_distance'],r['attempt']))
  coll=defaultdict(list)
  for x in rs:coll[x['raw_bit_distance']].append(x)
  collisions=[v for v in coll.values() if len(v)>=2]
  varying10=sum(len({x['yes10'] for x in v})>1 for v in collisions)
  varying60=sum(len({x['yes60'] for x in v})>1 for v in collisions)
  r={'parent_id':pid,'controls':len(rs),'unique_raw_distances':len(coll),'distance_min':near['raw_bit_distance'],
     'distance_max':far['raw_bit_distance'],'identical_G0_controls':sum(x['same_microstate'] for x in rs),
     'same_autonomous_orbit_controls':sum(x['same_autonomous_orbit'] for x in rs),
     'same_distance_control_groups':len(collisions),
     'same_distance_groups_with_different_yes10':varying10,
     'same_distance_groups_with_different_yes60':varying60,
     'near':near,'near_distinct':near_distinct,'far':far,'near_windows':near_windows,'far_windows':far_windows}
  for th in (10,60):
   x=[(z['raw_bit_distance'],z[f'yes{th}']) for z in rs]
   if len(x)>1 and len({a for a,_ in x})>1:
    mean_d=statistics.mean(a for a,_ in x);mean_y=statistics.mean(b for _,b in x)
    cov=sum((a-mean_d)*(b-mean_y) for a,b in x)
    variance=sum((a-mean_d)**2 for a,b in x)
    r[f'slope{th}']=cov/variance
   else:r[f'slope{th}']=None
  parents.append(r)
 all_controls=[x for rs in grouped.values() for x in rs]
 out={'experiment':146,'design':{
 'source':'Exp140/142 on-cycle phase0 states and control outcomes; no new intervention',
 'same_orbit':'canonical lexicographically minimal full physical microstate at scheduler phase0 on exact recurrent cycle',
 'raw_bit_distance':'sum of XOR bitcounts at 60 windows; range 0..240',
 'near_far':'one control per parent based on preoutcome raw distance, tie by original attempt',
 'within_distance':'different responses among multiple distinct controls at identical bit Hamming distance',
 'cluster':'113 parent groups; 970 controls and 30 probes per control not independent'},'summary':{},'parent_records':parents}
 s={'parents':113,'eligible_controls':len(all_controls),'exact_microstate_controls':sum(q['same_microstate'] for q in all_controls),
    'same_autonomous_orbit_controls':sum(q['same_autonomous_orbit'] for q in all_controls),
    'parents_with_same_orbit_control':sum(q['same_autonomous_orbit_controls']>0 for q in parents),
    'parents_with_multiple_raw_distances':sum(q['unique_raw_distances']>1 for q in parents),
    'near_tie_break_changes_control':sum(q['near']['attempt']!=q['near_windows']['attempt'] for q in parents),
    'far_tie_break_changes_control':sum(q['far']['attempt']!=q['far_windows']['attempt'] for q in parents),
    'within_parent_same_distance_groups':sum(q['same_distance_control_groups'] for q in parents),
    'within_parent_same_distance_differing_yes10':sum(q['same_distance_groups_with_different_yes10'] for q in parents),
    'within_parent_same_distance_differing_yes60':sum(q['same_distance_groups_with_different_yes60'] for q in parents)}
 for th in (10,60):
  near=[p['near'][f'yes{th}'] for p in parents];far=[p['far'][f'yes{th}'] for p in parents]
  s[f'spread{th}']={'near_control_yes':sum(near),'far_control_yes':sum(far),
    'near_with_window_tie_yes':sum(p['near_windows'][f'yes{th}'] for p in parents),
    'far_with_window_tie_yes':sum(p['far_windows'][f'yes{th}'] for p in parents),
    'far_minus_near_parent_mean_rate':statistics.mean((b-a)/30 for a,b in zip(near,far)),
    'far_higher_parents':sum(b>a for a,b in zip(near,far)),
    'near_higher_parents':sum(a>b for a,b in zip(near,far)),
    'tied_parents':sum(a==b for a,b in zip(near,far)),
    'positive_distance_response_slopes':sum(p[f'slope{th}']>0 for p in parents if p[f'slope{th}'] is not None),
    'negative_distance_response_slopes':sum(p[f'slope{th}']<0 for p in parents if p[f'slope{th}'] is not None),
    'zero_distance_response_slopes':sum(abs(p[f'slope{th}'])<1e-14 for p in parents if p[f'slope{th}'] is not None),
    'slope_evaluable_parents':sum(p[f'slope{th}'] is not None for p in parents),
    'near_excluding_identity_yes':sum(p['near_distinct'][f'yes{th}'] for p in parents),
    'near_excluding_identity_unknown':sum(p['near_distinct'].get(f'unknown{th}',0) for p in parents)}
 out['summary']=s
 assert s['same_autonomous_orbit_controls']==s['exact_microstate_controls']==1
 assert s['parents_with_same_orbit_control']==1
 assert s['spread10']['near_with_window_tie_yes']==615
 assert s['spread60']['near_with_window_tie_yes']==476
 assert s['spread10']['far_with_window_tie_yes']==740
 return out

def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'results/default.json');args=p.parse_args()
 out=assay();args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 print(json.dumps({'summary':out['summary']},indent=2,sort_keys=True))
if __name__=='__main__':main()
