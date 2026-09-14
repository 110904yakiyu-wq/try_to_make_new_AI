#!/usr/bin/env python3
import argparse
import random
from collections import Counter, defaultdict


def step(state, rule, size):
    mask = (1 << size) - 1
    left = ((state << 1) & mask) | (state >> (size - 1))
    right = (state >> 1) | ((state & 1) << (size - 1))
    center = state
    nl = (~left) & mask
    nc = (~center) & mask
    nr = (~right) & mask
    out = 0
    for index in range(8):
        if not ((rule >> index) & 1):
            continue
        l = (index >> 2) & 1
        c = (index >> 1) & 1
        r = index & 1
        out |= (
            (left if l else nl)
            & (center if c else nc)
            & (right if r else nr)
        )
    return out


def evolve(state, rule, size, steps):
    for _ in range(steps):
        state = step(state, rule, size)
    return state


def inject(state, pos, value, width, size):
    for j in range(width):
        bit = (value >> (width - 1 - j)) & 1
        index = (pos + j) % size
        if bit:
            state |= 1 << index
        else:
            state &= ~(1 << index)
    return state


def train(initial, pattern, schedule, steps, pos, width, rule, size):
    state = initial
    schedule = set(schedule)
    for t in range(steps):
        if t in schedule:
            state = inject(state, pos, pattern, width, size)
        state = step(state, rule, size)
    return state


def patch_value(state, pos, width, radius, size):
    value = 0
    start = pos - radius
    for j in range(width + 2 * radius):
        index = (start + j) % size
        value = (value << 1) | ((state >> index) & 1)
    return value


def local_quotient_label(state, pos, width, probe_steps, rule, size):
    baseline = evolve(state, rule, size, probe_steps)
    signatures = []
    for probe in range(1 << width):
        perturbed = inject(state, pos, probe, width, size)
        perturbed = evolve(perturbed, rule, size, probe_steps)
        signatures.append(baseline ^ perturbed)

    ids = []
    labels = {}
    next_id = 0
    for signature in signatures:
        if signature not in labels:
            labels[signature] = next_id
            next_id += 1
        ids.append(labels[signature])
    return tuple(ids)


def parse_schedule(text):
    return tuple(sorted({int(x.strip()) for x in text.split(",") if x.strip()}))


def build_samples(args):
    single = parse_schedule(args.single_schedule)
    repeat = parse_schedule(args.repeat_schedule)
    schedules = (("single", single), ("repeat", repeat))
    positions = tuple(range(0, args.size, args.position_stride))
    initial = 1 << (args.size // 2)

    samples = []
    for rule in range(256):
        for pattern in range(1 << args.core_width):
            for schedule_name, schedule in schedules:
                history = (pattern, schedule_name)
                for pos in positions:
                    state = train(
                        initial, pattern, schedule, args.training_time,
                        pos, args.core_width, rule, args.size,
                    )
                    q = (pos + args.assay_offset) % args.size
                    patch = patch_value(
                        state, q, args.core_width, args.radius, args.size
                    )
                    label = local_quotient_label(
                        state, q, args.core_width, args.probe_steps,
                        rule, args.size,
                    )
                    samples.append([rule, patch, label, history, pos])
    return samples


def predict_cross_history(samples):
    group_history = defaultdict(Counter)
    group_all = defaultdict(Counter)
    rule_history = defaultdict(Counter)
    rule_all = defaultdict(Counter)

    for rule, patch, label, history, _ in samples:
        group_history[(rule, patch, history)][label] += 1
        group_all[(rule, patch)][label] += 1
        rule_history[(rule, history)][label] += 1
        rule_all[rule][label] += 1

    covered = correct = 0
    base_covered = base_correct = 0

    for rule, patch, label, history, _ in samples:
        counts = group_all[(rule, patch)].copy()
        counts.subtract(group_history[(rule, patch, history)])
        counts = Counter({k: v for k, v in counts.items() if v > 0})
        if counts:
            prediction = max(counts.items(), key=lambda item: (item[1], repr(item[0])))[0]
            covered += 1
            correct += int(prediction == label)

        base = rule_all[rule].copy()
        base.subtract(rule_history[(rule, history)])
        base = Counter({k: v for k, v in base.items() if v > 0})
        if base:
            prediction = max(base.items(), key=lambda item: (item[1], repr(item[0])))[0]
            base_covered += 1
            base_correct += int(prediction == label)

    return (
        covered / len(samples),
        correct / covered if covered else 0.0,
        base_correct / base_covered if base_covered else 0.0,
    )


def shuffled_null(samples, trials, seed):
    rng = random.Random(seed)
    indices_by_rule = defaultdict(list)
    for i, sample in enumerate(samples):
        indices_by_rule[sample[0]].append(i)

    values = []
    coverage = []
    for _ in range(trials):
        shuffled = [sample[:] for sample in samples]
        for indices in indices_by_rule.values():
            patches = [shuffled[i][1] for i in indices]
            rng.shuffle(patches)
            for i, patch in zip(indices, patches):
                shuffled[i][1] = patch
        cov, acc, _ = predict_cross_history(shuffled)
        coverage.append(cov)
        values.append(acc)
    return values, coverage


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 023: recurrent endogenous local contexts across distinct histories."
    )
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--training-time", type=int, default=48)
    parser.add_argument("--assay-offset", type=int, default=20)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--null-trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    samples = build_samples(args)
    coverage, accuracy, rule_baseline = predict_cross_history(samples)
    null, null_coverage = shuffled_null(samples, args.null_trials, args.seed)

    print(f"samples={len(samples)}")
    print(f"radius={args.radius}")
    print(f"cross_history_coverage={coverage:.9f}")
    print(f"cross_history_accuracy={accuracy:.9f}")
    print(f"rule_only_accuracy={rule_baseline:.9f}")
    print(f"null_trials={len(null)}")
    print(f"null_mean_accuracy={sum(null) / len(null):.9f}")
    print(f"null_min_accuracy={min(null):.9f}")
    print(f"null_max_accuracy={max(null):.9f}")
    print(f"null_mean_coverage={sum(null_coverage) / len(null_coverage):.9f}")


if __name__ == "__main__":
    main()
