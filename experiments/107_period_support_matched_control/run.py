#!/usr/bin/env python3
"""Preintervention period/support-matched on-cycle comparison.

The independent randomized control is selected only by autonomous period
and cycle-union support size. Optional stronger filter also requires exact
phase-zero occupied positions. Censoring is always reported separately.
"""
import argparse
import importlib.util
import random
import statistics
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "106_on_cycle_control" / "run.py"
spec = importlib.util.spec_from_file_location("exp106", BASE)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
m = v.m

def select(index, frame, parent, attempts):
    for attempt in range(attempts):
        rng = random.Random(3_000_000 + index * 300_000 + attempt)
        candidate = bytes(rng.randrange(1, 16) if x else 0 for x in frame)
        r = m.orbit(candidate, phase=0, direction="left")
        if (r["status"] == "cycle" and r["active"]
            and r["period"] == parent["period"]
            and len(r["support"]) == len(parent["support"])):
            frames = [f for j, f in enumerate(r["cycle"])
                      if (r["phase"] + j) % 3 == 0]
            return max(frames, key=lambda f: sum(bool(x) for x in f)), r, attempt+1
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--attempts", type=int, default=100)
    ap.add_argument("--exact-phase0-occupancy", action="store_true")
    args = ap.parse_args()
    original = m.orbit
    def limited(*a, **kw):
        kw.setdefault("max_ticks", 500)
        return original(*a, **kw)
    m.orbit = limited
    pairs = []
    identical = 0
    for index, (_, frame, parent) in enumerate(m.parents("left")):
        accepted = select(index, frame, parent, args.attempts)
        if accepted is None:
            continue
        fake, control, attempt = accepted
        same = tuple(i for i in range(m.SIZE) if frame[i]) == tuple(
            i for i in range(m.SIZE) if fake[i])
        if args.exact_phase0_occupancy and not same:
            continue
        identical += int(same)
        pairs.append((v.outcomes(frame, parent), v.outcomes(fake, control), attempt))

    print(f"eligible={len(pairs)}/130 search_attempts={args.attempts} matched_period=yes matched_union_support_size=yes matched_phase0=yes" +
          (" exact_phase0_occupancy=yes" if args.exact_phase0_occupancy else ""))
    print(f"identical_occupied_positions={identical}")
    print("attempts_median=" + str(statistics.median(p[2] for p in pairs) if pairs else None))
    print("categories=" + ",".join(v.CAT))
    for name, idx in (("actual", 0), ("control", 1)):
        print(name + "=" + ",".join(str(sum(p[idx][0][c] for p in pairs)) for c in v.CAT))
        print(name + "_daughters=" + str(sum(p[idx][1] for p in pairs)))
    for c in ("strict_fission", "active_connected", "timeout"):
        diffs = [p[0][0][c] - p[1][0][c] for p in pairs]
        print(f"paired {c} actual_higher={sum(x>0 for x in diffs)} control_higher={sum(x<0 for x in diffs)} tie={sum(x==0 for x in diffs)} mean={statistics.mean(diffs) if diffs else 0:.6f}")

if __name__ == "__main__":
    main()
