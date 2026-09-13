#!/usr/bin/env python3
import argparse
import importlib.util
from collections import OrderedDict
from pathlib import Path


def load_exp000():
    path = Path(__file__).resolve().parents[1] / "000_ca_null_substrate" / "run.py"
    spec = importlib.util.spec_from_file_location("exp000", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contexts_at_t(exp, history, t, core_width, radius):
    row = history[t]
    n = len(row)
    contexts = []
    for i in range(n):
        left = exp.circular_slice(row, i - radius, radius)
        right = exp.circular_slice(row, i + core_width, radius)
        contexts.append((exp.bits_to_int(left), exp.bits_to_int(right)))
    return contexts


def partition(exp, cores, contexts, core_width, radius, horizon):
    groups = OrderedDict()
    for core in cores:
        sig = tuple(
            exp.assay_outcome(core, ctx, core_width, radius, horizon)
            for ctx in contexts
        )
        groups.setdefault(sig, []).append(core)
    return list(groups.values())


def relation(partition_value):
    rel = set()
    for group in partition_value:
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                rel.add((min(a, b), max(a, b)))
    return rel


def main():
    exp = load_exp000()
    parser = argparse.ArgumentParser(
        description="Experiment 002: fixed-budget quotient assay."
    )
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--steps", type=int, default=64)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--radius", type=int, default=3)
    parser.add_argument("--horizon", type=int, default=3)
    args = parser.parse_args()

    if args.horizon > args.radius:
        raise SystemExit("horizon must be <= radius")

    initial = exp.make_initial(args.size, "single")
    history = exp.run_history(initial, args.steps)
    cores = list(range(1 << args.core_width))

    previous_relation = None

    print("t  assays  classes  transition  partition")
    for t in range(args.steps + 1):
        contexts = contexts_at_t(exp, history, t, args.core_width, args.radius)
        part = partition(
            exp, cores, contexts, args.core_width, args.radius, args.horizon
        )
        rel = relation(part)

        if previous_relation is None:
            transition = "-"
        else:
            split = len(previous_relation - rel)
            merged = len(rel - previous_relation)
            if split or merged:
                transition = f"split_pairs={split},merged_pairs={merged}"
            else:
                transition = "same"

        print(
            f"{t:>2}  {len(contexts):>6}  {len(part):>7}  "
            f"{transition:<31}  {exp.format_partition(part, args.core_width)}"
        )

        previous_relation = rel


if __name__ == "__main__":
    main()
