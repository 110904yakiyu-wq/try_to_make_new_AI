#!/usr/bin/env python3
import argparse
import importlib.util
import math
from pathlib import Path


def load_exp007():
    path = Path(__file__).resolve().parents[1] / "007_response_geometry" / "run.py"
    spec = importlib.util.spec_from_file_location("exp007", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def l2(values):
    return math.sqrt(sum(x * x for x in values))


def rule_table(rule):
    return [(rule >> i) & 1 for i in range(8)]


def anf_degree(rule):
    coeff = rule_table(rule)
    for bit in range(3):
        for mask in range(8):
            if mask & (1 << bit):
                coeff[mask] ^= coeff[mask ^ (1 << bit)]
    degree = 0
    for mask, value in enumerate(coeff):
        if value:
            degree = max(degree, mask.bit_count())
    return degree


def permutive(rule, variable_bit):
    table = rule_table(rule)
    for mask in range(8):
        if not (mask & (1 << variable_bit)):
            if table[mask] == table[mask | (1 << variable_bit)]:
                return False
    return True


def average_sensitivity(rule):
    table = rule_table(rule)
    total = 0
    for mask in range(8):
        for bit in range(3):
            total += table[mask] != table[mask ^ (1 << bit)]
    return total / 8.0


def reflect_rule(rule):
    out = 0
    for left in (0, 1):
        for center in (0, 1):
            for right in (0, 1):
                dst = (left << 2) | (center << 1) | right
                src = (right << 2) | (center << 1) | left
                out |= ((rule >> src) & 1) << dst
    return out


def conjugate_rule(rule):
    out = 0
    for left in (0, 1):
        for center in (0, 1):
            for right in (0, 1):
                dst = (left << 2) | (center << 1) | right
                src = ((1-left) << 2) | ((1-center) << 1) | (1-right)
                out |= (1 - ((rule >> src) & 1)) << dst
    return out


def symmetry_orbit(rule):
    values = set()
    queue = [rule]
    while queue:
        value = queue.pop()
        if value in values:
            continue
        values.add(value)
        queue.extend((reflect_rule(value), conjugate_rule(value)))
    return tuple(sorted(values))


def ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        rank = (i + j - 1) / 2.0 + 1.0
        for k in range(i, j):
            out[order[k]] = rank
        i = j
    return out


def pearson(a, b):
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    da = [x - ma for x in a]
    db = [x - mb for x in b]
    va = sum(x*x for x in da)
    vb = sum(x*x for x in db)
    if va == 0.0 or vb == 0.0:
        return 0.0
    return sum(x*y for x, y in zip(da, db)) / math.sqrt(va * vb)


def spearman(a, b):
    return pearson(ranks(a), ranks(b))


def main():
    exp7 = load_exp007()
    exp4 = exp7.load_exp004()
    base = exp4.load_exp000()

    parser = argparse.ArgumentParser(description="Experiment 014: simple local-rule feature audit.")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--offset", type=int, default=20)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--a", type=int, default=0b011)
    parser.add_argument("--b", type=int, default=0b101)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=48)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--top", type=int, default=30)
    args = parser.parse_args()

    single = exp4.parse_schedule(args.single_schedule)
    repeat = exp4.parse_schedule(args.repeat_schedule)
    rows = []

    for rule in range(256):
        delta_single = exp7.probe_profile(
            exp4, base, rule, args.offset, single, args.size,
            args.position_stride, args.probe_time, args.probe_steps,
            args.a, args.b, args.core_width,
        )
        delta_repeat = exp7.probe_profile(
            exp4, base, rule, args.offset, repeat, args.size,
            args.position_stride, args.probe_time, args.probe_steps,
            args.a, args.b, args.core_width,
        )
        gains = [r - s for s, r in zip(delta_single, delta_repeat)]
        untrained = [g for i, g in enumerate(gains) if i not in (args.a, args.b)]
        rows.append({
            "rule": rule,
            "score": l2(untrained),
            "ones": rule.bit_count(),
            "balance_distance": abs(rule.bit_count() - 4),
            "degree": anf_degree(rule),
            "sensitivity": average_sensitivity(rule),
            "permutive_count": sum(permutive(rule, bit) for bit in range(3)),
            "perm_left": int(permutive(rule, 2)),
            "perm_center": int(permutive(rule, 1)),
            "perm_right": int(permutive(rule, 0)),
        })

    scores = [row["score"] for row in rows]
    features = [
        "ones", "balance_distance", "degree", "sensitivity",
        "permutive_count", "perm_left", "perm_center", "perm_right",
    ]

    print("feature  pearson  spearman")
    for feature in features:
        values = [row[feature] for row in rows]
        print(f"{feature:<17}  {pearson(values, scores):+.6f}  {spearman(values, scores):+.6f}")

    ordered = sorted(rows, key=lambda row: row["score"], reverse=True)
    top = ordered[: args.top]
    orbits = {symmetry_orbit(row["rule"]) for row in top}

    print()
    print(f"top_rules={len(top)}")
    print(f"distinct_reflection_conjugation_orbits={len(orbits)}")
    print()
    print("rule  score  ones  degree  sensitivity  permutive_count  symmetry_orbit")
    for row in top:
        orbit = ",".join(str(x) for x in symmetry_orbit(row["rule"]))
        print(
            f"{row['rule']:>4}  {row['score']:.9f}  {row['ones']:>4}  {row['degree']:>6}  "
            f"{row['sensitivity']:.2f}  {row['permutive_count']:>15}  {orbit}"
        )


if __name__ == "__main__":
    main()
