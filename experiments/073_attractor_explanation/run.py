#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter
from pathlib import Path


def load_exp068():
    path = Path(__file__).resolve().parents[1] / "068_reversal_and_metric_robustness" / "run.py"
    spec = importlib.util.spec_from_file_location("exp068", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cycle_info(k8, state, size, key_width, policy, max_steps=300000):
    seen = {}
    sequence = []
    for t in range(max_steps):
        if state in seen:
            mu = seen[state]
            cycle = sequence[mu:]
            return mu, len(cycle), min(cycle)
        seen[state] = t
        sequence.append(state)
        state, _ = k8.step(state, size, key_width, policy)
    return None


def main():
    exp068 = load_exp068()
    exp066 = exp068.load_exp066()
    k8 = exp066.load_exp057()

    p = argparse.ArgumentParser(description="Experiment 073: K8 attractor explanation.")
    p.add_argument("--backgrounds", type=int, default=8)
    args = p.parse_args()

    size = 18
    key_width = core_width = 3
    event_budget = 3
    n = 8
    masks = [1, 2, 4, 3, 5, 6]
    pairs = [(a, b) for i, a in enumerate(masks) for b in masks[i + 1:] if a.bit_count() == b.bit_count()]
    counts = Counter()

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(size)
        for policy in ("min", "max"):
            for pos in range(0, size, key_width):
                for p_mask, q_mask in pairs:
                    class A: pass
                    a = A()
                    a.size = size; a.key_width = key_width; a.core_width = core_width; a.event_budget = event_budget
                    p_state = exp068.train_schedule(exp066, initial, "Q" * n + "P" * n, p_mask, q_mask, pos, a, policy)
                    q_state = exp068.train_schedule(exp066, initial, "P" * n + "Q" * n, p_mask, q_mask, pos, a, policy)
                    pi = cycle_info(k8, p_state, size, key_width, policy)
                    qi = cycle_info(k8, q_state, size, key_width, policy)
                    if pi is None or qi is None:
                        counts["cycle_fail"] += 1
                    elif pi[1:] == qi[1:]:
                        counts["same_cycle"] += 1
                    else:
                        counts["different_cycle"] += 1

    for key in ("same_cycle", "different_cycle", "cycle_fail"):
        print(f"{key}={counts[key]}")


if __name__ == "__main__":
    main()
