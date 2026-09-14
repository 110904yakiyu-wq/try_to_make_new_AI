#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter
from pathlib import Path


def load_exp057():
    path = Path(__file__).resolve().parents[1] / "057_self_delimiting_k8" / "run.py"
    spec = importlib.util.spec_from_file_location("exp057", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    parser = argparse.ArgumentParser(description="Experiment 062: global K8 access-cost landscape.")
    parser.add_argument("--key-widths", default="3,4")
    parser.add_argument("--window-capacity", type=int, default=6)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--backgrounds", type=int, default=128)
    args = parser.parse_args()

    for width in [int(x) for x in args.key_widths.split(",") if x.strip()]:
        size = width * args.window_capacity
        counts = Counter()
        deltas = Counter()
        common_effects = 0
        common_effects_with_cost_diff = 0

        for seed in range(args.backgrounds):
            initial = random.Random(seed).getrandbits(size)
            for policy in ("min", "max"):
                for pos in range(0, size, width):
                    for a in range(1 << (args.core_width - 1)):
                        b = a ^ ((1 << args.core_width) - 1)
                        s1 = exp.train(
                            (a, a, a, b, b), pos, initial, size, width,
                            args.core_width, args.event_budget, policy,
                        )
                        s2 = exp.train(
                            (b, b, a, a, a), pos, initial, size, width,
                            args.core_width, args.event_budget, policy,
                        )
                        c1 = cost_landscape(exp, s1, size, width)
                        c2 = cost_landscape(exp, s2, size, width)
                        k1, k2 = set(c1), set(c2)
                        counts["history_pairs"] += 1
                        counts["same_effect_set"] += int(k1 == k2)
                        counts["same_cost_map"] += int(c1 == c2)

                        common = k1 & k2
                        common_effects += len(common)
                        differing = [key for key in common if c1[key] != c2[key]]
                        common_effects_with_cost_diff += len(differing)
                        counts["pairs_with_common_cost_diff"] += int(bool(differing))

                        if k1 == k2 and differing:
                            counts["same_effect_set_cost_reorg"] += 1
                            seq1_le = all(c1[key] <= c2[key] for key in k1)
                            seq2_le = all(c2[key] <= c1[key] for key in k1)
                            if seq1_le and any(c1[key] < c2[key] for key in k1):
                                counts["seq1_cost_dominates"] += 1
                            elif seq2_le and any(c2[key] < c1[key] for key in k1):
                                counts["seq2_cost_dominates"] += 1
                            else:
                                counts["cost_incomparable"] += 1

                        for key in differing:
                            deltas[c2[key] - c1[key]] += 1

        print(f"key_width={width}")
        for key in (
            "history_pairs",
            "same_effect_set",
            "same_cost_map",
            "pairs_with_common_cost_diff",
            "same_effect_set_cost_reorg",
            "seq1_cost_dominates",
            "seq2_cost_dominates",
            "cost_incomparable",
        ):
            print(f"{key}={counts[key]}")
        print(f"common_effects={common_effects}")
        print(f"common_effects_with_cost_diff={common_effects_with_cost_diff}")
        if common_effects:
            print(f"common_effect_cost_diff_fraction={common_effects_with_cost_diff/common_effects:.9f}")
        for delta, count in sorted(deltas.items()):
            print(f"cost_delta_seq2_minus_seq1={delta} count={count}")
        print()


if __name__ == "__main__":
    main()
