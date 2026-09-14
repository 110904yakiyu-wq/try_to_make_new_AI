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


def probe_cost(exp, state, probe, test_pos, size, key_width, core_width):
    state = exp.write_window(state, test_pos, probe, core_width, size)
    event = exp.candidate(state, test_pos, size, key_width)
    if event is None:
        return None
    return len(event[1])


def main():
    exp = load_exp057()
    parser = argparse.ArgumentParser(description="Experiment 063: raw-probe specificity control.")
    parser.add_argument("--key-widths", default="3,4,5")
    parser.add_argument("--window-capacity", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--backgrounds", type=int, default=256)
    args = parser.parse_args()

    for width in [int(x) for x in args.key_widths.split(",") if x.strip()]:
        size = width * args.window_capacity
        train_pos = 0
        test_pos = (args.window_capacity // 2) * width
        counts = Counter()
        score_sum = 0

        for seed in range(args.backgrounds):
            initial = random.Random(seed).getrandbits(size)
            for policy in ("min", "max"):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    sa = exp.train((a,) * 5, train_pos, initial, size, width,
                                   args.core_width, args.event_budget, policy)
                    sb = exp.train((b,) * 5, train_pos, initial, size, width,
                                   args.core_width, args.event_budget, policy)

                    aa = probe_cost(exp, sa, a, test_pos, size, width, args.core_width)
                    ba = probe_cost(exp, sb, a, test_pos, size, width, args.core_width)
                    bb = probe_cost(exp, sb, b, test_pos, size, width, args.core_width)
                    ab = probe_cost(exp, sa, b, test_pos, size, width, args.core_width)
                    counts["trials"] += 1

                    for label, value in (("AA", aa), ("BA", ba), ("BB", bb), ("AB", ab)):
                        counts[f"{label}_available"] += int(value is not None)

                    if aa is not None and ba is not None:
                        d = ba - aa
                        counts["A_comparable"] += 1
                        counts["A_match_cheaper"] += int(d > 0)
                        counts["A_match_equal"] += int(d == 0)
                        counts["A_match_costlier"] += int(d < 0)

                    if bb is not None and ab is not None:
                        d = ab - bb
                        counts["B_comparable"] += 1
                        counts["B_match_cheaper"] += int(d > 0)
                        counts["B_match_equal"] += int(d == 0)
                        counts["B_match_costlier"] += int(d < 0)

                    if None not in (aa, ba, bb, ab):
                        da = ba - aa
                        db = ab - bb
                        counts["full_crossover_comparable"] += 1
                        counts["both_match_cheaper"] += int(da > 0 and db > 0)
                        counts["both_match_noncostlier"] += int(da >= 0 and db >= 0 and (da > 0 or db > 0))
                        counts["both_reverse"] += int(da < 0 and db < 0)
                        score_sum += da + db

        print(f"key_width={width}")
        for key in (
            "trials", "AA_available", "BA_available", "BB_available", "AB_available",
            "A_comparable", "A_match_cheaper", "A_match_equal", "A_match_costlier",
            "B_comparable", "B_match_cheaper", "B_match_equal", "B_match_costlier",
            "full_crossover_comparable", "both_match_cheaper", "both_match_noncostlier", "both_reverse",
        ):
            print(f"{key}={counts[key]}")
        if counts["full_crossover_comparable"]:
            print(f"mean_crossover_score={score_sum / counts['full_crossover_comparable']:.9f}")
        print()


if __name__ == "__main__":
    main()
