#!/usr/bin/env python3
import json
import run as v

def main():
 r=v.analyze(v.read(v.SRC/'probes.csv'),v.read(v.SRC/'eligibility.csv'))
 assert r==json.loads((v.HERE/'results/default.json').read_text())
 for delay,total in (('24',228),('96',219)):
  d=r['results'][delay]
  assert d['pretest_probe_site_eligible']==total
  for names in ('sham__pulse7','sham__pulse11'):
   assert d['comparisons'][names]['both']['eligible_contexts']<=3
  assert d['comparisons']['pulse7__pulse11']['both']['eligible_contexts']>=76
 print('PASS Exp152 no-outcome feature overlap and summary regeneration')
if __name__=='__main__':main()
