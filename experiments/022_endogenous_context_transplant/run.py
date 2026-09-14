#!/usr/bin/env python3
import argparse
from collections import Counter


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


def transplant_window(recipient, donor, start, length, size):
    out = recipient
    for j in range(length):
        index = (start + j) % size
        bit = (donor >> index) & 1
        if bit:
            out |= 1 << index
        else:
            out &= ~(1 << index)
    return out


def quotient(rule, states, positions, args, donor_states=None, radius=None, distant=False):
    signatures = [[] for _ in range(1 << args.core_width)]

    for i, (pos, state) in enumerate(zip(positions, states)):
        q = (pos + args.assay_offset) % args.size

        if donor_states is not None:
            length = args.core_width + 2 * radius
            start = (q - radius) % args.size
            if distant:
                start = (start + args.size // 2) % args.size
            state = transplant_window(
                state, donor_states[i], start, length, args.size
            )

        baseline = evolve(state, rule, args.size, args.probe_steps)
        for probe in range(1 << args.core_width):
            perturbed = inject(state, q, probe, args.core_width, args.size)
            perturbed = evolve(perturbed, rule, args.size, args.probe_steps)
            signatures[probe].append(baseline ^ perturbed)

    signatures = [tuple(values) for values in signatures]
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
        groups.append(tuple(group))
    return tuple(groups)


def parse_schedule(text):
    return tuple(sorted({int(x.strip()) for x in text.split(",") if x.strip()}))


def parse_radii(text):
    return tuple(sorted({int(x.strip()) for x in text.split(",") if x.strip()}))


def fmt(groups, width):
    return " ".join(
        "{" + ",".join(format(x, f"0{width}b") for x in group) + "}"
        for group in groups
    )


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 022: transplant naturally generated local context between histories."
    )
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--training-time", type=int, default=48)
    parser.add_argument("--assay-offset", type=int, default=20)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--radii", default="0,1,2,4,8")
    parser.add_argument("--show", type=int, default=20)
    args = parser.parse_args()

    single = parse_schedule(args.single_schedule)
    repeat = parse_schedule(args.repeat_schedule)
    radii = parse_radii(args.radii)
    positions = tuple(range(0, args.size, args.position_stride))
    initial = 1 << (args.size // 2)

    counts = Counter()
    radius_counts = Counter()
    examples = []

    for rule in range(256):
        for training_pattern in range(1 << args.core_width):
            single_states = [
                train(initial, training_pattern, single, args.training_time,
                      pos, args.core_width, rule, args.size)
                for pos in positions
            ]
            repeat_states = [
                train(initial, training_pattern, repeat, args.training_time,
                      pos, args.core_width, rule, args.size)
                for pos in positions
            ]

            q_single = quotient(rule, single_states, positions, args)
            q_repeat = quotient(rule, repeat_states, positions, args)
            if q_single == q_repeat:
                continue

            counts["baseline_changed"] += 1
            repeat_to_single = None
            single_to_repeat = None
            distant_repeat_to_single = None
            distant_single_to_repeat = None

            for radius in radii:
                q_repeat_with_single = quotient(
                    rule, repeat_states, positions, args,
                    donor_states=single_states, radius=radius, distant=False,
                )
                q_single_with_repeat = quotient(
                    rule, single_states, positions, args,
                    donor_states=repeat_states, radius=radius, distant=False,
                )
                q_repeat_with_single_distant = quotient(
                    rule, repeat_states, positions, args,
                    donor_states=single_states, radius=radius, distant=True,
                )
                q_single_with_repeat_distant = quotient(
                    rule, single_states, positions, args,
                    donor_states=repeat_states, radius=radius, distant=True,
                )

                if repeat_to_single is None and q_repeat_with_single == q_single:
                    repeat_to_single = radius
                if single_to_repeat is None and q_single_with_repeat == q_repeat:
                    single_to_repeat = radius
                if (distant_repeat_to_single is None
                        and q_repeat_with_single_distant == q_single):
                    distant_repeat_to_single = radius
                if (distant_single_to_repeat is None
                        and q_single_with_repeat_distant == q_repeat):
                    distant_single_to_repeat = radius

            if repeat_to_single is not None:
                counts["repeat_to_single"] += 1
                radius_counts[("repeat_to_single", repeat_to_single)] += 1
            if single_to_repeat is not None:
                counts["single_to_repeat"] += 1
                radius_counts[("single_to_repeat", single_to_repeat)] += 1
            if repeat_to_single is not None and single_to_repeat is not None:
                counts["bidirectional"] += 1
            if distant_repeat_to_single is not None:
                counts["distant_repeat_to_single"] += 1
            if distant_single_to_repeat is not None:
                counts["distant_single_to_repeat"] += 1

            if len(examples) < args.show and repeat_to_single is not None:
                examples.append((
                    rule, training_pattern, q_single, q_repeat,
                    repeat_to_single, single_to_repeat,
                ))

    print(f"baseline_changed={counts['baseline_changed']}")
    print(f"repeat_to_single={counts['repeat_to_single']}")
    print(f"single_to_repeat={counts['single_to_repeat']}")
    print(f"bidirectional={counts['bidirectional']}")
    print(f"distant_repeat_to_single={counts['distant_repeat_to_single']}")
    print(f"distant_single_to_repeat={counts['distant_single_to_repeat']}")
    print()

    for direction in ("repeat_to_single", "single_to_repeat"):
        parts = [
            f"r{radius}:{radius_counts[(direction, radius)]}"
            for radius in radii
        ]
        print(direction + "_minimal_radius=" + ",".join(parts))
    print()

    for rule, pattern, qs, qr, r2s, s2r in examples:
        print(
            f"rule={rule} train={format(pattern, f'0{args.core_width}b')} "
            f"repeat_to_single_radius={r2s} single_to_repeat_radius={s2r}"
        )
        print(f"  single : {fmt(qs, args.core_width)}")
        print(f"  repeat : {fmt(qr, args.core_width)}")


if __name__ == "__main__":
    main()
