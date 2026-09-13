#!/usr/bin/env python3
import argparse
import importlib.util
import math
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


def probe_profile(exp, base, rule, offset, schedule, size, stride, probe_time, probe_steps, a, b, width):
    initial = base.make_initial(size, "single")
    per_probe = [[] for _ in range(1 << width)]

    for pos in range(0, size, stride):
        state_a = exp.run_training(base, initial, a, schedule, probe_time, pos, width, rule)
        state_b = exp.run_training(base, initial, b, schedule, probe_time, pos, width, rule)
        q = (pos + offset) % size

        for core in range(1 << width):
            impact_a = exp.probe_impact(base, state_a, core, q, width, probe_steps, rule)
            impact_b = exp.probe_impact(base, state_b, core, q, width, probe_steps, rule)
            per_probe[core].append(impact_a - impact_b)

    return [statistics.mean(values) for values in per_probe]


def main():
    exp = load_exp004()
    base = exp.load_exp000()

    parser = argparse.ArgumentParser(description="Experiment 007: response-geometry modulation.")
    parser.add_argument("--rule", type=int, default=129)
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--offset", type=int, default=20)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--a", type=int, default=0b011)
    parser.add_argument("--b", type=int, default=0b101)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=48)
    parser.add_argument("--probe-steps", type=int, default=8)
    args = parser.parse_args()

    single = exp.parse_schedule(args.single_schedule)
    repeat = exp.parse_schedule(args.repeat_schedule)

    delta_single = probe_profile(
        exp, base, args.rule, args.offset, single, args.size, args.position_stride,
        args.probe_time, args.probe_steps, args.a, args.b, args.core_width,
    )
    delta_repeat = probe_profile(
        exp, base, args.rule, args.offset, repeat, args.size, args.position_stride,
        args.probe_time, args.probe_steps, args.a, args.b, args.core_width,
    )

    gains = [r - s for s, r in zip(delta_single, delta_repeat)]
    l1 = sum(abs(x) for x in gains)
    l2 = math.sqrt(sum(x * x for x in gains))

    print("probe  delta_single  delta_repeat  geometry_change")
    for core, (single_value, repeat_value, gain) in enumerate(
        zip(delta_single, delta_repeat, gains)
    ):
        print(
            f"{format(core, f'0{args.core_width}b')}  "
            f"{single_value:+.9f}  {repeat_value:+.9f}  {gain:+.9f}"
        )

    untrained = [
        (core, gain)
        for core, gain in enumerate(gains)
        if core not in (args.a, args.b)
    ]
    print()
    print(f"L1_geometry_change={l1:.9f}")
    print(f"L2_geometry_change={l2:.9f}")
    print(
        "untrained_abs_gt_0.01="
        + str(sum(abs(gain) > 0.01 for _, gain in untrained))
        + f"/{len(untrained)}"
    )


if __name__ == "__main__":
    main()
