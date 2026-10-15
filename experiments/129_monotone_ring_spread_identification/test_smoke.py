#!/usr/bin/env python3
"""Verify monotone event certificates and match Exp128 independent C++ trace."""
import csv,sys,struct,json
from pathlib import Path
HERE=Path(__file__).parent;EXP=HERE.parent
sys.path.insert(0,str(EXP/'127_censor_resolution_work_budget'))
import build_states as m

def main():
 with (HERE/'results/probes.csv').open(newline='') as f:records=list(csv.DictReader(f))
 assert len(records)==3300
 recordmap={(int(r['parent_id']),int(r['arm']),int(r['side']),int(r['raw'])):r for r in records}
 with (EXP/'128_censored_trajectory_support_audit/results/censored_trace.csv').open(newline='') as f:other=list(csv.DictReader(f))
 for r in other:
  key=tuple(int(r[k])for k in ('parent_id','arm','side','raw'))
  assert int(r['first_union60'])==int(recordmap[key]['first_full_ring_tick'])
 blob=(EXP/'127_censor_resolution_work_budget/states.bin').read_bytes()
 states={}
 for i in range(55):
  off=124*i;pid,attempt,lo,hi=struct.unpack_from('<BBBB',blob,off)
  states[pid]=(bytes(blob[off+4:off+64]),bytes(blob[off+64:off+124]),lo,hi)
 chosen=[r for r in records if int(r['parent_id'])in (2,19,49,75,102,126) and int(r['raw'])in(1,7,15)]
 for r in chosen:
  pid,arm,side,raw=[int(r[k])for k in('parent_id','arm','side','raw')]
  g,c,lo,hi=states[pid];s=bytearray(g if arm==0 else c);s[lo if side==0 else hi]=raw
  sup={i for i,x in enumerate(s)if x};first=0 if len(sup)==60 else -1
  for t in range(1,501):
   s=m.step(s,(t-1)%3);sup.update(i for i,x in enumerate(s)if x)
   if len(sup)==60 and first==-1:first=t
  actual=int(r['first_full_ring_tick']);expected=actual if 0<=actual<=500 else -1
  assert first==expected, (pid,arm,side,raw,first,expected)
 result=json.loads((HERE/'results/default.json').read_text());summ=result['horizon_bounds']['50000']
 assert (summ['G0']['ever_full'],summ['control']['ever_full'])==(143,395)
 assert (summ['lower_count_difference'],summ['upper_count_difference'])==(-253,-252)
 print(f'exp129 smoke: PASS; cross-validated 537 censored full-hit times and {len(chosen)} Python 500-tick trajectories')
if __name__=='__main__':main()
