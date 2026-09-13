#!/usr/bin/env python3
import argparse
import importlib.util
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


def l2(values):
    return math.sqrt(sum(x * x for x in values))


def main():
    exp7 = load_exp007()
    exp4 = exp7.load_exp004()
    base = exp4.load_exp000()

    parser = argparse.ArgumentParser(
        description="Experiment 012: sweep all 256 ECA rules for remote response-geometry change."
    )
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--offset", type=int, default=20)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--a", type=int, default=0b011)
    parser.add_argument("--b", type=int, default=0b101)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=48)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--top", type=int, default=30)
    args = parser.parse_args()

    single = exp4.parse_schedule(args.single_schedule)
    repeat = exp4.parse_schedule(args.repeat_schedule)
    if max(single + repeat) >= args.probe_time:
        raise SystemExit("probe-time must be after all exposures")

    rows = []
    for rule in range(256):
        delta_single = exp7.probe_profile(
            exp4, base, rule, args.offset, single, args.size,
            args.position_stride, args.probe_time, args.probe_steps,
            args.a, args.b, args.core_width,
        )
        delta_repeat = exp7.probe_profile(
            exp4, base, rule, args.offset, repeat, args.size,
            args.position_stride, args.probe_time, args.probe_steps,
            args.a, args.b, args.core_width,
        )
        gains = [r - s for s, r in zip(delta_single, delta_repeat)]
        untrained = [
            gain for core, gain in enumerate(gains)
            if core not in (args.a, args.b)
        ]
        rows.append((
            l2(gains),
            l2(untrained),
            sum(abs(x) > 0.01 for x in untrained),
            rule,
        ))

    rows.sort(key=lambda row: row[1], reverse=True)
    print("rule  total_L2  untrained_L2  untrained_abs_gt_0.01")
    for total, untrained, count, rule in rows[: args.top]:
        print(f"{rule:>4}  {total:.9f}  {untrained:.9f}  {count:>2}/6")

    print()
    print("by_rule_table_ones")
    print("ones  mean_untrained_L2  median  max  nonzero/total  gt0.05  gt0.10")
    for ones in range(9):
        values = sorted(
            untrained for _, untrained, _, rule in rows
            if rule.bit_count() == ones
        )
        if not values:
            continue
        n = len(values)
        median = values[n // 2] if n % 2 else (values[n // 2 - 1] + values[n // 2]) / 2.0
        print(
            f"{ones:>4}  {sum(values)/n:.9f}  {median:.9f}  {max(values):.9f}  "
            f"{sum(x > 1e-12 for x in values):>2}/{n:<2}  "
            f"{sum(x > 0.05 for x in values):>2}  {sum(x > 0.10 for x in values):>2}"
        )


if __name__ == "__main__":
    main()
