#!/usr/bin/env python3
import argparse
import importlib.util
import math
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


def deposit_context(exp, state, event, size, width):
    positions, values = event[0], event[1]
    dest = (positions[-1] + width) % size
    out = state
    for j, value in enumerate(values):
        out = exp.write_window(out, (dest + j * width) % size, value, width, size)
    return out


def train(exp, initial, sequence, pos, size, width, event_budget, policy, retain):
    state = initial
    deposits = 0
    for perturb in sequence:
        original = exp.read_window(state, pos, width, size)
        state = xor_window(state, pos, perturb, width, size)
        for _ in range(event_budget):
            state, event = exp.step(state, size, width, policy)
            if event is None:
                break
            if retain and exp.read_window(state, pos, width, size) == original:
                state = deposit_context(exp, state, event, size, width)
                deposits += 1
    return state, deposits


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


def damage(exp, state, perturb, pos, size, width, recovery_events, policy):
    reference = cost_landscape(exp, state, size, width)
    out = xor_window(state, pos, perturb, width, size)
    out = exp.run_budget(out, recovery_events, size, width, policy)
    post = cost_landscape(exp, out, size, width)
    return operational_distance(reference, post, size // width + 1)


def run_condition(exp, retain, args):
    size = args.key_width * args.window_capacity
    masks = [1, 2, 4, 3, 5, 6]
    pairs = [(a, b) for i, a in enumerate(masks) for b in masks[i + 1:] if a.bit_count() == b.bit_count()]
    counts = Counter()
    deposits = []

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(size)
        for policy in ("min", "max"):
            for pos in range(0, size, args.key_width):
                for p_mask, q_mask in pairs:
                    for schedule_seed in range(args.schedule_seeds):
                        rng = random.Random(10000 + schedule_seed)
                        slots = list(range(args.exposures))
                        rng.shuffle(slots)
                        major_slots = set(slots[:args.major_count])
                        p_schedule = [p_mask if i in major_slots else q_mask for i in range(args.exposures)]
                        q_schedule = [q_mask if i in major_slots else p_mask for i in range(args.exposures)]

                        p_state, p_dep = train(exp, initial, p_schedule, pos, size, args.key_width, args.event_budget, policy, retain)
                        q_state, q_dep = train(exp, initial, q_schedule, pos, size, args.key_width, args.event_budget, policy, retain)
                        deposits.extend((p_dep, q_dep))

                        pp = damage(exp, p_state, p_mask, pos, size, args.key_width, args.recovery_events, policy)
                        qp = damage(exp, q_state, p_mask, pos, size, args.key_width, args.recovery_events, policy)
                        pq = damage(exp, p_state, q_mask, pos, size, args.key_width, args.recovery_events, policy)
                        qq = damage(exp, q_state, q_mask, pos, size, args.key_width, args.recovery_events, policy)

                        score = (qp - pp) + (pq - qq)
                        counts["cases"] += 1
                        if score > 0:
                            counts["net_match"] += 1
                        elif score < 0:
                            counts["net_mismatch"] += 1
                        else:
                            counts["tie"] += 1
                        if pp < qp and qq < pq:
                            counts["strict"] += 1

    return counts, deposits


def main():
    parser = argparse.ArgumentParser(description="Experiment 088: K8 self-delimiting repair retention.")
    parser.add_argument("--backgrounds", type=int, default=8)
    parser.add_argument("--schedule-seeds", type=int, default=4)
    parser.add_argument("--key-width", type=int, default=3)
    parser.add_argument("--window-capacity", type=int, default=6)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--recovery-events", type=int, default=3)
    parser.add_argument("--exposures", type=int, default=16)
    parser.add_argument("--major-count", type=int, default=12)
    args = parser.parse_args()
    exp = load_exp057()

    for retain in (False, True):
        counts, deposits = run_condition(exp, retain, args)
        name = "repair_trace" if retain else "baseline"
        print(
            f"{name} cases={counts['cases']} net_match={counts['net_match']} "
            f"net_mismatch={counts['net_mismatch']} tie={counts['tie']} strict={counts['strict']}"
        )
        if retain:
            mean_dep = sum(deposits) / len(deposits)
            frac = sum(x > 0 for x in deposits) / len(deposits)
            non_ties = counts['net_match'] + counts['net_mismatch']
            z = (counts['net_match'] - non_ties / 2) / math.sqrt(non_ties / 4)
            p = math.erfc(abs(z) / math.sqrt(2))
            print(f"mean_deposits={mean_dep:.6f} states_with_deposit_fraction={frac:.6f}")
            print(f"direction_normal_z={z:.6f} two_sided_p_normal={p:.6f}")


if __name__ == "__main__":
    main()
