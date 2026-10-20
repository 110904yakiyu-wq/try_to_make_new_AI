#!/usr/bin/env python3
"""Reproduce all five disjoint training folds and frozen heldout summaries."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import run

def main():
 x=run.assay();assert x==json.loads((HERE/'results/default.json').read_text())
 assert x['experiment']==149 and len(x['parent_records'])==565
 assert len({r['parent_id'] for r in x['parent_records']})==113
 assert [list(a) for a in run.FOLDS]==[[1,6,11],[2,7,12],[3,8,13],[4,9,14],[5,10,15]]
 for i in range(5):
  f=x['fold_summary'][str(i)];assert f['parents']==113
  assert len(f['train_raw'])==3 and len(f['test_raw'])==12
  assert set(f['train_raw']).isdisjoint(f['test_raw'])
  a=f['all113']
  assert a['first']['spread10']['upper_difference']<a['train_matched']['spread10']['upper_difference']<0
  assert a['first']['spread60']['upper_difference']<a['train_matched']['spread60']['upper_difference']<0
  assert a['train_matched']['spread10']['G0_yes']<=24*113
  assert a['first']['spread10']['G0_yes']==a['raw_nearest']['spread10']['G0_yes']==a['train_matched']['spread10']['G0_yes']
 assert x['summary']['all113_train_matched']['10']['min_lower']<-0.06
 assert -0.035<x['summary']['all113_train_matched']['10']['max_upper']<-0.03
 print('exp149 smoke PASS: five disjoint raw folds, 565 parent-fold records, heldout integrity')
if __name__=='__main__':main()
