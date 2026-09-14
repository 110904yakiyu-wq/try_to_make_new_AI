#!/usr/bin/env python3
import argparse
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
    return ((value << 1) & ((1 << width) - 1)) | (value >> (width - 1))


def prepare_disjoint(size, width):
    windows = [{(p + j) % size for j in range(width)} for p in range(size)]
    return [[windows[i].isdisjoint(windows[j]) for j in range(size)] for i in range(size)]


def compatible(a, b, c):
    return (a.bit_count() + b.bit_count() + c.bit_count()) % 3 == 0


def choose_triple(state, size, width, policy, disjoint):
    values = [read_window(state, p, width, size) for p in range(size)]
    best = None
    best_key = None
    for i in range(size):
        for j in range(i + 1, size):
            if not disjoint[i][j]:
                continue
            for k in range(j + 1, size):
                if not disjoint[i][k] or not disjoint[j][k]:
                    continue
                a, b, c = values[i], values[j], values[k]
                if not compatible(a, b, c):
                    continue
                key = (a + b + c, a ^ b ^ c, tuple(sorted((a, b, c))), i, j, k)
                if best is None or (policy == "min" and key < best_key) or (policy == "max" and key > best_key):
                    best = (i, j, k, a, b, c)
                    best_key = key
    return best


def rewrite(a, b, c, width):
    return rotl(b ^ c, width), rotl(a ^ c, width), rotl(a ^ b, width)


def step(state, size, width, policy, disjoint):
    event = choose_triple(state, size, width, policy, disjoint)
    if event is None:
        return state, None
    i, j, k, a, b, c = event
    a2, b2, c2 = rewrite(a, b, c, width)
    state = write_window(state, i, a2, width, size)
    state = write_window(state, j, b2, width, size)
    state = write_window(state, k, c2, width, size)
    return state, (i, j, k, a, b, c, a2, b2, c2)


def run_budget(state, budget, size, width, policy, disjoint, trace=False):
    events = []
    for _ in range(budget):
        state, event = step(state, size, width, policy, disjoint)
        if trace:
            events.append(event)
    return (state, tuple(events)) if trace else state


def train(sequence, pos, initial, args, policy, disjoint):
    state = initial
    for value in sequence:
        state = write_window(state, pos, value, args.core_width, args.size)
        state = run_budget(state, args.event_budget, args.size, args.key_width, policy, disjoint)
    return state


def repertoire(state, size, width, disjoint):
    values = [read_window(state, p, width, size) for p in range(size)]
    out = set()
    for i in range(size):
        for j in range(i + 1, size):
            if not disjoint[i][j]:
                continue
            for k in range(j + 1, size):
                if not disjoint[i][k] or not disjoint[j][k]:
                    continue
                a, b, c = values[i], values[j], values[k]
                if compatible(a, b, c):
                    out.add(tuple(sorted((a, b, c))))
    return frozenset(out)


def relation(left, right):
    if left == right:
        return "same"
    if left < right:
        return "seq2_superset"
    if right < left:
        return "seq1_superset"
    return "reorganize"


def main():
    parser = argparse.ArgumentParser(description="Experiment 050: role-symmetric K6.")
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=8)
    parser.add_argument("--future-budget", type=int, default=8)
    parser.add_argument("--backgrounds", type=int, default=8)
    args = parser.parse_args()

    disjoint = prepare_disjoint(args.size, args.key_width)
    counts = Counter()
    turnover = Counter()
    trace_diff = 0
    cases = 0

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(args.size)
        for policy in ("min", "max"):
            for pos in range(0, args.size, 8):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    s1 = train((a, a, a, b, b), pos, initial, args, policy, disjoint)
                    s2 = train((b, b, a, a, a), pos, initial, args, policy, disjoint)
                    counts[relation(repertoire(s1, args.size, args.key_width, disjoint), repertoire(s2, args.size, args.key_width, disjoint))] += 1
                    _, t1 = run_budget(s1, args.future_budget, args.size, args.key_width, policy, disjoint, trace=True)
                    _, t2 = run_budget(s2, args.future_budget, args.size, args.key_width, policy, disjoint, trace=True)
                    trace_diff += int(t1 != t2)
                    cases += 1

                    for state in (s1, s2):
                        e1 = choose_triple(state, args.size, args.key_width, policy, disjoint)
                        state2, _ = step(state, args.size, args.key_width, policy, disjoint)
                        e2 = choose_triple(state2, args.size, args.key_width, policy, disjoint)
                        if e1 is not None and e2 is not None:
                            turnover[len(set(e1[:3]) & set(e2[:3]))] += 1

    print(f"cases={cases}")
    print(f"same={counts['same']}")
    print(f"seq1_superset={counts['seq1_superset']}")
    print(f"seq2_superset={counts['seq2_superset']}")
    print(f"reorganize={counts['reorganize']}")
    print(f"future_trace_diff={trace_diff}")
    for overlap in (3, 2, 1, 0):
        print(f"event_endpoint_overlap_{overlap}={turnover[overlap]}")


if __name__ == "__main__":
    main()
