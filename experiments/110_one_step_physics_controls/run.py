#!/usr/bin/env python3
"""Experiment 110: one-step physical feature conditioning on Experiment 108 pairs.

Feature-stratified descriptive audit only. No matching model, causal
identification, or multiple-comparison-corrected claim is made.
"""
import importlib.util
import statistics
from pathlib import Path

BASE=Path(__file__).resolve().parents[1] / "108_cycle_union_geometry_match" / "run.py"
spec=importlib.util.spec_from_file_location("exp108",BASE)
v=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
m=v.m

def feature(frame):
    n=len(frame)
    before=bytes(frame)
    after=m.step(before, 0, "left")
    changed=frozenset(i for i,(a,b) in enumerate(zip(before,after)) if a!=b)
    return {
        "snapshot_popcount":sum(x.bit_count() for x in before),
        "adjacent_AND_popcount":sum((before[i]&before[(i+1)%n]).bit_count() for i in range(n)),
        "first_tick_hamming_flips":sum((a^b).bit_count() for a,b in zip(before,after)),
        "first_tick_changed_triples":sum(
            any(before[(j+k)%n]!=after[(j+k)%n] for k in range(3))
            for j in range(0,n,3)),
        "first_tick_exact_changed_sites":changed,
    }

def main():
    original=m.orbit
    def bounded(*args, **kw):
        kw.setdefault("max_ticks",500)
        return original(*args,**kw)
    m.orbit=bounded
    records=[]
    for index,(_,frame,parent) in enumerate(m.parents("left")):
        ctrl=v.matched_control(index,frame,parent,100)
        if ctrl is None: continue
        fake,_,_=ctrl
        ca,_=v.v.outcomes(frame,parent)
        cb,_=v.v.outcomes(fake,ctrl[1])
        records.append((ca["active_connected"]-cb["active_connected"],feature(frame),feature(fake)))
    print(f"matched_pairs={len(records)} snapshot_phase=0 outcome_horizon=500")
    for name in feature(bytes(m.SIZE)).keys():
        vals=[d for d,left,right in records if left[name]==right[name]]
        print(f"{name} equal_pairs={len(vals)} G0_higher={sum(d>0 for d in vals)} control_higher={sum(d<0 for d in vals)} tie={sum(d==0 for d in vals)} mean_connected_diff={statistics.mean(vals) if vals else float('nan'):.6f}")
    print("NOTE exploratory conditioning on one feature at a time; no causal attribution")

if __name__=="__main__":
    main()
