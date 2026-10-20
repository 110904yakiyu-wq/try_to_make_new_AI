"""Finite arbitrary-choice envelope over all 970 pre-response eligible controls.
Selection extrema are adversarial sensitivity bounds, not an outcome-aware policy.
"""
import csv,json,statistics
from collections import defaultdict,Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent

def read(path):
 with open(path,newline='') as f:return [{k:int(v) for k,v in q.items()} for q in csv.DictReader(f)]

def group(rows):
 d=defaultdict(list)
 for q in rows:d[(q['parent_id'],q['attempt'])].append(q)
 return d

def assay(allctrl=HERE/'results/probes.csv',first=HERE.parent/'140_extended_matched_spread/results/probes.csv'):
 ctrl=read(allctrl);standard=read(first)
 assert len(ctrl)==29100 and len(standard)==6780
 ga={(r['parent_id'],r['side'],r['raw']):r for r in standard if r['arm']==0}
 fa={(r['parent_id'],r['side'],r['raw']):r for r in standard if r['arm']==1}
 assert len(ga)==3390 and len(fa)==3390
 per=group(ctrl);parents=defaultdict(list)
 for (pid,att),rs in per.items():
  assert len(rs)==30 and all(q['arm']==1 for q in rs)
  # Every originally selected control must occur exactly in the full candidate pool.
  ids={(r['parent_id'],r['side'],r['raw']) for r in rs}
  assert len(ids)==30
  if att==standard[next(i for i,x in enumerate(standard) if x['parent_id']==pid)]['attempt']:
   assert all(r['first10']==fa[(pid,r['side'],r['raw'])]['first10'] and
              r['first60']==fa[(pid,r['side'],r['raw'])]['first60'] for r in rs)
  parents[pid].append((att,rs))
 assert len(parents)==113 and len(per)==970
 result={'experiment':142,'contract':{'eligible_controls':'all 970 Exp139 autonomous qualified candidates',
    'probe':'same 30 side/raw material probes at 50000-tick horizon',
    'uncertainty':'any censored nonarrival may arrive later; bound individually',
    'choice':'select at most one prequalified control per G0 parent',
    'envelope':'posthoc minima/maxima mathematical sensitivity, NOT permissible deployment selector',
    'independence':'113 G0 parents; 970 controls and 29100 probes are repeated dependent alternatives'},
    'summary':{},'parent_records':[]}
 for pid,choices in sorted(parents.items()):
  orig=[ga[(pid,side,raw)] for side in (0,1) for raw in range(1,16)]
  r={'parent_id':pid,'eligible_choices':len(choices),'first_attempt':min(z[0] for z in choices)}
  for th in (10,60):
   f=f'first{th}'
   actual=sum(q[f]>=0 for q in orig)
   actual_unknown=sum(q[f]<0 and q['recurrence']<0 for q in orig)
   vals=[]
   for att,rr in choices:
     confirmed=sum(q[f]>=0 for q in rr)
     unknown=sum(q[f]<0 and q['recurrence']<0 for q in rr)
     vals.append({'attempt':att,'yes':confirmed,'unknown':unknown})
   assert len(vals)==len(choices)
   r[f'spread{th}']={'G0_yes':actual,'G0_unknown':actual_unknown,
     'control_min_yes':min(x['yes'] for x in vals),
     'control_max_yes':max(x['yes'] for x in vals),
     'control_min_possible_yes':min(x['yes']+x['unknown'] for x in vals),
     'control_max_possible_yes':max(x['yes']+x['unknown'] for x in vals),
     'control_uniform_avg_yes':statistics.mean(x['yes'] for x in vals),
     'control_uniform_avg_unknown':statistics.mean(x['unknown'] for x in vals),
     'per_control':vals}
  result['parent_records'].append(r)
 old={int(x['parent_id']) for x in standard if int(x['attempt'])<=100}
 # For original 55, first accepted attempt <=100; all other 58 newly found.
 assert len(old)==55
 for name,rs in [('old55',[r for r in result['parent_records'] if r['parent_id'] in old]),
                 ('new58',[r for r in result['parent_records'] if r['parent_id'] not in old]),
                 ('all113',result['parent_records'])]:
  assert len(rs)=={'old55':55,'new58':58,'all113':113}[name]
  total=len(rs)*30
  s={'parents':len(rs),'available_controls':sum(x['eligible_choices'] for x in rs),'total_per_arm':total}
  for th in (10,60):
   x=[r[f'spread{th}'] for r in rs]
   g=sum(v['G0_yes'] for v in x); gu=sum(v['G0_unknown'] for v in x)
   # choose per parent the worst/best eligible control, retain censor uncertainty.
   low=(g-sum(v['control_max_possible_yes'] for v in x))/total
   high=(g+gu-sum(v['control_min_yes'] for v in x))/total
   mean=(g-sum(v['control_uniform_avg_yes'] for v in x))/total
   mean_lower=(g-sum(v['control_uniform_avg_yes']+v['control_uniform_avg_unknown'] for v in x))/total
   s[f'spread{th}']={'G0_confirmed_yes':g,'G0_unknown':gu,
      'arbitrary_control_choice_eventual_lower':low,
      'arbitrary_control_choice_eventual_upper':high,
      'uniform_candidate_parent_weighted_observed_diff':mean,
      'uniform_candidate_censor_aware_lower':mean_lower,
      'all_control_choices_sign_negative':high<0,
      'parents_with_choice_variation':sum(v['control_min_yes']!=v['control_max_yes'] for v in x)}
  result['summary'][name]=s
 assert result['summary']['all113']['available_controls']==970
 return result
def archive(out):
    per_control=HERE/'results/per_control.csv'
    with per_control.open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(('parent_id','attempt','yes10','unknown10','yes60','unknown60'))
        for p in out['parent_records']:
            a={v['attempt']:v for v in p['spread10']['per_control']}
            b={v['attempt']:v for v in p['spread60']['per_control']}
            assert a.keys()==b.keys()
            for attempt in sorted(a):
                writer.writerow((p['parent_id'],attempt,a[attempt]['yes'],a[attempt]['unknown'],
                                b[attempt]['yes'],b[attempt]['unknown']))
    # Compact primary JSON, without redundant per-control rows; CSV retains those rows.
    compact={k:v for k,v in out.items() if k!='parent_records'}
    compact['parent_records']=[]
    for p in out['parent_records']:
        cp={k:v for k,v in p.items() if k not in ('spread10','spread60')}
        cp['spread10']={k:v for k,v in p['spread10'].items() if k!='per_control'}
        cp['spread60']={k:v for k,v in p['spread60'].items() if k!='per_control'}
        compact['parent_records'].append(cp)
    compact['per_control_archive']='results/per_control.csv'
    (HERE/'results/default.json').write_text(json.dumps(compact,indent=2,sort_keys=True)+'\n')
    (HERE/'results/default.txt').write_text(json.dumps(out['summary'],indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
 out=assay();archive(out)
 print(json.dumps(out['summary'],indent=2,sort_keys=True))
