#!/usr/bin/env python3
import argparse
import random
import statistics


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
        proposal = None
        conflict = False
        for p in range(min_period, max_period + 1):
            same = True
            for j in range(p):
                if old[(target - 2 * p + j) % n] != old[(target - p + j) % n]:
                    same = False
                    break
            if not same:
                continue
            expected = old[(target - p) % n]
            if expected == old[target]:
                continue
            if proposal is None:
                proposal = expected
            elif proposal != expected:
                conflict = True
                break
        if proposal is not None and not conflict:
            new[target] = proposal
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


def minimal_p2_p3_coverage(state):
    n = len(state)
    p2 = 0
    p3 = 0

    def has_period(target, period):
        for j in range(period):
            reference = state[(target - period + j) % n]
            if (
                state[(target - 2 * period + j) % n] != reference
                or state[(target - 3 * period + j) % n] != reference
            ):
                return False
        return True

    for target in range(n):
        if has_period(target, 2):
            p2 += 1
        elif has_period(target, 3):
            p3 += 1
    return p2, p3


def initial_p2(seed, size, symbols):
    rng = random.Random(seed)
    labels = list(range(symbols))
    rng.shuffle(labels)
    a, b = labels[:2]
    phase = rng.randrange(2)
    return [a if (i + phase) % 2 == 0 else b for i in range(size)]


def run_constant_environment(seed, environment, noise, args):
    rng = random.Random(900000 + seed)
    state = initial_p2(seed, args.size, args.symbols)
    p2_tail = []
    p3_tail = []
    p3_births = 0
    previous_p3 = False
    current_lifetime = 0
    lifetimes = []
    max_p3 = 0
    first_p3 = None

    for step in range(args.steps):
        state = repetition_sweep(state)
        for _ in range(noise):
            state = mutate_one(state, rng, args.symbols)
        if environment is not None:
            state = rotate_blocks(state, environment)

        p2, p3 = minimal_p2_p3_coverage(state)
        max_p3 = max(max_p3, p3)
        if step >= args.steps - args.tail:
            p2_tail.append(p2)
            p3_tail.append(p3)

        has_p3 = p3 > 0
        if has_p3 and not previous_p3:
            p3_births += 1
            if first_p3 is None:
                first_p3 = step
        if has_p3:
            current_lifetime += 1
        elif current_lifetime:
            lifetimes.append(current_lifetime)
            current_lifetime = 0
        previous_p3 = has_p3

    if current_lifetime:
        lifetimes.append(current_lifetime)

    return {
        "p2": statistics.mean(p2_tail),
        "p3": statistics.mean(p3_tail),
        "max_p3": max_p3,
        "p3_births": p3_births,
        "mean_p3_lifetime": statistics.mean(lifetimes) if lifetimes else 0.0,
        "max_p3_lifetime": max(lifetimes) if lifetimes else 0,
        "first_p3": first_p3 if first_p3 is not None else args.steps,
    }


def run_switch(seed, first_environment, second_environment, args):
    rng = random.Random(920000 + seed)
    state = initial_p2(seed, args.size, args.symbols)
    history = []

    for step in range(args.steps):
        state = repetition_sweep(state)
        state = mutate_one(state, rng, args.symbols)
        environment = first_environment if step < args.switch_step else second_environment
        if environment is not None:
            state = rotate_blocks(state, environment)
        history.append(minimal_p2_p3_coverage(state))

    before = history[args.switch_step - args.switch_window:args.switch_step]
    after = history[-args.switch_window:]
    return (
        statistics.mean(x[0] for x in before),
        statistics.mean(x[1] for x in before),
        statistics.mean(x[0] for x in after),
        statistics.mean(x[1] for x in after),
    )


def main():
    parser = argparse.ArgumentParser(description="Experiment 084: environment-conditioned variant filtering.")
    parser.add_argument("--size", type=int, default=120)
    parser.add_argument("--symbols", type=int, default=8)
    parser.add_argument("--steps", type=int, default=600)
    parser.add_argument("--tail", type=int, default=200)
    parser.add_argument("--seeds", type=int, default=16)
    parser.add_argument("--switch-seeds", type=int, default=32)
    parser.add_argument("--switch-step", type=int, default=300)
    parser.add_argument("--switch-window", type=int, default=100)
    args = parser.parse_args()

    for environment in (None, 2, 3):
        values = [
            run_constant_environment(seed, environment, 1, args)
            for seed in range(args.seeds)
        ]
        name = "none" if environment is None else f"E{environment}"
        print(f"environment={name} noise=1")
        for key in values[0]:
            print(f"{key}={statistics.mean(v[key] for v in values):.6f}")

    no_noise = [
        run_constant_environment(seed, 3, 0, args)
        for seed in range(args.seeds)
    ]
    print("environment=E3 noise=0")
    print(f"p3={statistics.mean(v['p3'] for v in no_noise):.6f}")
    print(f"p3_births={statistics.mean(v['p3_births'] for v in no_noise):.6f}")

    for first, second in ((2, 3), (3, 2), (3, None)):
        values = [
            run_switch(seed, first, second, args)
            for seed in range(args.switch_seeds)
        ]
        first_name = "none" if first is None else f"E{first}"
        second_name = "none" if second is None else f"E{second}"
        print(
            f"switch={first_name}->{second_name} "
            f"before_p2={statistics.mean(v[0] for v in values):.6f} "
            f"before_p3={statistics.mean(v[1] for v in values):.6f} "
            f"after_p2={statistics.mean(v[2] for v in values):.6f} "
            f"after_p3={statistics.mean(v[3] for v in values):.6f}"
        )


if __name__ == "__main__":
    main()
