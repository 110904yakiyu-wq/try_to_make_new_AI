#!/usr/bin/env python3
import argparse
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


def mutate_one_detail(state, rng, symbols):
    out = state[:]
    i = rng.randrange(len(out))
    old = out[i]
    r = rng.randrange(symbols - 1)
    new = r if r < old else r + 1
    out[i] = new
    return out, i, old, new


def copy_trace(state, repaired_index, length):
    n = len(state)
    source = [state[(repaired_index - length + 1 + j) % n] for j in range(length)]
    out = state[:]
    for j, value in enumerate(source):
        out[(repaired_index + 1 + j) % n] = value
    return out


def step(state, rng, exp, symbols, environment, trace_length):
    mutated, index, old, _ = mutate_one_detail(state, rng, symbols)
    repaired = exp.repetition_sweep(mutated)
    if repaired[index] == old:
        repaired = copy_trace(repaired, index, trace_length)
    if environment is not None:
        repaired = exp.rotate_blocks(repaired, environment)
    return repaired


def run_switch(seed, trace_length, exp, size=120, symbols=8, steps=600, switch_step=300, window=100):
    rng = random.Random(940000 + 1000 * trace_length + seed)
    state = exp.initial_p2(seed, size, symbols)
    history = []
    for t in range(steps):
        env = 3 if t < switch_step else None
        state = step(state, rng, exp, symbols, env, trace_length)
        history.append(exp.minimal_p2_p3_coverage(state))
    before = history[switch_step - window:switch_step]
    after = history[-window:]
    return (
        statistics.mean(x[1] for x in before),
        statistics.mean(x[1] for x in after),
    )


def run_constant(seed, environment, exp, trace_length=6, size=120, symbols=8, steps=600, tail=200):
    rng = random.Random(950000 + seed)
    state = exp.initial_p2(seed, size, symbols)
    history = []
    for _ in range(steps):
        state = step(state, rng, exp, symbols, environment, trace_length)
        history.append(exp.minimal_p2_p3_coverage(state))
    tail_values = history[-tail:]
    return (
        statistics.mean(x[0] for x in tail_values),
        statistics.mean(x[1] for x in tail_values),
    )


def main():
    parser = argparse.ArgumentParser(description="Experiment 086: repair-trace geometry audit.")
    parser.add_argument("--seeds", type=int, default=16)
    args = parser.parse_args()
    exp = load_exp084()

    for length in range(2, 11):
        values = [run_switch(seed, length, exp) for seed in range(args.seeds)]
        print(
            f"L={length} "
            f"pre_p3={statistics.mean(v[0] for v in values):.6f} "
            f"post_p3={statistics.mean(v[1] for v in values):.6f}"
        )

    for environment in (None, 2, 3):
        values = [run_constant(seed, environment, exp) for seed in range(args.seeds)]
        name = "none" if environment is None else f"E{environment}"
        print(
            f"L6 environment={name} "
            f"late_p2={statistics.mean(v[0] for v in values):.6f} "
            f"late_p3={statistics.mean(v[1] for v in values):.6f}"
        )


if __name__ == "__main__":
    main()
