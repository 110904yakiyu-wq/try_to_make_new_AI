#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_exp020():
    path = Path(__file__).resolve().parents[1] / "020_autonomous_quotient_divergence" / "run.py"
    spec = importlib.util.spec_from_file_location("exp020", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_rules(text):
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values:
        raise ValueError("at least one rule is required")
    return values


def main():
    exp = load_exp020()

    parser = argparse.ArgumentParser(
        description="Experiment 021: exact-delay versus cumulative operational distinguishability depth."
    )
    parser.add_argument("--rules", default="98,14,113,142,226,143,126,129,110,151,159")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--training-time", type=int, default=48)
    parser.add_argument("--assay-offset", type=int, default=20)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--max-depth", type=int, default=16)
    args = parser.parse_args()

    single = exp.parse_schedule(args.single_schedule)
    repeat = exp.parse_schedule(args.repeat_schedule)

    for rule in parse_rules(args.rules):
        eligible = 0
        first_depth_hist = {}
        censored = 0
        trajectories = []

        for pattern in range(1 << args.core_width):
            q0_single = exp.quotient(rule, pattern, single, 0, args)
            q0_repeat = exp.quotient(rule, pattern, repeat, 0, args)
            if q0_single != q0_repeat:
                continue

            eligible += 1
            first = None
            exact = []
            for depth in range(1, args.max_depth + 1):
                qs = exp.quotient(rule, pattern, single, depth, args)
                qr = exp.quotient(rule, pattern, repeat, depth, args)
                different = qs != qr
                exact.append("!" if different else "=")
                if different and first is None:
                    first = depth

            if first is None:
                censored += 1
            else:
                first_depth_hist[first] = first_depth_hist.get(first, 0) + 1

            trajectories.append((pattern, first, "".join(exact)))

        hist_text = ",".join(
            f"d{depth}:{count}" for depth, count in sorted(first_depth_hist.items())
        ) or "-"
        print(
            f"rule={rule} eligible={eligible} first_depths={hist_text} "
            f"censored_gt_{args.max_depth}={censored}"
        )
        for pattern, first, exact in trajectories:
            first_text = str(first) if first is not None else f">{args.max_depth}"
            print(
                f"  train={format(pattern, f'0{args.core_width}b')} "
                f"first={first_text:<3} exact_delay={exact}"
            )
        print()


if __name__ == "__main__":
    main()
