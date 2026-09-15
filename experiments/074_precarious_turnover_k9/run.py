#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter
from functools import lru_cache
from pathlib import Path


def load_k8():
    path = Path(__file__).resolve().parents[1] / "057_self_delimiting_k8" / "run.py"
    spec = importlib.util.spec_from_file_location("k8", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_exp066():
    path = Path(__file__).resolve().parents[1] / "066_perturbation_recovery_audit" / "run.py"
    spec = importlib.util.spec_from_file_location("exp066", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_kernel(k8):
    @lru_cache(maxsize=None)
    def step(state, size, width, policy):
        event = k8.choose_event(state, size, width, policy)
        if event is None:
            target = (state.bit_count() * 7 + state) % size
            return state ^ (1 << target), None

        _, positions, values, outputs, field = event
        for pos, value in zip(positions, outputs):
            state = k8.write_window(state, pos, value, width, size)

        participant_bits = set()
        for pos in positions:
            for j in range(width):
                participant_bits.add((pos + j) % size)

        target = (sum(positions) + sum(values) + field) % size
        for _ in range(size):
            if target not in participant_bits:
                break
            target = (target + 1) % size
        state ^= 1 << target
        return state, (positions, values, outputs, field, target)

    @lru_cache(maxsize=None)
    def run_budget(state, budget, size, width, policy):
        for _ in range(budget):
            state, _ = step(state, size, width, policy)
        return state

    return step, run_budget


def xor_window(state, pos, mask, width, size):
    for j in range(width):
        if (mask >> (width - 1 - j)) & 1:
            state ^= 1 << ((pos + j) % size)
    return state


def cost_landscape(k8, state, size, width):
    costs = {}
    for start in range(size):
        event = k8.candidate(state, start, size, width)
        if event is None:
            continue
        effect = (event[2][0], event[4])
        depth = len(event[1])
        if effect not in costs or depth < costs[effect]:
            costs[effect] = depth
    return costs


def operational_distance(left, right, penalty):
    total = 0
    for key in set(left) | set(right):
        if key not in left or key not in right:
            total += penalty
        else:
            total += abs(left[key] - right[key])
    return total


def assay(k8, run_budget, schedule_p, schedule_q, backgrounds, washout):
    size = 18
    key_width = core_width = 3
    event_budget = recovery_events = 3
    penalty = 7
    masks = [1, 2, 4, 3, 5, 6]
    pairs = [(a, b) for i, a in enumerate(masks) for b in masks[i + 1:] if a.bit_count() == b.bit_count()]
    counts = Counter()

    def train(initial, schedule, p_mask, q_mask, pos, policy):
        state = initial
        for token in schedule:
            mask = p_mask if token == "P" else q_mask
            state = xor_window(state, pos, mask, core_width, size)
            state = run_budget(state, event_budget, size, key_width, policy)
        return state

    def damage(state, mask, pos, policy):
        reference = cost_landscape(k8, state, size, key_width)
        out = xor_window(state, pos, mask, core_width, size)
        out = run_budget(out, recovery_events, size, key_width, policy)
        post = cost_landscape(k8, out, size, key_width)
        return operational_distance(reference, post, penalty)

    for seed in range(backgrounds):
        initial = random.Random(seed).getrandbits(size)
        for policy in ("min", "max"):
            for pos in range(0, size, key_width):
                for p_mask, q_mask in pairs:
                    p_state = train(initial, schedule_p, p_mask, q_mask, pos, policy)
                    q_state = train(initial, schedule_q, p_mask, q_mask, pos, policy)
                    p_state = run_budget(p_state, washout, size, key_width, policy)
                    q_state = run_budget(q_state, washout, size, key_width, policy)

                    pp = damage(p_state, p_mask, pos, policy)
                    qp = damage(q_state, p_mask, pos, policy)
                    pq = damage(p_state, q_mask, pos, policy)
                    qq = damage(q_state, q_mask, pos, policy)
                    score = (qp - pp) + (pq - qq)
                    counts["cases"] += 1
                    if score > 0: counts["recent"] += 1
                    elif score < 0: counts["old"] += 1
                    else: counts["tie"] += 1
                    if pp < qp and qq < pq: counts["strict"] += 1
    return counts


def main():
    p = argparse.ArgumentParser(description="Experiment 074: minimal precarious-turnover K9.")
    p.add_argument("--backgrounds", type=int, default=16)
    args = p.parse_args()

    k8 = load_k8()
    _, run_budget = build_kernel(k8)
    block_p = "Q" * 8 + "P" * 8
    block_q = "P" * 8 + "Q" * 8
    jitter_p = "PQPQQPPQPQPQQPQP"
    jitter_q = "".join("Q" if x == "P" else "P" for x in jitter_p)

    for name, left, right in (("block", block_p, block_q), ("jitter", jitter_p, jitter_q)):
        c = assay(k8, run_budget, left, right, args.backgrounds, 6)
        print(f"{name} cases={c['cases']} recent={c['recent']} old={c['old']} tie={c['tie']} strict={c['strict']}")


if __name__ == "__main__":
    main()
