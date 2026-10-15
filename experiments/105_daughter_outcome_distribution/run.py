#!/usr/bin/env python3
"""Experiment 105: parent-clustered daughter outcome distribution.

Controls preserve occupied positions and injection protocol. Each randomly
valued compact frame is kept fixed across its 30 material perturbations.
A timeout is CENSORED, not a failure or evidence of no offspring.
"""
import argparse
import importlib.util
import random
import statistics
from collections import Counter
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "104_single_window_fission_audit" / "run.py"
spec = importlib.util.spec_from_file_location("exp104", SOURCE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
CATS = ("strict_fission", "fragmented_not_independent",
        "active_connected", "static", "timeout")

def one_parent(idx, frame, info, direction, nulls):
    union = bytes(int(i in info["support"]) for i in range(m.SIZE))
    positions = [m.boundary(union, side) for side in ("left", "right")]
    assert all(frame[p] == 0 for p in positions)
    arms = [frame]
    for rep in range(nulls):
        rng = random.Random(105_000_001 + idx * 1021 + rep * 53)
        arms.append(bytes(rng.randrange(1, 16) if v else 0 for v in frame))
    rows = []
    for arm in arms:
        counts = Counter()
        num_daughters = 0
        for p in positions:
            for raw in range(1, 16):
                label, n, _, _ = m.evaluate(arm, p, raw, direction)
                counts[label] += 1
                if label == "strict_fission":
                    num_daughters += n
        rows.append((counts, num_daughters))
    return rows

def assay(direction, nulls, max_ticks):
    original = m.orbit
    def finite_orbit(*args, **kwargs):
        kwargs.setdefault("max_ticks", max_ticks)
        return original(*args, **kwargs)
    m.orbit = finite_orbit
    try:
        groups = [one_parent(i, frame, info, direction, nulls)
                  for i, (_, frame, info) in enumerate(m.parents(direction))]
    finally:
        m.orbit = original
    return groups

def total(groups, replicate):
    counts = Counter()
    for parent in groups:
        counts.update(parent[replicate][0])
    return counts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--direction", choices=("left", "right"), default="left")
    ap.add_argument("--nulls", type=int, default=2)
    ap.add_argument("--max-ticks", type=int, default=500)
    args = ap.parse_args()
    groups = assay(args.direction, args.nulls, args.max_ticks)
    actual = total(groups, 0)
    controls = [total(groups, j) for j in range(1, args.nulls + 1)]
    print(f"direction={args.direction} parents={len(groups)} material_conditions_per_parent=30 max_ticks={args.max_ticks} null_replicates={args.nulls}")
    print("category_order=" + ",".join(CATS))
    print("actual=" + ",".join(str(actual[c]) for c in CATS))
    for j, item in enumerate(controls, 1):
        print(f"null_{j}=" + ",".join(str(item[c]) for c in CATS))
    for c in CATS:
        counts = [item[c] for item in controls]
        print(f"category={c} actual={actual[c]} null_mean={statistics.mean(counts):.3f} null_min={min(counts)} null_max={max(counts)}")
    for c in ("strict_fission", "active_connected", "timeout"):
        diffs = [p[0][0][c] -
                 statistics.mean(p[j][0][c] for j in range(1, args.nulls + 1))
                 for p in groups]
        print(f"parent_level category={c} mean_diff={statistics.mean(diffs):.6f} positive={sum(x>0 for x in diffs)} negative={sum(x<0 for x in diffs)} tie={sum(x==0 for x in diffs)}")
    observed = [actual[c] / (len(groups)*30) for c in CATS]
    expected = [statistics.mean(item[c] for item in controls)/(len(groups)*30)
                for c in CATS]
    tv = sum(abs(x-y) for x, y in zip(observed, expected))/2
    print(f"total_variation_between_pooled_outcome_distributions={tv:.6f}")
    actual_daughters = sum(p[0][1] for p in groups)
    control_daughters = [sum(p[j][1] for p in groups)
                         for j in range(1, args.nulls + 1)]
    print(f"daughters_actual={actual_daughters} daughters_null_replicates={control_daughters}")

if __name__ == "__main__":
    main()
