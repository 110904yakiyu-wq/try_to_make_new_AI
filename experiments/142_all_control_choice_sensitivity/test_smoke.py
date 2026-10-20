"""Cross-check original 100-proposal choice envelopes and recent regression."""
from pathlib import Path
import csv,sys,collections
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import analyze

def main():
 d=analyze.assay();assert d['summary']['all113']['available_controls']==970
 # Historical Experiment134: all 87 candidates within the original 100 proposals.
 first=list(csv.DictReader(open(HERE.parent/'140_extended_matched_spread/results/probes.csv',newline='')))
 choices=list(csv.DictReader(open(HERE/'results/probes.csv',newline='')))
 old={int(q['parent_id']) for q in first if int(q['attempt'])<=100}
 assert len(old)==55
 for th,baseline in [('first10',(-333, -189)),('first60',(-296,-172))]:
  orig=collections.Counter()
  for q in first:
   if int(q['parent_id']) in old and q['arm']=='0' and int(q[th])>=0:orig[int(q['parent_id'])]+=1
  cc=collections.defaultdict(lambda:collections.Counter())
  for q in choices:
   pid=int(q['parent_id']);att=int(q['attempt'])
   if pid not in old or att>100:continue
   cc[(pid,att)]['yes']+=int(q[th])>=0
   cc[(pid,att)]['unknown']+=int(q[th])<0 and int(q['recurrence'])<0
  assert len(cc)==87
  grouped=collections.defaultdict(list)
  for (pid,att),counts in cc.items():grouped[pid].append(counts)
  low=sum(orig[pid]-max(x['yes']+x['unknown'] for x in grouped[pid]) for pid in old)
  high=sum(orig[pid]-min(x['yes'] for x in grouped[pid]) for pid in old)
  assert (low,high)==baseline,(th,low,high)
 print('exp142 PASS: 87 first-100 controls reproduce Exp134 envelopes; 970-control audit')
if __name__=='__main__':main()
