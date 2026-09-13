#!/usr/bin/env python3
import argparse
import importlib.util
import statistics
from pathlib import Path


def load_exp000():
    path = Path(__file__).resolve().parents[1] / "000_ca_null_substrate" / "run.py"
    spec = importlib.util.spec_from_file_location("exp000", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def step_rule(state, rule):
    n = len(state)
    out = [0] * n
    for i in range(n):
        idx = (state[(i - 1) % n] << 2) | (state[i] << 1) | state[(i + 1) % n]
        out[i] = (rule >> idx) & 1
    return out


def inject_core(exp, state, pos, core, width):
    out = state[:]
    bits = exp.int_to_bits(core, width)
    n = len(out)
    for j, bit in enumerate(bits):
        out[(pos + j) % n] = bit
    return out


def run_training(exp, initial, core, schedule, steps, pos, width, rule):
    state = initial[:]
    schedule = set(schedule)
    for t in range(steps):
        if t in schedule:
            state = inject_core(exp, state, pos, core, width)
        state = step_rule(state, rule)
    return state


def probe_impact(exp, state, core, pos, width, steps, rule):
    baseline = state[:]
    probed = inject_core(exp, state, pos, core, width)
    for _ in range(steps):
        baseline = step_rule(baseline, rule)
        probed = step_rule(probed, rule)
    return sum(a != b for a, b in zip(baseline, probed)) / len(state)


def cross_over_score(
    exp,
    rule,
    size,
    stride,
    schedule,
    probe_time,
    probe_steps,
    a,
    b,
    width,
):
    initial = exp.make_initial(size, "single")
    scores = []

    for pos in range(0, size, stride):
        state_a = run_training(
            exp, initial, a, schedule, probe_time, pos, width, rule
        )
        state_b = run_training(
            exp, initial, b, schedule, probe_time, pos, width, rule
        )

        aa = probe_impact(exp, state_a, a, pos, width, probe_steps, rule)
        ab = probe_impact(exp, state_a, b, pos, width, probe_steps, rule)
        ba = probe_impact(exp, state_b, a, pos, width, probe_steps, rule)
        bb = probe_impact(exp, state_b, b, pos, width, probe_steps, rule)

        scores.append(((ab - aa) + (ba - bb)) / 2.0)

    return statistics.mean(scores)


def parse_schedule(text):
    values = sorted({int(x.strip()) for x in text.split(",") if x.strip()})
    if not values:
        raise ValueError("schedule must not be empty")
    return values


def main():
    exp = load_exp000()
    parser = argparse.ArgumentParser(description="Experiment 004: sweep all 256 ECA rules.")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--a", type=int, default=0b011)
    parser.add_argument("--b", type=int, default=0b101)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=48)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--top", type=int, default=25)
    args = parser.parse_args()

    single = parse_schedule(args.single_schedule)
    repeat = parse_schedule(args.repeat_schedule)
    if max(single + repeat) >= args.probe_time:
        raise SystemExit("probe-time must be after all exposures")

    rows = []
    for rule in range(256):
        single_score = cross_over_score(
            exp,
            rule,
            args.size,
            args.position_stride,
            single,
            args.probe_time,
            args.probe_steps,
            args.a,
            args.b,
            args.core_width,
        )
        repeat_score = cross_over_score(
            exp,
            rule,
            args.size,
            args.position_stride,
            repeat,
            args.probe_time,
            args.probe_steps,
            args.a,
            args.b,
            args.core_width,
        )
        gain = repeat_score - single_score
        rows.append((abs(gain), gain, single_score, repeat_score, rule))

    rows.sort(reverse=True)

    print("rule  repetition_gain  single_score  repeat_score")
    for _, gain, single_score, repeat_score, rule in rows[: args.top]:
        print(
            f"{rule:>4}  {gain:+.9f}  "
            f"{single_score:+.9f}  {repeat_score:+.9f}"
        )


if __name__ == "__main__":
    main()
