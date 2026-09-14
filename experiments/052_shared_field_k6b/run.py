#!/usr/bin/env python3
import argparse
import importlib.util
import itertools
import random
from collections import Counter
from pathlib import Path


def load_exp050():
    path = Path(__file__).resolve().parents[1] / "050_role_symmetric_k6" / "run.py"
    spec = importlib.util.spec_from_file_location("exp050", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rewrite(exp, a, b, c, width):
    mask = (1 << width) - 1
    field = exp.rotl(a ^ b ^ c, width)
    return (a ^ field) & mask, (b ^ field) & mask, (c ^ field) & mask


def step(exp, state, args, policy, disjoint):
    event = exp.choose_triple(state, args.size, args.key_width, policy, disjoint)
    if event is None:
        return state, None
    i, j, k, a, b, c = event
    a2, b2, c2 = rewrite(exp, a, b, c, args.key_width)
    state = exp.write_window(state, i, a2, args.key_width, args.size)
    state = exp.write_window(state, j, b2, args.key_width, args.size)
    state = exp.write_window(state, k, c2, args.key_width, args.size)
    return state, (i, j, k, a, b, c, a2, b2, c2)


def run_budget(exp, state, budget, args, policy, disjoint, trace=False):
    events = []
    for _ in range(budget):
        state, event = step(exp, state, args, policy, disjoint)
        if trace:
            events.append(event)
    return (state, tuple(events)) if trace else state


def train(exp, sequence, pos, initial, args, policy, disjoint):
    state = initial
    for value in sequence:
        state = exp.write_window(state, pos, value, args.core_width, args.size)
        state = run_budget(exp, state, args.event_budget, args, policy, disjoint)
    return state


def transplant(exp, recipient, donor, positions, subset, args):
    state = recipient
    for index in subset:
        pos = positions[index]
        value = exp.read_window(donor, pos, args.key_width, args.size)
        state = exp.write_window(state, pos, value, args.key_width, args.size)
    return state


def main():
    exp = load_exp050()
    parser = argparse.ArgumentParser(description="Experiment 052: shared-field K6b.")
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=8)
    parser.add_argument("--future-budget", type=int, default=8)
    parser.add_argument("--backgrounds", type=int, default=8)
    args = parser.parse_args()

    disjoint = exp.prepare_disjoint(args.size, args.key_width)
    counts = Counter()
    turnover = Counter()
    subset_counts = Counter()
    trace_diff = 0
    cases = 0
    directed = 0

    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(args.size)
        for policy in ("min", "max"):
            for pos in range(0, args.size, 8):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    s1 = train(exp, (a, a, a, b, b), pos, initial, args, policy, disjoint)
                    s2 = train(exp, (b, b, a, a, a), pos, initial, args, policy, disjoint)
                    r1 = exp.repertoire(s1, args.size, args.key_width, disjoint)
                    r2 = exp.repertoire(s2, args.size, args.key_width, disjoint)
                    counts[exp.relation(r1, r2)] += 1

                    _, t1 = run_budget(exp, s1, args.future_budget, args, policy, disjoint, trace=True)
                    _, t2 = run_budget(exp, s2, args.future_budget, args, policy, disjoint, trace=True)
                    different = t1 != t2
                    trace_diff += int(different)
                    cases += 1

                    for state in (s1, s2):
                        e1 = exp.choose_triple(state, args.size, args.key_width, policy, disjoint)
                        state2, _ = step(exp, state, args, policy, disjoint)
                        e2 = exp.choose_triple(state2, args.size, args.key_width, policy, disjoint)
                        if e1 is not None and e2 is not None:
                            turnover[len(set(e1[:3]) & set(e2[:3]))] += 1

                    if not different:
                        continue

                    for donor, recipient, donor_trace in ((s1, s2, t1), (s2, s1, t2)):
                        directed += 1
                        event = exp.choose_triple(donor, args.size, args.key_width, policy, disjoint)
                        if event is None:
                            subset_counts["none"] += 1
                            continue
                        positions = event[:3]
                        best = None
                        for width in (1, 2, 3):
                            for subset in itertools.combinations(range(3), width):
                                state = transplant(exp, recipient, donor, positions, subset, args)
                                _, trace = run_budget(exp, state, args.future_budget, args, policy, disjoint, trace=True)
                                if trace == donor_trace:
                                    best = width
                                    break
                            if best is not None:
                                break
                        subset_counts[best if best is not None else "none"] += 1

    print(f"cases={cases}")
    print(f"same={counts['same']}")
    print(f"seq1_superset={counts['seq1_superset']}")
    print(f"seq2_superset={counts['seq2_superset']}")
    print(f"reorganize={counts['reorganize']}")
    print(f"future_trace_diff={trace_diff}")
    for overlap in (3, 2, 1, 0):
        print(f"event_endpoint_overlap_{overlap}={turnover[overlap]}")
    print(f"directed_trace_diff_cases={directed}")
    print(f"minimum_1_endpoint={subset_counts[1]}")
    print(f"minimum_2_endpoints={subset_counts[2]}")
    print(f"minimum_3_endpoints={subset_counts[3]}")
    print(f"not_reproduced_by_selected_triple={subset_counts['none']}")


if __name__ == "__main__":
    main()
