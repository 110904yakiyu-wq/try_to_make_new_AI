"""Exp144: side/material robustness in independently newly eligible 58 parents.
Fixed selected control and response outcome records of Exp140. No new probes.
"""
import json,csv
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'140_extended_matched_spread/results/probes.csv'

def calc(rows,k):
 c={a:Counter('yes' if q[f'first{k}']>=0 else 'unknown' if q['recurrence']<0 else 'no' for q in rows if q['arm']==a) for a in (0,1)}
 n=sum(c[0].values());assert n==sum(c[1].values()) and n>0
 lo=(c[0]['yes']-c[1]['yes']-c[1]['unknown'])/n;hi=(c[0]['yes']+c[0]['unknown']-c[1]['yes'])/n
 return {'n_per_arm':n,'G0_yes':c[0]['yes'],'control_yes':c[1]['yes'],'G0_unknown':c[0]['unknown'],'control_unknown':c[1]['unknown'],
         'lower_rate':lo,'upper_rate':hi,'sign_guaranteed_negative':hi<0}

def assay(path=SOURCE):
 with open(path,newline='') as f:rows=[{k:int(v) for k,v in q.items()} for q in csv.DictReader(f)]
 newly={r['parent_id'] for r in rows if r['attempt']>100};assert len(newly)==58
 eligible=[r for r in rows if r['parent_id'] in newly];assert len(eligible)==58*60
 result={'experiment':144,'contract':{'cohort':'58 newly eligible G0 parents only','selection':'first autonomous control within 1000',
   'stratification':'both sides and raw1..15 were fixed before outcomes',
   'outcomes':'Exp140 exact 50000-tick spread traces, repeated per parent',
   'note':'direction and material slices share trajectories; not independent replications'},'total':{},'by_side':{},'by_raw':{}}
 for th in (10,60):
  t=str(th);result['total'][t]=calc(eligible,th)
  result['by_side'][t]={str(side):calc([r for r in eligible if r['side']==side],th) for side in (0,1)}
  result['by_raw'][t]={str(raw):calc([r for r in eligible if r['raw']==raw],th) for raw in range(1,16)}
  assert all(q['sign_guaranteed_negative'] for q in result['by_side'][t].values())
  assert all(q['sign_guaranteed_negative'] for q in result['by_raw'][t].values())
 assert result['total']['10']['G0_yes']==153 and result['total']['10']['control_yes']==312
 assert result['total']['60']['G0_yes']==97 and result['total']['60']['control_yes']==239
 return result
if __name__=='__main__':
 d=assay();(HERE/'results/default.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
 (HERE/'results/default.txt').write_text(json.dumps({'total':d['total'],'by_side':d['by_side']},indent=2,sort_keys=True)+'\n')
 print('exp144 newly58: all sides and 15 raws retain negative sign at both thresholds')
