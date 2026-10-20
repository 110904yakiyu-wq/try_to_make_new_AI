#!/usr/bin/env python3
"""Recompute selection from frozen preoutcome physical states and response archives."""
import json, math
from pathlib import Path
import run
HERE=Path(__file__).resolve().parent

def main():
 d=run.assay()
 frozen=json.loads((HERE/'results/default.json').read_text())
 assert d==frozen and len(d['parent_records'])==113
 s=d['summary']['all113']
 assert sum(p['controls'] for p in d['parent_records'])==970
 assert (s['first']['spread10']['G0_yes'],s['first']['spread10']['control_yes'])==(326,765)
 assert (s['first']['spread60']['G0_yes'],s['first']['spread60']['control_yes'])==(240,634)
 assert (s['min_raw_bit_distance']['spread10']['control_yes'],s['min_raw_bit_distance']['spread60']['control_yes'])==(615,476)
 assert s['min_raw_bit_distance']['different_from_first']==91
 for cohort in s,d['summary']['old55'],d['summary']['new58']:
  assert all(x['spread10']['upper_delta_fraction']<0 and x['spread60']['upper_delta_fraction']<0 for x in cohort.values())
 for p in d['parent_records']:
  for rule,x in p['selected'].items():
   assert p['raw_distance_min']<=x['raw_bit_distance']<=p['raw_distance_max']
   assert 0<=x['yes60']<=x['yes10']<=30
 print('exp145 smoke PASS (all cohorts, exact preoutcome selection, reference counts)')
if __name__=='__main__':main()
