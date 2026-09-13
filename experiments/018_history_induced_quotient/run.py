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


def full_probe_effect(exp4, base, state, probe, pos, width, steps, rule):
    baseline = state[:]
    perturbed = exp4.inject_core(base, state, pos, probe, width)
    for _ in range(steps):
        baseline = exp4.step_rule(baseline, rule)
        perturbed = exp4.step_rule(perturbed, rule)
    return tuple(int(a != b) for a, b in zip(baseline, perturbed))


def probe_signatures(exp4, base, rule, training_pattern, schedule, size, stride,
                     offset, probe_time, probe_steps, width):
    initial = base.make_initial(size, "single")
    signatures = [[] for _ in range(1 << width)]

    for pos in range(0, size, stride):
        state = exp4.run_training(
            base, initial, training_pattern, schedule,
            probe_time, pos, width, rule,
        )
        q = (pos + offset) % size
        for probe in range(1 << width):
            signatures[probe].extend(
                full_probe_effect(
                    exp4, base, state, probe, q, width, probe_steps, rule
                )
            )

    return [tuple(signature) for signature in signatures]


def partition(signatures):
    groups = []
    used = set()
    for i, signature in enumerate(signatures):
        if i in used:
            continue
        group = [i]
        used.add(i)
        for j in range(i + 1, len(signatures)):
            if j not in used and signatures[j] == signature:
                group.append(j)
                used.add(j)
        groups.append(group)
    return groups


def refines(left, right):
    """Return True when partition left refines partition right."""
    right_sets = [set(group) for group in right]
    return all(any(set(group) <= parent for parent in right_sets) for group in left)


def relation(before, after):
    after_refines_before = refines(after, before)
    before_refines_after = refines(before, after)
    if after_refines_before and before_refines_after:
        return "same"
    if after_refines_before:
        return "refine"
    if before_refines_after:
        return "coarsen"
    return "reorganize"


def fmt(groups, width):
    return " ".join(
        "{" + ",".join(format(x, f"0{width}b") for x in group) + "}"
        for group in groups
    )


def main():
    exp4 = load_exp004()
    base = exp4.load_exp000()

    parser = argparse.ArgumentParser(
        description="Experiment 018: quotient change caused only by substrate history."
    )
    parser.add_argument("--rules", default="98,14,113,142,226,143,126,129,110,151,159")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--offset", type=int, default=20)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--probe-time", type=int, default=48)
    parser.add_argument("--probe-steps", type=int, default=8)
    args = parser.parse_args()

    single = exp4.parse_schedule(args.single_schedule)
    repeat = exp4.parse_schedule(args.repeat_schedule)

    for rule in parse_rules(args.rules):
        counts = {"same": 0, "refine": 0, "coarsen": 0, "reorganize": 0}
        changes = []

        for training_pattern in range(1 << args.core_width):
            before = partition(
                probe_signatures(
                    exp4, base, rule, training_pattern, single,
                    args.size, args.position_stride, args.offset,
                    args.probe_time, args.probe_steps, args.core_width,
                )
            )
            after = partition(
                probe_signatures(
                    exp4, base, rule, training_pattern, repeat,
                    args.size, args.position_stride, args.offset,
                    args.probe_time, args.probe_steps, args.core_width,
                )
            )
            kind = relation(before, after)
            counts[kind] += 1
            if kind != "same":
                changes.append((training_pattern, kind, before, after))

        print(
            f"rule={rule} same={counts['same']} refine={counts['refine']} "
            f"coarsen={counts['coarsen']} reorganize={counts['reorganize']}"
        )
        for training_pattern, kind, before, after in changes:
            print(
                f"  train={format(training_pattern, f'0{args.core_width}b')} "
                f"{kind}: {fmt(before, args.core_width)} -> {fmt(after, args.core_width)}"
            )
        print()


if __name__ == "__main__":
    main()
