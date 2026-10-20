"""Analyze deterministic original-budget and 1000-candidate eligibility.
This script does not simulate perturbation outcomes.
"""
import csv,json
from collections import Counter,defaultdict
from pathlib import Path
import core
HERE=Path(__file__).resolve().parent

def assay(csv_path=HERE/'results/accepted.csv'):
    parent_list=list(core.parents())
    with open(csv_path,newline='',encoding='utf-8') as f:
        accepted=[{'parent_id':int(r['parent_id']),'attempt':int(r['attempt']),
                   'control_hex':r['accepted_control_hex']} for r in csv.DictReader(f)]
    groups=defaultdict(list)
    for r in accepted:
        p=r['parent_id']; assert 0<=p<130 and 1<=r['attempt']<=1000
        assert len(r['control_hex'])==120 and all(int(r['control_hex'][i:i+2],16)<16 for i in range(0,120,2))
        groups[p].append(r)
    assert len(accepted)==970
    census=[]
    for pid,(seed,g0,orb) in enumerate(parent_list):
        lst=sorted(groups[pid],key=lambda a:a['attempt'])
        assert len({x['attempt'] for x in lst})==len(lst)
        census.append({'parent_id':pid,'seed':list(seed),'period':orb['period'],
                       'support_size':len(orb['support']),'first_eligible_attempt':lst[0]['attempt'] if lst else None,
                       'eligible_in_100':sum(x['attempt']<=100 for x in lst),
                       'eligible_in_1000':len(lst),
                       'all_accepted_attempts':[x['attempt'] for x in lst]})
    assert Counter(r['eligible_in_100'] for r in census)=={0:75,1:33,2:16,3:3,4:2,5:1}
    bins={str(b):sum(r['first_eligible_attempt'] is not None and r['first_eligible_attempt']<=b for r in census) for b in (1,5,10,25,50,100,200,300,500,750,1000)}
    strata={}
    for period in sorted({r['period'] for r in census}):
        rows=[r for r in census if r['period']==period]
        strata[str(period)]={'parents':len(rows),'eligible100':sum(r['eligible_in_100']>0 for r in rows),
                             'eligible1000':sum(r['eligible_in_1000']>0 for r in rows)}
    assert bins['100']==55 and bins['1000']==113
    return {'experiment':139,'contract':{'kernel':'Exp104/108 exact 60-window 3-phase rot-left mutual modulation',
      'phase':0,'control_candidate_seed':'3000000 + parent_id*300000 + zero_based_attempt',
      'matching_horizon':500,'max_attempts':1000,
      'eligibility':'same autonomous period, exact cycle-union support positions, phase0 occupied sites',
      'future_intervention_outcomes_used':False,'independence':'one 130-parent original G0 catalog, not 130000 independent parents'},
      'summary':{'G0_parents':130,'proposals_total':130000,'matched100':55,'matched1000':113,
                 'newly_matched':58,'still_unmatched':17,'total_accepted_100':87,'total_accepted_1000':970,
                 'budget_cumulative_matches':bins,'period_strata':strata,
                 'still_unmatched_parent_ids':[r['parent_id'] for r in census if not r['eligible_in_1000']]},
      'parent_records':census}
if __name__=='__main__':
    res=assay();p=HERE/'results/default.json';p.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
    (HERE/'results/default.txt').write_text(json.dumps(res['summary'],indent=2,sort_keys=True)+'\n')
    print(json.dumps(res['summary'],indent=2,sort_keys=True))
