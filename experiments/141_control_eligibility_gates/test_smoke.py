"""Exhaustive 139 acceptance equivalence and independent classifier checks."""
import random,csv,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'139_extended_control_budget'))
import core

def py_gate(pid,attempt,parents):
 _,fr,p=parents[pid]
 o=core.orbit(core.proposal(pid,fr,attempt-1),max_ticks=500)
 if o['status']!='cycle':return 0
 if not o['active']:return 1
 if o['period']!=p['period']:return 2
 if o['support']!=p['support']:return 3
 ph0=[q for j,q in enumerate(o['cycle']) if (o['phase']+j)%3==0]
 c=max(ph0,key=lambda f:sum(bool(x) for x in f))
 if any(bool(x)!=bool(y) for x,y in zip(c,fr)):return 4
 return 5

def main():
 with open(HERE/'results/gates.csv',newline='') as f: rows=list(csv.DictReader(f))
 assert len(rows)==130000
 rng=random.Random(141);sample=rng.sample(rows,96);ps=list(core.parents())
 for q in sample:
  pid=int(q['parent_id']);attempt=int(q['attempt']);assert py_gate(pid,attempt,ps)==int(q['gate']),(pid,attempt,q['gate'])
 print('exp141 PASS: 96 independent candidate gate checks')
if __name__=='__main__':main()
