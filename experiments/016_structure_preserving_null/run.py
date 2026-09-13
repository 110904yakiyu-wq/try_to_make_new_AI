#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_exp009():
    path = Path(__file__).resolve().parents[1] / "009_low_dimensional_modes" / "run.py"
    spec = importlib.util.spec_from_file_location("exp009", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_rules(text):
    rules = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not rules:
        raise ValueError("at least one rule is required")
    if any(rule < 0 or rule > 255 for rule in rules):
        raise ValueError("rules must be in [0,255]")
    return rules


def pattern_profile(exp7, exp4, base, rule, offset, schedule, size, stride,
                    probe_time, probe_steps, pattern, width):
    initial = base.make_initial(size, "single")
    values = [[] for _ in range(1 << width)]

    for pos in range(0, size, stride):
        state = exp4.run_training(
            base, initial, pattern, schedule, probe_time, pos, width, rule
        )
        q = (pos + offset) % size
        for probe in range(1 << width):
            values[probe].append(
                exp4.probe_impact(base, state, probe, q, width, probe_steps, rule)
            )

    return [sum(column) / len(column) for column in values]


def history_effect_matrix(exp7, exp4, base, args, rule):
    single = exp4.parse_schedule(args.single_schedule)
    repeat = exp4.parse_schedule(args.repeat_schedule)
    matrix = []

    for pattern in range(1 << args.core_width):
        one = pattern_profile(
            exp7, exp4, base, rule, args.offset, single, args.size,
            args.position_stride, args.probe_time, args.probe_steps,
            pattern, args.core_width,
        )
        many = pattern_profile(
            exp7, exp4, base, rule, args.offset, repeat, args.size,
            args.position_stride, args.probe_time, args.probe_steps,
            pattern, args.core_width,
        )
        matrix.append([r - s for s, r in zip(one, many)])

    return matrix


def main():
    exp9 = load_exp009()
    exp7 = exp9.load_exp007()
    exp4 = exp7.load_exp004()
    base = exp4.load_exp000()

    parser = argparse.ArgumentParser(
        description="Experiment 016: structure-preserving null for low-dimensional history effects."
    )
    parser.add_argument("--rules", default="98,159,151,143,142,14,113,226,129,110,126")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--offset", type=int, default=20)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=48)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--null-trials", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    args.rules = parse_rules(args.rules)

    print("rule  H_top2  null_mean  null_q975  null_max  null_ge_observed")
    for rule in args.rules:
        matrix = history_effect_matrix(exp7, exp4, base, args, rule)
        ratios = exp9.explained_variance(matrix)
        observed = sum(ratios[:2])

        # Important: shuffle probe labels inside each of the eight pattern-specific
        # rows. This preserves the fact that all pairwise differences would be
        # generated from the same eight underlying history-effect vectors.
        null = exp9.shuffle_null(matrix, args.null_trials, args.seed + rule)
        ge = sum(value >= observed for value in null)

        print(
            f"{rule:>4}  {observed:.9f}  {sum(null)/len(null):.9f}  "
            f"{exp9.quantile(null, 0.975):.9f}  {max(null):.9f}  {ge}/{len(null)}"
        )


if __name__ == "__main__":
    main()
