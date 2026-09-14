#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter
from pathlib import Path


def load_exp057():
    path = Path(__file__).resolve().parents[1] / "057_self_delimiting_k8" / "run.py"
    spec = importlib.util.spec_from_file_location("exp057", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def query(exp, state, probe, pos, size, key_width, core_width):
    state = exp.write_window(state, pos, probe, core_width, size)
    event = exp.candidate(state, pos, size, key_width)
    if event is None:
        return None
    return event[2][0], event[4], len(event[1])


def sweep(exp, width, args):
    size = width * args.window_capacity
    counts = Counter()

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(size)
        for policy in ("min", "max"):
            for pos in range(0, size, width):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)

                    state_a = exp.train(
                        (a,) * args.repeats, pos, initial, size, width,
                        args.core_width, args.event_budget, policy,
                    )
                    state_b = exp.train(
                        (b,) * args.repeats, pos, initial, size, width,
                        args.core_width, args.event_budget, policy,
                    )

                    aa = query(exp, state_a, a, pos, size, width, args.core_width)
                    ba = query(exp, state_b, a, pos, size, width, args.core_width)
                    ab = query(exp, state_a, b, pos, size, width, args.core_width)
                    bb = query(exp, state_b, b, pos, size, width, args.core_width)
                    counts["cases"] += 1

                    if aa is not None and ba is not None and aa[:2] == ba[:2]:
                        counts["A_comparable"] += 1
                        if aa[2] < ba[2]:
                            counts["A_match_cheaper"] += 1
                        elif aa[2] > ba[2]:
                            counts["A_mismatch_cheaper"] += 1
                        else:
                            counts["A_equal"] += 1

                    if ab is not None and bb is not None and ab[:2] == bb[:2]:
                        counts["B_comparable"] += 1
                        if bb[2] < ab[2]:
                            counts["B_match_cheaper"] += 1
                        elif bb[2] > ab[2]:
                            counts["B_mismatch_cheaper"] += 1
                        else:
                            counts["B_equal"] += 1

                    if (
                        aa is not None and ba is not None and
                        ab is not None and bb is not None and
                        aa[:2] == ba[:2] and ab[:2] == bb[:2]
                    ):
                        counts["both_comparable"] += 1
                        if aa[2] < ba[2] and bb[2] < ab[2]:
                            counts["strict_crossover"] += 1
                        score = (ba[2] - aa[2]) + (ab[2] - bb[2])
                        if score > 0:
                            counts["net_specific_match"] += 1
                        elif score < 0:
                            counts["net_specific_mismatch"] += 1
                        else:
                            counts["net_tie"] += 1

    print(f"key_width={width}")
    for key in (
        "cases",
        "A_comparable", "A_match_cheaper", "A_equal", "A_mismatch_cheaper",
        "B_comparable", "B_match_cheaper", "B_equal", "B_mismatch_cheaper",
        "both_comparable", "strict_crossover",
        "net_specific_match", "net_tie", "net_specific_mismatch",
    ):
        print(f"{key}={counts[key]}")
    print()


def main():
    exp = load_exp057()
    parser = argparse.ArgumentParser(description="Experiment 063: experience-specific K8 cost compilation.")
    parser.add_argument("--key-widths", default="3,4")
    parser.add_argument("--window-capacity", type=int, default=6)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--backgrounds", type=int, default=16)
    args = parser.parse_args()

    for width in [int(x) for x in args.key_widths.split(",") if x.strip()]:
        sweep(exp, width, args)


if __name__ == "__main__":
    main()
