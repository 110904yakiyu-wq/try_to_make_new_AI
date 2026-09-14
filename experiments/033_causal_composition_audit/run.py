#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_exp032():
    path = Path(__file__).resolve().parents[1] / "032_recurrent_execution_macro" / "run.py"
    spec = importlib.util.spec_from_file_location("exp032", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def transplant_patch(exp, recipient, donor, pos, width, radius, size):
    out = recipient
    for j in range(width + 2 * radius):
        index = (pos - radius + j) % size
        target = exp.bit(donor, index, size)
        if exp.bit(out, index, size) != target:
            out ^= 1 << index
    return out


def trace_distance(a, b):
    return sum(x != y for x, y in zip(a, b))


def main():
    exp = load_exp032()
    parser = argparse.ArgumentParser(description="Experiment 033: causal pair-composition audit.")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--train-pos", type=int, default=0)
    parser.add_argument("--second-offset", type=int, default=6)
    parser.add_argument("--event-budget", type=int, default=128)
    parser.add_argument("--cascade-budget", type=int, default=32)
    args = parser.parse_args()

    eligible = p_exact = q_exact = joint_exact = joint_better = strict_synergy = 0

    for policy in ("min", "max"):
        for rule in range(256):
            for a in range(1 << (args.core_width - 1)):
                b = a ^ ((1 << args.core_width) - 1)
                seq1 = (a, a, a, b, b)
                seq2 = (b, b, a, a, a)
                s1 = exp.train(rule, seq1, args, policy)
                s2 = exp.train(rule, seq2, args, policy)

                for recipient, donor in ((s1, s2), (s2, s1)):
                    _, recipient_trace = exp.run_budget(
                        recipient, rule, args.size, args.cascade_budget, policy, trace=True
                    )
                    _, donor_trace = exp.run_budget(
                        donor, rule, args.size, args.cascade_budget, policy, trace=True
                    )
                    if recipient_trace == donor_trace:
                        continue
                    eligible += 1

                    p_state = transplant_patch(
                        exp, recipient, donor, args.train_pos,
                        args.core_width, args.radius, args.size,
                    )
                    q_pos = (args.train_pos + args.second_offset) % args.size
                    q_state = transplant_patch(
                        exp, recipient, donor, q_pos,
                        args.core_width, args.radius, args.size,
                    )
                    pq_state = transplant_patch(
                        exp, p_state, donor, q_pos,
                        args.core_width, args.radius, args.size,
                    )

                    _, p_trace = exp.run_budget(
                        p_state, rule, args.size, args.cascade_budget, policy, trace=True
                    )
                    _, q_trace = exp.run_budget(
                        q_state, rule, args.size, args.cascade_budget, policy, trace=True
                    )
                    _, pq_trace = exp.run_budget(
                        pq_state, rule, args.size, args.cascade_budget, policy, trace=True
                    )

                    dp = trace_distance(p_trace, donor_trace)
                    dq = trace_distance(q_trace, donor_trace)
                    dpq = trace_distance(pq_trace, donor_trace)
                    p_exact += int(p_trace == donor_trace)
                    q_exact += int(q_trace == donor_trace)
                    joint_exact += int(pq_trace == donor_trace)
                    joint_better += int(dpq < min(dp, dq))
                    strict_synergy += int(
                        pq_trace == donor_trace
                        and p_trace != donor_trace
                        and q_trace != donor_trace
                    )

    print(f"eligible={eligible}")
    print(f"p_exact={p_exact}")
    print(f"q_exact={q_exact}")
    print(f"joint_exact={joint_exact}")
    print(f"joint_better_than_both={joint_better}")
    print(f"strict_joint_only_exact={strict_synergy}")


if __name__ == "__main__":
    main()
