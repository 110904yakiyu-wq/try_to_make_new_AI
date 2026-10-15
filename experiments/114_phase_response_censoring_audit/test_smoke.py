#!/usr/bin/env python3
"""Invariants and frozen 112 regression for Experiment 114."""
import importlib.util
import json
from pathlib import Path

BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('exp114',BASE/'run.py')
e=importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def main():
    assert e.m.CENTER == 30 and e.m.SIZE == 60
    assert e.m.step(bytes(60),0,'left') == bytes(60)
    frozen=e.load_reference(BASE.parent/'112_probe_discrimination_audit/results/default.json')
    assert len(frozen['parent_records']) == 20
    # Check that frozen 108 first-accepted random controls are identical to
    # both the reconstructed direct attempt and original matching search.
    originals=list(e.m.parents('left'))
    original_orbit=e.m.orbit
    def bounded(*args,**kw):
        kw.setdefault('max_ticks',500)
        return original_orbit(*args,**kw)
    e.m.orbit=bounded
    try:
        for key in (0, 9, 19):
            row=frozen['parent_records'][key]
            pid=row['parent_id']
            _,g0,parent=originals[pid]
            direct=e.reference_control(pid,g0,parent,row['control_match_attempt'])
            selected=e.v.matched_control(pid,g0,parent,100)
            assert selected is not None
            assert selected[0] == direct and selected[2] == row['control_match_attempt']
            # One-step response mask trivially equals injection-site only at
            # t=0; at t>0 it is measured by the physical kernel, not guessed.
            assert e.changed_mask(g0,g0)==0
    finally:
        e.m.orbit=original_orbit
    path=BASE/'results/default.json'
    if path.exists():
        record=json.loads(path.read_text(encoding='utf-8'))
        s=record['summary']
        assert len(record['parent_metadata']) == 20
        assert s['horizons']['500']['aggregate']['both_resolved']==420
        assert s['horizons']['500']['aggregate']['resolved_class_disagreement']==10
        assert s['horizons']['500']['aggregate']['actual_censored']==81
        assert s['horizons']['500']['aggregate']['control_censored']==112
        assert s['delayed']['b_resolved_500_to_2000']==1
        assert s['delayed']['a_resolved_500_to_2000']==0
        assert s['early']['6']['equal_response_mask_count']==71
        assert s['equal_500_class_early_response']['6']['same_mask_count']==67
    print('exp114 smoke PASS')

if __name__=='__main__':
    main()
