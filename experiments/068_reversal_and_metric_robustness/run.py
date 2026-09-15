#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter, defaultdict
from pathlib import Path


def load_exp066():
    path = Path(__file__).resolve().parents[1] / "066_perturbation_recovery_audit" / "run.py"
    spec = importlib.util.spec_from_file_location("exp066", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def train_schedule(exp, initial, tokens, p_mask, q_mask, pos, args, policy):
    state = initial
    for token in tokens:
        mask = p_mask if token == "P" else q_mask
        state = exp.xor_window(state, pos, mask, args.core_width, args.size)
        state = exp.exp.run_budget(state, args.event_budget, args.size, args.key_width, policy)
    return state


def compare(exp, tokens_p_recent, tokens_q_recent, args, penalty):
    masks = [1, 2, 4, 3, 5, 6]
    pairs = [(a, b) for i, a in enumerate(masks) for b in masks[i + 1:] if a.bit_count() == b.bit_count()]
    total = Counter()
    by_pair = defaultdict(Counter)

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(args.size)
        for policy in ("min", "max"):
            for pos in range(0, args.size, args.key_width):
                for p_mask, q_mask in pairs:
                    p_state = train_schedule(exp, initial, tokens_p_recent, p_mask, q_mask, pos, args, policy)
                    q_state = train_schedule(exp, initial, tokens_q_recent, p_mask, q_mask, pos, args, policy)
                    p_state = exp.exp.run_budget(p_state, args.washout_events, args.size, args.key_width, policy)
                    q_state = exp.exp.run_budget(q_state, args.washout_events, args.size, args.key_width, policy)

                    def dmg(state, mask):
                        reference = exp.cost_landscape(exp.exp, state, args.size, args.key_width)
                        out = exp.xor_window(state, pos, mask, args.core_width, args.size)
                        out = exp.exp.run_budget(out, args.recovery_events, args.size, args.key_width, policy)
                        post = exp.cost_landscape(exp.exp, out, args.size, args.key_width)
                        return exp.operational_distance(reference, post, penalty)

                    pp = dmg(p_state, p_mask)
                    qp = dmg(q_state, p_mask)
                    pq = dmg(p_state, q_mask)
                    qq = dmg(q_state, q_mask)
                    score = (qp - pp) + (pq - qq)

                    c = by_pair[(p_mask, q_mask)]
                    total["cases"] += 1
                    c["cases"] += 1
                    if score > 0:
                        total["recent"] += 1
                        c["recent"] += 1
                    elif score < 0:
                        total["old"] += 1
                        c["old"] += 1
                    else:
                        total["tie"] += 1
                        c["tie"] += 1
                    if pp < qp and qq < pq:
                        total["strict"] += 1
                        c["strict"] += 1

    return total, by_pair


def main():
    exp066 = load_exp066()
    # expose its loaded K8 module once so helper calls can share it
    exp066.exp = exp066.load_exp057()

    p = argparse.ArgumentParser(description="Experiment 068: reversal and metric robustness.")
    p.add_argument("--backgrounds", type=int, default=16)
    p.add_argument("--key-width", type=int, default=3)
    p.add_argument("--window-capacity", type=int, default=6)
    p.add_argument("--core-width", type=int, default=3)
    p.add_argument("--event-budget", type=int, default=3)
    p.add_argument("--recovery-events", type=int, default=3)
    p.add_argument("--washout-events", type=int, default=6)
    args = p.parse_args()
    args.size = args.key_width * args.window_capacity

    p_recent = "Q" * 8 + "P" * 8
    q_recent = "P" * 8 + "Q" * 8
    default_penalty = args.window_capacity + 1

    total, by_pair = compare(exp066, p_recent, q_recent, args, default_penalty)
    print("block_reversal")
    for key in ("cases", "recent", "old", "tie", "strict"):
        print(f"{key}={total[key]}")
    for pair in sorted(by_pair):
        c = by_pair[pair]
        print(f"pair={pair[0]},{pair[1]} recent={c['recent']} old={c['old']} tie={c['tie']} strict={c['strict']}")

    original_backgrounds = args.backgrounds
    args.backgrounds = min(8, original_backgrounds)
    print("metric_penalty_sweep")
    for penalty in (1, 2, 4, 7, 10, 20):
        c, _ = compare(exp066, p_recent, q_recent, args, penalty)
        print(f"penalty={penalty} recent={c['recent']} old={c['old']} tie={c['tie']} strict={c['strict']}")


if __name__ == "__main__":
    main()
