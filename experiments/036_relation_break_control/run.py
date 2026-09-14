#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_exp035():
    path = Path(__file__).resolve().parents[1] / "035_rendezvous_k2" / "run.py"
    spec = importlib.util.spec_from_file_location("exp035", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    exp = load_exp035()
    parser = argparse.ArgumentParser(description="Experiment 036: break the rendezvous relation after joint transplant.")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=32)
    parser.add_argument("--cascade-budget", type=int, default=16)
    args = parser.parse_args()

    eligible = 0
    joint_exact = 0
    broken_exact = 0
    broken_same_as_joint = 0

    for policy in ("min", "max"):
        for pos in range(0, args.size, 8):
            for a in range(1 << (args.core_width - 1)):
                b = a ^ ((1 << args.core_width) - 1)
                seq1 = (a, a, a, b, b)
                seq2 = (b, b, a, a, a)
                s1 = exp.train(seq1, pos, args, policy)
                s2 = exp.train(seq2, pos, args, policy)

                for recipient, donor in ((s1, s2), (s2, s1)):
                    donor_pair = exp.choose_pair(
                        exp.rendezvous_pairs(donor, args.size, args.key_width), policy
                    )
                    if donor_pair is None:
                        continue
                    _, recipient_trace = exp.run_budget(
                        recipient, args.cascade_budget, args.size, args.key_width, policy, trace=True
                    )
                    _, donor_trace = exp.run_budget(
                        donor, args.cascade_budget, args.size, args.key_width, policy, trace=True
                    )
                    if recipient_trace == donor_trace:
                        continue
                    eligible += 1

                    i, j, _ = donor_pair
                    joint = exp.transplant(
                        recipient, donor, i, args.key_width, 0, args.size
                    )
                    joint = exp.transplant(
                        joint, donor, j, args.key_width, 0, args.size
                    )
                    _, joint_trace = exp.run_budget(
                        joint, args.cascade_budget, args.size, args.key_width, policy, trace=True
                    )
                    if joint_trace != donor_trace:
                        continue
                    joint_exact += 1

                    # Minimal relation-breaking control: flip one bit in endpoint j's key.
                    broken = joint ^ (1 << ((j + args.key_width - 1) % args.size))
                    _, broken_trace = exp.run_budget(
                        broken, args.cascade_budget, args.size, args.key_width, policy, trace=True
                    )
                    broken_exact += int(broken_trace == donor_trace)
                    broken_same_as_joint += int(broken_trace == joint_trace)

    print(f"eligible={eligible}")
    print(f"joint_exact={joint_exact}")
    print(f"broken_relation_exact={broken_exact}")
    print(f"broken_relation_same_as_joint={broken_same_as_joint}")


if __name__ == "__main__":
    main()
