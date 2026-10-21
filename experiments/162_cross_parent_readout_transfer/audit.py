#!/usr/bin/env python3
"""Post-run audit; source/label separation and matched Exp161 regressions."""
import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent

def audit(current, exp161=None):
    r=json.loads(Path(current).read_text())
    inv=r['inventory']
    assert inv['parents']==130 and inv['raw_mask_splits']==12
    assert inv['phase_aware_orbit_classes']==126 and inv['repeated_orbit_classes']==4
    assert len(r['parent_split_records'])==130*12*4
    groups={x['group']:set(x['parent_ids']) for x in r['parent_groups']}
    assert sorted(pid for g in groups.values() for pid in g)==list(range(130))
    assert len(set.union(*groups.values()))==130
    assert all(len({g for g,ids in groups.items() if set(cl)&ids})==1
               for cl in r['orbit_classes_with_multiple_seeds'])
    assert all(set(x['train_masks']).isdisjoint(x['heldout_masks']) for x in r['raw_mask_partitions'])
    old_score={
      'raw_linear':0.5129893162393162,
      'raw_rbf':0.5641875000000001,
    }
    for name, expected in old_score.items():
        assert abs(r['summary'][name]['means']['within_ba']-expected)<1e-12
    identical_rows=0
    if exp161:
        old=json.loads(Path(exp161).read_text())
        old_lookup={(x['parent_id'],x['fold_id']):x for x in old['parent_fold_records']}
        assert len(old_lookup)==130*12
        for row in r['parent_split_records']:
            parent=old_lookup[row['parent_id'],row['split_id']]
            attr=f'terminal_{row["method"]}_ba'
            assert abs(row['within_ba']-parent[attr])<1e-12,(row, parent)
            identical_rows+=1
    # Treat identical phase-aware autonomous cycles as one bootstrap cluster.
    multiple=r['orbit_classes_with_multiple_seeds']
    members=set(i for ids in multiple for i in ids)
    classes=list(multiple)+[[i] for i in range(130) if i not in members]
    assert len(classes)==126 and sum(map(len,classes))==130
    perparent=defaultdict(list)
    for row in r['parent_split_records']:
        if row['method']=='rbf':
            perparent[row['parent_id']].append(row)
    values=[]
    for parent,rr in sorted(perparent.items()):
        vals={kind:sum(x['transfer_ba'] for x in rr if x['mode']==kind)/12 for kind in ('raw','sham_delta')}
        values.append(vals['sham_delta']-vals['raw'])
    vals=np.asarray(values)
    class_sums=np.asarray([sum(vals[i] for i in cluster) for cluster in classes],dtype=float)
    class_n=np.asarray([len(cluster) for cluster in classes],dtype=float)
    rng=np.random.default_rng(162990)
    inds=rng.integers(len(classes),size=(5000,len(classes)))
    ci=np.quantile(class_sums[inds].sum(axis=1)/class_n[inds].sum(axis=1),[.025,.975])
    old_count={}
    for mode in ('raw','sham_delta'):
        for method in ('linear','rbf'):
            v=r['summary'][f'{mode}_{method}']
            cluster_per_parent=np.asarray([
                sum(z['transfer_ba'] for z in r['parent_split_records']
                    if z['mode']==mode and z['method']==method and z['parent_id']==pid)/12
                for pid in range(130)])
            classsum=np.asarray([sum(cluster_per_parent[j] for j in ids) for ids in classes])
            clsize=np.asarray([len(ids) for ids in classes])
            random=np.random.default_rng(162500 + (0 if mode=='raw' else 10) + (0 if method=='linear' else 1))
            chosen=random.integers(len(classes),size=(5000,len(classes)))
            classci=np.quantile(classsum[chosen].sum(axis=1)/clsize[chosen].sum(axis=1),[.025,.975])
            old_count[f'{mode}_{method}']={
                'transfer_orbit_class_bootstrap_95pct_descriptive':[float(x) for x in classci],
                'transfer_mean_ba':v['means']['transfer_ba'],
                'transfer_minus_shuffled':v['means']['transfer_minus_shuffled'],
                'fold_means_above_chance':sum(x['transfer_ba']>.5 for x in v['per_split']),
                'range_split_mean':[min(x['transfer_ba'] for x in v['per_split']),
                                    max(x['transfer_ba'] for x in v['per_split'])],
            }
    return {'audit_status':'PASS', 'phase_aware_groups':len(groups), 'bootstrap_independent_orbit_classes':len(classes),
            'unique_phase_aware_orbit_classes':inv['phase_aware_orbit_classes'],
            'orbit_duplicate_groups_not_leaked':r['orbit_classes_with_multiple_seeds'],
            'exp161_exact_within_parent_compared_records':identical_rows,
            'posthoc_sham_delta_minus_raw_transfer_rbf':{
                'mean':float(vals.mean()), 'bootstrap_95pct_descriptive':[float(x) for x in ci],
                'scope':'posthoc orbit-class cluster bootstrap, 126 clusters; conditions on training decoder and mask splits; exploratory after first Exp162 v0 results'},
            'readout_summary':old_count,
            'caution':'Orbit-class resampling accounts for the four repeated autonomous cycles but still conditions on fixed pooled decoder training, five parent groups and 12 correlated mask splits. Exploratory sensitivity, not a confidence statement for independent populations.'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',type=Path,default=HERE/'results/default.json')
    ap.add_argument('--exp161',type=Path)
    ap.add_argument('--output',type=Path,default=HERE/'results/audit.json')
    a=ap.parse_args()
    result=audit(a.input,a.exp161)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
