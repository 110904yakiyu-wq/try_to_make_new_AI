#!/usr/bin/env python3
import argparse
import itertools
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


def prepare_groups(size, width, max_arity):
    windows = [{(p + j) % size for j in range(width)} for p in range(size)]
    groups = {}
    for arity in range(2, max_arity + 1):
        items = []
        for positions in itertools.combinations(range(size), arity):
            used = set()
            ok = True
            for pos in positions:
                if used & windows[pos]:
                    ok = False
                    break
                used |= windows[pos]
            if ok:
                items.append(positions)
        groups[arity] = items
    return groups


def event_from(state, positions, width, size):
    values = tuple(read_window(state, p, width, size) for p in positions)
    xor_value = 0
    for value in values:
        xor_value ^= value
    if xor_value != 0:
        return None

    mask = (1 << width) - 1
    field = rotl(sum(values) & mask, width)
    outputs = tuple((value + field) & mask for value in values)
    if outputs == values:
        return None

    # Stateless ordering; arity is not an explicit priority term.
    key = (
        sum(values),
        sum(value * value for value in values),
        math.prod(value + 1 for value in values),
        tuple(sorted(values)),
        positions,
    )
    return key, positions, values, outputs, field


def choose_event(state, size, width, groups, policy):
    best = None
    for positions_by_arity in groups.values():
        for positions in positions_by_arity:
            event = event_from(state, positions, width, size)
            if event is None:
                continue
            if best is None:
                best = event
            elif policy == "min" and event[0] < best[0]:
                best = event
            elif policy == "max" and event[0] > best[0]:
                best = event
    return best


def step(state, size, width, groups, policy):
    event = choose_event(state, size, width, groups, policy)
    if event is None:
        return state, None
    _, positions, values, outputs, field = event
    for pos, value in zip(positions, outputs):
        state = write_window(state, pos, value, width, size)
    return state, (positions, values, outputs, field)


def run_budget(state, budget, size, width, groups, policy, trace=False):
    events = []
    for _ in range(budget):
        state, event = step(state, size, width, groups, policy)
        if trace:
            events.append(event)
    return (state, tuple(events)) if trace else state


def train(sequence, pos, initial, args, groups, policy):
    state = initial
    for value in sequence:
        state = write_window(state, pos, value, args.core_width, args.size)
        state = run_budget(
            state, args.event_budget, args.size, args.key_width, groups, policy
        )
    return state


def repertoire(state, args, groups):
    out = set()
    for arity, positions_by_arity in groups.items():
        for positions in positions_by_arity:
            event = event_from(state, positions, args.key_width, args.size)
            if event is not None:
                values = event[2]
                out.add((arity, tuple(sorted(values))))
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
    args.key_width = key_width
    groups = prepare_groups(args.size, args.key_width, args.max_arity)
    counts = Counter()
    arity_pair_counts = Counter()
    arity_diff = 0
    trace_diff = 0
    cases = 0

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(args.size)
        for policy in ("min", "max"):
            for pos in range(0, args.size, args.position_stride):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    s1 = train((a, a, a, b, b), pos, initial, args, groups, policy)
                    s2 = train((b, b, a, a, a), pos, initial, args, groups, policy)
                    r1 = repertoire(s1, args, groups)
                    r2 = repertoire(s2, args, groups)
                    counts[relation(r1, r2)] += 1

                    arities1 = frozenset(arity for arity, _ in r1)
                    arities2 = frozenset(arity for arity, _ in r2)
                    arity_diff += int(arities1 != arities2)
                    arity_pair_counts[(tuple(sorted(arities1)), tuple(sorted(arities2)))] += 1

                    _, t1 = run_budget(
                        s1, args.future_budget, args.size, args.key_width,
                        groups, policy, trace=True,
                    )
                    _, t2 = run_budget(
                        s2, args.future_budget, args.size, args.key_width,
                        groups, policy, trace=True,
                    )
                    trace_diff += int(t1 != t2)
                    cases += 1

    print(f"key_width={key_width}")
    print(f"cases={cases}")
    print(f"same={counts['same']}")
    print(f"seq1_superset={counts['seq1_superset']}")
    print(f"seq2_superset={counts['seq2_superset']}")
    print(f"reorganize={counts['reorganize']}")
    print(f"arity_repertoire_diff={arity_diff}")
    print(f"future_trace_diff={trace_diff}")
    for pair, count in arity_pair_counts.most_common(12):
        print(f"arity_transition={pair[0]}->{pair[1]} count={count}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Experiment 054: variable-arity K7.")
    parser.add_argument("--size", type=int, default=20)
    parser.add_argument("--key-widths", default="3,4,5")
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--max-arity", type=int, default=4)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--future-budget", type=int, default=6)
    parser.add_argument("--position-stride", type=int, default=5)
    parser.add_argument("--backgrounds", type=int, default=8)
    args = parser.parse_args()

    for key_width in [int(x) for x in args.key_widths.split(",") if x.strip()]:
        sweep(args, key_width)


if __name__ == "__main__":
    main()
