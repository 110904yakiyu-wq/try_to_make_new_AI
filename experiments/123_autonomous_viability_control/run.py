#!/usr/bin/env python3
"""Exp123 pre-material autonomous recurrence audit of frozen Exp121 states.

No probe outcome is used to select a null. Recurrence considered only a
finite-horizon observer label, not intrinsic goal or survival concept.
"""
import argparse,importlib.util,json,statistics
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('exp121',ROOT/'121_equal_budget_heldout'/'run.py')
f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f);e=f.e
ARMS=('G0_reference','recipient_reference','transplant','equal_edit_null','fixed_patch_null')

def orbit_summary(frame):
 state=bytes(frame);seen={(state,0):0};frames=[state]
 for tick in range(1,2001):
  state=e.m.step(state,(tick-1)%3,'left')
  key=(state,tick%3)
  if key in seen:
   entry=seen[key];cycle=frames[entry:tick]
   support={i for fr in cycle for i,v in enumerate(fr) if v}
   components=0;rem=set(support)
   while rem:
    components+=1;front=[rem.pop()]
    while front:
     v=front.pop()
     for j in ((v-1)%e.m.SIZE,(v+1)%e.m.SIZE):
      if j in rem:rem.remove(j);front.append(j)
   cls='static' if len(set(cycle))<=1 else ('connected' if components==1 else 'fragmented')
   return {'recurrence_tick':tick,'preperiod':entry,'period':tick-entry,'class':cls,'censored_500':tick>500,'censored_2000':False}
  seen[key]=tick;frames.append(state)
 return {'recurrence_tick':None,'preperiod':None,'period':None,'class':'censored','censored_500':True,'censored_2000':True}

def aggregate(rows):
 out={}
 for width in e.WIDTHS:
  rs=[x for x in rows if x['width']==width];parents=defaultdict(list)
  for v in rs:parents[v['pid']].append(v)
  cluster=[]
  for pid,r in sorted(parents.items()):
   q={'parent_id':pid,'patches':len(r)}
   for arm in ARMS:
    for metric in ('censored_500','censored_2000'):
     q[f'{arm}_{metric}']=statistics.mean(int(x[arm][metric]) for x in r)
    for cls in ('connected','fragmented','static'):
     q[f'{arm}_{cls}_500']=statistics.mean(x[arm]['class']==cls and not x[arm]['censored_500'] for x in r)
   cluster.append(q)
  entry={'patches':len(rs),'parents':len(cluster),'parent_details':cluster}
  for arm in ARMS:
   for metric in ('censored_500','censored_2000','connected_500','fragmented_500','static_500'):
    entry[f'{arm}_{metric}_mean']=statistics.mean(x[f'{arm}_{metric}'] for x in cluster) if cluster else None
  for a,b in [('transplant','equal_edit_null'),('transplant','fixed_patch_null')]:
   for metric in ('censored_500','connected_500'):
    dd=[x[f'{a}_{metric}']-x[f'{b}_{metric}'] for x in cluster]
    k=f'{a}_minus_{b}_{metric}'
    entry[k+'_mean']=statistics.mean(dd) if dd else None
    entry[k+'_wins']=sum(t>1e-12 for t in dd)
    entry[k+'_losses']=sum(t< -1e-12 for t in dd)
    entry[k+'_ties']=sum(abs(t)<=1e-12 for t in dd)
  out[str(width)]=entry
 return out

def assay(ref_file,pretest_file,max_parents=None):
 ref=json.loads(Path(ref_file).read_text());prev=json.loads(Path(pretest_file).read_text());assert prev['experiment']==121 and len(ref['parent_records'])==20
 prevs={(q['pid'],q['width'],tuple(q['patch'])):q for q in prev['patch_records']}
 catalog=list(e.m.parents('left'));result=[];inventory=Counter()
 for j,entry in enumerate(ref['parent_records']):
  if max_parents is not None and j>=max_parents:break
  pid=entry['parent_id'];_,g0,parent=catalog[pid]
  ctrl=e.reference_control(pid,g0,parent,entry['control_match_attempt'])
  mask=e.first_mask(g0);assert mask==e.first_mask(ctrl)
  site=(min(parent['support'])-1,max(parent['support'])+1)
  inventory['parents']+=1
  for width in e.WIDTHS:
   for patch in e.changed_patches(g0,ctrl,parent['support'],width):
    key=(pid,width,tuple(patch));old=prevs.get(key)
    if old is None:continue
    donor=e.replace(ctrl,g0,patch)
    pool=f.equal_budget_pool(ctrl,g0,patch,donor,parent)
    base=list(e.exact_physical_nulls(ctrl,g0,patch,mask,e.features(donor)))
    donor_panel=f.f.panel(donor,*site)
    def nearest(seq):return min(seq,key=lambda z:(f.f.hd(f.f.panel(z,*site),donor_panel,f.TRAIN),z))
    chosen=nearest(pool);other=nearest(base)
    assert f.f.hd(f.f.panel(chosen,*site),donor_panel,f.TRAIN)==old['equal_budget_nearest_train_distance']
    states={'G0_reference':g0,'recipient_reference':ctrl,'transplant':donor,'equal_edit_null':chosen,'fixed_patch_null':other}
    record={'pid':pid,'width':width,'patch':list(patch)}
    record.update({name:orbit_summary(state) for name,state in states.items()})
    result.append(record);inventory[f'w{width}_patches']+=1
 assert max_parents is not None or len(result)==15
 return {'experiment':123,'protocol':{'scope':'same 15 Exp121/122 heldout patch contexts and selected controls',
     'selection':'frozen 121 preoutcome early-response nearest controls, no new tuning',
     'new_observation':'autonomous no-material first recurrence by tick500/2000, with preperiod and exact phase-coupled key',
     'question':'do off-cycle local edits have different baseline convergence, potentially confounding material-injected connected rates?',
     'censoring':'finite time unresolved, not inactive, dead, or nonreproductive',
     'independence':'parent level; patch arms repeated measures, no autonomous source causal identification'},
     'inventory':dict(sorted(inventory.items())),'summary':aggregate(result),'patch_records':result}

def main():
 p=argparse.ArgumentParser();p.add_argument('--reference',type=Path,default=ROOT/'112_probe_discrimination_audit/results/default.json');p.add_argument('--pretest',type=Path,default=ROOT/'121_equal_budget_heldout/results/default.json');p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results/default.json');p.add_argument('--max-parents',type=int,default=None);z=p.parse_args()
 if z.max_parents is not None and z.max_parents<1:p.error('positive max-parents')
 r=assay(z.reference,z.pretest,z.max_parents);z.output.parent.mkdir(parents=True,exist_ok=True);z.output.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'inventory':r['inventory'],'summary':{w:{k:v for k,v in q.items() if k!='parent_details'} for w,q in r['summary'].items()}},sort_keys=True,indent=2))
if __name__=='__main__':main()
