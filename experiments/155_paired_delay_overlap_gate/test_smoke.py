#!/usr/bin/env python3
import json
import run as v

def main():
 x=v.assay(v.read(v.SOURCE/'probes.csv'),v.read(v.SOURCE/'eligibility.csv'))
 assert x==json.loads((v.HERE/'results/default.json').read_text())
 assert x['inventory']['shared_eligible_contexts']==215
 assert x['inventory']['shared_parent_clusters']==127
 assert x['results']['pulse7']['union_affected_sites']['delay24_parent_mean_difference']>0
 print('PASS Exp155 shared-parent/direction fixed-delay contrast regeneration')
if __name__=='__main__':main()
