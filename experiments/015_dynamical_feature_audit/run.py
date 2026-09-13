#!/usr/bin/env python3
import argparse
import importlib.util
import math
import random
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
    return math.sqrt(sum(x*x for x in values))


def step_int(state, rule, size):
    mask = (1 << size) - 1
    left = ((state << 1) & mask) | (state >> (size - 1))
    right = (state >> 1) | ((state & 1) << (size - 1))
    center = state
    not_left = (~left) & mask
    not_center = (~center) & mask
    not_right = (~right) & mask

    out = 0
    for index in range(8):
        if not ((rule >> index) & 1):
            continue
        l = (index >> 2) & 1
        c = (index >> 1) & 1
        r = index & 1
        out |= (
            (left if l else not_left)
            & (center if c else not_center)
            & (right if r else not_right)
        )
    return out


def evolve_int(state, rule, size, steps):
    for _ in range(steps):
        state = step_int(state, rule, size)
    return state


def dynamical_metrics(rule, size, horizon, trials, seed, separation):
    rng = random.Random(seed)
    final_sum = peak_sum = auc_sum = radius_sum = survival_sum = 0.0
    interaction_sum = 0.0

    for _ in range(trials):
        initial = rng.getrandbits(size)
        p = rng.randrange(size)
        q = (p + separation) % size

        a = initial
        b = initial ^ (1 << p)
        auc = peak = max_radius = 0

        for _ in range(horizon):
            a = step_int(a, rule, size)
            b = step_int(b, rule, size)
            damage = a ^ b
            mass = damage.bit_count()
            auc += mass
            peak = max(peak, mass)

            bits = damage
            while bits:
                one = bits & -bits
                i = one.bit_length() - 1
                distance = abs(i - p)
                distance = min(distance, size - distance)
                max_radius = max(max_radius, distance)
                bits -= one

        final = (a ^ b).bit_count()
        final_sum += final
        peak_sum += peak
        auc_sum += auc
        radius_sum += max_radius
        survival_sum += final > 0

        f0 = evolve_int(initial, rule, size, horizon)
        fp = evolve_int(initial ^ (1 << p), rule, size, horizon)
        fq = evolve_int(initial ^ (1 << q), rule, size, horizon)
        fpq = evolve_int(initial ^ (1 << p) ^ (1 << q), rule, size, horizon)
        interaction_sum += (fpq ^ fp ^ fq ^ f0).bit_count() / size

    return {
        "final": final_sum / trials,
        "peak": peak_sum / trials,
        "auc": auc_sum / trials,
        "radius": radius_sum / trials,
        "survival": survival_sum / trials,
        "interaction": interaction_sum / trials,
    }


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

    parser = argparse.ArgumentParser(description="Experiment 015: dynamical-feature audit.")
    parser.add_argument("--assay-size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--offset", type=int, default=20)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--a", type=int, default=0b011)
    parser.add_argument("--b", type=int, default=0b101)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=48)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--damage-size", type=int, default=128)
    parser.add_argument("--damage-horizon", type=int, default=32)
    parser.add_argument("--damage-trials", type=int, default=32)
    parser.add_argument("--interaction-separation", type=int, default=7)
    parser.add_argument("--seed", type=int, default=12345)
    args = parser.parse_args()

    single = exp4.parse_schedule(args.single_schedule)
    repeat = exp4.parse_schedule(args.repeat_schedule)

    rows = []
    for rule in range(256):
        delta_single = exp7.probe_profile(
            exp4, base, rule, args.offset, single, args.assay_size,
            args.position_stride, args.probe_time, args.probe_steps,
            args.a, args.b, args.core_width,
        )
        delta_repeat = exp7.probe_profile(
            exp4, base, rule, args.offset, repeat, args.assay_size,
            args.position_stride, args.probe_time, args.probe_steps,
            args.a, args.b, args.core_width,
        )
        gains = [r - s for s, r in zip(delta_single, delta_repeat)]
        untrained = [g for i, g in enumerate(gains) if i not in (args.a, args.b)]
        metrics = dynamical_metrics(
            rule, args.damage_size, args.damage_horizon, args.damage_trials,
            args.seed, args.interaction_separation,
        )
        rows.append((l2(untrained), metrics))

    scores = [score for score, _ in rows]
    print("metric  pearson  spearman")
    for key in ("final", "peak", "auc", "radius", "survival", "interaction"):
        values = [metrics[key] for _, metrics in rows]
        print(f"{key:<12}  {pearson(values, scores):+.6f}  {spearman(values, scores):+.6f}")


if __name__ == "__main__":
    main()
