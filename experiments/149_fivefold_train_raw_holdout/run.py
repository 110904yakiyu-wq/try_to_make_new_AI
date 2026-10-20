#!/usr/bin/env python3
"""Exp149: five disjoint raw train panels, each with 6 side/raw probes,
select one matched control by phase-consistent early response at ticks 1,3,6.
Remaining 24 side/raw probes are heldout against the frozen Exp140/142 results.
"""
import argparse,csv,json,sys,statistics
from pathlib import Path
from collections import defaultdict
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'139_extended_control_budget'))
import core
FOLDS=tuple(tuple(range(i,16,5)) for i in range(1,6))
TICKS=(1,3,6)
assert len(FOLDS)==5 and all(len(p)==3 for p in FOLDS) and set(x for p in FOLDS for x in p)==set(range(1,16))

def read(p):
 with open(p,newline='',encoding='utf-8') as f:return list(csv.DictReader(f))

def response(s,site,raw):
 assert s[site]==0
 b=bytes(s);p=bytearray(s);p[site]=raw;p=bytes(p);res=[]
 for tick in range(1,7):
  b=core.step(b,(tick-1)%3);p=core.step(p,(tick-1)%3)
  if tick in TICKS:res.append(sum(1<<i for i,(x,y) in enumerate(zip(b,p)) if x!=y))
 return res

def signatures(s,lo,hi):
 return {(side,raw):response(s,site,raw) for side,site in ((0,lo),(1,hi)) for raw in range(1,16)}

def select(rs,kind):
 if kind=='first':return min(rs,key=lambda x:x['attempt'])
 if kind=='raw_nearest':return min(rs,key=lambda x:(x['raw_hd'],x['window_hd'],x['attempt']))
 if kind=='train_matched':return min(rs,key=lambda x:(x['train_distance'],x['raw_hd'],x['window_hd'],x['attempt']))
 raise ValueError(kind)

def score_outcomes(probes,th):
 f='first'+str(th)
 return (sum(int(q[f])>=0 for q in probes),sum(int(q[f])<0 and int(q['recurrence'])<0 for q in probes))

def assay():
 ref={}
 for r in read(ROOT/'140_extended_matched_spread/results/selected_states.csv'):
  if int(r['arm'])==0:ref[int(r['parent_id'])]=(bytes.fromhex(r['frame_hex']),int(r['left']),int(r['right']),int(r['attempt']))
 assert len(ref)==113
 G0_out={(int(q['parent_id']),int(q['side']),int(q['raw'])):q for q in read(ROOT/'140_extended_matched_spread/results/probes.csv') if q['arm']=='0'}
 CTRL_out={(int(q['parent_id']),int(q['attempt']),int(q['side']),int(q['raw'])):q for q in read(ROOT/'142_all_control_choice_sensitivity/results/probes.csv')}
 assert len(G0_out)==3390 and len(CTRL_out)==29100
 G0_sig={pid:signatures(a,lo,hi) for pid,(a,lo,hi,_) in ref.items()}
 controls=defaultdict(list)
 for q in read(ROOT/'142_all_control_choice_sensitivity/results/eligible_states.csv'):
  pid=int(q['parent_id']);att=int(q['attempt']);s=bytes.fromhex(q['frame_hex']);g,lo,hi,first=ref[pid]
  assert int(q['left'])==lo and int(q['right'])==hi
  d={'attempt':att,'raw_hd':sum((a^b).bit_count() for a,b in zip(s,g)),'window_hd':sum(a!=b for a,b in zip(s,g))}
  cs=signatures(s,lo,hi)
  d['train_distance_by_fold']={str(i):sum((a^b).bit_count() for side in (0,1) for raw in raws
    for a,b in zip(cs[side,raw],G0_sig[pid][side,raw])) for i,raws in enumerate(FOLDS)}
  controls[pid].append(d)
 assert len(controls)==113 and sum(len(q) for q in controls.values())==970
 parent_records=[];fold_summary={}
 for index,train in enumerate(FOLDS):
  hold=tuple(r for r in range(1,16) if r not in train)
  assert len(hold)==12 and not set(train)&set(hold)
  rows=[]
  for pid,rs in sorted(controls.items()):
   ranked=[{**r,'train_distance':r['train_distance_by_fold'][str(index)]} for r in rs]
   chosen={}
   for kind in ('first','raw_nearest','train_matched'):
    r=select(ranked,kind)
    held=[CTRL_out[pid,r['attempt'],side,raw] for side in (0,1) for raw in hold]
    k10,u10=score_outcomes(held,10);k60,u60=score_outcomes(held,60)
    chosen[kind]={'attempt':r['attempt'],'raw_hd':r['raw_hd'],'train_distance':r['train_distance'],
         'yes10':k10,'unknown10':u10,'yes60':k60,'unknown60':u60}
   gt=[G0_out[pid,side,raw] for side in (0,1) for raw in hold]
   g10,gu10=score_outcomes(gt,10);g60,gu60=score_outcomes(gt,60)
   rows.append({'fold':index,'parent_id':pid,'first_attempt':ref[pid][3],
                'G0':{'yes10':g10,'unknown10':gu10,'yes60':g60,'unknown60':gu60},'selected':chosen})
  parent_records.extend(rows)
  fs={'train_raw':list(train),'test_raw':list(hold),'parents':len(rows),'training_conditions_per_parent':6,'heldout_conditions_per_parent':24}
  for cohort,rsub in (('all113',rows),('old55',[r for r in rows if r['first_attempt']<=100]),('new58',[r for r in rows if r['first_attempt']>100])):
   assert len(rsub)=={'all113':113,'old55':55,'new58':58}[cohort]
   s={}
   for kind in ('first','raw_nearest','train_matched'):
    a={'parents':len(rsub),'changed_from_first':sum(r['selected'][kind]['attempt']!=r['selected']['first']['attempt'] for r in rsub)}
    for th in (10,60):
     g=sum(r['G0'][f'yes{th}'] for r in rsub);gu=sum(r['G0'][f'unknown{th}'] for r in rsub)
     b=sum(r['selected'][kind][f'yes{th}'] for r in rsub);bu=sum(r['selected'][kind][f'unknown{th}'] for r in rsub)
     n=24*len(rsub)
     a[f'spread{th}']={'G0_yes':g,'control_yes':b,'G0_unknown':gu,'control_unknown':bu,
                       'lower_difference':(g-b-bu)/n,'upper_difference':(g+gu-b)/n}
    s[kind]=a
   fs[cohort]=s
  fold_summary[str(index)]=fs
 summary={}
 for cohort in ('all113','old55','new58'):
  for kind in ('first','raw_nearest','train_matched'):
   summary[f'{cohort}_{kind}']={th:{'min_lower':min(fold_summary[str(i)][cohort][kind][f'spread{th}']['lower_difference'] for i in range(5)),
     'max_upper':max(fold_summary[str(i)][cohort][kind][f'spread{th}']['upper_difference'] for i in range(5)),
     'fold_mean_lower':statistics.mean(fold_summary[str(i)][cohort][kind][f'spread{th}']['lower_difference'] for i in range(5)),
     'fold_mean_upper':statistics.mean(fold_summary[str(i)][cohort][kind][f'spread{th}']['upper_difference'] for i in range(5))} for th in ('10','60')}
 return {'experiment':149,'design':{'physical_kernel':'104/139 unchanged',
 'folds':'five disjoint 3-raw train groups; each repeated on left/right (6 probes), 12 other raws per side held out (24)',
 'train': 'phase-consistent causal response position masks at t1,3,6; sum symmetric-difference bitcounts, tie raw distance, windows, attempt',
 'endpoint': 'frozen Exp140/142 50000-tick ever10 and ever60 spread; right-censored 60 retain uncertainty',
 'dependence':'5 splits share the SAME 113 matched parents and 970 controls; not 5 independent experiments'},
 'fold_summary':fold_summary,'summary':summary,'parent_records':parent_records}

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'results/default.json');args=p.parse_args()
 x=assay();args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'summary':x['summary'],'fold_summary':{i:{'train_raw':v['train_raw'],
    'diff10':{k: v['all113'][k]['spread10']['lower_difference'] for k in ('first','raw_nearest','train_matched')},
    'diff60':{k: v['all113'][k]['spread60']['lower_difference'] for k in ('first','raw_nearest','train_matched')}} for i,v in x['fold_summary'].items()}},indent=2,sort_keys=True))
if __name__=='__main__':main()
