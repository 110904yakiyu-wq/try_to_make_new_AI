#!/usr/bin/env python3
import csv,json
import run as v

def main():
 parents=list(v.m.parents());seed,fr,o=parents[0]
 lo=min(o['support'])-1;hi=max(o['support'])+1
 s=v.trajectory(fr,lo,hi,'simultaneous')
 check=bytearray(fr);check[lo]=7;check[hi]=11
 assert s==v.v.evolve(check,v.END_TICK)
 result=v.assay(4)
 assert result['inventory']['parents_evaluated']==4
 assert len(result['records'])==12*len(result['contexts'])
 frozen=json.loads((v.HERE/'results/default.json').read_text())
 assert frozen['inventory']['heldout_eligible_side_contexts']==110
 assert frozen['inventory']['two_order_interventions_both_feasible']==111
 assert frozen['summary']['state_identity']['all_three_same']==46
 with (v.HERE/'results/probes.csv').open(newline='',encoding='utf-8') as f:rr=list(csv.DictReader(f))
 assert len(rr)==1320
 print('PASS Exp153 phase0 schedules, exact no-overwrite eligibility and results')
if __name__=='__main__':main()
