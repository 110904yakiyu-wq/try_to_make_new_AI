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
    return out, i, old


def successful_periods(state, target, expected_old, min_period=2, max_period=8):
    n = len(state)
    periods = []
    proposed_values = set()
    for p in range(min_period, max_period + 1):
        if not all(state[(target - 2 * p + j) % n] == state[(target - p + j) % n] for j in range(p)):
            continue
        expected = state[(target - p) % n]
        if expected == state[target]:
            continue
        periods.append((p, expected))
        proposed_values.add(expected)
    if len(proposed_values) != 1 or not periods:
        return []
    if next(iter(proposed_values)) != expected_old:
        return []
    return [p for p, _ in periods]


def copy_span(state, repaired_index, span):
    n = len(state)
    source = [state[(repaired_index - span + 1 + j) % n] for j in range(span)]
    out = state[:]
    for j, value in enumerate(source):
        out[(repaired_index + 1 + j) % n] = value
    return out


def step(state, rng, exp, mode, environment, symbols=8):
    mutated, index, old = mutate_one_detail(state, rng, symbols)
    periods = successful_periods(mutated, index, old)
    repaired = exp.repetition_sweep(mutated)

    if periods and repaired[index] == old:
        if mode == "union":
            span = 2 * max(periods)
        elif mode == "intersection":
            span = 2 * min(periods)
        elif mode == "one_block":
            span = max(periods)
        else:
            raise ValueError(mode)
        repaired = copy_span(repaired, index, span)

    if environment is not None:
        repaired = exp.rotate_blocks(repaired, environment)
    return repaired


def run(seed, mode, exp, size=120, symbols=8, steps=600, switch_step=300, window=100):
    rng = random.Random(960000 + seed)
    state = exp.initial_p2(seed, size, symbols)
    history = []
    for t in range(steps):
        state = step(state, rng, exp, mode, 3 if t < switch_step else None, symbols)
        history.append(exp.minimal_p2_p3_coverage(state))
    before = history[switch_step - window:switch_step]
    after = history[-window:]
    return (
        statistics.mean(x[1] for x in before),
        statistics.mean(x[1] for x in after),
    )


def main():
    parser = argparse.ArgumentParser(description="Experiment 087: support-delimited repair trace.")
    parser.add_argument("--seeds", type=int, default=32)
    args = parser.parse_args()
    exp = load_exp084()

    print(f"seeds={args.seeds}")
    for mode in ("union", "intersection", "one_block"):
        values = [run(seed, mode, exp) for seed in range(args.seeds)]
        print(
            f"{mode} "
            f"pre_p3={statistics.mean(v[0] for v in values):.6f} "
            f"post_p3={statistics.mean(v[1] for v in values):.6f}"
        )


if __name__ == "__main__":
    main()
