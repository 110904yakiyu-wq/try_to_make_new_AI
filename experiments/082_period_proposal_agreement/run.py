#!/usr/bin/env python3
import argparse
import random
import statistics
from collections import Counter


def mutate_one(state, rng, symbols):
    state = state[:]
    i = rng.randrange(len(state))
    old = state[i]
    r = rng.randrange(symbols - 1)
    state[i] = r if r < old else r + 1
    return state


def sweep(state, min_period, max_period):
    old = state
    new = state[:]
    n = len(state)
    events = 0
    conflicts = 0

    for target in range(n):
        proposals = []
        for p in range(min_period, max_period + 1):
            same = True
            for j in range(p):
                if old[(target - 2 * p + j) % n] != old[(target - p + j) % n]:
                    same = False
                    break
            if not same:
                continue
            expected = old[(target - p) % n]
            if expected != old[target]:
                proposals.append(expected)

        if not proposals:
            continue
        if all(value == proposals[0] for value in proposals):
            new[target] = proposals[0]
            events += 1
        else:
            conflicts += 1

    return new, events, conflicts


def period_coverage(state, min_period, max_period):
    """Observer-side minimal persistent period over three equal blocks."""
    n = len(state)
    counts = Counter()
    for target in range(n):
        for p in range(min_period, max_period + 1):
            ok = True
            for j in range(p):
                reference = state[(target - p + j) % n]
                if (
                    state[(target - 2 * p + j) % n] != reference
                    or state[(target - 3 * p + j) % n] != reference
                ):
                    ok = False
                    break
            if ok:
                counts[p] += 1
                break
    return counts


def run_one(seed, noise, args):
    rng = random.Random(seed)
    state = [rng.randrange(args.symbols) for _ in range(args.size)]
    events = []
    conflicts = []
    samples = []

    sample_start = args.steps - args.tail_samples * args.sample_every
    for step in range(args.steps):
        state, event_count, conflict_count = sweep(
            state, args.min_period, args.max_period
        )
        for _ in range(noise):
            state = mutate_one(state, rng, args.symbols)
        events.append(event_count)
        conflicts.append(conflict_count)
        if step >= sample_start and step % args.sample_every == 0:
            samples.append(
                period_coverage(state, args.min_period, args.max_period)
            )

    means = {
        p: statistics.mean(sample[p] for sample in samples)
        for p in range(args.min_period, args.max_period + 1)
    }
    active_types = statistics.mean(len(sample) for sample in samples)
    return (
        means,
        statistics.mean(events[-args.tail_events:]),
        statistics.mean(conflicts[-args.tail_events:]),
        active_types,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 082: remove period-priority tie breaking."
    )
    parser.add_argument("--size", type=int, default=120)
    parser.add_argument("--symbols", type=int, default=8)
    parser.add_argument("--min-period", type=int, default=2)
    parser.add_argument("--max-period", type=int, default=8)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--seeds", type=int, default=16)
    parser.add_argument("--noise", default="0,1,2,4")
    parser.add_argument("--tail-events", type=int, default=200)
    parser.add_argument("--tail-samples", type=int, default=20)
    parser.add_argument("--sample-every", type=int, default=10)
    args = parser.parse_args()

    for noise in [int(x) for x in args.noise.split(",") if x.strip()]:
        values = [run_one(seed, noise, args) for seed in range(args.seeds)]
        print(f"noise={noise}")
        print(f"mean_events={statistics.mean(v[1] for v in values):.6f}")
        print(f"mean_conflicts={statistics.mean(v[2] for v in values):.6f}")
        print(f"mean_active_period_types={statistics.mean(v[3] for v in values):.6f}")
        for p in range(args.min_period, args.max_period + 1):
            print(
                f"period={p} mean_coverage="
                f"{statistics.mean(v[0][p] for v in values):.6f}"
            )


if __name__ == "__main__":
    main()
