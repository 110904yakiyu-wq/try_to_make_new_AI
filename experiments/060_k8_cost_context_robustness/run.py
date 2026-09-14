#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter, defaultdict
from pathlib import Path


def load_exp057():
    path = Path(__file__).resolve().parents[1] / "057_self_delimiting_k8" / "run.py"
    spec = importlib.util.spec_from_file_location("exp057", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def same_target_effect(event, target, desired_depth):
    return (
        event is not None
        and len(event[1]) == desired_depth
        and event[2][0] == target[2][0]
        and event[4] == target[4]
    )


def collect_strict_cases(exp, width, args):
    size = width * args.window_capacity
    cases = []
    starts = 0

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
                    for start in range(size):
                        starts += 1
                        e1 = exp.candidate(s1, start, size, width)
                        e2 = exp.candidate(s2, start, size, width)
                        if e1 is None or e2 is None:
                            continue
                        if len(e1[1]) == len(e2[1]):
                            continue
                        if e1[2][0] != e2[2][0] or e1[4] != e2[4]:
                            continue
                        if len(e1[1]) < len(e2[1]):
                            cheap, expensive, cheap_event, expensive_event = s1, s2, e1, e2
                        else:
                            cheap, expensive, cheap_event, expensive_event = s2, s1, e2, e1
                        cases.append((start, cheap, expensive, cheap_event, expensive_event))
    return starts, cases


def context_signature(exp, state, event, width, size):
    return tuple(
        exp.read_window(state, pos, width, size)
        for pos in event[1][1:]
    )


def transplant_context(exp, recipient, target_event, values, width, size):
    state = recipient
    for pos, value in zip(target_event[1][1:], values):
        state = exp.write_window(state, pos, value, width, size)
    return state


def main():
    exp = load_exp057()
    parser = argparse.ArgumentParser(description="Experiment 060: K8 cost-context robustness and specificity.")
    parser.add_argument("--key-widths", default="3,4,5,6")
    parser.add_argument("--window-capacity", type=int, default=6)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--backgrounds", type=int, default=32)
    args = parser.parse_args()

    for width in [int(x) for x in args.key_widths.split(",") if x.strip()]:
        size = width * args.window_capacity
        starts, cases = collect_strict_cases(exp, width, args)
        counts = Counter()
        signatures = []

        for start, cheap, expensive, cheap_event, _ in cases:
            signature = context_signature(exp, cheap, cheap_event, width, size)
            signatures.append(signature)
            transplanted = transplant_context(
                exp, expensive, cheap_event, signature, width, size
            )
            event = exp.candidate(transplanted, start, size, width)
            if same_target_effect(event, cheap_event, len(cheap_event[1])):
                counts["restore"] += 1
                last_pos = cheap_event[1][-1]
                break_bit = (last_pos + width - 1) % size
                broken = transplanted ^ (1 << break_bit)
                broken_event = exp.candidate(broken, start, size, width)
                if not same_target_effect(
                    broken_event, cheap_event, len(cheap_event[1])
                ):
                    counts["one_bit_break"] += 1

        print(f"key_width={width} start_comparisons={starts}")
        print(f"strict_cost_difference={len(cases)}")
        print(f"causal_restore={counts['restore']}")
        print(f"one_bit_break_destroys_restore={counts['one_bit_break']}")

        if width in (3, 4):
            by_depth = defaultdict(list)
            for index, case in enumerate(cases):
                by_depth[len(case[3][1])].append(index)

            control = Counter()
            for i, (start, _, expensive, cheap_event, _) in enumerate(cases):
                depth = len(cheap_event[1])
                for j in by_depth[depth]:
                    if j == i:
                        continue
                    state = transplant_context(
                        exp, expensive, cheap_event, signatures[j], width, size
                    )
                    event = exp.candidate(state, start, size, width)
                    ok = same_target_effect(event, cheap_event, depth)
                    if signatures[j] == signatures[i]:
                        control["same_signature_total"] += 1
                        control["same_signature_success"] += int(ok)
                    else:
                        control["different_signature_total"] += 1
                        control["different_signature_success"] += int(ok)

            for key in (
                "same_signature_total",
                "same_signature_success",
                "different_signature_total",
                "different_signature_success",
            ):
                print(f"{key}={control[key]}")
        print()


if __name__ == "__main__":
    main()
