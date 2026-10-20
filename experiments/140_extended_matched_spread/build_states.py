"""Freeze first eligible candidate before testing response, for 113 G0 parents."""
import csv,sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'139_extended_control_budget'))
import core
SOURCE=HERE.parent/'139_extended_control_budget/results/accepted.csv'

def build(source=SOURCE,output=HERE/'results/selected_states.csv'):
  by={}
  with open(source,newline='') as f:
    for r in csv.DictReader(f):
      pid=int(r['parent_id']); att=int(r['attempt'])
      if pid not in by or att<by[pid][0]:by[pid]=(att,bytes.fromhex(r['accepted_control_hex']))
  ps=list(core.parents());assert len(ps)==130 and len(by)==113
  Path(output).parent.mkdir(parents=True,exist_ok=True)
  with open(output,'w',newline='') as f:
    w=csv.writer(f,lineterminator="\n");w.writerow(['parent_id','attempt','arm','left','right','frame_hex'])
    for pid,(seed,frame,orb) in enumerate(ps):
      if pid not in by:continue
      attempt,ctrl=by[pid];support=orb['support'];left=min(support)-1;right=max(support)+1
      assert frame[left]==frame[right]==ctrl[left]==ctrl[right]==0
      assert core.qualifying_control(pid,frame,orb,attempt-1)==ctrl,('control mismatch',pid,attempt)
      w.writerow([pid,attempt,0,left,right,frame.hex()]);w.writerow([pid,attempt,1,left,right,ctrl.hex()])
  return len(by)
if __name__=='__main__':print('states',build())
