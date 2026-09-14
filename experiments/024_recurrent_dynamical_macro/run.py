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


def quotient_label(state, pos, width, probe_steps, rule, size):
    baseline = evolve(state, rule, size, probe_steps)
    signatures = []
    for probe in range(1 << width):
        perturbed = inject(state, pos, probe, width, size)
        perturbed = evolve(perturbed, rule, size, probe_steps)
        signatures.append(baseline ^ perturbed)

    labels = {}
    ids = []
    next_id = 0
    for signature in signatures:
        if signature not in labels:
            labels[signature] = next_id
            next_id += 1
        ids.append(labels[signature])
    return tuple(ids)


def trajectory_label(state, pos, delays, width, probe_steps, rule, size):
    return tuple(
        quotient_label(
            evolve(state, rule, size, delay),
            pos, width, probe_steps, rule, size,
        )
        for delay in delays
    )


def parse_ints(text):
    return tuple(sorted({int(x.strip()) for x in text.split(",") if x.strip()}))


def build_samples(args):
    schedules = (
        ("single", parse_ints(args.single_schedule)),
        ("repeat", parse_ints(args.repeat_schedule)),
    )
    delays = parse_ints(args.delays)
    positions = tuple(range(0, args.size, args.position_stride))
    initial = 1 << (args.size // 2)

    samples_by_rule = {}
    label_ids = {}
    next_label = 0

    for rule in range(256):
        samples = []
        for pattern in range(1 << args.core_width):
            for schedule_index, (schedule_name, schedule) in enumerate(schedules):
                history_id = pattern * len(schedules) + schedule_index
                for pos in positions:
                    state = train(
                        initial, pattern, schedule, args.training_time,
                        pos, args.core_width, rule, args.size,
                    )
                    q = (pos + args.assay_offset) % args.size
                    patch = patch_value(
                        state, q, args.core_width, args.radius, args.size
                    )
                    label = trajectory_label(
                        state, q, delays, args.core_width,
                        args.probe_steps, rule, args.size,
                    )
                    key = (rule, label)
                    if key not in label_ids:
                        label_ids[key] = next_label
                        next_label += 1
                    samples.append((patch, label_ids[key], history_id))
        samples_by_rule[rule] = samples

    return samples_by_rule


def predict_rule(samples, patch_override=None):
    patches = [sample[0] for sample in samples] if patch_override is None else patch_override

    group_all = defaultdict(Counter)
    group_history = defaultdict(Counter)
    rule_all = Counter()
    rule_history = defaultdict(Counter)

    for i, (_, label, history_id) in enumerate(samples):
        patch = patches[i]
        group_all[patch][label] += 1
        group_history[(patch, history_id)][label] += 1
        rule_all[label] += 1
        rule_history[history_id][label] += 1

    covered = correct = 0
    base_covered = base_correct = 0

    for i, (_, label, history_id) in enumerate(samples):
        patch = patches[i]

        counts = group_all[patch].copy()
        counts.subtract(group_history[(patch, history_id)])
        valid = [(count, candidate) for candidate, count in counts.items() if count > 0]
        if valid:
            prediction = max(valid)[1]
            covered += 1
            correct += int(prediction == label)

        base = rule_all.copy()
        base.subtract(rule_history[history_id])
        valid_base = [(count, candidate) for candidate, count in base.items() if count > 0]
        if valid_base:
            prediction = max(valid_base)[1]
            base_covered += 1
            base_correct += int(prediction == label)

    return covered, correct, base_covered, base_correct


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 024: recurrent local context predicts future operational trajectory."
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
    parser.add_argument("--delays", default="0,1,2,4,8")
    parser.add_argument("--null-trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    samples_by_rule = build_samples(args)
    total_samples = sum(len(samples) for samples in samples_by_rule.values())

    observed = [0, 0, 0, 0]
    for samples in samples_by_rule.values():
        values = predict_rule(samples)
        observed = [a + b for a, b in zip(observed, values)]

    coverage = observed[0] / total_samples
    accuracy = observed[1] / observed[0]
    rule_only = observed[3] / observed[2]

    rng = random.Random(args.seed)
    null_accuracy = []
    null_coverage = []

    for _ in range(args.null_trials):
        totals = [0, 0, 0, 0]
        for samples in samples_by_rule.values():
            patches = [sample[0] for sample in samples]
            rng.shuffle(patches)
            values = predict_rule(samples, patches)
            totals = [a + b for a, b in zip(totals, values)]
        null_coverage.append(totals[0] / total_samples)
        null_accuracy.append(totals[1] / totals[0])

    print(f"samples={total_samples}")
    print(f"radius={args.radius}")
    print(f"delays={args.delays}")
    print(f"cross_history_coverage={coverage:.9f}")
    print(f"trajectory_accuracy={accuracy:.9f}")
    print(f"rule_only_accuracy={rule_only:.9f}")
    print(f"null_trials={len(null_accuracy)}")
    print(f"null_mean_accuracy={sum(null_accuracy) / len(null_accuracy):.9f}")
    print(f"null_min_accuracy={min(null_accuracy):.9f}")
    print(f"null_max_accuracy={max(null_accuracy):.9f}")
    print(f"null_mean_coverage={sum(null_coverage) / len(null_coverage):.9f}")


if __name__ == "__main__":
    main()
