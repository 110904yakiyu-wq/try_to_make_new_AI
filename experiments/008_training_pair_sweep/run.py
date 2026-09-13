#!/usr/bin/env python3
import argparse
import importlib.util
import itertools
import math
from pathlib import Path


def load_exp007():
    path = Path(__file__).resolve().parents[1] / "007_response_geometry" / "run.py"
    spec = importlib.util.spec_from_file_location("exp007", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    exp7 = load_exp007()
    exp4 = exp7.load_exp004()
    base = exp4.load_exp000()

    parser = argparse.ArgumentParser(description="Experiment 008: sweep all 3-bit training pairs.")
    parser.add_argument("--rule", type=int, default=129)
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--offset", type=int, default=20)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=48)
    parser.add_argument("--probe-steps", type=int, default=8)
    args = parser.parse_args()

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
        gains = [r - s for s, r in zip(delta_single, delta_repeat)]
        l1 = sum(abs(x) for x in gains)
        l2 = math.sqrt(sum(x * x for x in gains))
        untrained = sum(
            abs(gain) > 0.01
            for core, gain in enumerate(gains)
            if core not in (a, b)
        )
        rows.append((l1, l2, untrained, a, b, gains))

    rows.sort(reverse=True)
    print("A    B    L1_change    L2_change    untrained>|0.01|")
    for l1, l2, untrained, a, b, _ in rows:
        print(
            f"{format(a, f'0{args.core_width}b')}  "
            f"{format(b, f'0{args.core_width}b')}  "
            f"{l1:.9f}  {l2:.9f}  {untrained}/6"
        )

    print()
    print(f"pairs={len(rows)}")
    print(f"min_L1={min(row[0] for row in rows):.9f}")
    print(f"max_L1={max(row[0] for row in rows):.9f}")
    print(f"pairs_L1_lt_0.01={sum(row[0] < 0.01 for row in rows)}")


if __name__ == "__main__":
    main()
