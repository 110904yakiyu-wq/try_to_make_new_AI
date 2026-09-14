#!/usr/bin/env python3
import argparse
import math
import random
from collections import Counter


def bit(state, index, size):
    return (state >> (index % size)) & 1


def read_window(state, pos, width, size):
    value = 0
    for j in range(width):
        value = (value << 1) | bit(state, pos + j, size)
    return value


def write_window(state, pos, value, width, size):
    out = state
    for j in range(width):
        index = (pos + j) % size
        target = (value >> (width - 1 - j)) & 1
        if bit(out, index, size) != target:
            out ^= 1 << index
    return out


def rotl(value, width):
    mask = (1 << width) - 1
    return ((value << 1) & mask) | (value >> (width - 1))


def candidate(state, start, size, width):
    # The ring capacity itself bounds the scan. Experiments use size % width == 0.
    capacity = size // width
    values = []
    positions = []
    xor_value = 0
    mask = (1 << width) - 1

    for offset in range(capacity):
        pos = (start + offset * width) % size
        value = read_window(state, pos, width, size)
        positions.append(pos)
        values.append(value)
        xor_value ^= value

        if len(values) < 2 or xor_value != 0:
            continue

        field = rotl(sum(values) & mask, width)
        outputs = tuple((value + field) & mask for value in values)
        if outputs == tuple(values):
            continue

        key = (
            sum(values),
            sum(value * value for value in values),
            math.prod(value + 1 for value in values),
            tuple(sorted(values)),
            tuple(positions),
        )
        return key, tuple(positions), tuple(values), outputs, field

    return None


def choose_event(state, size, width, policy):
    best = None
    for start in range(size):
        event = candidate(state, start, size, width)
        if event is None:
            continue
        if best is None:
            best = event
        elif policy == "min" and event[0] < best[0]:
            best = event
        elif policy == "max" and event[0] > best[0]:
            best = event
    return best


def step(state, size, width, policy):
    event = choose_event(state, size, width, policy)
    if event is None:
        return state, None
    _, positions, values, outputs, field = event
    for pos, value in zip(positions, outputs):
        state = write_window(state, pos, value, width, size)
    return state, (positions, values, outputs, field)


def run_budget(state, budget, size, width, policy, trace=False):
    events = []
    for _ in range(budget):
        state, event = step(state, size, width, policy)
        if trace:
            events.append(event)
    return (state, tuple(events)) if trace else state


def train(sequence, pos, initial, size, key_width, core_width, event_budget, policy):
    state = initial
    for value in sequence:
        state = write_window(state, pos, value, core_width, size)
        state = run_budget(state, event_budget, size, key_width, policy)
    return state


def repertoire(state, size, width):
    out = set()
    for start in range(size):
        event = candidate(state, start, size, width)
        if event is not None:
            positions, values = event[1], event[2]
            out.add((len(positions), tuple(sorted(values))))
    return frozenset(out)


def relation(left, right):
    if left == right:
        return "same"
    if left < right:
        return "seq2_superset"
    if right < left:
        return "seq1_superset"
    return "reorganize"


def sweep(args, key_width):
    size = key_width * args.window_capacity
    counts = Counter()
    arity_transitions = Counter()
    arity_diff = 0
    trace_diff = 0
    cases = 0

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(size)
        for policy in ("min", "max"):
            for pos in range(0, size, key_width):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    s1 = train(
                        (a, a, a, b, b), pos, initial, size, key_width,
                        args.core_width, args.event_budget, policy,
                    )
                    s2 = train(
                        (b, b, a, a, a), pos, initial, size, key_width,
                        args.core_width, args.event_budget, policy,
                    )
                    r1 = repertoire(s1, size, key_width)
                    r2 = repertoire(s2, size, key_width)
                    counts[relation(r1, r2)] += 1

                    a1 = frozenset(arity for arity, _ in r1)
                    a2 = frozenset(arity for arity, _ in r2)
                    arity_diff += int(a1 != a2)
                    arity_transitions[(tuple(sorted(a1)), tuple(sorted(a2)))] += 1

                    _, t1 = run_budget(s1, args.future_budget, size, key_width, policy, trace=True)
                    _, t2 = run_budget(s2, args.future_budget, size, key_width, policy, trace=True)
                    trace_diff += int(t1 != t2)
                    cases += 1

    print(f"key_width={key_width} size={size}")
    print(f"cases={cases}")
    print(f"same={counts['same']}")
    print(f"seq1_superset={counts['seq1_superset']}")
    print(f"seq2_superset={counts['seq2_superset']}")
    print(f"reorganize={counts['reorganize']}")
    print(f"arity_repertoire_diff={arity_diff}")
    print(f"future_trace_diff={trace_diff}")
    for pair, count in arity_transitions.most_common(12):
        print(f"arity_transition={pair[0]}->{pair[1]} count={count}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Experiment 057: self-delimiting K8.")
    parser.add_argument("--key-widths", default="4,5,6")
    parser.add_argument("--window-capacity", type=int, default=6)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--future-budget", type=int, default=6)
    parser.add_argument("--backgrounds", type=int, default=8)
    args = parser.parse_args()

    for key_width in [int(x) for x in args.key_widths.split(",") if x.strip()]:
        sweep(args, key_width)


if __name__ == "__main__":
    main()
