#!/usr/bin/env python3
import argparse
import importlib.util
import itertools
import random
from collections import Counter, defaultdict
from pathlib import Path


def load_exp045():
    path = Path(__file__).resolve().parents[1] / "045_mediator_conditioned_rewrite_k5" / "run.py"
    spec = importlib.util.spec_from_file_location("exp045", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def majority(values):
    return Counter(values).most_common(1)[0][0]


def unique_orders(a, b):
    return sorted(set(itertools.permutations((a, a, a, b, b))))


def content_trace(exp, state, budget, args, policy, disjoint):
    trace = []
    for _ in range(budget):
        state, event = exp.step(
            state, args.size, args.key_width, policy, disjoint
        )
        trace.append(None if event is None else event[3:])
    return tuple(trace)


def evaluate(samples, mediator_labels):
    triple_groups = defaultdict(list)
    pair_groups = defaultdict(list)
    for i, sample in enumerate(samples):
        policy, _, _, _, aval, bval, _, _ = sample
        triple_groups[(policy, aval, bval, mediator_labels[i])].append(i)
        pair_groups[(policy, aval, bval)].append(i)

    covered = triple_correct = pair_correct = 0
    for i, sample in enumerate(samples):
        policy, _, _, _, aval, bval, _, target = sample
        peers = [
            j for j in triple_groups[(policy, aval, bval, mediator_labels[i])]
            if j != i
        ]
        if not peers:
            continue
        covered += 1
        triple_pred = majority(samples[j][7] for j in peers)
        triple_correct += int(triple_pred == target)

        pair_peers = [
            j for j in pair_groups[(policy, aval, bval)]
            if j != i
        ]
        pair_pred = majority(samples[j][7] for j in pair_peers)
        pair_correct += int(pair_pred == target)

    return covered, triple_correct, pair_correct


def main():
    exp = load_exp045()
    parser = argparse.ArgumentParser(
        description="Experiment 046: recurrent mediator-conditioned transformation context."
    )
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=8)
    parser.add_argument("--future-budget", type=int, default=8)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--null-trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    disjoint = exp.prepare_disjoint(args.size, args.key_width)
    samples = []

    for policy in ("min", "max"):
        for pos in range(0, args.size, args.position_stride):
            for a in range(1 << (args.core_width - 1)):
                b = a ^ ((1 << args.core_width) - 1)
                for sequence in unique_orders(a, b):
                    state = exp.train(sequence, pos, args, policy, disjoint)
                    event = exp.choose_triple(
                        state, args.size, args.key_width, policy, disjoint
                    )
                    if event is None:
                        continue
                    aval, bval, mval = event[3:6]
                    target = content_trace(
                        exp, state, args.future_budget, args, policy, disjoint
                    )
                    samples.append(
                        (policy, pos, a, sequence, aval, bval, mval, target)
                    )

    labels = [sample[6] for sample in samples]
    covered, correct, pair_correct = evaluate(samples, labels)

    print(f"samples={len(samples)}")
    print(f"covered={covered}")
    print(f"triple_accuracy={correct / covered:.9f}")
    print(f"pair_only_accuracy={pair_correct / covered:.9f}")

    for policy in ("min", "max"):
        subset = [sample for sample in samples if sample[0] == policy]
        sub_labels = [sample[6] for sample in subset]
        c, ok, pair_ok = evaluate(subset, sub_labels)
        print(
            f"policy={policy} samples={len(subset)} covered={c} "
            f"triple_accuracy={ok / c:.9f} pair_accuracy={pair_ok / c:.9f}"
        )

    rng = random.Random(args.seed)
    pair_indices = defaultdict(list)
    for i, sample in enumerate(samples):
        pair_indices[(sample[0], sample[4], sample[5])].append(i)

    null_accuracies = []
    for _ in range(args.null_trials):
        shuffled = labels[:]
        for indices in pair_indices.values():
            values = [shuffled[i] for i in indices]
            rng.shuffle(values)
            for i, value in zip(indices, values):
                shuffled[i] = value
        c, ok, _ = evaluate(samples, shuffled)
        null_accuracies.append(ok / c)

    print(f"null_trials={len(null_accuracies)}")
    print(f"null_mean_accuracy={sum(null_accuracies) / len(null_accuracies):.9f}")
    print(f"null_max_accuracy={max(null_accuracies):.9f}")


if __name__ == "__main__":
    main()
