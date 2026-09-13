#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_exp004():
    path = Path(__file__).resolve().parents[1] / "004_rule_sweep" / "run.py"
    spec = importlib.util.spec_from_file_location("exp004", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_rules(text):
    rules = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not rules:
        raise ValueError("at least one rule is required")
    return rules


def history_effect_signature(exp4, base, rule, pattern, size, stride, offset,
                             probe_time, probe_steps, width, single, repeat):
    initial = base.make_initial(size, "single")
    signature = []

    for pos in range(0, size, stride):
        one = exp4.run_training(
            base, initial, pattern, single, probe_time, pos, width, rule
        )
        many = exp4.run_training(
            base, initial, pattern, repeat, probe_time, pos, width, rule
        )
        q = (pos + offset) % size

        for probe in range(1 << width):
            one_impact = exp4.probe_impact(
                base, one, probe, q, width, probe_steps, rule
            )
            many_impact = exp4.probe_impact(
                base, many, probe, q, width, probe_steps, rule
            )
            signature.append(many_impact - one_impact)

    return tuple(signature)


def partition(signatures, tolerance=1e-12):
    groups = []
    used = set()

    for i, left in enumerate(signatures):
        if i in used:
            continue
        group = [i]
        used.add(i)
        for j in range(i + 1, len(signatures)):
            if j in used:
                continue
            right = signatures[j]
            if max(abs(a - b) for a, b in zip(left, right)) <= tolerance:
                group.append(j)
                used.add(j)
        groups.append(group)

    return groups


def format_partition(groups, width):
    return " ".join(
        "{" + ",".join(format(x, f"0{width}b") for x in group) + "}"
        for group in groups
    )


def main():
    exp4 = load_exp004()
    base = exp4.load_exp000()

    parser = argparse.ArgumentParser(description="Experiment 017: operational quotient drift.")
    parser.add_argument("--rules", default="98,14,113,142,226,143,126,129,110,151")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-steps", type=int, default=8)
    args = parser.parse_args()

    single = exp4.parse_schedule(args.single_schedule)
    repeat = exp4.parse_schedule(args.repeat_schedule)
    conditions = [
        ("baseline", 20, 48),
        ("offset12_t48", 12, 48),
        ("offset20_t40", 20, 40),
        ("offset20_t56", 20, 56),
    ]

    for rule in parse_rules(args.rules):
        print(f"rule={rule}")
        for name, offset, probe_time in conditions:
            signatures = [
                history_effect_signature(
                    exp4, base, rule, pattern, args.size, args.position_stride,
                    offset, probe_time, args.probe_steps, args.core_width,
                    single, repeat,
                )
                for pattern in range(1 << args.core_width)
            ]
            groups = partition(signatures)
            print(
                f"  {name:<14} classes={len(groups)}  "
                f"{format_partition(groups, args.core_width)}"
            )
        print()


if __name__ == "__main__":
    main()
