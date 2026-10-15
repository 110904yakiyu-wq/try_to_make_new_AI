#!/usr/bin/env python3
"""Phase-0 on-cycle support-randomized control, pre-intervention selection only."""
import importlib.util
import random
import statistics
from collections import Counter
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "104_single_window_fission_audit" / "run.py"
spec = importlib.util.spec_from_file_location("exp104", SOURCE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
CAT = ("strict_fission", "fragmented_not_independent",
       "active_connected", "static", "timeout")

def choose_control(index, frame, attempts=12):
    for attempt in range(attempts):
        rng = random.Random(2_000_000 + index * 10_000 + attempt)
        fake = bytes(rng.randrange(1, 16) if value else 0 for value in frame)
        result = m.orbit(fake, phase=0, direction="left")
        if result["status"] != "cycle" or not result["active"] or len(result["support"]) > 13:
            continue
        candidates = [f for j, f in enumerate(result["cycle"])
                      if (result["phase"] + j) % 3 == 0]
        return max(candidates, key=lambda f: sum(bool(x) for x in f)), result
    return None

def outcomes(frame, result):
    union = bytes(int(i in result["support"]) for i in range(m.SIZE))
    positions = [m.boundary(union, side) for side in ("left", "right")]
    assert all(frame[p] == 0 for p in positions)
    counts = Counter()
    daughters = 0
    for pos in positions:
        for raw in range(1, 16):
            label, n, _, _ = m.evaluate(frame, pos, raw, "left")
            counts[label] += 1
            if label == "strict_fission":
                daughters += n
    return counts, daughters

def main():
    original = m.orbit
    def limit(*a, **k):
        k.setdefault("max_ticks", 500)
        return original(*a, **k)
    m.orbit = limit
    matched = []
    geometry = Counter()
    for index, (_, frame, parent) in enumerate(m.parents("left")):
        accepted = choose_control(index, frame)
        if accepted is None:
            continue
        fake, control = accepted
        geometry[(parent["period"] == control["period"],
                  len(parent["support"]) == len(control["support"]))] += 1
        matched.append((outcomes(frame, parent), outcomes(fake, control)))
    print(f"eligible_parent_pairs={len(matched)}/130 preintervention_selection=yes matched_phase0=yes")
    print("geometry_matches(period_equal,support_size_equal)=" + str(dict(sorted(geometry.items()))))
    print("category_order=" + ",".join(CAT))
    for label, side in (("actual", 0), ("oncycle_control", 1)):
        print(label + "=" + ",".join(str(sum(row[side][0][c] for row in matched)) for c in CAT))
        print(label + "_daughters=" + str(sum(row[side][1] for row in matched)))
    for c in ("strict_fission", "active_connected", "timeout"):
        diff = [row[0][0][c] - row[1][0][c] for row in matched]
        print(f"paired {c} actual_higher={sum(x>0 for x in diff)} control_higher={sum(x<0 for x in diff)} tie={sum(x==0 for x in diff)} mean={statistics.mean(diff):.6f}")

if __name__ == "__main__":
    main()
