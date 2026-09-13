#!/usr/bin/env python3
import argparse
import importlib.util
import math
from pathlib import Path
from types import SimpleNamespace


def load_exp009():
    path = Path(__file__).resolve().parents[1] / "009_low_dimensional_modes" / "run.py"
    spec = importlib.util.spec_from_file_location("exp009", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def covariance(exp9, matrix):
    centered = exp9.centered_rows(matrix)
    return exp9.gram_xtx(centered)


def frobenius_cosine(a, b):
    dot = 0.0
    aa = 0.0
    bb = 0.0
    for i in range(len(a)):
        for j in range(len(a[i])):
            dot += a[i][j] * b[i][j]
            aa += a[i][j] * a[i][j]
            bb += b[i][j] * b[i][j]
    if aa == 0.0 or bb == 0.0:
        return 0.0
    return dot / math.sqrt(aa * bb)


def build_args(base, offset, probe_time):
    return SimpleNamespace(
        rule=base.rule,
        size=base.size,
        position_stride=base.position_stride,
        offset=offset,
        core_width=base.core_width,
        single_schedule=base.single_schedule,
        repeat_schedule=base.repeat_schedule,
        probe_time=probe_time,
        probe_steps=base.probe_steps,
    )


def main():
    exp9 = load_exp009()
    exp7 = exp9.load_exp007()
    exp4 = exp7.load_exp004()
    base_ca = exp4.load_exp000()

    parser = argparse.ArgumentParser(
        description="Experiment 010: cross-condition response-mode comparison."
    )
    parser.add_argument("--rule", type=int, default=129)
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-steps", type=int, default=8)
    args = parser.parse_args()

    conditions = [
        ("baseline", 20, 48),
        ("offset12_t48", 12, 48),
        ("offset20_t40", 20, 40),
        ("offset20_t56", 20, 56),
    ]

    matrices = {}
    covariances = {}
    top2 = {}

    print("condition      offset  probe_time  top2_explained")
    for name, offset, probe_time in conditions:
        local_args = build_args(args, offset, probe_time)
        matrix = exp9.geometry_matrix(exp7, exp4, base_ca, local_args)
        matrices[name] = matrix
        covariances[name] = covariance(exp9, matrix)
        ratios = exp9.explained_variance(matrix)
        top2[name] = sum(ratios[:2])
        print(f"{name:<14} {offset:>6}  {probe_time:>10}  {top2[name]:.9f}")

    print()
    names = [name for name, _, _ in conditions]
    print("pairwise covariance Frobenius cosine")
    print("condition       " + "  ".join(f"{name:>14}" for name in names))
    for a in names:
        values = [
            frobenius_cosine(covariances[a], covariances[b])
            for b in names
        ]
        print(f"{a:<14} " + "  ".join(f"{value:>14.9f}" for value in values))


if __name__ == "__main__":
    main()
