#!/usr/bin/env python3
import argparse
import importlib.util
from collections import Counter, defaultdict
from pathlib import Path


def load_exp000():
    path = Path(__file__).resolve().parents[1] / "000_ca_null_substrate" / "run.py"
    spec = importlib.util.spec_from_file_location("exp000", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def baseline_relation(partition):
    relation = set()
    for group in partition:
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                relation.add((min(a, b), max(a, b)))
    return relation


def main():
    exp = load_exp000()
    parser = argparse.ArgumentParser(
        description="Experiment 001: recurring discriminating contexts."
    )
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--steps", type=int, default=64)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--radius", type=int, default=8)
    parser.add_argument("--horizon", type=int, default=3)
    parser.add_argument("--min-times", type=int, default=2)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    initial = exp.make_initial(args.size, "single")
    history = exp.run_history(initial, args.steps)

    baseline_contexts, _ = exp.collect_contexts(
        history, 0, args.core_width, args.radius, 1_000_000
    )
    cores = list(range(1 << args.core_width))
    base_partition = exp.partition_cores(
        cores, baseline_contexts, args.core_width, args.radius, args.horizon
    )
    base_rel = baseline_relation(base_partition)

    occurrences = Counter()
    times = defaultdict(set)
    first_seen = {}

    for t, row in enumerate(history):
        n = len(row)
        for i in range(n):
            left = exp.circular_slice(row, i - args.radius, args.radius)
            right = exp.circular_slice(row, i + args.core_width, args.radius)
            ctx = (exp.bits_to_int(left), exp.bits_to_int(right))
            occurrences[ctx] += 1
            times[ctx].add(t)
            first_seen.setdefault(ctx, t)

    rows = []
    for ctx, count in occurrences.items():
        if first_seen[ctx] == 0:
            continue

        split_pairs = []
        for a, b in sorted(base_rel):
            oa = exp.assay_outcome(a, ctx, args.core_width, args.radius, args.horizon)
            ob = exp.assay_outcome(b, ctx, args.core_width, args.radius, args.horizon)
            if oa != ob:
                split_pairs.append((a, b))

        if split_pairs and len(times[ctx]) >= args.min_times:
            rows.append(
                (
                    len(split_pairs),
                    len(times[ctx]),
                    count,
                    first_seen[ctx],
                    ctx,
                    split_pairs,
                )
            )

    rows.sort(key=lambda x: (-x[0], -x[1], -x[2], x[3], x[4]))

    print("baseline partition:", exp.format_partition(base_partition, args.core_width))
    print("baseline equivalent pairs:", len(base_rel))
    print("reusable discriminators:", len(rows))
    print()
    print("gain  times  count  first  left|right             split_pairs")

    for gain, n_times, count, first, ctx, pairs in rows[: args.top]:
        left, right = ctx
        pair_text = ",".join(
            f"{exp.format_core(a, args.core_width)}!={exp.format_core(b, args.core_width)}"
            for a, b in pairs
        )
        flank_text = (
            f"{format(left, f'0{args.radius}b')}|"
            f"{format(right, f'0{args.radius}b')}"
        )
        print(
            f"{gain:>4}  {n_times:>5}  {count:>5}  {first:>5}  "
            f"{flank_text:<21}  {pair_text}"
        )


if __name__ == "__main__":
    main()
