#!/usr/bin/env python3
import argparse


def step(state, rule, size):
    mask = (1 << size) - 1
    left = ((state << 1) & mask) | (state >> (size - 1))
    right = (state >> 1) | ((state & 1) << (size - 1))
    center = state
    nl = (~left) & mask
    nc = (~center) & mask
    nr = (~right) & mask
    out = 0
    for index in range(8):
        if not ((rule >> index) & 1):
            continue
        l = (index >> 2) & 1
        c = (index >> 1) & 1
        r = index & 1
        out |= (
            (left if l else nl)
            & (center if c else nc)
            & (right if r else nr)
        )
    return out


def evolve(state, rule, size, steps):
    for _ in range(steps):
        state = step(state, rule, size)
    return state


def inject(state, pos, value, width, size):
    for j in range(width):
        bit = (value >> (width - 1 - j)) & 1
        index = (pos + j) % size
        if bit:
            state |= 1 << index
        else:
            state &= ~(1 << index)
    return state


def train(initial, pattern, schedule, steps, pos, width, rule, size):
    state = initial
    schedule = set(schedule)
    for t in range(steps):
        if t in schedule:
            state = inject(state, pos, pattern, width, size)
        state = step(state, rule, size)
    return state


def effect(state, probe, pos, width, steps, rule, size):
    baseline = evolve(state, rule, size, steps)
    perturbed = inject(state, pos, probe, width, size)
    perturbed = evolve(perturbed, rule, size, steps)
    return baseline ^ perturbed


def quotient(rule, training_pattern, schedule, extra_steps, args):
    initial = 1 << (args.size // 2)
    signatures = [[] for _ in range(1 << args.core_width)]

    for pos in range(0, args.size, args.position_stride):
        state = train(
            initial, training_pattern, schedule, args.training_time,
            pos, args.core_width, rule, args.size,
        )
        state = evolve(state, rule, args.size, extra_steps)
        assay_pos = (pos + args.assay_offset) % args.size
        for probe in range(1 << args.core_width):
            signatures[probe].append(
                effect(
                    state, probe, assay_pos, args.core_width,
                    args.probe_steps, rule, args.size,
                )
            )

    groups = []
    used = set()
    signatures = [tuple(row) for row in signatures]
    for i, signature in enumerate(signatures):
        if i in used:
            continue
        group = [i]
        used.add(i)
        for j in range(i + 1, len(signatures)):
            if j not in used and signatures[j] == signature:
                group.append(j)
                used.add(j)
        groups.append(group)
    return groups


def fmt(groups, width):
    return " ".join(
        "{" + ",".join(format(x, f"0{width}b") for x in group) + "}"
        for group in groups
    )


def parse_schedule(text):
    return sorted({int(x.strip()) for x in text.split(",") if x.strip()})


def parse_deltas(text):
    return sorted({int(x.strip()) for x in text.split(",") if x.strip()})


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 020: autonomous divergence of a currently identical operational quotient."
    )
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--training-time", type=int, default=48)
    parser.add_argument("--assay-offset", type=int, default=20)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--future-deltas", default="1,2,4,8,12,16")
    parser.add_argument("--show", type=int, default=40)
    args = parser.parse_args()

    single = parse_schedule(args.single_schedule)
    repeat = parse_schedule(args.repeat_schedule)
    deltas = parse_deltas(args.future_deltas)

    eligible = 0
    cases = []
    rules_with_cases = set()

    for rule in range(256):
        for training_pattern in range(1 << args.core_width):
            now_single = quotient(rule, training_pattern, single, 0, args)
            now_repeat = quotient(rule, training_pattern, repeat, 0, args)
            if now_single != now_repeat:
                continue
            eligible += 1

            for delta in deltas:
                future_single = quotient(rule, training_pattern, single, delta, args)
                future_repeat = quotient(rule, training_pattern, repeat, delta, args)
                if future_single != future_repeat:
                    rules_with_cases.add(rule)
                    cases.append((
                        rule, training_pattern, delta,
                        now_single, future_single, future_repeat,
                    ))
                    break

    print(f"eligible_same_now={eligible}")
    print(f"autonomous_divergence_cases={len(cases)}")
    print(f"rules_with_cases={len(rules_with_cases)}/256")
    print()

    for rule, training_pattern, delta, now_q, single_q, repeat_q in cases[: args.show]:
        print(
            f"rule={rule} train={format(training_pattern, f'0{args.core_width}b')} "
            f"earliest_delta={delta}"
        )
        print(f"  now    : {fmt(now_q, args.core_width)}")
        print(f"  single : {fmt(single_q, args.core_width)}")
        print(f"  repeat : {fmt(repeat_q, args.core_width)}")


if __name__ == "__main__":
    main()
