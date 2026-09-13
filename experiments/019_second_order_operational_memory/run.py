#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_exp018():
    path = Path(__file__).resolve().parents[1] / "018_history_induced_quotient" / "run.py"
    spec = importlib.util.spec_from_file_location("exp018", path)
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


def step_int(state, rule, size):
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
        state = step_int(state, rule, size)
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
        state = step_int(state, rule, size)
    return state


def probe_effect(state, probe, pos, width, steps, rule, size):
    baseline = state
    perturbed = inject(state, pos, probe, width, size)
    baseline = evolve(baseline, rule, size, steps)
    perturbed = evolve(perturbed, rule, size, steps)
    return baseline ^ perturbed


def signatures(rule, training_pattern, schedule, bridge_pattern, args):
    initial = 1 << (args.size // 2)
    result = [[] for _ in range(1 << args.core_width)]

    for pos in range(0, args.size, args.position_stride):
        state = train(
            initial, training_pattern, schedule, args.training_time,
            pos, args.core_width, rule, args.size,
        )
        if bridge_pattern is not None:
            state = inject(
                state, (pos + args.bridge_offset) % args.size,
                bridge_pattern, args.core_width, args.size,
            )
        state = evolve(state, rule, args.size, args.bridge_steps)
        assay_pos = (pos + args.assay_offset) % args.size

        for probe in range(1 << args.core_width):
            result[probe].append(
                probe_effect(
                    state, probe, assay_pos, args.core_width,
                    args.probe_steps, rule, args.size,
                )
            )

    return [tuple(row) for row in result]


def partition(signatures):
    groups = []
    used = set()
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


def refines(left, right):
    parents = [set(group) for group in right]
    return all(any(set(group) <= parent for parent in parents) for group in left)


def transition(before, after):
    after_refines = refines(after, before)
    before_refines = refines(before, after)
    if after_refines and before_refines:
        return "same"
    if after_refines:
        return "refine"
    if before_refines:
        return "coarsen"
    return "reorganize"


def fmt(groups, width):
    return " ".join(
        "{" + ",".join(format(x, f"0{width}b") for x in group) + "}"
        for group in groups
    )


def main():
    exp18 = load_exp018()
    exp4 = exp18.load_exp004()

    parser = argparse.ArgumentParser(
        description="Experiment 019: prior history changes how a later bridge changes the operational quotient."
    )
    parser.add_argument("--rules", default="14,113,142,143,159,226,126,129,98,110,151")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--training-time", type=int, default=48)
    parser.add_argument("--bridge-offset", type=int, default=20)
    parser.add_argument("--bridge-steps", type=int, default=8)
    parser.add_argument("--assay-offset", type=int, default=32)
    parser.add_argument("--probe-steps", type=int, default=8)
    args = parser.parse_args()

    single = exp4.parse_schedule(args.single_schedule)
    repeat = exp4.parse_schedule(args.repeat_schedule)

    for rule in parse_rules(args.rules):
        cases = []
        training_patterns = set()

        for training_pattern in range(1 << args.core_width):
            base_single = partition(signatures(rule, training_pattern, single, None, args))
            base_repeat = partition(signatures(rule, training_pattern, repeat, None, args))

            # We intentionally keep only cases where the current first-order
            # quotient is the same. Any later difference is therefore a
            # second-order distinction between the two histories under this assay.
            if base_single != base_repeat:
                continue

            for bridge in range(1 << args.core_width):
                after_single = partition(signatures(rule, training_pattern, single, bridge, args))
                after_repeat = partition(signatures(rule, training_pattern, repeat, bridge, args))
                single_kind = transition(base_single, after_single)
                repeat_kind = transition(base_repeat, after_repeat)

                if single_kind != repeat_kind:
                    training_patterns.add(training_pattern)
                    cases.append((
                        training_pattern, bridge, single_kind, repeat_kind,
                        base_single, after_single, after_repeat,
                    ))

        pats = ",".join(format(x, f"0{args.core_width}b") for x in sorted(training_patterns)) or "-"
        print(f"rule={rule} second_order_cases={len(cases)} training_patterns={pats}")
        for train_pattern, bridge, sk, rk, base_q, single_q, repeat_q in cases:
            print(
                f"  train={format(train_pattern, f'0{args.core_width}b')} "
                f"bridge={format(bridge, f'0{args.core_width}b')} "
                f"single={sk} repeat={rk}"
            )
            print(f"    base   : {fmt(base_q, args.core_width)}")
            print(f"    single : {fmt(single_q, args.core_width)}")
            print(f"    repeat : {fmt(repeat_q, args.core_width)}")
        print()


if __name__ == "__main__":
    main()
