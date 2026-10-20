#!/usr/bin/env python3
"""Integrity and positive/negative controls, no fake learning test."""
import csv,json
from pathlib import Path
import run as v

def main():
 assert len(list(v.m.parents()))==130
 assert v.m.CENTER==30 and v.m.SIZE==60
 assert v.response(bytes(60),0,0)['union_affected_sites']==0
 a=bytearray(60);a[30]=7;a[31]=11
 assert v.m.step(a,0)==v.m.step(bytes(a),0)
 for s in (bytes(a), bytes(60)):
  assert v.evolve(s,24)==v.evolve(v.evolve(s,12),12)
 subset=v.assay(3)
 assert subset['inventory']['processed_parents']==3
 assert subset['inventory']['total_response_records']==3*subset['inventory']['per_arm_probe_records']
 rows=v.csv.DictReader((v.HERE/'results/probes.csv').open(encoding='utf-8'))
 full=list(rows)
 summary=json.loads((v.HERE/'results/default.json').read_text())
 assert summary['inventory']['total_response_records']==len(full)==5364
 assert summary['inventory']['eligible_contexts']==447
 assert len(list(csv.DictReader((v.HERE/'results/eligibility.csv').open())))==520
 assert summary['summary']['24:union_affected_sites']['contrasts']['pulse7-sham']['mean']>0
 print('PASS Exp151 physics, phase, self-baseline, parent clustering, frozen counts')
if __name__=='__main__':main()
