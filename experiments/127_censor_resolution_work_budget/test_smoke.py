#!/usr/bin/env python3
"""Cross-language exact dynamics and frozen 125/126 distribution regression."""
import csv,json,struct
from pathlib import Path
import build_states as p
ROOT=Path(__file__).parent

def classify(initial,h):
 r=p.orbit(initial,max_ticks=h)
 if r['status']!='cycle':return -1
 if not r['active']:return 0
 supp=r['support'];n=sum(int(x in supp and (x-1)%60 not in supp) for x in supp)
 if len(supp)==60:n=1
 return 1 if n==1 else 2

def test():
 with (ROOT/'results/probes.csv').open(newline='') as f:rows=list(csv.DictReader(f))
 assert len(rows)==3300
 states=(ROOT/'states.bin').read_bytes();assert len(states)==55*124
 roster={}
 for i in range(55):
  off=i*124
  pid,attempt,left,right=struct.unpack_from('<BBBB',states,off)
  g=bytes(states[off+4:off+64]);c=bytes(states[off+64:off+124]);roster[pid]=(g,c,left,right)
 # Deterministic observations across sample parents, arms, probes and horizons.
 selections=[r for r in rows if int(r['pid']) in [2,8,19,35,49,75,102,126]
             and int(r['raw']) in [1,7,15] and int(r['side']) in [0,1]]
 for q in selections:
  pid,arm,side,raw=[int(q[k]) for k in ('pid','arm','side','raw')]
  g,c,lo,hi=roster[pid]
  s=bytearray(g if arm==0 else c);assert s[lo if side==0 else hi]==0
  s[lo if side==0 else hi]=raw
  for h in (500,2000):
   actual=classify(s,h)
   rt=int(q['recurrence']);expect=int(q['class']) if rt!=-1 and rt<=h else -1
   assert actual==expect, (pid,arm,side,raw,h,actual,expect)
 data=json.loads((ROOT/'results/default.json').read_text())
 z=data['aggregate'];v=z['500'];w=z['2000'];x=z['50000']
 assert (v['G0']['connected'],v['control']['connected'],v['G0']['censored'],v['control']['censored'])==(1486,1215,143,398)
 assert (w['G0']['connected'],w['control']['connected'],w['G0']['censored'],w['control']['censored'])==(1486,1218,143,395)
 assert (x['G0']['censored'],x['control']['censored'],x['robust_G0_parents'],x['sign_indeterminate_parents'])==(143,394,12,42)
 assert len(selections)>50
 print(f'exp127 smoke: PASS; cross-language paired orbits={len(selections)*2}; historical invariants intact')
if __name__=='__main__':test()
