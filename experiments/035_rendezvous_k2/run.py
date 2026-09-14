#!/usr/bin/env python3
import argparse


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


def nonoverlap(i, j, width, size):
    left = {(i + x) % size for x in range(width)}
    right = {(j + x) % size for x in range(width)}
    return left.isdisjoint(right)


def rendezvous_pairs(state, size, key_width):
    buckets = {}
    for pos in range(size):
        key = read_window(state, pos, key_width, size)
        buckets.setdefault(key, []).append(pos)

    pairs = []
    for key, positions in buckets.items():
        if rotl(key, key_width) == key and rotr(key, key_width) == key:
            continue
        for a in range(len(positions)):
            for b in range(a + 1, len(positions)):
                i, j = positions[a], positions[b]
                if nonoverlap(i, j, key_width, size):
                    pairs.append((i, j, key))
    return pairs


def choose_pair(pairs, policy):
    if not pairs:
        return None
    if policy == "min":
        return min(pairs, key=lambda x: (x[0], x[1], x[2]))
    if policy == "max":
        return max(pairs, key=lambda x: (x[0], x[1], x[2]))
    raise ValueError(policy)


def step(state, size, key_width, policy):
    pair = choose_pair(rendezvous_pairs(state, size, key_width), policy)
    if pair is None:
        return state, None
    i, j, key = pair
    state = write_window(state, i, rotl(key, key_width), key_width, size)
    state = write_window(state, j, rotr(key, key_width), key_width, size)
    return state, pair


def run_budget(state, budget, size, key_width, policy, trace=False):
    events = []
    for _ in range(budget):
        state, event = step(state, size, key_width, policy)
        if trace:
            events.append(event)
    return (state, tuple(events)) if trace else state


def inject(state, pos, value, width, size):
    return write_window(state, pos, value, width, size)


def train(sequence, pos, args, policy):
    state = 1 << (args.size // 2)
    for value in sequence:
        state = inject(state, pos, value, args.core_width, args.size)
        state = run_budget(
            state, args.event_budget, args.size, args.key_width, policy
        )
    return state


def transplant(state, donor, pos, width, radius, size):
    out = state
    for j in range(width + 2 * radius):
        index = (pos - radius + j) % size
        target = bit(donor, index, size)
        if bit(out, index, size) != target:
            out ^= 1 << index
    return out


def trace_distance(a, b):
    return sum(x != y for x, y in zip(a, b))


def main():
    parser = argparse.ArgumentParser(description="Experiment 035: dynamic rendezvous K2.")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=32)
    parser.add_argument("--cascade-budget", type=int, default=16)
    parser.add_argument("--endpoint-radius", type=int, default=0)
    args = parser.parse_args()

    order_relation_diff = 0
    order_trace_diff = 0
    order_cases = 0

    eligible = first_exact = second_exact = both_exact = both_only = joint_better = 0

    for policy in ("min", "max"):
        for pos in range(0, args.size, 8):
            for a in range(1 << (args.core_width - 1)):
                b = a ^ ((1 << args.core_width) - 1)
                seq1 = (a, a, a, b, b)
                seq2 = (b, b, a, a, a)
                s1 = train(seq1, pos, args, policy)
                s2 = train(seq2, pos, args, policy)
                order_cases += 1
                order_relation_diff += int(
                    set(rendezvous_pairs(s1, args.size, args.key_width))
                    != set(rendezvous_pairs(s2, args.size, args.key_width))
                )
                _, tr1 = run_budget(
                    s1, 32, args.size, args.key_width, policy, trace=True
                )
                _, tr2 = run_budget(
                    s2, 32, args.size, args.key_width, policy, trace=True
                )
                order_trace_diff += int(tr1 != tr2)

                for recipient, donor in ((s1, s2), (s2, s1)):
                    donor_pair = choose_pair(
                        rendezvous_pairs(donor, args.size, args.key_width), policy
                    )
                    if donor_pair is None:
                        continue
                    _, recipient_trace = run_budget(
                        recipient, args.cascade_budget,
                        args.size, args.key_width, policy, trace=True,
                    )
                    _, donor_trace = run_budget(
                        donor, args.cascade_budget,
                        args.size, args.key_width, policy, trace=True,
                    )
                    if recipient_trace == donor_trace:
                        continue
                    eligible += 1
                    i, j, _ = donor_pair
                    left = transplant(
                        recipient, donor, i, args.key_width,
                        args.endpoint_radius, args.size,
                    )
                    right = transplant(
                        recipient, donor, j, args.key_width,
                        args.endpoint_radius, args.size,
                    )
                    both = transplant(
                        left, donor, j, args.key_width,
                        args.endpoint_radius, args.size,
                    )
                    _, tl = run_budget(left, args.cascade_budget, args.size, args.key_width, policy, trace=True)
                    _, tr = run_budget(right, args.cascade_budget, args.size, args.key_width, policy, trace=True)
                    _, tb = run_budget(both, args.cascade_budget, args.size, args.key_width, policy, trace=True)
                    first_exact += int(tl == donor_trace)
                    second_exact += int(tr == donor_trace)
                    both_exact += int(tb == donor_trace)
                    both_only += int(tb == donor_trace and tl != donor_trace and tr != donor_trace)
                    joint_better += int(
                        trace_distance(tb, donor_trace)
                        < min(trace_distance(tl, donor_trace), trace_distance(tr, donor_trace))
                    )

    print(f"equal_budget_order_cases={order_cases}")
    print(f"relation_repertoire_diff={order_relation_diff}")
    print(f"future_trace_diff={order_trace_diff}")
    print(f"causal_eligible={eligible}")
    print(f"first_endpoint_exact={first_exact}")
    print(f"second_endpoint_exact={second_exact}")
    print(f"both_endpoints_exact={both_exact}")
    print(f"both_only_exact={both_only}")
    print(f"joint_better_than_both_singles={joint_better}")


if __name__ == "__main__":
    main()
