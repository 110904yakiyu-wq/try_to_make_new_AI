#!/usr/bin/env python3
"""Exp159: exact-state equivalence of LR/RL history and heldout XOR responses."""
import argparse,csv,importlib.util,json,statistics
from pathlib import Path
from collections import defaultdict
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
s=importlib.util.spec_from_file_location('exp157',ROOT/'157_boundary_xor_multiepisode_gain_gate'/'run.py')
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)


def assay(source=None):
    src=Path(source or ROOT/'157_boundary_xor_multiepisode_gain_gate'/'results/default.json')
    old=json.loads(src.read_text()); assert old['experiment']==157
    contexts=old['contexts'];parents=list(v.m.parents());assert len(parents)==130
    bypid=defaultdict(list)
    for row in contexts: bypid[row['parent_id']].append(row)
    with (src.parent/'probes.csv').open(newline='') as f:
        records=list(csv.DictReader(f))
    result=[]
    for pid,rows in sorted(bypid.items()):
        if not all(row['feasible']['LR'] and row['feasible']['RL'] for row in rows):continue
        seed,frame,o=parents[pid]
        lo=(min(o['support'])-1)%60;hi=(max(o['support'])+1)%60
        x=v.v.evolve(frame,lo,hi,v.v.ARMS['LR']);y=v.v.evolve(frame,lo,hi,v.v.ARMS['RL'])
        assert x is not None and y is not None
        hamming=sum((a^b).bit_count() for a,b in zip(x,y))
        different_windows=sum(a!=b for a,b in zip(x,y))
        response_lr={(int(r['test_side']),int(r['test_mask'])):r for r in records if int(r['parent_id'])==pid and r['arm']=='LR'}
        response_rl={(int(r['test_side']),int(r['test_mask'])):r for r in records if int(r['parent_id'])==pid and r['arm']=='RL'}
        assert set(response_lr)==set(response_rl)=={(side,mask) for side in (0,1) for mask in v.MASKS}
        mismatches=sum(any(response_lr[k][f]!=response_rl[k][f] for f in
                           ('union_affected_sites','reached_10','reached_30','instant_affected_t1',
                            'instant_affected_t3','instant_affected_t6','instant_affected_t24','instant_affected_t60'))
                       for k in response_lr)
        diff=statistics.mean(int(response_lr[k]['union_affected_sites'])-int(response_rl[k]['union_affected_sites']) for k in response_lr)
        assert hamming!=0 or mismatches==0
        result.append({'parent_id':pid,'seed':list(seed),'same_full_microstate':x==y,
                       'raw_hamming_bits':hamming,'changed_windows':different_windows,
                       'heldout_XOR_mismatching_probes':mismatches,'num_heldout_probes':8,
                       'mean_LR_minus_RL_affected_sites':diff})
    exact=[x for x in result if x['same_full_microstate']]
    unequal=[x for x in result if not x['same_full_microstate']]
    return {'experiment':159,'protocol':{'physics':'frozen 104/139 phase0 three-phase local deterministic Markov rule',
       'history_pair':'exactly one raw7 left and raw11 right at t0/t24, order exchanged, both compare at t96 phase0',
       'selection':'both externally scheduled raw pulses must obey empty-site material insertion contract',
       'heldout':'eight XOR probes: original support left/right boundaries x masks1,2,4,8 (Exp157 frozen)',
       'inference':'equal complete microstate and scheduler phase imply identical future; differing order responses do not imply learned memory'},
       'inventory':{'original_parents':130,'both_orders_feasible_parents':len(result),'same_current_state_parents':len(exact),
                   'different_current_state_parents':len(unequal)},
       'summary':{'same_current_state_probes_identical':sum(x['heldout_XOR_mismatching_probes']==0 for x in exact),
           'same_current_state_probe_records':8*len(exact),
           'unequal_current_state_parents_with_response_difference':sum(x['heldout_XOR_mismatching_probes']>0 for x in unequal),
           'mean_bit_distance_if_unequal':statistics.mean(x['raw_hamming_bits'] for x in unequal) if unequal else None,
           'mean_LR_minus_RL_affected_sites':statistics.mean(x['mean_LR_minus_RL_affected_sites'] for x in result) if result else None,
           'order_LR_greater':sum(x['mean_LR_minus_RL_affected_sites']>0 for x in result),
           'order_RL_greater':sum(x['mean_LR_minus_RL_affected_sites']<0 for x in result),
           'order_tied':sum(x['mean_LR_minus_RL_affected_sites']==0 for x in result)},
       'parent_records':result}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'results/default.json')
    a=ap.parse_args();result=assay();a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'inventory':result['inventory'],'summary':result['summary']},sort_keys=True,indent=2))

if __name__=='__main__':main()
