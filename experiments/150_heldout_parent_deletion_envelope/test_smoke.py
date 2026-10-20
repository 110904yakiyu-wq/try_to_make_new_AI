#!/usr/bin/env python3
"""Frozen 149 parent records and deterministic worst-case deletion bounds."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import run

def main():
 x=run.assay()
 assert x==json.loads((HERE/'results/default.json').read_text())
 assert len(x['parent_records'])==5*113*3*2
 e=x['envelope']
 assert e['train_matched_spread10']['first_nonnegative_deletion_counts_by_fold']==[14,11,18,14,10]
 assert e['train_matched_spread60']['first_nonnegative_deletion_counts_by_fold']==[15,12,19,15,10]
 assert e['train_matched_spread10']['minimum_guaranteed_deletion_robustness_across_five_folds']==9
 assert e['train_matched_spread60']['minimum_guaranteed_deletion_robustness_across_five_folds']==9
 for fold in x['summary'].values():
  for key,v in fold.items():
   d=v['censor_aware_worst_case'];assert d['original_upper_sum']<0
   assert d['minimal_deletion_count_to_allow_nonnegative_upper']==d['robust_to_every_deletion_up_to']+1
   assert d['worst_case_curve'][0]['worst_remaining_upper_sum']==d['original_upper_sum']
 print('exp150 smoke PASS: all 5 folds, 3 control rules, 2 spread thresholds, exact parent-deletion bound')
if __name__=='__main__':main()
