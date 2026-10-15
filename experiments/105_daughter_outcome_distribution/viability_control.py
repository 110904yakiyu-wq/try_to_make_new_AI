#!/usr/bin/env python3
"""An exploratory support-matched control conditional on *prior* viability.

Select a randomized compact frame if it forms a localized active cycle
WITHOUT material injection. The outcome is never used for selection.
This is not phase/cycle-geometry matched and is not a causal fertility assay.
"""
import importlib.util
import random
import statistics
from collections import Counter
from pathlib import Path

base = Path(__file__).with_name("run.py")
spec = importlib.util.spec_from_file_location("exp105", base)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
m = v.m

def main():
    original = m.orbit
    def finite_orbit(*args, **kw):
        kw.setdefault("max_ticks", 500)
        return original(*args, **kw)
    m.orbit = finite_orbit
    matched = []
    periods = []
    supports = []
    for index, (pair, frame, info) in enumerate(m.parents("left")):
        accepted = None
        for attempt in range(12):
            rng = random.Random(2_000_000 + index*10_000 + attempt)
            candidate = bytes(rng.randrange(1,16) if value else 0 for value in frame)
            r = m.orbit(candidate, phase=0, direction="left")
            if r["status"] == "cycle" and r["active"] and len(r["support"]) <= 13:
                accepted = candidate
                periods.append(r["period"])
                supports.append(len(r["support"]))
                break
        if accepted is None:
            continue
        union = bytes(int(i in info["support"]) for i in range(m.SIZE))
        positions = [m.boundary(union, side) for side in ("left", "right")]
        rows = []
        for current in (frame, accepted):
            counts = Counter()
            daughters = 0
            for pos in positions:
                for raw in range(1, 16):
                    label, n, _, _ = m.evaluate(current, pos, raw, "left")
                    counts[label] += 1
                    if label == "strict_fission":
                        daughters += n
            rows.append((counts, daughters))
        matched.append(rows)

    print(f"parents_total=130 parents_matched={len(matched)} parents_no_viable_null={130-len(matched)} attempts_per_parent=12")
    print("selection_without_material_test=yes")
    print(f"viable_null_period_median={statistics.median(periods)} support_median={statistics.median(supports)}")
    print("categories=" + ",".join(v.CATS))
    for name, arm in (("actual_matched", 0), ("viability_control", 1)):
        print(name + "=" + ",".join(str(sum(rows[arm][0][cat] for rows in matched))
                                   for cat in v.CATS))
    for cat in ("strict_fission", "active_connected", "timeout"):
        differences = [rows[0][0][cat] - rows[1][0][cat] for rows in matched]
        print(f"parent_diff {cat} greater={sum(x>0 for x in differences)} lower={sum(x<0 for x in differences)} ties={sum(x==0 for x in differences)} mean={statistics.mean(differences):.6f}")
    print("daughters actual=", sum(rows[0][1] for rows in matched),
          "control=",sum(rows[1][1] for rows in matched))

if __name__ == "__main__":
    main()
