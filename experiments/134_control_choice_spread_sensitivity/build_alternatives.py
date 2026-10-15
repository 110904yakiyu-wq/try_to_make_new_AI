#!/usr/bin/env python3
"""Reconstruct other accepted 100-attempt controls, using only autonomous dynamics.

These replacements are NOT chosen using any material-injection outcomes.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,csv,random,json
ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('exp133',ROOT/'133_eligible_control_multiplicity/run.py')
e=importlib.util.module_from_spec(s);s.loader.exec_module(e)
m=e.m

def build(reference):
  manifest=json.loads(Path(reference).read_text())
  assert manifest['experiment']==133 and manifest['summary']['eligible_parents']==55
  byid={p['parent_id']:p for p in manifest['parent_records']}
  states=[]
  for pid,(seed,g0,parent) in enumerate(m.parents()):
    ref=byid[pid]
    assert ref['seed']==list(seed)
    if not ref['accepted_attempts']:continue
    for rank,attempt in enumerate(ref['accepted_attempts']):
      rng=random.Random(3_000_000+pid*300_000+attempt-1)
      can=bytes(rng.randrange(1,16) if x else 0 for x in g0)
      o=m.orbit(can,max_ticks=500)
      assert o['status']=='cycle' and o['active'] and o['period']==parent['period'] and o['support']==parent['support']
      frames=[f for i,f in enumerate(o['cycle']) if (o['phase']+i)%3==0]
      ctrl=max(frames,key=lambda x:sum(bool(v) for v in x))
      assert all(bool(x)==bool(y) for x,y in zip(ctrl,g0))
      assert hashlib.sha256(ctrl).hexdigest()==ref['accepted_microstate_sha256'][rank]
      if rank==0:continue # The frozen 130 reference already includes first accepted control.
      states.append({'parent_id':pid,'attempt':attempt,'rank':rank+1,
        'left':min(parent['support'])-1,'right':max(parent['support'])+1,
        'phase0_60_window_hex':ctrl.hex(),'sha256':hashlib.sha256(ctrl).hexdigest()})
  assert len(states)==32
  return states

def main():
  ap=argparse.ArgumentParser();ap.add_argument('--reference',type=Path,default=ROOT/'133_eligible_control_multiplicity/results/default.json')
  ap.add_argument('--output',type=Path,default=HERE/'results/alternative_controls.csv');a=ap.parse_args()
  rows=build(a.reference);a.output.parent.mkdir(parents=True,exist_ok=True)
  with a.output.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
  print('alternative_controls',len(rows),'parents',len({x['parent_id'] for x in rows}))
if __name__=='__main__':main()
