import run

def main():
 d=run.assay()
 assert all(len(d['by_raw'][x])==15 for x in ('10','60'))
 for x in ('10','60'):
  assert all(v['sign_guaranteed_negative'] for v in d['by_side'][x].values())
  assert all(v['sign_guaranteed_negative'] for v in d['by_raw'][x].values())
 assert d['total']['10']['n_per_arm']==1740
 print('exp144 smoke: PASS')
if __name__=='__main__':main()
