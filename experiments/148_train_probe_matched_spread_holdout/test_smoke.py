#!/usr/bin/env python3
"""Frozen train/test-probe disjointness and class outcome integrity audit."""
import csv,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import run

def main():
 x=run.assay();assert x==json.loads((HERE/'results/default.json').read_text())
 assert len(run.TRAIN)==3 and len(run.HOLD)==12 and set(run.HOLD).isdisjoint(run.TRAIN)
 a=x['summary']['all113'];assert len(x['parent_records'])==113
 assert sum(p['num_eligible_controls'] for p in x['parent_records'])==970
 assert (a['first']['spread10']['G0_yes'],a['first']['spread10']['control_yes'])==(247,580)
 assert (a['first']['spread60']['G0_yes'],a['first']['spread60']['control_yes'])==(187,474)
 assert (a['train_t1_3_6']['spread10']['G0_yes'],a['train_t1_3_6']['spread10']['control_yes'])==(247,348)
 assert (a['train_t1_3_6']['spread60']['G0_yes'],a['train_t1_3_6']['spread60']['control_yes'])==(187,272)
 assert all(v['spread10']['upper_difference']<0 and v['spread60']['upper_difference']<0 for v in a.values())
 assert all(p['choices']['first']['attempt']==p['first_attempt'] for p in x['parent_records'])
 for p in x['parent_records']:
  assert p['G0']['yes60']<=p['G0']['yes10']<=24
  for k,q in p['choices'].items():
   assert 0<=q['yes60']<=q['yes10']<=24
   assert 0<=q['unknown60']<=24-q['yes60']
 print('exp148 smoke PASS: 6 train, 24 heldout, 113 parent clusters, frozen 140/142 outcomes')
if __name__=='__main__':main()
