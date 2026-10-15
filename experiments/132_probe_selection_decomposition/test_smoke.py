#!/usr/bin/env python3
"""Independent fixed-cohort decomposition invariants for Experiment 132."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'results/default.json').read_text())
assert r['experiment']==132
for tier,p,e,u in [('all',55,1650,0),('popcount',15,450,0),('pop_and',14,168,252),('pop_and_flips',10,126,174),('first_changed_mask',6,102,78)]:
    a=r['decomposition'][tier]
    assert a['eligible_parents']==p
    sub=a['components']; assert sub['feature_eligible_probes']['probes']==e
    assert sub['same_parents_feature_ineligible_probes']['probes']==u
    for k in (10,20,30,40,50,60):
        parent=sub['same_eligible_parents_all_30']['by_threshold'][str(k)]['pooled']
        pos=sub['feature_eligible_probes']['by_threshold'][str(k)]['pooled']
        neg=sub['same_parents_feature_ineligible_probes']['by_threshold'][str(k)]['pooled']
        if neg:
            for bound in ('lower_fraction','upper_fraction'):
                assert abs(parent[bound]-(e*pos[bound]+u*neg[bound])/(e+u))<1e-12
assert r['decomposition']['first_changed_mask']['components']['feature_eligible_probes']['by_threshold']['10']['pooled']['g0']['yes']==23
assert r['decomposition']['first_changed_mask']['components']['same_parents_feature_ineligible_probes']['by_threshold']['10']['pooled']['control']['yes']==26
print('exp132 smoke: PASS')
