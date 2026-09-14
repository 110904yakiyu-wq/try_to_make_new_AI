#!/usr/bin/env python3
import argparse
import importlib.util
import itertools
import random
from collections import Counter
from pathlib import Path


def load_exp050():
    path = Path(__file__).resolve().parents[1] / "050_role_symmetric_k6" / "run.py"
    spec = importlib.util.spec_from_file_location("exp050", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def transplant(exp, recipient, donor, positions, subset, args):
    state = recipient
    for index in subset:
        pos = positions[index]
        value = exp.read_window(donor, pos, args.key_width, args.size)
        state = exp.write_window(state, pos, value, args.key_width, args.size)
    return state


def main():
    exp = load_exp050()
    parser = argparse.ArgumentParser(description="Experiment 051: K6 distributed causality.")
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=8)
    parser.add_argument("--future-budget", type=int, default=8)
    parser.add_argument("--backgrounds", type=int, default=8)
    args = parser.parse_args()

    disjoint = exp.prepare_disjoint(args.size, args.key_width)
    counts = Counter()
    directed = 0

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(args.size)
        for policy in ("min", "max"):
            for pos in range(0, args.size, 8):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    s1 = exp.train((a, a, a, b, b), pos, initial, args, policy, disjoint)
                    s2 = exp.train((b, b, a, a, a), pos, initial, args, policy, disjoint)
                    _, t1 = exp.run_budget(s1, args.future_budget, args.size, args.key_width, policy, disjoint, trace=True)
                    _, t2 = exp.run_budget(s2, args.future_budget, args.size, args.key_width, policy, disjoint, trace=True)
                    if t1 == t2:
                        continue

                    for donor, recipient, donor_trace in ((s1, s2, t1), (s2, s1, t2)):
                        directed += 1
                        event = exp.choose_triple(donor, args.size, args.key_width, policy, disjoint)
                        if event is None:
                            counts["none"] += 1
                            continue
                        positions = event[:3]
                        best = None
                        for width in (1, 2, 3):
                            for subset in itertools.combinations(range(3), width):
                                state = transplant(exp, recipient, donor, positions, subset, args)
                                _, trace = exp.run_budget(state, args.future_budget, args.size, args.key_width, policy, disjoint, trace=True)
                                if trace == donor_trace:
                                    best = width
                                    break
                            if best is not None:
                                break
                        counts[best if best is not None else "none"] += 1

    print(f"directed_trace_diff_cases={directed}")
    print(f"minimum_1_endpoint={counts[1]}")
    print(f"minimum_2_endpoints={counts[2]}")
    print(f"minimum_3_endpoints={counts[3]}")
    print(f"not_reproduced_by_selected_triple={counts['none']}")


if __name__ == "__main__":
    main()
