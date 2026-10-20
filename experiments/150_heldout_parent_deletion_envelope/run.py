#!/usr/bin/env python3
"""Exp150: finite-population worst-case parent-deletion spread sign envelope
for the five frozen heldout 149 training-panel control selections.
No intervention or physical updates; 113 correlated parent clusters only.
"""
import argparse,json
from pathlib import Path
from collections import defaultdict
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'149_fivefold_train_raw_holdout/results/default.json'

def deletion_bound(delta):
 """Any k deleted: maximize remaining sum by removing k smallest deltas.
For signed eventual spread, upper deltas use G0 YES+UNKNOWN − CTRL YES;
lower deltas use G0 YES − CTRL YES−UNKNOWN.
"""
 vals=sorted(delta);n=len(vals);total=sum(vals);current=total;curve=[];first_k=None
 for k in range(n+1):
  if k>0:current-=vals[k-1]
  if current>=0 and first_k is None:first_k=k
  if k in (0,1,5,9,10,15,20,30,n):curve.append({'removed_parents':k,'worst_remaining_upper_sum':current,'remaining_parents':n-k})
 assert first_k is not None
 return {'parents':n,'original_upper_sum':total,'minimal_deletion_count_to_allow_nonnegative_upper':first_k,
    'robust_to_every_deletion_up_to':first_k-1,'worst_case_curve':curve}

def assay(reference=SOURCE):
 obj=json.loads(Path(reference).read_text())
 assert obj['experiment']==149 and len(obj['parent_records'])==565
 grouped=defaultdict(list)
 for r in obj['parent_records']:grouped[r['fold']].append(r)
 assert set(grouped)==set(range(5))
 summary={};details=[]
 for fold,rs in sorted(grouped.items()):
  assert len(rs)==113 and len({r['parent_id'] for r in rs})==113
  foldres={}
  for label in ('first','raw_nearest','train_matched'):
   for th in (10,60):
    delta_lo=[r['G0'][f'yes{th}']-r['selected'][label][f'yes{th}']-r['selected'][label][f'unknown{th}'] for r in rs]
    delta_hi=[r['G0'][f'yes{th}']+r['G0'][f'unknown{th}']-r['selected'][label][f'yes{th}'] for r in rs]
    n=len(rs)*24
    assert sum(delta_lo)/n==obj['fold_summary'][str(fold)]['all113'][label][f'spread{th}']['lower_difference']
    assert sum(delta_hi)/n==obj['fold_summary'][str(fold)]['all113'][label][f'spread{th}']['upper_difference']
    key=f'{label}_spread{th}'
    foldres[key]={'positive_parent_count':sum(x>0 for x in delta_hi),
      'negative_parent_count':sum(x<0 for x in delta_hi),'tied_parent_count':sum(x==0 for x in delta_hi),
      'observed_difference_lower':sum(delta_lo)/n,'observed_difference_upper':sum(delta_hi)/n,
      'censor_aware_worst_case':deletion_bound(delta_hi)}
    details.extend({'fold':fold,'parent_id':r['parent_id'],'selector':label,'threshold':th,'lower':lo,'upper':hi} for r,lo,hi in zip(rs,delta_lo,delta_hi))
  summary[str(fold)]=foldres
 envelope={}
 for label in ('first','raw_nearest','train_matched'):
  for th in (10,60):
   key=f'{label}_spread{th}'
   envelope[key]={'minimum_guaranteed_deletion_robustness_across_five_folds':min(summary[str(i)][key]['censor_aware_worst_case']['robust_to_every_deletion_up_to'] for i in range(5)),
    'maximum_guaranteed_deletion_robustness_across_five_folds':max(summary[str(i)][key]['censor_aware_worst_case']['robust_to_every_deletion_up_to'] for i in range(5)),
    'first_nonnegative_deletion_counts_by_fold':[summary[str(i)][key]['censor_aware_worst_case']['minimal_deletion_count_to_allow_nonnegative_upper'] for i in range(5)]}
 return {'experiment':150,'contract':{'source':'Exp149 frozen 5 fold × 113 parent selected and G0 heldout counts',
  'delete':'arbitrary deletion of exactly k parent clusters, maximize remaining G0−control difference',
  'upper_bound':'G0 event confirmed+unknown minus control confirmed event; right censor never called negative',
  'no_selection_adjustment':'pure posthoc worst-case sensitivity bound, not a deployable parent selection',
  'dependence':'five folds reuse same parents and controls; no independent samples',
  'physics':'unchanged'},'summary':summary,'envelope':envelope,'parent_records':details}

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'results/default.json');a=p.parse_args()
 r=assay();a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,separators=(',',':'),sort_keys=True)+'\n')
 print(json.dumps({'envelope':r['envelope'],'matched_fold':r['summary']['4']['train_matched_spread10']},sort_keys=True,indent=2))
if __name__=='__main__':main()
