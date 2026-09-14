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


def exact_same_closure(left, right):
    if left is None or right is None:
        return False
    return (
        len(left[1]) == len(right[1])
        and left[2] == right[2]
        and left[4] == right[4]
    )


def main():
    exp = load_exp057()
    parser = argparse.ArgumentParser(description="Experiment 059: causal history-dependent closure-cost compression.")
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--window-capacity", type=int, default=6)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--backgrounds", type=int, default=64)
    args = parser.parse_args()

    size = args.key_width * args.window_capacity
    counts = Counter()
    depth_pairs = Counter()

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(size)
        for policy in ("min", "max"):
            for pos in range(0, size, args.key_width):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    s1 = exp.train(
                        (a, a, a, b, b), pos, initial, size, args.key_width,
                        args.core_width, args.event_budget, policy,
                    )
                    s2 = exp.train(
                        (b, b, a, a, a), pos, initial, size, args.key_width,
                        args.core_width, args.event_budget, policy,
                    )

                    for start in range(size):
                        e1 = exp.candidate(s1, start, size, args.key_width)
                        e2 = exp.candidate(s2, start, size, args.key_width)
                        d1 = len(e1[1]) if e1 is not None else args.window_capacity + 1
                        d2 = len(e2[1]) if e2 is not None else args.window_capacity + 1
                        counts["start_comparisons"] += 1
                        if d1 < d2:
                            counts["seq1_cheaper"] += 1
                        elif d2 < d1:
                            counts["seq2_cheaper"] += 1
                        else:
                            counts["equal_cost"] += 1

                        if e1 is None or e2 is None:
                            continue
                        if e1[2][0] != e2[2][0] or e1[4] != e2[4]:
                            continue

                        counts["same_seed_and_field"] += 1
                        if d1 == d2:
                            counts["same_seed_field_equal_cost"] += 1
                            continue

                        counts["strict_cost_difference"] += 1
                        if d1 < d2:
                            cheap_state, expensive_state, cheap_event, expensive_event = s1, s2, e1, e2
                        else:
                            cheap_state, expensive_state, cheap_event, expensive_event = s2, s1, e2, e1

                        depth_pairs[(len(cheap_event[1]), len(expensive_event[1]))] += 1

                        # Keep the identical first window untouched. Copy only the
                        # additional history-generated prefix context from the cheaper state.
                        transplanted = expensive_state
                        for prefix_pos in cheap_event[1][1:]:
                            value = exp.read_window(
                                cheap_state, prefix_pos, args.key_width, size
                            )
                            transplanted = exp.write_window(
                                transplanted, prefix_pos, value, args.key_width, size
                            )

                        new_event = exp.candidate(
                            transplanted, start, size, args.key_width
                        )
                        if exact_same_closure(new_event, cheap_event):
                            counts["causal_restore"] += 1

                            # One-bit break control in the final transplanted context window.
                            last_pos = cheap_event[1][-1]
                            break_bit = (last_pos + args.key_width - 1) % size
                            broken = transplanted ^ (1 << break_bit)
                            broken_event = exp.candidate(
                                broken, start, size, args.key_width
                            )
                            if not exact_same_closure(broken_event, cheap_event):
                                counts["one_bit_break_destroys_restore"] += 1

    for key in (
        "start_comparisons",
        "equal_cost",
        "seq1_cheaper",
        "seq2_cheaper",
        "same_seed_and_field",
        "same_seed_field_equal_cost",
        "strict_cost_difference",
        "causal_restore",
        "one_bit_break_destroys_restore",
    ):
        print(f"{key}={counts[key]}")
    for pair, count in sorted(depth_pairs.items()):
        print(f"depth_transition={pair[1]}->{pair[0]} count={count}")


if __name__ == "__main__":
    main()
