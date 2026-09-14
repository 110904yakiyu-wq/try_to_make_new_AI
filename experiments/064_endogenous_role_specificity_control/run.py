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


def first_event_identity(exp, initial, probe, pos, size, width, core_width, policy):
    state = exp.write_window(initial, pos, probe, core_width, size)
    event = exp.choose_event(state, size, width, policy)
    if event is None:
        return None
    return event[2][0], event[4]


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


def main():
    exp = load_exp057()
    parser = argparse.ArgumentParser(description="Experiment 064: endogenous-role specificity control.")
    parser.add_argument("--key-widths", default="3,4,5")
    parser.add_argument("--window-capacity", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--backgrounds", type=int, default=64)
    args = parser.parse_args()

    for width in [int(x) for x in args.key_widths.split(",") if x.strip()]:
        size = width * args.window_capacity
        counts = Counter()
        score_sum = 0

        for seed in range(args.backgrounds):
            initial = random.Random(seed).getrandbits(size)
            for policy in ("min", "max"):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    ea = first_event_identity(exp, initial, a, 0, size, width, args.core_width, policy)
                    eb = first_event_identity(exp, initial, b, 0, size, width, args.core_width, policy)
                    if ea is None or eb is None:
                        counts["no_target"] += 1
                        continue

                    counts["target_trials"] += 1
                    counts["distinct_targets"] += int(ea != eb)

                    sa1 = exp.train((a,), 0, initial, size, width, args.core_width, args.event_budget, policy)
                    sb1 = exp.train((b,), 0, initial, size, width, args.core_width, args.event_budget, policy)
                    sa5 = exp.train((a,) * 5, 0, initial, size, width, args.core_width, args.event_budget, policy)
                    sb5 = exp.train((b,) * 5, 0, initial, size, width, args.core_width, args.event_budget, policy)

                    ca1 = cost_landscape(exp, sa1, size, width)
                    cb1 = cost_landscape(exp, sb1, size, width)
                    ca5 = cost_landscape(exp, sa5, size, width)
                    cb5 = cost_landscape(exp, sb5, size, width)

                    caa, cba = ca5.get(ea), cb5.get(ea)
                    cbb, cab = cb5.get(eb), ca5.get(eb)

                    if caa is not None and cba is not None:
                        d = cba - caa
                        counts["A_finite_comparable"] += 1
                        counts["A_specific_cheaper"] += int(d > 0)
                        counts["A_equal"] += int(d == 0)
                        counts["A_specific_costlier"] += int(d < 0)
                    if cbb is not None and cab is not None:
                        d = cab - cbb
                        counts["B_finite_comparable"] += 1
                        counts["B_specific_cheaper"] += int(d > 0)
                        counts["B_equal"] += int(d == 0)
                        counts["B_specific_costlier"] += int(d < 0)

                    unavailable = args.window_capacity + 1
                    da = (cba if cba is not None else unavailable) - (caa if caa is not None else unavailable)
                    db = (cab if cab is not None else unavailable) - (cbb if cbb is not None else unavailable)

                    counts["A_ordinal_specific"] += int(da > 0)
                    counts["A_ordinal_equal"] += int(da == 0)
                    counts["A_ordinal_reverse"] += int(da < 0)
                    counts["B_ordinal_specific"] += int(db > 0)
                    counts["B_ordinal_equal"] += int(db == 0)
                    counts["B_ordinal_reverse"] += int(db < 0)

                    if ea != eb:
                        counts["distinct_target_trials"] += 1
                        counts["strict_both_specific"] += int(da > 0 and db > 0)
                        counts["strict_both_noncostlier"] += int(da >= 0 and db >= 0 and (da > 0 or db > 0))
                        counts["strict_both_reverse"] += int(da < 0 and db < 0)
                        score_sum += da + db

                    own_a1 = ca1.get(ea)
                    own_b1 = cb1.get(eb)
                    if own_a1 is not None and caa is not None:
                        counts["A_one_vs_five_comparable"] += 1
                        counts["A_five_cheaper_than_one"] += int(caa < own_a1)
                        counts["A_five_equal_one"] += int(caa == own_a1)
                        counts["A_five_costlier_than_one"] += int(caa > own_a1)
                    if own_b1 is not None and cbb is not None:
                        counts["B_one_vs_five_comparable"] += 1
                        counts["B_five_cheaper_than_one"] += int(cbb < own_b1)
                        counts["B_five_equal_one"] += int(cbb == own_b1)
                        counts["B_five_costlier_than_one"] += int(cbb > own_b1)

        print(f"key_width={width}")
        for key in sorted(counts):
            print(f"{key}={counts[key]}")
        if counts["distinct_target_trials"]:
            print(f"mean_distinct_target_crossover_score={score_sum / counts['distinct_target_trials']:.9f}")
        print()


if __name__ == "__main__":
    main()
