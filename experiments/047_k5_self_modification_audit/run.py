#!/usr/bin/env python3
import argparse
import importlib.util
import itertools
from collections import Counter
from pathlib import Path


def load_exp045():
    path = Path(__file__).resolve().parents[1] / "045_mediator_conditioned_rewrite_k5" / "run.py"
    spec = importlib.util.spec_from_file_location("exp045", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unique_orders(a, b):
    return sorted(set(itertools.permutations((a, a, a, b, b))))


def apply_first_event(exp, state, event, args, rewrite_m):
    i, j, mpos, a, b, m = event
    a2, b2, m2 = exp.rewrite(a, b, m, args.key_width)
    state = exp.write_window(state, i, a2, args.key_width, args.size)
    state = exp.write_window(state, j, b2, args.key_width, args.size)
    if rewrite_m:
        state = exp.write_window(state, mpos, m2, args.key_width, args.size)
    return state


def main():
    exp = load_exp045()
    parser = argparse.ArgumentParser(description="Experiment 047: K5 M-rewrite audit.")
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=8)
    parser.add_argument("--future-budget", type=int, default=7)
    parser.add_argument("--position-stride", type=int, default=8)
    args = parser.parse_args()

    disjoint = exp.prepare_disjoint(args.size, args.key_width)
    counts = Counter()
    histories = 0
    nonzero_ab = 0
    grammar_diff = 0
    trace_diff = 0

    for policy in ("min", "max"):
        for pos in range(0, args.size, args.position_stride):
            for a0 in range(1 << (args.core_width - 1)):
                b0 = a0 ^ ((1 << args.core_width) - 1)
                for sequence in unique_orders(a0, b0):
                    state = exp.train(sequence, pos, args, policy, disjoint)
                    event = exp.choose_triple(
                        state, args.size, args.key_width, policy, disjoint
                    )
                    if event is None:
                        continue
                    histories += 1
                    nonzero_ab += int((event[3] & event[4]) != 0)

                    before = exp.transformation_grammar(
                        state, args.size, args.key_width
                    )
                    normal = apply_first_event(exp, state, event, args, True)
                    frozen = apply_first_event(exp, state, event, args, False)
                    normal_g = exp.transformation_grammar(
                        normal, args.size, args.key_width
                    )
                    frozen_g = exp.transformation_grammar(
                        frozen, args.size, args.key_width
                    )

                    rel = exp.relation(before, normal_g)
                    if rel == "same":
                        counts["same"] += 1
                    elif rel == "seq2_superset":
                        counts["strict_expansion"] += 1
                    else:
                        counts["reorganize"] += 1

                    grammar_diff += int(normal_g != frozen_g)
                    _, normal_trace = exp.run_budget(
                        normal, args.future_budget, args.size, args.key_width,
                        policy, disjoint, trace=True,
                    )
                    _, frozen_trace = exp.run_budget(
                        frozen, args.future_budget, args.size, args.key_width,
                        policy, disjoint, trace=True,
                    )
                    trace_diff += int(normal_trace != frozen_trace)

    print(f"histories={histories}")
    print(f"selected_a_and_b_nonzero={nonzero_ab}")
    print(f"post_event_grammar_same={counts['same']}")
    print(f"post_event_grammar_strict_expansion={counts['strict_expansion']}")
    print(f"post_event_grammar_reorganize={counts['reorganize']}")
    print(f"normal_vs_frozen_m_grammar_diff={grammar_diff}")
    print(f"normal_vs_frozen_m_future_trace_diff={trace_diff}")


if __name__ == "__main__":
    main()
