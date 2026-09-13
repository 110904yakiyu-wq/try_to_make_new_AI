#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_exp005():
    path = Path(__file__).resolve().parents[1] / "005_spatial_transfer" / "run.py"
    spec = importlib.util.spec_from_file_location("exp005", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_csv_ints(text):
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def main():
    exp5 = load_exp005()
    exp4 = exp5.load_exp004()
    base = exp4.load_exp000()

    parser = argparse.ArgumentParser(
        description="Experiment 006: exposure-spacing robustness."
    )
    parser.add_argument("--rules", default="129,195,153,203,110")
    parser.add_argument("--spacings", default="2,3,4,5,6,7,8")
    parser.add_argument("--offsets", default="0,20")
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--probe-time", type=int, default=48)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--a", type=int, default=0b011)
    parser.add_argument("--b", type=int, default=0b101)
    args = parser.parse_args()

    rules = parse_csv_ints(args.rules)
    spacings = parse_csv_ints(args.spacings)
    offsets = parse_csv_ints(args.offsets)
    single = [0]

    print("rule  spacing  offset  repetition_gain")
    for rule in rules:
        for spacing in spacings:
            repeat = [spacing * i for i in range(5)]
            if repeat[-1] >= args.probe_time:
                continue
            for offset in offsets:
                one = exp5.score_at_offset(
                    exp4,
                    base,
                    rule,
                    offset,
                    single,
                    args.size,
                    args.position_stride,
                    args.probe_time,
                    args.probe_steps,
                    args.a,
                    args.b,
                    args.core_width,
                )
                many = exp5.score_at_offset(
                    exp4,
                    base,
                    rule,
                    offset,
                    repeat,
                    args.size,
                    args.position_stride,
                    args.probe_time,
                    args.probe_steps,
                    args.a,
                    args.b,
                    args.core_width,
                )
                print(f"{rule:>4}  {spacing:>7}  {offset:>6}  {many - one:+.9f}")


if __name__ == "__main__":
    main()
