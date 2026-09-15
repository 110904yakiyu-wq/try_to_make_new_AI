#!/usr/bin/env python3
import argparse
import random
import statistics
from collections import Counter


def sequential_sweep(state):
    state = state[:]
    n = len(state)
    events = 0
    for i in range(n):
        a = state[i]
        b = state[(i + 1) % n]
        c = state[(i + 2) % n]
        d = state[(i + 3) % n]
        if a == c and a != b and d != b:
            state[(i + 3) % n] = b
            events += 1
    return state, events


def parallel_sweep(state):
    old = state
    new = state[:]
    n = len(state)
    events = 0
    for i in range(n):
        a = old[i]
        b = old[(i + 1) % n]
        c = old[(i + 2) % n]
        d = old[(i + 3) % n]
        if a == c and a != b and d != b:
            new[(i + 3) % n] = b
            events += 1
    return new, events


def mutate_one(state, rng, symbols):
    state = state[:]
    i = rng.randrange(len(state))
    old = state[i]
    r = rng.randrange(symbols - 1)
    state[i] = r if r < old else r + 1
    return state


def pair_counts(state):
    n = len(state)
    counts = Counter()
    for i in range(n):
        a = state[i]
        b = state[(i + 1) % n]
        c = state[(i + 2) % n]
        if a == c and a != b:
            counts[tuple(sorted((a, b)))] += 1
    return counts


def run_one(seed, mode, noise, args):
    rng = random.Random(seed)
    state = [rng.randrange(args.symbols) for _ in range(args.size)]
    pair_sets = []
    pair_numbers = []
    dominance = []
    events = []

    for _ in range(args.steps):
        if mode == "parallel":
            state, event_count = parallel_sweep(state)
        else:
            state, event_count = sequential_sweep(state)
        for _ in range(noise):
            state = mutate_one(state, rng, args.symbols)

        counts = pair_counts(state)
        pair_sets.append(set(counts))
        pair_numbers.append(len(counts))
        total = sum(counts.values())
        dominance.append(max(counts.values()) / total if total else 0.0)
        events.append(event_count)

    tail = args.tail
    recent_sets = pair_sets[-(tail + 1):]
    jaccard = []
    for left, right in zip(recent_sets[:-1], recent_sets[1:]):
        union = left | right
        jaccard.append(len(left & right) / len(union) if union else 1.0)

    return (
        statistics.mean(pair_numbers[-tail:]),
        statistics.mean(dominance[-tail:]),
        statistics.mean(jaccard),
        statistics.mean(events[-tail:]),
    )


def two_domain_control(args):
    half = args.size // 2
    state = []
    for i in range(args.size):
        if i < half:
            a, b = 0, 1
            state.append(a if i % 2 == 0 else b)
        else:
            a, b = 2, 3
            state.append(a if (i - half) % 2 == 0 else b)

    initial = pair_counts(state)
    for _ in range(args.domain_sweeps):
        state, _ = parallel_sweep(state)
    final = pair_counts(state)
    return initial, final


def main():
    parser = argparse.ArgumentParser(description="Experiment 079: parallel relational ecology.")
    parser.add_argument("--size", type=int, default=96)
    parser.add_argument("--symbols", type=int, default=8)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--tail", type=int, default=200)
    parser.add_argument("--seeds", type=int, default=32)
    parser.add_argument("--noise", default="0,1,2,4")
    parser.add_argument("--domain-sweeps", type=int, default=100)
    args = parser.parse_args()

    for noise in [int(x) for x in args.noise.split(",") if x.strip()]:
        for mode in ("sequential", "parallel"):
            values = [run_one(seed, mode, noise, args) for seed in range(args.seeds)]
            print(
                f"noise={noise} mode={mode} "
                f"mean_active_pairs={statistics.mean(v[0] for v in values):.6f} "
                f"mean_dominant_pair_fraction={statistics.mean(v[1] for v in values):.6f} "
                f"mean_pairset_jaccard={statistics.mean(v[2] for v in values):.6f} "
                f"mean_events={statistics.mean(v[3] for v in values):.6f}"
            )

    initial, final = two_domain_control(args)
    print(f"two_domain_initial={dict(sorted(initial.items()))}")
    print(f"two_domain_final={dict(sorted(final.items()))}")


if __name__ == "__main__":
    main()
