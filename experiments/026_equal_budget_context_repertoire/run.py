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


def recurrent_repertoire(state, rule, args):
    seen_times = Counter()

    for _ in range(args.autonomous_window + 1):
        patches = {
            patch_value(state, pos, args.core_width, args.radius, args.size)
            for pos in range(args.size)
        }
        for patch in patches:
            seen_times[patch] += 1
        state = step(state, rule, args.size)

    return {
        patch for patch, count in seen_times.items()
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
        description="Experiment 026: equal interaction budget, different order, endogenous context repertoire."
    )
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--training-time", type=int, default=48)
    parser.add_argument("--times", default="0,4,8,12,16")
    parser.add_argument("--autonomous-window", type=int, default=8)
    parser.add_argument("--min-time-slices", type=int, default=2)
    parser.add_argument("--train-pos", type=int, default=0)
    args = parser.parse_args()

    times = tuple(int(x.strip()) for x in args.times.split(",") if x.strip())
    if len(times) != 5:
        raise SystemExit("default sequence comparison expects exactly five injection times")

    initial = 1 << (args.size // 2)
    counts = Counter()
    novel_seq2 = 0
    novel_seq1 = 0
    size_seq1 = 0
    size_seq2 = 0

    # A=0..3 avoids counting the complementary A/B pair twice.
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

            rep1 = recurrent_repertoire(state1, rule, args)
            rep2 = recurrent_repertoire(state2, rule, args)

            counts[relation(rep1, rep2)] += 1
            novel_seq2 += len(rep2 - rep1)
            novel_seq1 += len(rep1 - rep2)
            size_seq1 += len(rep1)
            size_seq2 += len(rep2)

    total = sum(counts.values())
    changed = total - counts["same"]

    print(f"cases={total}")
    print(f"same={counts['same']}")
    print(f"reorganize={counts['reorganize']}")
    print(f"seq1_superset={counts['seq1_superset']}")
    print(f"seq2_superset={counts['seq2_superset']}")
    print(f"changed={changed}")
    print(f"changed_fraction={changed / total:.9f}")
    print(f"mean_seq1_repertoire={size_seq1 / total:.9f}")
    print(f"mean_seq2_repertoire={size_seq2 / total:.9f}")
    print(f"mean_seq1_only={novel_seq1 / total:.9f}")
    print(f"mean_seq2_only={novel_seq2 / total:.9f}")


if __name__ == "__main__":
    main()
