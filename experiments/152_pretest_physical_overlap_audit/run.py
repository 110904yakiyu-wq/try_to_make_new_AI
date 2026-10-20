#!/usr/bin/env python3
"""Exp152: pretest physical-overlap audit for Experience Gate 151.

No added kernel operation or new trajectories. Conditioning on posttraining
physical features is NOT a causal mediation or adjustment estimator.
"""
import argparse,csv,json,statistics
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
SRC=HERE.parent/'151_experience_heldout_response_gate/results'
PAIRS=(('sham','pulse7'),('sham','pulse11'),('pulse7','pulse11'))
METRICS=('union_affected_sites','reached_10','reached_30')

def read(path):
 with Path(path).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))

def score(v):
 return float(v=='True') if v in ('True','False') else float(v)

def analyze(probes,eligibility):
 bycontext=defaultdict(lambda:defaultdict(list))
 for r in probes:
  key=(int(r['parent_id']),int(r['train_side']),int(r['delay']))
  bycontext[key][r['arm']].append(r)
 contexts={ (int(r['parent_id']),int(r['train_side']),int(r['delay'])):r for r in eligibility }
 assert len(contexts)==520 and len(probes)==5364
 assert sum(r['eligible']=='True' for r in contexts.values())==447
 out={}
 for delay in (24,96):
  cohorts=[(key,entry) for key,entry in contexts.items() if key[2]==delay]
  assert len(cohorts)==260
  q={}
  for a,b in PAIRS:
   def passes(entry,criterion):
    eq_bits=entry['physical_bits_before_test_'+a]==entry['physical_bits_before_test_'+b]
    eq_occ=entry['occupied_windows_before_test_'+a]==entry['occupied_windows_before_test_'+b]
    return criterion=='unconditional' or (criterion=='bits' and eq_bits) or (criterion=='occupancy' and eq_occ) or (criterion=='both' and eq_bits and eq_occ)
   outpair={}
   for cond in ('unconditional','bits','occupancy','both'):
    eligible=[k for k,e in cohorts if e['eligible']=='True' and passes(e,cond)]
    parentids=sorted(set(k[0] for k in eligible))
    stats={}
    for metric in METRICS:
     byparent=defaultdict(list)
     for key in eligible:
      ar=bycontext[key];assert sorted(x['test_raw'] for x in ar[a])==['1','14','5','9']
      assert len(ar[a])==len(ar[b])==4
      mean_a=statistics.mean(score(x[metric]) for x in ar[a]);mean_b=statistics.mean(score(x[metric]) for x in ar[b]);byparent[key[0]].append(mean_b-mean_a)
     diffs=[statistics.mean(v) for v in byparent.values()]
     stats[metric]={'mean_b_minus_a':statistics.mean(diffs) if diffs else None,
                   'parent_b_higher':sum(d>0 for d in diffs),
                   'parent_a_higher':sum(d<0 for d in diffs),
                   'parent_tied':sum(d==0 for d in diffs)}
    outpair[cond]={'eligible_contexts':len(eligible),'parent_clusters':len(parentids),'metrics':stats}
   q[a+'__'+b]=outpair
  out[str(delay)]={'all_parent_side_contexts':260,'pretest_probe_site_eligible':sum(e['eligible']=='True' for _,e in cohorts),
                   'ineligible':sum(e['eligible']!='True' for _,e in cohorts),
                   'comparisons':q}
 return {'experiment':152,'source':'Exp151 immutable pretest eligibility and distinct heldout probe CSV',
         'protocol':{'physics':'unchanged 104/139; no resimulation',
                     'features':'total 4bit popcount and occupied window count immediately before heldout injection',
                     'cohorts':'pretest site must be empty in all three arms',
                     'estimand':'selected descriptive parent-weighted difference, NOT causal mediation',
                     'selection_warning':'post-training state matching is conditioning on mediator; low overlap limits identification',
                     'do_not_impute':'test event undefined at occupied site under non-overwriting intervention'},
         'results':out}

def main():
 p=argparse.ArgumentParser();p.add_argument('--probes',type=Path,default=SRC/'probes.csv');p.add_argument('--eligibility',type=Path,default=SRC/'eligibility.csv');p.add_argument('--output',type=Path,default=HERE/'results/default.json');a=p.parse_args()
 r=analyze(read(a.probes),read(a.eligibility));a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r['results'],sort_keys=True,indent=2))
if __name__=='__main__':main()
