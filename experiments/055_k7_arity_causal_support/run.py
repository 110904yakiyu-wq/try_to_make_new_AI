#!/usr/bin/env python3
import argparse
import importlib.util
import itertools
import random
from collections import Counter
from pathlib import Path


def load_exp054():
    path = Path(__file__).resolve().parents[1] / "054_variable_arity_k7" / "run.py"
    spec = importlib.util.spec_from_file_location("exp054", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def transplant(exp, recipient, donor, positions, subset, width, size):
    state = recipient
    for index in subset:
        pos = positions[index]
        value = exp.read_window(donor, pos, width, size)
        state = exp.write_window(state, pos, value, width, size)
    return state


def main():
    exp = load_exp054()
    parser = argparse.ArgumentParser(description="Experiment 055: causal support of variable-arity K7 events.")
    parser.add_argument("--size", type=int, default=20)
    parser.add_argument("--key-width", type=int, default=5)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--max-arity", type=int, default=4)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--future-budget", type=int, default=2)
    parser.add_argument("--position-stride", type=int, default=5)
    parser.add_argument("--backgrounds", type=int, default=8)
    args = parser.parse_args()

    groups = exp.prepare_groups(args.size, args.key_width, args.max_arity)
    counts = Counter()
    directed = 0
    no_event = 0

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(args.size)
        for policy in ("min", "max"):
            for pos in range(0, args.size, args.position_stride):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    s1 = exp.train((a, a, a, b, b), pos, initial, args, groups, policy)
                    s2 = exp.train((b, b, a, a, a), pos, initial, args, groups, policy)
                    _, t1 = exp.run_budget(
                        s1, args.future_budget, args.size, args.key_width, groups, policy, trace=True
                    )
                    _, t2 = exp.run_budget(
                        s2, args.future_budget, args.size, args.key_width, groups, policy, trace=True
                    )
                    if t1 == t2:
                        continue

                    for donor, recipient, donor_trace in ((s1, s2, t1), (s2, s1, t2)):
                        directed += 1
                        event = exp.choose_event(donor, args.size, args.key_width, groups, policy)
                        if event is None:
                            no_event += 1
                            continue

                        positions = event[1]
                        arity = len(positions)
                        best = None
                        for subset_size in range(1, arity + 1):
                            for subset in itertools.combinations(range(arity), subset_size):
                                state = transplant(
                                    exp, recipient, donor, positions, subset,
                                    args.key_width, args.size,
                                )
                                _, trace = exp.run_budget(
                                    state, args.future_budget, args.size, args.key_width,
                                    groups, policy, trace=True,
                                )
                                if trace == donor_trace:
                                    best = subset_size
                                    break
                            if best is not None:
                                break
                        counts[(arity, best if best is not None else 0)] += 1

    print(f"directed_trace_diff_cases={directed}")
    print(f"donor_has_no_enabled_event={no_event}")
    for arity in range(2, args.max_arity + 1):
        total = sum(count for (k, _), count in counts.items() if k == arity)
        print(f"arity_{arity}_cases={total}")
        for minimum in range(0, arity + 1):
            print(f"arity_{arity}_minimum_{minimum}={counts[(arity, minimum)]}")


if __name__ == "__main__":
    main()
