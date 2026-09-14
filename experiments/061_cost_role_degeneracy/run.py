#!/usr/bin/env python3
import argparse
import importlib.util
from collections import Counter, defaultdict
from pathlib import Path


def load_exp060():
    path = Path(__file__).resolve().parents[1] / "060_k8_cost_context_robustness" / "run.py"
    spec = importlib.util.spec_from_file_location("exp060", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def role_of(case):
    _, _, _, cheap_event, _ = case
    return cheap_event[2][0], cheap_event[4], len(cheap_event[1])


def signature_of(exp, case, width, size):
    _, cheap, _, cheap_event, _ = case
    return tuple(
        exp.read_window(cheap, pos, width, size)
        for pos in cheap_event[1][1:]
    )


def transplant_and_test(exp, case, signature, width, size):
    start, _, expensive, cheap_event, _ = case
    state = expensive
    for pos, value in zip(cheap_event[1][1:], signature):
        state = exp.write_window(state, pos, value, width, size)
    event = exp.candidate(state, start, size, width)
    if event is None:
        return False
    return (
        event[2][0], event[4], len(event[1])
    ) == role_of(case)


def main():
    m = load_exp060()
    exp = m.load_exp057()

    parser = argparse.ArgumentParser(description="Experiment 061: operational degeneracy of K8 cost-compressing contexts.")
    parser.add_argument("--key-widths", default="3,4,5")
    parser.add_argument("--window-capacity", type=int, default=6)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--backgrounds", type=int, default=32)
    args = parser.parse_args()

    for width in [int(x) for x in args.key_widths.split(",") if x.strip()]:
        size = width * args.window_capacity
        _, cases = m.collect_strict_cases(exp, width, args)

        roles = defaultdict(set)
        signatures = []
        for case in cases:
            signature = signature_of(exp, case, width, size)
            signatures.append(signature)
            roles[role_of(case)].add(signature)

        multiplicity = Counter(len(values) for values in roles.values())
        multi_roles = sum(1 for values in roles.values() if len(values) >= 2)

        same_role_total = 0
        same_role_success = 0
        different_role_same_depth_total = 0
        different_role_same_depth_success = 0

        by_role = defaultdict(list)
        by_depth = defaultdict(list)
        for index, case in enumerate(cases):
            role = role_of(case)
            by_role[role].append(index)
            by_depth[role[2]].append(index)

        for i, case in enumerate(cases):
            role = role_of(case)
            own_signature = signatures[i]

            for j in by_role[role]:
                if j == i or signatures[j] == own_signature:
                    continue
                same_role_total += 1
                same_role_success += int(
                    transplant_and_test(exp, case, signatures[j], width, size)
                )

            for j in by_depth[role[2]]:
                if j == i or role_of(cases[j]) == role:
                    continue
                different_role_same_depth_total += 1
                different_role_same_depth_success += int(
                    transplant_and_test(exp, case, signatures[j], width, size)
                )

        print(f"key_width={width}")
        print(f"strict_cases={len(cases)}")
        print(f"unique_effective_roles={len(roles)}")
        print(f"roles_with_multiple_raw_signatures={multi_roles}")
        print(f"unique_raw_signatures={len(set(signatures))}")
        print(f"max_raw_signatures_per_role={max((len(v) for v in roles.values()), default=0)}")
        for n in sorted(multiplicity):
            print(f"roles_with_{n}_signatures={multiplicity[n]}")
        print(f"different_signature_same_role_total={same_role_total}")
        print(f"different_signature_same_role_success={same_role_success}")
        print(f"different_role_same_depth_total={different_role_same_depth_total}")
        print(f"different_role_same_depth_success={different_role_same_depth_success}")
        print()


if __name__ == "__main__":
    main()
