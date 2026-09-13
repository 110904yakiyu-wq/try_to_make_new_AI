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


def jacobi_eigensystem(matrix, eps=1e-14, max_iter=10000):
    a = [row[:] for row in matrix]
    n = len(a)
    vectors = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

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

        tau = (aqq - app) / (2.0 * apq)
        if tau >= 0.0:
            t = 1.0 / (tau + math.sqrt(1.0 + tau * tau))
        else:
            t = -1.0 / (-tau + math.sqrt(1.0 + tau * tau))
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = t * c

        for k in range(n):
            if k == p or k == q:
                continue
            akp = a[k][p]
            akq = a[k][q]
            a[k][p] = a[p][k] = c * akp - s * akq
            a[k][q] = a[q][k] = s * akp + c * akq

        a[p][p] = app - t * apq
        a[q][q] = aqq + t * apq
        a[p][q] = a[q][p] = 0.0

        for k in range(n):
            vkp = vectors[k][p]
            vkq = vectors[k][q]
            vectors[k][p] = c * vkp - s * vkq
            vectors[k][q] = s * vkp + c * vkq

    pairs = [(a[i][i], [vectors[k][i] for k in range(n)]) for i in range(n)]
    pairs.sort(key=lambda item: item[0], reverse=True)
    return pairs


def covariance(exp9, matrix):
    return exp9.gram_xtx(exp9.centered_rows(matrix))


def top_basis(cov, k=2):
    pairs = jacobi_eigensystem(cov)
    basis = [vector for _, vector in pairs[:k]]
    total = sum(max(0.0, value) for value, _ in pairs)
    own = sum(max(0.0, value) for value, _ in pairs[:k]) / total if total else 0.0
    return basis, own


def quadratic_form(vector, matrix):
    total = 0.0
    for i, vi in enumerate(vector):
        for j, vj in enumerate(vector):
            total += vi * matrix[i][j] * vj
    return total


def captured_variance(basis, covariance_matrix):
    trace = sum(covariance_matrix[i][i] for i in range(len(covariance_matrix)))
    if trace == 0.0:
        return 0.0
    return sum(quadratic_form(v, covariance_matrix) for v in basis) / trace


def local_args(base, offset, probe_time):
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

    parser = argparse.ArgumentParser(description="Experiment 011: mode transfer across observer conditions.")
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

    covariances = {}
    bases = {}
    own_top2 = {}

    for name, offset, probe_time in conditions:
        matrix = exp9.geometry_matrix(exp7, exp4, base_ca, local_args(args, offset, probe_time))
        cov = covariance(exp9, matrix)
        basis, own = top_basis(cov, 2)
        covariances[name] = cov
        bases[name] = basis
        own_top2[name] = own

    names = [name for name, _, _ in conditions]

    print("captured variance using source condition's top-two axes")
    print("source\\target   " + "  ".join(f"{name:>14}" for name in names))
    for source in names:
        values = [captured_variance(bases[source], covariances[target]) for target in names]
        print(f"{source:<14} " + "  ".join(f"{value:>14.9f}" for value in values))

    print()
    print("relative capture versus target's own optimal top-two")
    print("source\\target   " + "  ".join(f"{name:>14}" for name in names))
    for source in names:
        values = [
            captured_variance(bases[source], covariances[target]) / own_top2[target]
            if own_top2[target] else 0.0
            for target in names
        ]
        print(f"{source:<14} " + "  ".join(f"{value:>14.9f}" for value in values))


if __name__ == "__main__":
    main()
