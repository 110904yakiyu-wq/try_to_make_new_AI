#!/usr/bin/env python3
import argparse
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
    return ((value << 1) & ((1 << width) - 1)) | (value >> (width - 1))


def rotr(value, width):
    return (value >> 1) | ((value & 1) << (width - 1))


def nonoverlap3(i, j, m, width, size):
    a = {(i + x) % size for x in range(width)}
    b = {(j + x) % size for x in range(width)}
    c = {(m + x) % size for x in range(width)}
    return a.isdisjoint(b) and a.isdisjoint(c) and b.isdisjoint(c)


def choose_triple(state, size, key_width, policy):
    values = [read_window(state, pos, key_width, size) for pos in range(size)]
    buckets = {}
    for pos, value in enumerate(values):
        buckets.setdefault(value, []).append(pos)

    best = None
    for i in range(size):
        a = values[i]
        for j in range(i + 1, size):
            b = values[j]
            mediator = a ^ b
            for m in buckets.get(mediator, []):
                if m == i or m == j:
                    continue
                if not nonoverlap3(i, j, m, key_width, size):
                    continue
                candidate = (i, j, m, a, b, mediator)
                if best is None:
                    best = candidate
                elif policy == "min" and candidate[:3] < best[:3]:
                    best = candidate
                elif policy == "max" and candidate[:3] > best[:3]:
                    best = candidate
    return best


def step(state, size, key_width, policy):
    event = choose_triple(state, size, key_width, policy)
    if event is None:
        return state, None
    i, j, m, a, b, mediator = event
    state = write_window(state, i, rotl(a, key_width), key_width, size)
    state = write_window(state, j, rotr(b, key_width), key_width, size)
    state = write_window(
        state, m, mediator ^ ((1 << key_width) - 1), key_width, size
    )
    return state, event


def run_budget(state, budget, size, key_width, policy, trace=False):
    events = []
    for _ in range(budget):
        state, event = step(state, size, key_width, policy)
        if trace:
            events.append(event)
    return (state, tuple(events)) if trace else state


def train(sequence, pos, args, policy):
    state = 1 << (args.size // 2)
    for value in sequence:
        state = write_window(state, pos, value, args.core_width, args.size)
        state = run_budget(
            state, args.event_budget, args.size, args.key_width, policy
        )
    return state


def mediator_values(state, size, key_width):
    return {
        read_window(state, pos, key_width, size)
        for pos in range(size)
    }


def effective_pair_grammar(state, size, key_width):
    mediators = mediator_values(state, size, key_width)
    return frozenset(
        (a, b)
        for a in range(1 << key_width)
        for b in range(a + 1, 1 << key_width)
        if (a ^ b) in mediators
    )


def relation(left, right):
    if left == right:
        return "same"
    if left < right:
        return "seq2_superset"
    if right < left:
        return "seq1_superset"
    return "reorganize"


def main():
    parser = argparse.ArgumentParser(description="Experiment 041: mediated relation grammar K3.")
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=8)
    parser.add_argument("--future-budget", type=int, default=8)
    args = parser.parse_args()

    counts = Counter()
    trace_diff = 0
    total = 0

    for policy in ("min", "max"):
        for pos in range(0, args.size, 8):
            for a in range(1 << (args.core_width - 1)):
                b = a ^ ((1 << args.core_width) - 1)
                seq1 = (a, a, a, b, b)
                seq2 = (b, b, a, a, a)
                s1 = train(seq1, pos, args, policy)
                s2 = train(seq2, pos, args, policy)
                g1 = effective_pair_grammar(s1, args.size, args.key_width)
                g2 = effective_pair_grammar(s2, args.size, args.key_width)
                counts[relation(g1, g2)] += 1
                _, t1 = run_budget(
                    s1, args.future_budget, args.size, args.key_width, policy, trace=True
                )
                _, t2 = run_budget(
                    s2, args.future_budget, args.size, args.key_width, policy, trace=True
                )
                trace_diff += int(t1 != t2)
                total += 1

    print(f"cases={total}")
    print(f"same={counts['same']}")
    print(f"seq1_superset={counts['seq1_superset']}")
    print(f"seq2_superset={counts['seq2_superset']}")
    print(f"reorganize={counts['reorganize']}")
    print(f"future_trace_diff={trace_diff}")


if __name__ == "__main__":
    main()
