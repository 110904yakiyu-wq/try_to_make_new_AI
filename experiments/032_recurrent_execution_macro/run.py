#!/usr/bin/env python3
import argparse
import random
from collections import Counter, defaultdict


def bit(state, index, size):
    return (state >> (index % size)) & 1


def synchronous_step(state, rule, size):
    mask = (1 << size) - 1
    left = ((state << 1) & mask) | (state >> (size - 1))
    right = (state >> 1) | ((state & 1) << (size - 1))
    center = state
    nl = (~left) & mask
    nc = (~center) & mask
    nr = (~right) & mask
    out = 0
    for code in range(8):
        if not ((rule >> code) & 1):
            continue
        l = (code >> 2) & 1
        c = (code >> 1) & 1
        r = code & 1
        out |= (
            (left if l else nl)
            & (center if c else nc)
            & (right if r else nr)
        )
    return out


def enabled_mask(state, rule, size):
    return state ^ synchronous_step(state, rule, size)


def choose_event(mask, policy):
    if not mask:
        return None
    if policy == "min":
        low = mask & -mask
        return low.bit_length() - 1
    if policy == "max":
        return mask.bit_length() - 1
    raise ValueError(policy)


def run_budget(state, rule, size, budget, policy, trace=False):
    events = []
    for _ in range(budget):
        enabled = enabled_mask(state, rule, size)
        index = choose_event(enabled, policy)
        if index is None:
            if trace:
                events.append(-1)
            continue
        state ^= 1 << index
        if trace:
            events.append(index)
    return (state, tuple(events)) if trace else state


def inject(state, pos, value, width, size):
    for j in range(width):
        index = (pos + j) % size
        target = (value >> (width - 1 - j)) & 1
        if bit(state, index, size) != target:
            state ^= 1 << index
    return state


def patch_value(state, pos, core_width, radius, size):
    value = 0
    for j in range(core_width + 2 * radius):
        index = (pos - radius + j) % size
        value = (value << 1) | bit(state, index, size)
    return value


def train(rule, sequence, args, policy):
    state = 1 << (args.size // 2)
    for value in sequence:
        state = inject(
            state, args.train_pos, value,
            args.core_width, args.size,
        )
        state = run_budget(
            state, rule, args.size,
            args.event_budget, policy,
        )
    return state


def majority(values):
    return Counter(values).most_common(1)[0][0]


def evaluate(samples, patch_labels):
    by_patch = defaultdict(list)
    by_rule = defaultdict(list)
    for index, sample in enumerate(samples):
        policy, rule, _, _, _, _ = sample
        by_patch[(policy, rule, patch_labels[index])].append(index)
        by_rule[(policy, rule)].append(index)

    covered = 0
    correct = 0
    rule_correct = 0

    for index, sample in enumerate(samples):
        policy, rule, _, _, _, trace = sample
        peers = [
            j for j in by_patch[(policy, rule, patch_labels[index])]
            if j != index
        ]
        if not peers:
            continue

        covered += 1
        predicted = majority(samples[j][5] for j in peers)
        correct += int(predicted == trace)

        rule_peers = [j for j in by_rule[(policy, rule)] if j != index]
        rule_predicted = majority(samples[j][5] for j in rule_peers)
        rule_correct += int(rule_predicted == trace)

    return covered, correct, rule_correct


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 032: natural recurrence of local K1 execution macros."
    )
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--train-pos", type=int, default=0)
    parser.add_argument("--event-budget", type=int, default=128)
    parser.add_argument("--cascade-budget", type=int, default=32)
    parser.add_argument("--null-trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    samples = []
    for policy in ("min", "max"):
        for rule in range(256):
            for a in range(1 << (args.core_width - 1)):
                b = a ^ ((1 << args.core_width) - 1)
                for order, sequence in (
                    ("seq1", (a, a, a, b, b)),
                    ("seq2", (b, b, a, a, a)),
                ):
                    state = train(rule, sequence, args, policy)
                    patch = patch_value(
                        state, args.train_pos,
                        args.core_width, args.radius, args.size,
                    )
                    _, trace = run_budget(
                        state, rule, args.size,
                        args.cascade_budget, policy, trace=True,
                    )
                    samples.append((policy, rule, a, order, patch, trace))

    labels = [sample[4] for sample in samples]
    covered, correct, rule_correct = evaluate(samples, labels)

    print(f"samples={len(samples)}")
    print(f"covered={covered}")
    print(f"coverage_fraction={covered / len(samples):.9f}")
    print(f"patch_trace_correct={correct}")
    print(f"patch_trace_accuracy={correct / covered:.9f}")
    print(f"rule_only_correct_on_covered={rule_correct}")
    print(f"rule_only_accuracy_on_covered={rule_correct / covered:.9f}")

    rng = random.Random(args.seed)
    groups = defaultdict(list)
    for i, sample in enumerate(samples):
        groups[(sample[0], sample[1])].append(i)

    null_accuracies = []
    for _ in range(args.null_trials):
        shuffled = labels[:]
        for indices in groups.values():
            values = [shuffled[i] for i in indices]
            rng.shuffle(values)
            for index, value in zip(indices, values):
                shuffled[index] = value
        null_covered, null_correct, _ = evaluate(samples, shuffled)
        if null_covered != covered:
            raise RuntimeError("within-rule shuffle unexpectedly changed coverage")
        null_accuracies.append(null_correct / null_covered)

    print(f"null_trials={len(null_accuracies)}")
    print(f"null_mean_accuracy={sum(null_accuracies) / len(null_accuracies):.9f}")
    print(f"null_max_accuracy={max(null_accuracies):.9f}")


if __name__ == "__main__":
