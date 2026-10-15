#!/usr/bin/env python3
"""Cycle-union geometry and phase-zero occupancy matched G0 persistence audit."""
import argparse, importlib.util, random, statistics
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "106_on_cycle_control" / "run.py"
spec = importlib.util.spec_from_file_location("exp106", BASE)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
m = v.m

def matched_control(index, frame, parent, attempts):
    for attempt in range(attempts):
        rng = random.Random(3_000_000 + index * 300_000 + attempt)
        candidate = bytes(rng.randrange(1, 16) if x else 0 for x in frame)
        r = m.orbit(candidate, phase=0, direction="left")
        if r["status"] != "cycle" or not r["active"]:
            continue
        if r["period"] != parent["period"] or r["support"] != parent["support"]:
            continue
        phase0 = [f for j, f in enumerate(r["cycle"])
                  if (r["phase"] + j) % 3 == 0]
        control_frame = max(phase0, key=lambda f: sum(bool(x) for x in f))
        if any(bool(a) != bool(b) for a, b in zip(frame, control_frame)):
            continue
        return control_frame, r, attempt + 1
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--attempts", type=int, default=100)
    ap.add_argument("--max-ticks", type=int, default=500)
    args = ap.parse_args()
    original = m.orbit
    def bounded(*a, **kw):
        kw.setdefault("max_ticks", args.max_ticks)
        return original(*a, **kw)
    m.orbit = bounded

    aggregate = [Counter(), Counter()]
    per_parent = []
    accepted_attempts = []
    total = 0
    for index, (pair, frame, parent) in enumerate(m.parents("left")):
        total += 1
        control = matched_control(index, frame, parent, args.attempts)
        if control is None:
            continue
        fake, control_orbit, nth = control
        assert control_orbit["period"] == parent["period"]
        assert control_orbit["support"] == parent["support"]
        assert all(bool(x) == bool(y) for x, y in zip(frame, fake))
        actual, actual_children = v.outcomes(frame, parent)
        null, null_children = v.outcomes(fake, control_orbit)
        aggregate[0].update(actual)
        aggregate[1].update(null)
        accepted_attempts.append(nth)
        per_parent.append((actual, null, actual_children, null_children))

    print(f"matched={len(per_parent)}/{total} attempts={args.attempts} horizon={args.max_ticks}")
    print("matching=period+exact_cycle_union_support+phase0_occupancy+phase0_scheduler")
    print("category_order=" + ",".join(v.CAT))
    for name, ix in (("G0", 0), ("control", 1)):
        print(name+"="+",".join(str(aggregate[ix][c]) for c in v.CAT))
        print(name+"_daughters="+str(sum(p[2+ix] for p in per_parent)))
    for cat in ("strict_fission", "active_connected", "timeout"):
        diffs = [p[0][cat] - p[1][cat] for p in per_parent]
        print(f"{cat} G0_higher={sum(x>0 for x in diffs)} null_higher={sum(x<0 for x in diffs)} tie={sum(x==0 for x in diffs)} mean_diff_per_parent={statistics.mean(diffs) if diffs else 0:.6f}")
    print("accepted_attempt_median="+str(statistics.median(accepted_attempts) if accepted_attempts else None))

if __name__=="__main__":
    main()
