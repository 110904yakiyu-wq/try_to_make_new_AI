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


def prepare_disjoint(size, width):
    windows = [
        {(pos + j) % size for j in range(width)}
        for pos in range(size)
    ]
    return [
        [windows[i].isdisjoint(windows[j]) for j in range(size)]
        for i in range(size)
    ]


def choose_triple(state, size, width, policy, disjoint):
    values = [read_window(state, pos, width, size) for pos in range(size)]

    if policy == "min":
        irange = range(size)
        for i in irange:
            for j in range(i + 1, size):
                if not disjoint[i][j]:
                    continue
                pair_parity = (values[i] ^ values[j]).bit_count() & 1
                for m in range(size):
                    if m == i or m == j:
                        continue
                    if not disjoint[i][m] or not disjoint[j][m]:
                        continue
                    if ((values[m].bit_count() & 1) ^ pair_parity) == 0:
                        return (i, j, m, values[i], values[j], values[m])
    elif policy == "max":
        for i in range(size - 2, -1, -1):
            for j in range(size - 1, i, -1):
                if not disjoint[i][j]:
                    continue
                pair_parity = (values[i] ^ values[j]).bit_count() & 1
                for m in range(size - 1, -1, -1):
                    if m == i or m == j:
                        continue
                    if not disjoint[i][m] or not disjoint[j][m]:
                        continue
                    if ((values[m].bit_count() & 1) ^ pair_parity) == 0:
                        return (i, j, m, values[i], values[j], values[m])
    else:
        raise ValueError(policy)

    return None


def rewrite(a, b, m, width):
    mask = (1 << width) - 1
    a2 = (a ^ m) & mask
    b2 = (b ^ rotl(m, width)) & mask
    m2 = (m ^ (a & b)) & mask
    return a2, b2, m2


def step(state, size, width, policy, disjoint):
    event = choose_triple(state, size, width, policy, disjoint)
    if event is None:
        return state, None

    i, j, mpos, a, b, m = event
    a2, b2, m2 = rewrite(a, b, m, width)
    state = write_window(state, i, a2, width, size)
    state = write_window(state, j, b2, width, size)
    state = write_window(state, mpos, m2, width, size)
    return state, (i, j, mpos, a, b, m, a2, b2, m2)


def run_budget(state, budget, size, width, policy, disjoint, trace=False):
    events = []
    for _ in range(budget):
        state, event = step(state, size, width, policy, disjoint)
        if trace:
            events.append(event)
    return (state, tuple(events)) if trace else state


def train(sequence, pos, args, policy, disjoint):
    state = 1 << (args.size // 2)
    for value in sequence:
        state = write_window(state, pos, value, args.core_width, args.size)
        state = run_budget(
            state, args.event_budget, args.size, args.key_width,
            policy, disjoint,
        )
    return state


def mediator_values(state, size, width):
    return {read_window(state, pos, width, size) for pos in range(size)}


def transformation_grammar(state, size, width):
    mediators = mediator_values(state, size, width)
    grammar = set()
    for a in range(1 << width):
        for b in range(1 << width):
            pair_parity = (a ^ b).bit_count() & 1
            for m in mediators:
                if ((m.bit_count() & 1) ^ pair_parity) != 0:
                    continue
                a2, b2, _ = rewrite(a, b, m, width)
                grammar.add((a, b, a2, b2))
    return frozenset(grammar)


def relation(left, right):
    if left == right:
        return "same"
    if left < right:
        return "seq2_superset"
    if right < left:
        return "seq1_superset"
    return "reorganize"


def trace_distance(left, right):
    return sum(a != b for a, b in zip(left, right))


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 045: mediator-conditioned rewrite K5."
    )
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=8)
    parser.add_argument("--future-budget", type=int, default=8)
    parser.add_argument("--position-stride", type=int, default=8)
    args = parser.parse_args()

    disjoint = prepare_disjoint(args.size, args.key_width)
    counts = Counter()
    trace_diff = 0
    total = 0
    samples = []

    for policy in ("min", "max"):
        for pos in range(0, args.size, args.position_stride):
            for a in range(1 << (args.core_width - 1)):
                b = a ^ ((1 << args.core_width) - 1)
                seq1 = (a, a, a, b, b)
                seq2 = (b, b, a, a, a)

                s1 = train(seq1, pos, args, policy, disjoint)
                s2 = train(seq2, pos, args, policy, disjoint)
                g1 = transformation_grammar(s1, args.size, args.key_width)
                g2 = transformation_grammar(s2, args.size, args.key_width)
                counts[relation(g1, g2)] += 1

                _, t1 = run_budget(
                    s1, args.future_budget, args.size, args.key_width,
                    policy, disjoint, trace=True,
                )
                _, t2 = run_budget(
                    s2, args.future_budget, args.size, args.key_width,
                    policy, disjoint, trace=True,
                )
                trace_diff += int(t1 != t2)
                total += 1
                samples.append((policy, pos, a, s1, s2, t1, t2))

    directed = 0
    same_relation = 0
    exact_first = 0
    improved_trace = 0
    exact_trace = 0

    for policy, pos, a, s1, s2, t1, t2 in samples:
        e1 = choose_triple(s1, args.size, args.key_width, policy, disjoint)
        e2 = choose_triple(s2, args.size, args.key_width, policy, disjoint)
        if e1 is None or e2 is None:
            continue

        # Isolated subset: identical endpoint positions and A/B contents,
        # but a different selected mediator value.
        if e1[:2] != e2[:2] or e1[3:5] != e2[3:5] or e1[5] == e2[5]:
            continue

        for donor, recipient, donor_event, donor_trace, recipient_trace in (
            (s1, s2, e1, t1, t2),
            (s2, s1, e2, t2, t1),
        ):
            i, j, mpos, aval, bval, mval = donor_event
            if read_window(recipient, i, args.key_width, args.size) != aval:
                continue
            if read_window(recipient, j, args.key_width, args.size) != bval:
                continue

            directed += 1
            transplanted = write_window(
                recipient, mpos, mval, args.key_width, args.size
            )
            selected = choose_triple(
                transplanted, args.size, args.key_width, policy, disjoint
            )
            _, new_trace = run_budget(
                transplanted, args.future_budget, args.size, args.key_width,
                policy, disjoint, trace=True,
            )

            if selected is not None:
                same_relation += int(
                    selected[:2] == donor_event[:2]
                    and selected[3:6] == donor_event[3:6]
                )
                exact_first += int(selected == donor_event)

            before = trace_distance(recipient_trace, donor_trace)
            after = trace_distance(new_trace, donor_trace)
            improved_trace += int(after < before)
            exact_trace += int(new_trace == donor_trace)

    print(f"cases={total}")
    print(f"same={counts['same']}")
    print(f"seq1_superset={counts['seq1_superset']}")
    print(f"seq2_superset={counts['seq2_superset']}")
    print(f"reorganize={counts['reorganize']}")
    print(f"future_trace_diff={trace_diff}")
    print(f"isolated_directed_transfers={directed}")
    print(f"same_endpoint_relation_after_m_transfer={same_relation}")
    print(f"exact_first_event_after_m_transfer={exact_first}")
    print(f"future_trace_improved={improved_trace}")
    print(f"exact_future_trace_transfer={exact_trace}")


if __name__ == "__main__":
    main()
