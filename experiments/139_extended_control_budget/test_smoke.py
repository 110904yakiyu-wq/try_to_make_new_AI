"""Exp139 original 133 exact first100 distribution and independent CPython checks."""
import csv,json,random
from collections import Counter
from pathlib import Path
import core,analyze
HERE=Path(__file__).resolve().parent
# Freeze original Exp126 first accepted attempt list: independent of new candidates.
MANIFEST={2:85,4:47,5:61,6:12,8:13,9:20,11:96,12:51,13:49,17:38,19:91,22:5,23:4,24:23,25:30,26:16,28:15,29:12,32:55,33:39,34:9,35:6,36:2,37:83,38:30,39:8,42:35,45:58,46:79,48:67,49:24,52:41,59:29,61:58,62:52,63:61,66:75,73:30,75:54,76:26,77:27,79:19,80:87,85:26,86:9,90:7,91:83,92:70,99:1,102:32,104:74,106:51,108:33,111:27,126:5}

def main():
 d=analyze.assay()
 assert d['summary']['matched100']==55 and d['summary']['matched1000']==113
 first={r['parent_id']:r['first_eligible_attempt'] for r in d['parent_records'] if r['eligible_in_100']}
 assert first==MANIFEST
 ps=list(core.parents())
 rows=list(csv.DictReader(open(HERE/'results/accepted.csv',newline='')))
 rng=random.Random(139)
 sample=rng.sample(rows,64)
 for r in sample:
  pid=int(r['parent_id']);att=int(r['attempt'])
  got=core.qualifying_control(pid,ps[pid][1],ps[pid][2],att-1)
  assert got is not None and got.hex()==r['accepted_control_hex'],(pid,att)
 # Explicitly test some non-acceptances with Python, too.
 yes={(int(r['parent_id']),int(r['attempt'])) for r in rows}
 for _ in range(32):
  pid=rng.randrange(130);att=rng.randrange(1,1001)
  got=core.qualifying_control(pid,ps[pid][1],ps[pid][2],att-1)
  assert (got is not None)==((pid,att) in yes),(pid,att)
 print('exp139 PASS: first100 manifest exact and 96 independent candidate classifications')
if __name__=='__main__':main()
