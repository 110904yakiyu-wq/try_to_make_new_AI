#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter
from pathlib import Path


def load_exp054():
    path = Path(__file__).resolve().parents[1] / "054_variable_arity_k7" / "run.py"
    spec = importlib.util.spec_from_file_location("exp054", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arity_repertoire(full_repertoire):
    return frozenset(arity for arity, _ in full_repertoire)


def full_event_signature(event):
    if event is None:
        return None
    return tuple(event[1]), tuple(event[2])


def run_audit(exp, args, use_full_repertoire):
    groups = exp.prepare_groups(args.size, args.key_width, args.max_arity)
    counts = Counter()

    def observe(state):
        full = exp.repertoire(state, args, groups)
        return full if use_full_repertoire else arity_repertoire(full)

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(args.size)
        for policy in ("min", "max"):
            for pos in range(0, args.size, args.position_stride):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    s1 = exp.train((a, a, a, b, b), pos, initial, args, groups, policy)
                    s2 = exp.train((b, b, a, a, a), pos, initial, args, groups, policy)
                    if observe(s1) != observe(s2):
                        continue
                    counts["initial_equal"] += 1

                    for bridge in range(1 << args.core_width):
                        x1 = exp.write_window(s1, pos, bridge, args.core_width, args.size)
                        x2 = exp.write_window(s2, pos, bridge, args.core_width, args.size)
                        counts["bridge_trials"] += 1
                        if observe(x1) != observe(x2):
                            continue
                        counts["postbridge_equal"] += 1

                        e1 = exp.choose_event(x1, args.size, args.key_width, groups, policy)
                        e2 = exp.choose_event(x2, args.size, args.key_width, groups, policy)
                        if full_event_signature(e1) != full_event_signature(e2):
                            continue
                        counts["same_full_event"] += 1

                        y1, _ = exp.step(x1, args.size, args.key_width, groups, policy)
                        y2, _ = exp.step(x2, args.size, args.key_width, groups, policy)
                        if observe(y1) != observe(y2):
                            counts["postevent_divergence"] += 1

    return counts


def main():
    exp = load_exp054()
    parser = argparse.ArgumentParser(description="Experiment 056: K7 second-order arity audit.")
    parser.add_argument("--size", type=int, default=20)
    parser.add_argument("--key-width", type=int, default=5)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--max-arity", type=int, default=4)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--position-stride", type=int, default=5)
    parser.add_argument("--backgrounds", type=int, default=8)
    args = parser.parse_args()

    for name, full in (("arity_only", False), ("full_relation_repertoire", True)):
        counts = run_audit(exp, args, full)
        print(f"mode={name}")
        for key in ("initial_equal", "bridge_trials", "postbridge_equal", "same_full_event", "postevent_divergence"):
            print(f"{key}={counts[key]}")
        print()


if __name__ == "__main__":
    main()
