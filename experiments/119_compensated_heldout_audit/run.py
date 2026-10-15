#!/usr/bin/env python3
"""Exp119: held-out responses for Exp118 distance-compensated physical nulls.

Physical nulls are enumerated without outcomes. Match train t1/t3 response
mask using fixed 6 probes, then test the other 24 probes at t6/t12/t24.
"""
import argparse,importlib.util,json,statistics
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('exp117',ROOT/'117_probe_split_robustness'/'run.py')
f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f)
e=f.e;z=f.FOLDS[0];train_ix=f.indices(z);test_ix=f.indices([x for x in range(1,16) if x not in z])

def compensators(ctrl,g0,patch,parent,trans,pool):
    goal_dist=e_distance(trans,g0);goal_features=e.features(trans);mask=e.first_mask(trans)
    sites=[i for i in sorted(parent['support']) if i not in patch and ctrl[i]!=g0[i]]
    states=set()
    for base in pool:
        for pos in sites:
            for val in range(1,16):
                if val==base[pos]:continue
                temp=bytearray(base);temp[pos]=val;q=bytes(temp)
                if e_distance(q,g0)!=goal_dist:continue
                if e.first_mask(q)!=mask:continue
                if e.features(q)!=goal_features:continue
                states.add(q)
    return sorted(states)

def e_distance(a,b):return sum((x^y).bit_count() for x,y in zip(a,b))

def stats(records):
    ans={}
    for width in e.WIDTHS:
        entries=[r for r in records if r['width']==width]
        groups=defaultdict(list)
        for r in entries:groups[r['pid']].append(r)
        pp=[]
        for pid,rows in sorted(groups.items()):
            item={'parent_id':pid,'patches':len(rows),'total_compensated_states':sum(x['compensated_pool'] for x in rows)}
            for t in (6,12,24):
                for metric in ('jaccard','exact'):
                    k=f'{t}_{metric}'
                    item[k+'_donor']=statistics.mean(x['donor'][str(t)][metric] for x in rows)
                    item[k+'_uncompensated_nearest']=statistics.mean(x['uncompensated_nearest'][str(t)][metric] for x in rows)
                    item[k+'_compensated_nearest']=statistics.mean(x['compensated_nearest'][str(t)][metric] for x in rows)
                    item[k+'_donor_minus_compensated']=item[k+'_donor']-item[k+'_compensated_nearest']
                    item[k+'_donor_minus_uncompensated']=item[k+'_donor']-item[k+'_uncompensated_nearest']
                    item[k+'_compensated_minus_uncompensated']=item[k+'_compensated_nearest']-item[k+'_uncompensated_nearest']
            pp.append(item)
        a={'patches':len(entries),'parents':len(pp),'compensated_microstates_per_patch_sum':sum(x['compensated_pool'] for x in entries),'parent_details':pp}
        for t in (6,12,24):
            for metric in ('jaccard','exact'):
                k=f'{t}_{metric}'
                for kind in ('donor_minus_compensated','donor_minus_uncompensated','compensated_minus_uncompensated'):
                    v=[p[k+'_'+kind] for p in pp]
                    a[k+'_'+kind+'_mean']=statistics.mean(v) if v else None
                    a[k+'_'+kind+'_wins']=sum(x>1e-12 for x in v)
                    a[k+'_'+kind+'_losses']=sum(x< -1e-12 for x in v)
                    a[k+'_'+kind+'_ties']=sum(abs(x)<=1e-12 for x in v)
        ans[str(width)]=a
    return ans

def assay(reference,max_parents=None):
    frozen=json.loads(Path(reference).read_text());assert frozen['experiment']==112 and len(frozen['parent_records'])==20
    catalog=list(e.m.parents('left'));assert len(catalog)==130
    rows=[];inventory=Counter()
    for j,p in enumerate(frozen['parent_records']):
        if max_parents is not None and j>=max_parents:break
        pid=p['parent_id'];_,g0,parent=catalog[pid]
        ctrl=e.reference_control(pid,g0,parent,p['control_match_attempt'])
        mask=e.first_mask(g0);assert mask==e.first_mask(ctrl)
        sites=(min(parent['support'])-1,max(parent['support'])+1)
        gp=f.panel(g0,*sites)
        inventory['parents']+=1
        for width in e.WIDTHS:
            for patch in e.changed_patches(g0,ctrl,parent['support'],width):
                donor=e.replace(ctrl,g0,patch)
                if e.first_mask(donor)!=mask:continue
                original_pool=list(e.exact_physical_nulls(ctrl,g0,patch,mask,e.features(donor)))
                if not original_pool:continue
                viable=compensators(ctrl,g0,patch,parent,donor,original_pool)
                if not viable:continue
                inventory[f'w{width}_matched_patches']+=1;inventory[f'w{width}_compensated_states']+=len(viable)
                assert all(e_distance(q,g0)==e_distance(donor,g0) and e.first_mask(q)==mask and e.features(q)==e.features(donor) for q in viable)
                donor_p=f.panel(donor,*sites)
                nearest_std=min(original_pool,key=lambda st:(f.hd(f.panel(st,*sites),donor_p,train_ix),st))
                nearest_new=min(viable,key=lambda st:(f.hd(f.panel(st,*sites),donor_p,train_ix),st))
                def h(st):return f.heldout(f.panel(st,*sites),gp,test_ix)
                rows.append({'pid':pid,'width':width,'patch':list(patch),'uncompensated_pool':len(original_pool),
                    'compensated_pool':len(viable),'raw_hamming_to_G0':e_distance(donor,g0),
                    'minimum_train_distance_old':f.hd(f.panel(nearest_std,*sites),donor_p,train_ix),
                    'minimum_train_distance_new':f.hd(f.panel(nearest_new,*sites),donor_p,train_ix),
                    'donor':h(donor),'uncompensated_nearest':h(nearest_std),'compensated_nearest':h(nearest_new)})
    result={'experiment':119,'protocol':{'cohort':'112 20 parent pairs, only 118 compensated exact-feature eligible patch contexts',
      'raw_distance':'exactly donor-to-G0 raw Hamming for compensated nulls',
      'nuisance':'same first-tick changed position mask, popcount, adjacent AND and bit flip count',
      'control_difference':'old alternative alters patch only; compensated alternative additionally changes 1 originally donor-different outside-patch site',
      'train':'6 raw probes from fold 0 (1,7,15) x both sides at ticks 1 and 3; select nearest response Hamming; no evaluation response',
      'test':'other 24 raw-value probes at ticks 6,12,24; compare response mask Jaccard/exact to original G0',
      'independence':'parent-level unit; patch/control evaluations nested',
      'interpretation':'distance overlap repair with unequal edit budget, not source-causal identification'},
      'inventory':dict(sorted(inventory.items())),'summary':stats(rows),'patch_records':rows}
    f.panel.cache_clear();return result

def main():
 a=argparse.ArgumentParser();a.add_argument('--reference',type=Path,default=ROOT/'112_probe_discrimination_audit/results/default.json');a.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json');a.add_argument('--max-parents',type=int,default=None);z=a.parse_args()
 if z.max_parents is not None and z.max_parents<1:a.error('positive max-parents')
 data=assay(z.reference,z.max_parents);z.output.parent.mkdir(parents=True,exist_ok=True);z.output.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'inventory':data['inventory'],'summary':{w:{k:v for k,v in val.items() if k!='parent_details'} for w,val in data['summary'].items()}},sort_keys=True,indent=2))
if __name__=='__main__':main()
