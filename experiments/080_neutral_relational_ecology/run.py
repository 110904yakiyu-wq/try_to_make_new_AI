#!/usr/bin/env python3
import argparse
import random
import statistics
from collections import Counter


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


def ecology_run(seed, noise, args, collect_occupancy=False):
    rng = random.Random(seed)
    state = [rng.randrange(args.symbols) for _ in range(args.size)]
    previous = set(pair_counts(state))
    ever = set(previous)
    previous_dominant = None

    births = 0
    deaths = 0
    reappearances = 0
    dominant_switches = 0
    pair_numbers = []
    dominance = []
    jaccard = []
    occupancy = Counter()

    for _ in range(args.steps):
        state, _ = parallel_sweep(state)
        for _ in range(noise):
            state = mutate_one(state, rng, args.symbols)

        counts = pair_counts(state)
        current = set(counts)
        born = current - previous
        gone = previous - current

        births += len(born)
        deaths += len(gone)
        reappearances += sum(pair in ever for pair in born)
        ever |= current

        union = previous | current
        jaccard.append(len(previous & current) / len(union) if union else 1.0)
        pair_numbers.append(len(current))

        if counts:
            dominant = max(counts, key=lambda pair: (counts[pair], pair))
            total = sum(counts.values())
            dominance.append(counts[dominant] / total)
        else:
            dominant = None
            dominance.append(0.0)

        if (
            previous_dominant is not None
            and dominant is not None
            and dominant != previous_dominant
        ):
            dominant_switches += 1
        previous_dominant = dominant

        if collect_occupancy:
            for pair in current:
                occupancy[pair] += 1

        previous = current

    tail = args.tail
    result = {
        "births_per_sweep": births / args.steps,
        "deaths_per_sweep": deaths / args.steps,
        "reappearances_per_sweep": reappearances / args.steps,
        "dominant_switches_per_sweep": dominant_switches / args.steps,
        "mean_active_pairs": statistics.mean(pair_numbers[-tail:]),
        "mean_dominant_pair_fraction": statistics.mean(dominance[-tail:]),
        "mean_pairset_jaccard": statistics.mean(jaccard[-tail:]),
        "ever_seen_pairs": len(ever),
    }
    return result, occupancy


def two_domain_static_control(args):
    half = args.size // 2
    state = []
    for i in range(args.size):
        if i < half:
            state.append(0 if i % 2 == 0 else 1)
        else:
            state.append(2 if (i - half) % 2 == 0 else 3)
    initial = pair_counts(state)
    for _ in range(args.domain_sweeps):
        state, _ = parallel_sweep(state)
    return initial, pair_counts(state)


def main():
    parser = argparse.ArgumentParser(description="Experiment 080: neutral relational ecology.")
    parser.add_argument("--size", type=int, default=96)
    parser.add_argument("--symbols", type=int, default=8)
    parser.add_argument("--steps", type=int, default=1500)
    parser.add_argument("--tail", type=int, default=500)
    parser.add_argument("--seeds", type=int, default=32)
    parser.add_argument("--occupancy-seeds", type=int, default=64)
    parser.add_argument("--noise", default="0,1,2,4")
    parser.add_argument("--domain-sweeps", type=int, default=100)
    args = parser.parse_args()

    initial, final = two_domain_static_control(args)
    print(f"static_domain_initial={dict(sorted(initial.items()))}")
    print(f"static_domain_final={dict(sorted(final.items()))}")

    for noise in [int(x) for x in args.noise.split(",") if x.strip()]:
        values = []
        for seed in range(args.seeds):
            result, _ = ecology_run(seed, noise, args)
            values.append(result)
        print(f"noise={noise}")
        for key in values[0]:
            print(f"{key}={statistics.mean(v[key] for v in values):.6f}")

    aggregate = Counter()
    for seed in range(args.occupancy_seeds):
        _, occupancy = ecology_run(seed, 1, args, collect_occupancy=True)
        aggregate.update(occupancy)

    fractions = []
    denom = args.occupancy_seeds * args.steps
    for a in range(args.symbols):
        for b in range(a + 1, args.symbols):
            fractions.append(aggregate[(a, b)] / denom)
    mean = statistics.mean(fractions)
    stdev = statistics.pstdev(fractions)
    print(f"noise1_pair_occupancy_min={min(fractions):.9f}")
    print(f"noise1_pair_occupancy_max={max(fractions):.9f}")
    print(f"noise1_pair_occupancy_mean={mean:.9f}")
    print(f"noise1_pair_occupancy_cv={stdev / mean:.9f}")


if __name__ == "__main__":
    main()
