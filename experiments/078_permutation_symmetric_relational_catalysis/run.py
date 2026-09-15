#!/usr/bin/env python3
import argparse
import random
import statistics


def sweep_relational(state, reverse=False):
    """Permutation-symmetric relational catalyst:

    A B A D -> A B A B, when A != B and D != B.

    Only equality/inequality relations matter. No symbol value has a special
    meaning, and the rule is equivariant under arbitrary permutations of the
    symbol alphabet.
    """
    state = state[:]
    n = len(state)
    events = 0
    indices = range(n - 1, -1, -1) if reverse else range(n)
    for i in indices:
        a = state[i % n]
        b = state[(i + 1) % n]
        c = state[(i + 2) % n]
        d = state[(i + 3) % n]
        if a == c and a != b and d != b:
            state[(i + 3) % n] = b
            events += 1
    return state, events


def mutate_one(state, rng, symbols):
    state = state[:]
    i = rng.randrange(len(state))
    old = state[i]
    r = rng.randrange(symbols - 1)
    new = r if r < old else r + 1
    state[i] = new
    return state


def active_motif_count(state):
    n = len(state)
    return sum(
        1
        for i in range(n)
        if state[i] == state[(i + 2) % n]
        and state[i] != state[(i + 1) % n]
    )


def active_pair_count(state):
    n = len(state)
    pairs = set()
    for i in range(n):
        a = state[i]
        b = state[(i + 1) % n]
        c = state[(i + 2) % n]
        if a == c and a != b:
            pairs.add(tuple(sorted((a, b))))
    return len(pairs)


def run_one(seed, rule, noise_per_sweep, args):
    rng = random.Random(seed)
    state = [rng.randrange(args.symbols) for _ in range(args.size)]
    motifs = []
    pairs = []
    events = []

    for _ in range(args.steps):
        if rule:
            state, event_count = sweep_relational(state)
        else:
            event_count = 0
        for _ in range(noise_per_sweep):
            state = mutate_one(state, rng, args.symbols)
        motifs.append(active_motif_count(state))
        pairs.append(active_pair_count(state))
        events.append(event_count)

    tail = args.tail
    return (
        statistics.mean(motifs[-tail:]),
        statistics.mean(pairs[-tail:]),
        statistics.mean(events[-tail:]),
    )


def permutation_equivariance_trials(args):
    passed = 0
    for trial in range(args.equivariance_trials):
        rng = random.Random(10000 + trial)
        state = [rng.randrange(args.symbols) for _ in range(args.size)]
        perm = list(range(args.symbols))
        rng.shuffle(perm)

        permuted_state = [perm[x] for x in state]
        left, _ = sweep_relational(permuted_state)
        right_raw, _ = sweep_relational(state)
        right = [perm[x] for x in right_raw]
        passed += int(left == right)
    return passed


def single_defect_repair(args):
    repaired = 0
    total = 0
    n = args.size
    for a in range(args.symbols):
        for b in range(a + 1, args.symbols):
            for pos in range(n):
                for replacement in range(args.symbols):
                    if replacement in (a, b):
                        continue
                    state = [a if i % 2 == 0 else b for i in range(n)]
                    state[pos] = replacement
                    post, _ = sweep_relational(state)
                    total += 1
                    repaired += int(active_motif_count(post) == n)
    return repaired, total


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 078: remove absolute catalytic symbol bias."
    )
    parser.add_argument("--size", type=int, default=96)
    parser.add_argument("--symbols", type=int, default=8)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--tail", type=int, default=200)
    parser.add_argument("--seeds", type=int, default=32)
    parser.add_argument("--noise", default="0,1,2,4")
    parser.add_argument("--equivariance-trials", type=int, default=512)
    args = parser.parse_args()

    for noise in [int(x) for x in args.noise.split(",") if x.strip()]:
        for rule in (False, True):
            values = [run_one(seed, rule, noise, args) for seed in range(args.seeds)]
            print(
                f"noise={noise} rule={int(rule)} "
                f"mean_active_motifs={statistics.mean(v[0] for v in values):.6f} "
                f"mean_active_pairs={statistics.mean(v[1] for v in values):.6f} "
                f"mean_events={statistics.mean(v[2] for v in values):.6f}"
            )

    passed = permutation_equivariance_trials(args)
    print(
        f"permutation_equivariance={passed}/{args.equivariance_trials}"
    )

    repaired, total = single_defect_repair(args)
    print(f"single_defect_motif_repair={repaired}/{total}")


if __name__ == "__main__":
    main()
