"""Non-outcome causal eligibility gate census, first failure classified."""
import csv,json,sys
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'139_extended_control_budget'))
import core
GATES={0:'right_censored_500',1:'autonomous_static',2:'wrong_period',3:'wrong_cycle_union_support',4:'wrong_phase0_occupancy',5:'accepted'}

def assay(path=HERE/'results/gates.csv',accepted=HERE.parent/'139_extended_control_budget/results/accepted.csv'):
    par=list(core.parents());assert len(par)==130
    with open(path,newline='') as f:raw=list(csv.DictReader(f))
    assert len(raw)==130000
    accepted_139={(int(q['parent_id']),int(q['attempt'])) for q in csv.DictReader(open(accepted,newline=''))}
    actual={(int(q['parent_id']),int(q['attempt'])) for q in raw if int(q['gate'])==5}
    assert accepted_139==actual and len(actual)==970
    groups=defaultdict(Counter);allgate=Counter();per=[]
    for i in range(130):
        sub=Counter(int(q['gate']) for q in raw if int(q['parent_id'])==i)
        assert sum(sub.values())==1000
        allgate.update(sub)
        groups[par[i][2]['period']].update(sub)
        per.append({'parent_id':i,'period':par[i][2]['period'],'support_size':len(par[i][2]['support']),
                    'accepted_candidates':sub[5],**{GATES[k]:sub[k] for k in sorted(GATES)}})
    summary={'total_attempts':len(raw),'gates':{GATES[k]:allgate[k] for k in sorted(GATES)},
      'by_period':{str(p):{'parents':sum(q['period']==p for q in per),**{GATES[k]:count[k] for k in sorted(GATES)}} for p,count in sorted(groups.items())},
      'still_unmatched_1000':[q for q in per if not q['accepted_candidates']]}
    return {'experiment':141,'contract':{'source':'same 130000 pre-response 500tick autonomous candidates as Exp139',
      'failure_order':'unresolved, static, period mismatch, cycle support mismatch, phase0 occupancy mismatch, accepted',
      'important':'candidate non-convergence by500 is censored; not proof that its autonomous cycle differs',
      'sample':'130 parent clusters, same 1000 deterministic proposals per parent'},'summary':summary,'parent_records':per}
if __name__=='__main__':
    r=assay();(HERE/'results/default.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');
    (HERE/'results/default.txt').write_text(json.dumps(r['summary'],indent=2,sort_keys=True)+'\n');
    print(json.dumps(r['summary']['gates'],indent=2))
