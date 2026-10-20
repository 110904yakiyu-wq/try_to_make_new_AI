#!/usr/bin/env python3
"""Regenerate phase-aligned controls and cross-validate Exp145 raw selection."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'145_preoutcome_raw_proximity_choice'))
import run as r145
sys.path[0]=str(HERE)
import importlib.util
spec=importlib.util.spec_from_file_location('exp147', HERE/'run.py')
r147=importlib.util.module_from_spec(spec);spec.loader.exec_module(r147)

def main():
 x=r147.assay();assert x==json.loads((HERE/'results/default.json').read_text())
 b=r145.assay();a=x['summary']['all113'];z=b['summary']['all113']['min_raw_bit_distance']
 for t in (10,60):
  assert a['raw0'][f'spread{t}']['control_yes']==z[f'spread{t}']['control_yes']
 assert a['phase0_3_6']['spread10']['control_yes']==586
 assert a['phase0_3_6']['spread60']['control_yes']==462
 assert len(x['parent_records'])==113
 for cohort in x['summary'].values():
  assert all(s['spread10']['upper_difference']<0 and s['spread60']['upper_difference']<0 for s in cohort.values())
 for p in x['parent_records']:
  assert len(p['choice'])==5
  for key,q in p['choice'].items(): assert q['training_distance']>=0
 print('exp147 smoke PASS (5 preoutcome temporal choices, Exp145 raw-distance agreement)')
if __name__=='__main__':main()
