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
    """Extend the shortest locally repeated block by one symbol.

    For each target t, find the smallest p for which the two immediately
    preceding length-p blocks are equal. If the current target disagrees with
    the periodic continuation, copy the expected symbol into t.

    The rule is symbol-permutation equivariant, but it is *not* period
    symmetric because it explicitly chooses the shortest eligible p.
    """
    old = state
    new = state[:]
    n = len(state)
    events = 0
    used_periods = Counter()

    for t in range(n):
        chosen = None
        for p in range(min_period, max_period + 1):
            left = tuple(old[(t - 2 * p + j) % n] for j in range(p))
            right = tuple(old[(t - p + j) % n] for j in range(p))
            if left == right:
                chosen = p
                break
        if chosen is None:
            continue
        expected = old[(t - chosen) % n]
        if old[t] != expected:
            new[t] = expected
            events += 1
            used_periods[chosen] += 1

    return new, events, used_periods


def local_min_period(state, target, min_period, max_period):
    """Observer-side persistent local period: three matching blocks."""
    n = len(state)
    for p in range(min_period, max_period + 1):
        reference = tuple(state[(target - p + j) % n] for j in range(p))
        ok = True
        for block_back in (2, 3):
            block = tuple(
                state[(target - block_back * p + j) % n] for j in range(p)
            )
            if block != reference:
                ok = False
                break
        if ok:
            return p
    return None


def period_coverage(state, min_period, max_period):
    counts = Counter()
    for target in range(len(state)):
        p = local_min_period(state, target, min_period, max_period)
        if p is not None:
            counts[p] += 1
    return counts


def run_one(seed, noise, args):
    rng = random.Random(seed)
    state = [rng.randrange(args.symbols) for _ in range(args.size)]
    coverages = []
    events = []
    active_types = []

    for _ in range(args.steps):
        state, event_count, _ = sweep(state, args.min_period, args.max_period)
        for _ in range(noise):
            state = mutate_one(state, rng, args.symbols)
        coverage = period_coverage(state, args.min_period, args.max_period)
        coverages.append(coverage)
        events.append(event_count)
        active_types.append(len(coverage))

    tail = args.tail
    means = {
        p: statistics.mean(c[p] for c in coverages[-tail:])
        for p in range(args.min_period, args.max_period + 1)
    }
    return means, statistics.mean(events[-tail:]), statistics.mean(active_types[-tail:])


def main():
    parser = argparse.ArgumentParser(description="Experiment 081: shortest-repeat bias audit.")
    parser.add_argument("--size", type=int, default=120)
    parser.add_argument("--symbols", type=int, default=8)
    parser.add_argument("--min-period", type=int, default=2)
    parser.add_argument("--max-period", type=int, default=8)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--tail", type=int, default=200)
    parser.add_argument("--seeds", type=int, default=16)
    parser.add_argument("--noise", default="0,1,2,4")
    args = parser.parse_args()

    for noise in [int(x) for x in args.noise.split(",") if x.strip()]:
        values = [run_one(seed, noise, args) for seed in range(args.seeds)]
        print(f"noise={noise}")
        print(f"mean_events={statistics.mean(v[1] for v in values):.6f}")
        print(f"mean_active_period_types={statistics.mean(v[2] for v in values):.6f}")
        for p in range(args.min_period, args.max_period + 1):
            print(
                f"period={p} mean_coverage="
                f"{statistics.mean(v[0][p] for v in values):.6f}"
            )


if __name__ == "__main__":
    main()
