#!/usr/bin/env python3
import importlib.util
import random
import statistics
from pathlib import Path


def load_exp084():
    path = Path(__file__).resolve().parents[1] / "084_environment_conditioned_variant_selection" / "run.py"
    spec = importlib.util.spec_from_file_location("exp084", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replication_sweep(state, min_period=2, max_period=8):
    old = state
    n = len(state)
    proposals = [set() for _ in range(n)]

    for start in range(n):
        for period in range(min_period, max_period + 1):
            if all(old[(start + j) % n] == old[(start + period + j) % n] for j in range(period)):
                for j in range(period):
                    proposals[(start + 2 * period + j) % n].add(old[(start + j) % n])

    new = old[:]
    for i, values in enumerate(proposals):
        if len(values) == 1:
            new[i] = next(iter(values))
    return new


def run(seed, replicate, exp, size=120, symbols=8, steps=600, switch_step=300, window=100):
    rng = random.Random(930000 + seed)
    state = exp.initial_p2(seed, size, symbols)
    history = []

    for step in range(steps):
        state = exp.repetition_sweep(state)
        if replicate:
            state = replication_sweep(state)
        state = exp.mutate_one(state, rng, symbols)
        if step < switch_step:
            state = exp.rotate_blocks(state, 3)
        history.append(exp.minimal_p2_p3_coverage(state))

    before = history[switch_step - window:switch_step]
    after = history[-window:]
    return {
        "pre_p2": statistics.mean(x[0] for x in before),
        "pre_p3": statistics.mean(x[1] for x in before),
        "post_p2": statistics.mean(x[0] for x in after),
        "post_p3": statistics.mean(x[1] for x in after),
    }


def main():
    exp = load_exp084()
    for replicate in (False, True):
        values = [run(seed, replicate, exp) for seed in range(16)]
        name = "replication" if replicate else "baseline"
        print(name, end="")
        for key in values[0]:
            print(f" {key}={statistics.mean(v[key] for v in values):.6f}", end="")
        print()


if __name__ == "__main__":
    main()
