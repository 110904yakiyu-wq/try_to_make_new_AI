from pathlib import Path
import run

def main():
 d=run.assay()
 counts=[v['parents'] for v in d['budgets'].values()]
 assert counts==sorted(counts)
 assert d['budgets']['100']['parents']==55
 assert d['budgets']['1000']['parents']==113
 assert all(v['spread10']['upper_rate']<0 and v['spread60']['upper_rate']<0 for v in d['budgets'].values())
 print('exp143 smoke: PASS (original Exp137 budgets validated in run.assay)')
if __name__=='__main__':main()
