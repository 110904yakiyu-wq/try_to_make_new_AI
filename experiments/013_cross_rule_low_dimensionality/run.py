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
    values = []
    for item in text.split(","):
        item = item.strip()
        if item:
            value = int(item)
            if not 0 <= value <= 255:
                raise ValueError("ECA rules must be in [0,255]")
            values.append(value)
    if not values:
        raise ValueError("at least one rule is required")
    return values


def main():
    exp9 = load_exp009()
    exp7 = exp9.load_exp007()
    exp4 = exp7.load_exp004()
    base = exp4.load_exp000()

    parser = argparse.ArgumentParser(
        description="Experiment 013: low-dimensional response modes across fixed ECA rules."
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
    parser.add_argument("--null-trials", type=int, default=500)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    args.rules = parse_rules(args.rules)

    print("rule  top1  top2  top3  null_mean_top2  null_q975  null_max  null_ge_observed")
    for rule in args.rules:
        args.rule = rule
        matrix = exp9.geometry_matrix(exp7, exp4, base, args)
        ratios = exp9.explained_variance(matrix)
        observed = sum(ratios[:2])
        null = exp9.shuffle_null(matrix, args.null_trials, args.seed + rule)
        ge = sum(value >= observed for value in null)
        print(
            f"{rule:>4}  {ratios[0]:.9f}  {observed:.9f}  {sum(ratios[:3]):.9f}  "
            f"{sum(null)/len(null):.9f}  {exp9.quantile(null, 0.975):.9f}  "
            f"{max(null):.9f}  {ge}/{len(null)}"
        )


if __name__ == "__main__":
    main()
