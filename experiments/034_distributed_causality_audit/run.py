#!/usr/bin/env python3
import argparse
import importlib.util
import itertools
from collections import Counter
from pathlib import Path


def load_exp032():
    path = Path(__file__).resolve().parents[1] / "032_recurrent_execution_macro" / "run.py"
    spec = importlib.util.spec_from_file_location("exp032", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def transplant_patch(exp, recipient, donor, pos, width, radius, size):
    out = recipient
    for j in range(width + 2 * radius):
        index = (pos - radius + j) % size
        target = exp.bit(donor, index, size)
        if exp.bit(out, index, size) != target:
            out ^= 1 << index
    return out


def parse_positions(text):
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise ValueError("at least one position is required")
    return values


def main():
    exp = load_exp032()
    parser = argparse.ArgumentParser(description="Experiment 034: distributed causality audit.")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--train-pos", type=int, default=0)
    parser.add_argument("--positions", default="0,8,16,24")
    parser.add_argument("--event-budget", type=int, default=128)
    parser.add_argument("--cascade-budget", type=int, default=32)
    args = parser.parse_args()

    positions = parse_positions(args.positions)
    eligible = 0
    minimum_size = Counter()
    unreproduced = 0

    for policy in ("min", "max"):
        for rule in range(256):
            for a in range(1 << (args.core_width - 1)):
                b = a ^ ((1 << args.core_width) - 1)
                seq1 = (a, a, a, b, b)
                seq2 = (b, b, a, a, a)
                s1 = exp.train(rule, seq1, args, policy)
                s2 = exp.train(rule, seq2, args, policy)

                for recipient, donor in ((s1, s2), (s2, s1)):
                    _, recipient_trace = exp.run_budget(
                        recipient, rule, args.size, args.cascade_budget, policy, trace=True
                    )
                    _, donor_trace = exp.run_budget(
                        donor, rule, args.size, args.cascade_budget, policy, trace=True
                    )
                    if recipient_trace == donor_trace:
                        continue
                    eligible += 1

                    found = None
                    for count in range(1, len(positions) + 1):
                        for subset in itertools.combinations(positions, count):
                            state = recipient
                            for pos in subset:
                                state = transplant_patch(
                                    exp, state, donor, pos,
                                    args.core_width, args.radius, args.size,
                                )
                            _, trace = exp.run_budget(
                                state, rule, args.size,
                                args.cascade_budget, policy, trace=True,
                            )
                            if trace == donor_trace:
                                found = count
                                break
                        if found is not None:
                            break

                    if found is None:
                        unreproduced += 1
                    else:
                        minimum_size[found] += 1

    print(f"eligible={eligible}")
    for count in range(1, len(positions) + 1):
        print(f"minimum_regions_{count}={minimum_size[count]}")
    print(f"unreproduced={unreproduced}")


if __name__ == "__main__":
    main()
