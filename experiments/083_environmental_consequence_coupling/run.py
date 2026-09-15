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


def repetition_sweep(state, min_period=2, max_period=8):
    old = state
    new = state[:]
    n = len(state)
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
        if proposals and all(value == proposals[0] for value in proposals):
            new[target] = proposals[0]
    return new


def rotate_blocks(state, block):
    out = state[:]
    n = len(state)
    for start in range(0, n, block):
        if start + block > n:
            break
        values = state[start:start + block]
        out[start:start + block] = values[1:] + values[:1]
    return out


def period_coverage(state, max_period=8):
    n = len(state)
    counts = Counter()
    for target in range(n):
        for p in range(2, max_period + 1):
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


def fixed_two_domain(size):
    half = size // 2
    state = []
    for i in range(half):
        state.append((0, 1)[i % 2])
    for i in range(half, size):
        state.append((2, 3, 4)[(i - half) % 3])
    return state


def randomized_two_domain(seed, size, symbols):
    rng = random.Random(seed)
    labels = list(range(symbols))
    rng.shuffle(labels)
    p2 = labels[:2]
    p3 = labels[2:5]
    half = size // 2
    phase2 = rng.randrange(2)
    phase3 = rng.randrange(3)
    state = []
    for i in range(half):
        state.append(p2[(i + phase2) % 2])
    for i in range(half, size):
        state.append(p3[(i - half + phase3) % 3])
    shift = rng.randrange(size)
    return state[shift:] + state[:shift]


def run_fixed_environment(block, interval, args):
    state = fixed_two_domain(args.size)
    p2 = []
    p3 = []
    for step in range(args.static_steps):
        state = repetition_sweep(state)
        if (step + 1) % interval == 0:
            state = rotate_blocks(state, block)
        if step >= args.static_steps - args.tail:
            counts = period_coverage(state)
            p2.append(counts[2])
            p3.append(counts[3])
    return statistics.mean(p2), statistics.mean(p3)


def run_turnover(seed, block, interval, args):
    rng = random.Random(100000 + seed)
    state = randomized_two_domain(seed, args.size, args.symbols)
    p2 = []
    p3 = []
    for step in range(args.steps):
        state = repetition_sweep(state)
        for _ in range(args.noise):
            state = mutate_one(state, rng, args.symbols)
        if (step + 1) % interval == 0:
            state = rotate_blocks(state, block)
        if step >= args.steps - args.tail:
            counts = period_coverage(state)
            p2.append(counts[2])
            p3.append(counts[3])
    return statistics.mean(p2), statistics.mean(p3)


def main():
    parser = argparse.ArgumentParser(description="Experiment 083: environment-dependent relational consequence.")
    parser.add_argument("--size", type=int, default=120)
    parser.add_argument("--symbols", type=int, default=8)
    parser.add_argument("--static-steps", type=int, default=300)
    parser.add_argument("--steps", type=int, default=600)
    parser.add_argument("--tail", type=int, default=200)
    parser.add_argument("--noise", type=int, default=1)
    parser.add_argument("--seeds", type=int, default=16)
    parser.add_argument("--intervals", default="1,2,5")
    args = parser.parse_args()

    fixed_interval = 5
    for block in (2, 3):
        p2, p3 = run_fixed_environment(block, fixed_interval, args)
        print(f"fixed_domains environment=E{block} interval={fixed_interval} p2={p2:.6f} p3={p3:.6f}")

    for interval in [int(x) for x in args.intervals.split(",") if x.strip()]:
        for block in (2, 3):
            values = [run_turnover(seed, block, interval, args) for seed in range(args.seeds)]
            print(
                f"turnover environment=E{block} interval={interval} "
                f"p2={statistics.mean(v[0] for v in values):.6f} "
                f"p3={statistics.mean(v[1] for v in values):.6f}"
            )


if __name__ == "__main__":
    main()
