"""Prepare all 970 accepted states for post-selection sensitivity tests."""
import csv,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'139_extended_control_budget'))
import core
SOURCE=HERE.parent/'139_extended_control_budget/results/accepted.csv'

def main():
    p=list(core.parents()); assert len(p)==130
    out=HERE/'results/eligible_states.csv'
    with open(SOURCE,newline='') as f,open(out,'w',newline='') as g:
        inp=csv.DictReader(f);wr=csv.writer(g,lineterminator='\n')
        wr.writerow(['parent_id','attempt','arm','left','right','frame_hex'])
        for r in inp:
            pid=int(r['parent_id']); att=int(r['attempt'])
            seed,base,orb=p[pid];left=min(orb['support'])-1;right=max(orb['support'])+1
            frame=bytes.fromhex(r['accepted_control_hex'])
            assert frame[left]==frame[right]==0
            wr.writerow([pid,att,1,left,right,frame.hex()])
    return out
if __name__=='__main__':print(main())
