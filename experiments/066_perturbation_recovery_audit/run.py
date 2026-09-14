#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter
from pathlib import Path


def load_exp057():
    path = Path(__file__).resolve().parents[1] / "057_self_delimiting_k8" / "run.py"
    spec = importlib.util.spec_from_file_location("exp057", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def xor_window(state, pos, mask, width, size):
    for j in range(width):
        if (mask >> (width - 1 - j)) & 1:
            state ^= 1 << ((pos + j) % size)
    return state


def train(exp, initial, perturb, pos, repeats, size, key_width, core_width, event_budget, policy):
    state = initial
    for _ in range(repeats):
        state = xor_window(state, pos, perturb, core_width, size)
        state = exp.run_budget(state, event_budget, size, key_width, policy)
    return state


def cost_landscape(exp, state, size, width):
    costs = {}
    for start in range(size):
        event = exp.candidate(state, start, size, width)
        if event is None:
            continue
        effect = (event[2][0], event[4])
        depth = len(event[1])
        if effect not in costs or depth < costs[effect]:
            costs[effect] = depth
    return costs


def operational_distance(left, right, missing_penalty):
    total = 0
    for key in set(left) | set(right):
        if key not in left or key not in right:
            total += missing_penalty
        else:
            total += abs(left[key] - right[key])
    return total


def damage(exp, state, perturb, pos, recovery_events, size, key_width, core_width, policy, metric):
    if metric == "state":
        reference = state
    else:
        reference = cost_landscape(exp, state, size, key_width)
    out = xor_window(state, pos, perturb, core_width, size)
    out = exp.run_budget(out, recovery_events, size, key_width, policy)
    if metric == "state":
        return (reference ^ out).bit_count()
    post = cost_landscape(exp, out, size, key_width)
    return operational_distance(reference, post, size // key_width + 1)


def main():
    exp = load_exp057()
    p = argparse.ArgumentParser()
    p.add_argument("--metric", choices=("state", "operational"), default="state")
    p.add_argument("--backgrounds", type=int, default=16)
    p.add_argument("--key-width", type=int, default=3)
    p.add_argument("--window-capacity", type=int, default=6)
    p.add_argument("--core-width", type=int, default=3)
    p.add_argument("--event-budget", type=int, default=3)
    p.add_argument("--repeats", type=int, default=5)
    p.add_argument("--recovery-events", type=int, default=3)
    p.add_argument("--washout-events", type=int, default=0)
    p.add_argument("--test-shift", type=int, default=0)
    args = p.parse_args()

    size = args.key_width * args.window_capacity
    masks = [1, 2, 4, 3, 5, 6]
    pairs = [(a, b) for i, a in enumerate(masks) for b in masks[i + 1:] if a.bit_count() == b.bit_count()]
    counts = Counter()

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(size)
        for policy in ("min", "max"):
            for pos in range(0, size, args.key_width):
                test_pos = (pos + args.test_shift) % size
                for p_mask, q_mask in pairs:
                    p_state = train(exp, initial, p_mask, pos, args.repeats, size, args.key_width, args.core_width, args.event_budget, policy)
                    q_state = train(exp, initial, q_mask, pos, args.repeats, size, args.key_width, args.core_width, args.event_budget, policy)
                    p_state = exp.run_budget(p_state, args.washout_events, size, args.key_width, policy)
                    q_state = exp.run_budget(q_state, args.washout_events, size, args.key_width, policy)

                    pp = damage(exp, p_state, p_mask, test_pos, args.recovery_events, size, args.key_width, args.core_width, policy, args.metric)
                    qp = damage(exp, q_state, p_mask, test_pos, args.recovery_events, size, args.key_width, args.core_width, policy, args.metric)
                    pq = damage(exp, p_state, q_mask, test_pos, args.recovery_events, size, args.key_width, args.core_width, policy, args.metric)
                    qq = damage(exp, q_state, q_mask, test_pos, args.recovery_events, size, args.key_width, args.core_width, policy, args.metric)

                    counts["cases"] += 1
                    if pp < qp: counts["P_match"] += 1
                    elif pp > qp: counts["P_mismatch"] += 1
                    else: counts["P_equal"] += 1
                    if qq < pq: counts["Q_match"] += 1
                    elif qq > pq: counts["Q_mismatch"] += 1
                    else: counts["Q_equal"] += 1
                    if pp < qp and qq < pq: counts["strict"] += 1
                    score = (qp - pp) + (pq - qq)
                    if score > 0: counts["net_match"] += 1
                    elif score < 0: counts["net_mismatch"] += 1
                    else: counts["net_tie"] += 1

    for key in ("cases", "net_match", "net_mismatch", "net_tie", "strict", "P_match", "P_mismatch", "P_equal", "Q_match", "Q_mismatch", "Q_equal"):
        print(f"{key}={counts[key]}")


if __name__ == "__main__":
    main()
