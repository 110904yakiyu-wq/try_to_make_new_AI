#!/usr/bin/env python3
import argparse
import importlib.util
import itertools
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


def centered_rows(matrix):
    cols = len(matrix[0])
    means = [sum(row[j] for row in matrix) / len(matrix) for j in range(cols)]
    return [[row[j] - means[j] for j in range(cols)] for row in matrix]


def gram_xtx(matrix):
    cols = len(matrix[0])
    out = [[0.0] * cols for _ in range(cols)]
    for row in matrix:
        for i in range(cols):
            for j in range(i, cols):
                out[i][j] += row[i] * row[j]
    for i in range(cols):
        for j in range(i):
            out[i][j] = out[j][i]
    return out


def jacobi_eigenvalues(matrix, eps=1e-14, max_iter=10000):
    a = [row[:] for row in matrix]
    n = len(a)

    for _ in range(max_iter):
        p = q = 0
        largest = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                value = abs(a[i][j])
                if value > largest:
                    largest = value
                    p, q = i, j

        if largest < eps:
            break

        app = a[p][p]
        aqq = a[q][q]
        apq = a[p][q]
        angle = 0.5 * math.atan2(2.0 * apq, aqq - app)
        c = math.cos(angle)
        s = math.sin(angle)

        for k in range(n):
            if k == p or k == q:
                continue
            akp = a[k][p]
            akq = a[k][q]
            a[k][p] = a[p][k] = c * akp - s * akq
            a[k][q] = a[q][k] = s * akp + c * akq

        a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        a[p][q] = a[q][p] = 0.0

    return sorted((max(0.0, a[i][i]) for i in range(n)), reverse=True)


def explained_variance(matrix):
    eigenvalues = jacobi_eigenvalues(gram_xtx(centered_rows(matrix)))
    total = sum(eigenvalues)
    if total == 0.0:
        return [0.0 for _ in eigenvalues]
    return [value / total for value in eigenvalues]


def geometry_matrix(exp7, exp4, base, args):
    single = exp4.parse_schedule(args.single_schedule)
    repeat = exp4.parse_schedule(args.repeat_schedule)
    patterns = list(range(1 << args.core_width))
    rows = []

    for a, b in itertools.combinations(patterns, 2):
        delta_single = exp7.probe_profile(
            exp4, base, args.rule, args.offset, single, args.size,
            args.position_stride, args.probe_time, args.probe_steps,
            a, b, args.core_width,
        )
        delta_repeat = exp7.probe_profile(
            exp4, base, args.rule, args.offset, repeat, args.size,
            args.position_stride, args.probe_time, args.probe_steps,
            a, b, args.core_width,
        )
        rows.append([r - s for s, r in zip(delta_single, delta_repeat)])

    return rows


def shuffle_null(matrix, trials, seed):
    rng = random.Random(seed)
    values = []
    for _ in range(trials):
        shuffled = []
        for row in matrix:
            copy = row[:]
            rng.shuffle(copy)
            shuffled.append(copy)
        ratios = explained_variance(shuffled)
        values.append(sum(ratios[:2]))
    values.sort()
    return values


def quantile(values, q):
    x = (len(values) - 1) * q
    lo = int(x)
    hi = min(lo + 1, len(values) - 1)
    frac = x - lo
    return values[lo] * (1.0 - frac) + values[hi] * frac


def main():
    exp7 = load_exp007()
    exp4 = exp7.load_exp004()
    base = exp4.load_exp000()

    parser = argparse.ArgumentParser(description="Experiment 009: low-dimensional response modes.")
    parser.add_argument("--rule", type=int, default=129)
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--offset", type=int, default=20)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=48)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--null-trials", type=int, default=500)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    matrix = geometry_matrix(exp7, exp4, base, args)
    ratios = explained_variance(matrix)

    running = 0.0
    print(f"rows={len(matrix)} cols={len(matrix[0])}")
    print("component  explained  cumulative")
    for i, value in enumerate(ratios, 1):
        running += value
        print(f"{i:>9}  {value:.9f}  {running:.9f}")

    null = shuffle_null(matrix, args.null_trials, args.seed)
    observed_top2 = sum(ratios[:2])

    print()
    print(f"observed_top2={observed_top2:.9f}")
    print(f"null_trials={len(null)}")
    print(f"null_mean={sum(null) / len(null):.9f}")
    print(f"null_q025={quantile(null, 0.025):.9f}")
    print(f"null_median={quantile(null, 0.5):.9f}")
    print(f"null_q975={quantile(null, 0.975):.9f}")
    print(f"null_max={max(null):.9f}")


if __name__ == "__main__":
    main()
