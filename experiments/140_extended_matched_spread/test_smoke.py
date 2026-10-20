"""Cross-language regression: all 3300 old observations and 64 new trajectories."""
import csv,random,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'139_extended_control_budget'))
import core
sys.path.insert(0,str(HERE))
import analyze

def py_trace(initial,limit=500):
    s=bytes(initial);seen={(s,0):0};union={i for i,x in enumerate(s) if x}
    f10=0 if len(union)>=10 else -1;f60=0 if len(union)>=60 else -1
    if f60>=0:return f10,f60,-1
    for tick in range(1,limit+1):
        s=core.step(s,(tick-1)%3)
        union|={i for i,x in enumerate(s) if x}
        if f10<0 and len(union)>=10:f10=tick
        if len(union)>=60:return f10,tick,-1
        key=(s,tick%3)
        if key in seen:return f10,f60,tick
        seen[key]=tick
    return f10,-1,-1

def main():
    r=analyze.assay(HERE/'results/probes.csv',HERE.parent/'130_spread_threshold_robustness/results/probes.csv')
    assert r['summary']['all113']['parents']==113
    states={}
    with open(HERE/'results/selected_states.csv',newline='') as f:
        for row in csv.DictReader(f):states[(int(row['parent_id']),int(row['arm']))]=row
    with open(HERE/'results/probes.csv',newline='') as f: rows=list(csv.DictReader(f))
    new=[x for x in rows if int(x['parent_id']) not in {p['parent_id'] for p in r['parent_records'] if p['subset']=='old55'}]
    # Cover both event-positive and cycle-certified negative outcomes, old/new parent IDs.
    yes=[x for x in new if int(x['first60'])>=0 and int(x['first60'])<=500]
    no=[x for x in new if int(x['recurrence'])>=0 and int(x['first60'])<0]
    rng=random.Random(140)
    picked=rng.sample(yes,min(32,len(yes)))+rng.sample(no,min(32,len(no)))
    for row in picked:
        pid=int(row['parent_id']);arm=int(row['arm']);s=int(row['side']);raw=int(row['raw'])
        meta=states[(pid,arm)];p=int(meta['right'] if s else meta['left']);f=bytearray.fromhex(meta['frame_hex']);assert f[p]==0;f[p]=raw
        a,b,c=py_trace(f,500)
        assert a==int(row['first10']),(pid,s,raw,a,row['first10'])
        assert b==int(row['first60']),(pid,s,raw,b,row['first60'])
        if b<0:assert c==int(row['recurrence']),(pid,s,raw,c,row['recurrence'])
    print('exp140 independent Python first500 trace smoke PASS; rows',len(rows),'new_sample',len(picked))
if __name__=='__main__':main()
