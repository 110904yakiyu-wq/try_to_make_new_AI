#!/usr/bin/env python3
"""Check 128 C++ trace against original Python 104 step for sampled probes."""
from pathlib import Path
import csv,json,struct,sys
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT.parent/'127_censor_resolution_work_budget'))
import build_states as m

def validate():
 data=list(csv.DictReader((ROOT/'results/censored_trace.csv').open(newline='')))
 assert len(data)==537
 blob=(ROOT.parent/'127_censor_resolution_work_budget/states.bin').read_bytes()
 roster={}
 for i in range(55):
  off=124*i
  pid,attempt,lo,hi=struct.unpack_from('<BBBB',blob,off)
  roster[pid]=(bytes(blob[off+4:off+64]),bytes(blob[off+64:off+124]),lo,hi)
 sample=data[::57]
 assert len(sample)>=9
 for row in sample:
  pid,arm,side,raw=[int(row[k]) for k in ('parent_id','arm','side','raw')]
  g,c,lo,hi=roster[pid]
  s=bytearray(g if arm==0 else c);s[lo if side==0 else hi]=raw
  union={i for i,x in enumerate(s)if x}
  checkpoints={}
  for t in range(1,2001):
   s=m.step(s,(t-1)%3)
   union.update(i for i,x in enumerate(s)if x)
   if t in (500,2000):checkpoints[t]=len(union)
  assert checkpoints[500]==int(row['union_500'])
  assert checkpoints[2000]==int(row['union_2000'])
 obj=json.loads((ROOT/'results/default.json').read_text())
 assert obj['summary']['overall']['full_ring_union_50000']==536
 print('exp128 smoke: PASS; Python checkpoint support validation on',len(sample),'censored traces')
if __name__=='__main__':validate()
