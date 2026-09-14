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


def train_sequence(initial, sequence, times, steps, pos, width, rule, size):
    state = initial
    injections = dict(zip(times, sequence))
    for t in range(steps):
        if t in injections:
            state = inject(state, pos, injections[t], width, size)
        state = step(state, rule, size)
    return state


def patch_value(state, pos, width, radius, size):
    value = 0
    start = pos - radius
    for j in range(width + 2 * radius):
        index = (start + j) % size
        value = (value << 1) | ((state >> index) & 1)
    return value


def quotient_label(state, pos, width, probe_steps, rule, size):
    baseline = evolve(state, rule, size, probe_steps)
    signatures = []
    for probe in range(1 << width):
        perturbed = inject(state, pos, probe, width, size)
        perturbed = evolve(perturbed, rule, size, probe_steps)
        signatures.append(baseline ^ perturbed)

    labels = {}
    ids = []
    next_id = 0
    for signature in signatures:
        if signature not in labels:
            labels[signature] = next_id
            next_id += 1
        ids.append(labels[signature])
    return tuple(ids)


def recurrent_first_occurrences(state, rule, args):
    seen_times = Counter()
    first = {}

    for delay in range(args.autonomous_window + 1):
        patches_this_time = set()
        for pos in range(args.size):
            patch = patch_value(
                state, pos, args.core_width, args.radius, args.size
            )
            patches_this_time.add(patch)
            first.setdefault(patch, (state, pos, delay))
        for patch in patches_this_time:
            seen_times[patch] += 1
        state = step(state, rule, args.size)

    return {
        patch: first[patch]
        for patch, count in seen_times.items()
        if count >= args.min_time_slices
    }


def relation(left, right):
    if left == right:
        return "same"
    if left < right:
        return "seq2_superset"
    if right < left:
        return "seq1_superset"
    return "reorganize"


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 027: equal-budget history changes recurrent operational repertoire."
    )
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--training-time", type=int, default=48)
    parser.add_argument("--times", default="0,4,8,12,16")
    parser.add_argument("--autonomous-window", type=int, default=8)
    parser.add_argument("--min-time-slices", type=int, default=2)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--train-pos", type=int, default=0)
    args = parser.parse_args()

    times = tuple(int(x.strip()) for x in args.times.split(",") if x.strip())
    if len(times) != 5:
        raise SystemExit("default sequence comparison expects exactly five injection times")

    initial = 1 << (args.size // 2)
    op_relations = Counter()
    physical_vs_operational = Counter()
    exclusive_operational_cases = 0
    seq1_exclusive_operational_types = 0
    seq2_exclusive_operational_types = 0

    for rule in range(256):
        for a in range(1 << (args.core_width - 1)):
            b = a ^ ((1 << args.core_width) - 1)
            seq1 = (a, a, a, b, b)
            seq2 = (b, b, a, a, a)

            state1 = train_sequence(
                initial, seq1, times, args.training_time,
                args.train_pos, args.core_width, rule, args.size,
            )
            state2 = train_sequence(
                initial, seq2, times, args.training_time,
                args.train_pos, args.core_width, rule, args.size,
            )

            contexts1 = recurrent_first_occurrences(state1, rule, args)
            contexts2 = recurrent_first_occurrences(state2, rule, args)
            patches1 = set(contexts1)
            patches2 = set(contexts2)

            op1 = {
                quotient_label(
                    state, pos, args.core_width, args.probe_steps,
                    rule, args.size,
                )
                for state, pos, _ in contexts1.values()
            }
            op2 = {
                quotient_label(
                    state, pos, args.core_width, args.probe_steps,
                    rule, args.size,
                )
                for state, pos, _ in contexts2.values()
            }

            op_relations[relation(op1, op2)] += 1
            physical_vs_operational[
                ("phys_changed" if patches1 != patches2 else "phys_same",
                 "op_changed" if op1 != op2 else "op_same")
            ] += 1

            exclusive1 = patches1 - patches2
            exclusive2 = patches2 - patches1
            novel1 = {
                quotient_label(
                    contexts1[patch][0], contexts1[patch][1],
                    args.core_width, args.probe_steps, rule, args.size,
                )
                for patch in exclusive1
            } - op2
            novel2 = {
                quotient_label(
                    contexts2[patch][0], contexts2[patch][1],
                    args.core_width, args.probe_steps, rule, args.size,
                )
                for patch in exclusive2
            } - op1

            if novel1 or novel2:
                exclusive_operational_cases += 1
                seq1_exclusive_operational_types += len(novel1)
                seq2_exclusive_operational_types += len(novel2)

    total = sum(op_relations.values())
    operational_changed = total - op_relations["same"]

    print(f"cases={total}")
    print(f"operational_same={op_relations['same']}")
    print(f"operational_reorganize={op_relations['reorganize']}")
    print(f"operational_seq1_superset={op_relations['seq1_superset']}")
    print(f"operational_seq2_superset={op_relations['seq2_superset']}")
    print(f"operational_changed={operational_changed}")
    print(f"operational_changed_fraction={operational_changed / total:.9f}")
    print()
    for physical in ("phys_same", "phys_changed"):
        for operational in ("op_same", "op_changed"):
            print(
                f"{physical}_{operational}="
                f"{physical_vs_operational[(physical, operational)]}"
            )
    print()
    print(f"exclusive_patch_operational_novelty_cases={exclusive_operational_cases}")
    print(f"seq1_exclusive_operational_types={seq1_exclusive_operational_types}")
    print(f"seq2_exclusive_operational_types={seq2_exclusive_operational_types}")


if __name__ == "__main__":
    main()
