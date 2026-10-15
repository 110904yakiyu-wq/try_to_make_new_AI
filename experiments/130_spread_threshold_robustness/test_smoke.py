#!/usr/bin/env python3
"""Exact per-probe 60-threshold regression against Experiment129."""
import csv,json
from pathlib import Path
HERE=Path(__file__).parent

def main():
 def read(p):
  with p.open(newline='')as f:return [r for r in csv.DictReader(f)]
 a=read(HERE/'results/probes.csv')
 b=read(HERE.parent/'129_monotone_ring_spread_identification/results/probes.csv')
 assert len(a)==len(b)==3300
 for x,y in zip(a,b):
  assert tuple(x[k] for k in('parent_id','arm','side','raw','recurrence'))==tuple(y[k] for k in('parent_id','arm','side','raw','recurrence'))
  assert x['first60']==y['first_full_ring_tick']
  fs=[int(x[f'first{k}'])for k in(10,20,30,40,50,60)]
  known=[t for t in fs if t>=0];assert known==sorted(known)
  assert all(t<0 for t in fs[len(known):])
 data=json.loads((HERE/'results/default.json').read_text())
 for k in(10,20,30,40,50,60):assert data['results'][str(k)]['50000']['upper_count']<0
 print('exp130 smoke: PASS; all 3300 threshold-60 records match Exp129 and all sign intervals are negative')
if __name__=='__main__':main()
