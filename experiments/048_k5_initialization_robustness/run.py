#!/usr/bin/env python3
import argparse
import importlib.util
import itertools
import random
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


def train_from(exp, sequence, pos, initial, args, policy, disjoint):
    state = initial
    for value in sequence:
        state = exp.write_window(state, pos, value, args.core_width, args.size)
        state = exp.run_budget(
            state, args.event_budget, args.size, args.key_width,
            policy, disjoint,
        )
    return state


def apply_first(exp, state, event, args, rewrite_m):
    i, j, mpos, a, b, m = event
    a2, b2, m2 = exp.rewrite(a, b, m, args.key_width)
    state = exp.write_window(state, i, a2, args.key_width, args.size)
    state = exp.write_window(state, j, b2, args.key_width, args.size)
    if rewrite_m:
        state = exp.write_window(state, mpos, m2, args.key_width, args.size)
    return state


def backgrounds(size):
    out = []
    for seed in range(8):
        out.append((f"rand{seed}", random.Random(seed).getrandbits(size)))
    alt = sum(((i % 2) & 1) << i for i in range(size))
    out.append(("alt01", alt))
    out.append(("alt10", ((1 << size) - 1) ^ alt))
    return out


def main():
    exp = load_exp045()
    parser = argparse.ArgumentParser(description="Experiment 048: K5 initialization robustness.")
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--key-width", type=int, default=4)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=8)
    parser.add_argument("--future-budget", type=int, default=7)
    parser.add_argument("--position-stride", type=int, default=8)
    args = parser.parse_args()

    disjoint = exp.prepare_disjoint(args.size, args.key_width)
    total = active = grammar_diff = trace_diff = 0

    for name, initial in backgrounds(args.size):
        bt = ba = bg = btr = 0
        for policy in ("min", "max"):
            for pos in range(0, args.size, args.position_stride):
                for a0 in range(1 << (args.core_width - 1)):
                    b0 = a0 ^ ((1 << args.core_width) - 1)
                    for sequence in unique_orders(a0, b0):
                        state = train_from(exp, sequence, pos, initial, args, policy, disjoint)
                        event = exp.choose_triple(state, args.size, args.key_width, policy, disjoint)
                        if event is None:
                            continue
                        total += 1
                        bt += 1
                        is_active = int((event[3] & event[4]) != 0)
                        active += is_active
                        ba += is_active

                        normal = apply_first(exp, state, event, args, True)
                        frozen = apply_first(exp, state, event, args, False)
                        ng = exp.transformation_grammar(normal, args.size, args.key_width)
                        fg = exp.transformation_grammar(frozen, args.size, args.key_width)
                        gd = int(ng != fg)
                        grammar_diff += gd
                        bg += gd

                        _, nt = exp.run_budget(
                            normal, args.future_budget, args.size, args.key_width,
                            policy, disjoint, trace=True,
                        )
                        _, ft = exp.run_budget(
                            frozen, args.future_budget, args.size, args.key_width,
                            policy, disjoint, trace=True,
                        )
                        td = int(nt != ft)
                        trace_diff += td
                        btr += td
        print(f"{name}={bt},{ba},{bg},{btr}")

    print(f"valid_states={total}")
    print(f"selected_a_and_b_nonzero={active}")
    print(f"normal_vs_frozen_m_grammar_diff={grammar_diff}")
    print(f"normal_vs_frozen_m_future_trace_diff={trace_diff}")


if __name__ == "__main__":
    main()
