#!/usr/bin/env python3
import argparse
import importlib.util
import statistics
from pathlib import Path


def load_exp004():
    path = Path(__file__).resolve().parents[1] / "004_rule_sweep" / "run.py"
    spec = importlib.util.spec_from_file_location("exp004", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def score_at_offset(
    exp,
    base,
    rule,
    offset,
    schedule,
    size,
    stride,
    probe_time,
    probe_steps,
    a,
    b,
    width,
):
    initial = base.make_initial(size, "single")
    scores = []

    for pos in range(0, size, stride):
        state_a = exp.run_training(
            base, initial, a, schedule, probe_time, pos, width, rule
        )
        state_b = exp.run_training(
            base, initial, b, schedule, probe_time, pos, width, rule
        )
        q = (pos + offset) % size

        aa = exp.probe_impact(base, state_a, a, q, width, probe_steps, rule)
        ab = exp.probe_impact(base, state_a, b, q, width, probe_steps, rule)
        ba = exp.probe_impact(base, state_b, a, q, width, probe_steps, rule)
        bb = exp.probe_impact(base, state_b, b, q, width, probe_steps, rule)

        scores.append(((ab - aa) + (ba - bb)) / 2.0)

    return statistics.mean(scores)


def parse_csv_ints(text):
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def main():
    exp = load_exp004()
    base = exp.load_exp000()

    parser = argparse.ArgumentParser(
        description="Experiment 005: spatial transfer of repetition gain."
    )
    parser.add_argument("--rules", default="195,153,129,203,110")
    parser.add_argument("--offsets", default="0,4,8,12,16,20,24,28,32,36,40")
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--a", type=int, default=0b011)
    parser.add_argument("--b", type=int, default=0b101)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=32)
    parser.add_argument("--probe-steps", type=int, default=8)
    args = parser.parse_args()

    rules = parse_csv_ints(args.rules)
    offsets = parse_csv_ints(args.offsets)
    single = exp.parse_schedule(args.single_schedule)
    repeat = exp.parse_schedule(args.repeat_schedule)

    print("rule  offset  single_score  repeat_score  transfer_gain")
    for rule in rules:
        for offset in offsets:
            single_score = score_at_offset(
                exp,
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
            repeat_score = score_at_offset(
                exp,
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
            gain = repeat_score - single_score
            print(
                f"{rule:>4}  {offset:>6}  {single_score:+.9f}  "
                f"{repeat_score:+.9f}  {gain:+.9f}"
            )


if __name__ == "__main__":
    main()
