#!/usr/bin/env python3
"""Frozen-data and physical-null invariants for Experiment 113."""
import importlib.util
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('exp113', ROOT / 'run.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def main():
    assert e.m.SIZE == 60 and e.m.CENTER == 30 and e.m.CENTER % 3 == 0
    assert e.physical_features(bytes(60)) == (0, 0, 0)
    archive = json.loads((ROOT/'results/default.json').read_text(encoding='utf-8'))
    assert archive['experiment'] == 113
    assert archive['inventory']['matched_parents'] == 20
    assert archive['inventory']['informative_parents'] == 8
    assert len(archive['patch_records']) == 71
    assert e.analyze(archive['patch_records']) == archive['summary']
    for w, n in ((1, (35, 34, 31, 23, 23)), (2, (16,16,16,14,14)),
                 (3,(20,20,20,20,20))):
        assert tuple(archive['inventory'].get(f'width{w}_{key}',0) for key in
                     ('g0_mask_eligible','mask_eligible','popcount_eligible',
                      'pop_and_eligible','pop_and_flips_eligible')) == n
    for q in archive['patch_records']:
        sizes = [q['pool_sizes'][tier] for tier in e.TIERS]
        assert sizes == sorted(sizes,reverse=True)
        assert all(q['eligible'][key] == (q['pool_sizes'][key] > 0) for key in e.TIERS)
        for tier in e.TIERS:
            if q['eligible'][tier] and q['informative_probes']:
                assert 0 <= q['null_expected_confirmed'][tier] <= q['informative_probes']
                assert 0 <= q['null_censored_microstates'][tier] <= q['pool_sizes'][tier] * q['informative_probes']
    # Verify the nested conditions, nonzero occupancy, changed positions,
    # and exact-donor-value exclusion on at least one real on-cycle pair.
    ref = e.r.decode_archive(json.loads((ROOT.parent/'112_probe_discrimination_audit'/'results/default.json').read_text()))
    p=ref['parent_records'][0]
    parents=list(e.m.parents('left'))
    pid=p['parent_id']
    _, donor, original=parents[pid]
    match=e.e.v.matched_control(pid,donor,original,100)
    ctrl=match[0]
    mask=e.e.first_mask(ctrl)
    assert e.e.first_mask(donor)==mask
    checked=False
    for width in (1,2,3):
        for patch in e.e.changed_patches(donor,ctrl,original['support'],width):
            transplant=e.e.replace(ctrl,donor,patch)
            if e.e.first_mask(transplant)!=mask:continue
            g0feat=e.physical_features(transplant)
            pool=[(s,e.physical_features(s)) for s in e.unique_mask_pool(ctrl,donor,patch,mask)]
            matched=e.conditions(pool,g0feat)
            assert all(s[i] in range(1,16) and s[i]!=ctrl[i] for s,_ in pool for i in patch)
            assert all(any(s[i]!=donor[i] for i in patch) for s,_ in pool)
            assert all(e.e.first_mask(s)==mask for s,_ in pool)
            assert all(e.physical_features(s)[:k]==g0feat[:k] for tier,k in
                       (('popcount',1),('pop_and',2),('pop_and_flips',3)) for s in matched[tier])
            checked=True
            break
        if checked:break
    assert checked
    print('exp113 smoke: PASS')

if __name__=='__main__':main()
