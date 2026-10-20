#!/usr/bin/env python3
import csv,json
import run as v

def main():
 meta=json.loads((v.SOURCE/'default.json').read_text())
 with (v.SOURCE/'probes.csv').open(newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
 r=v.analyze(meta,rows)
 assert r==json.loads((v.HERE/'results/default.json').read_text())
 assert r['integrity']['same_state_future_mismatches']==0
 assert r['results']['same_state']['paired_heldout_probes']==184
 assert r['results']['different_state']['paired_heldout_probes']==256
 print('PASS Exp154 exact microstate equality implies identical heldout futures')
if __name__=='__main__':main()
