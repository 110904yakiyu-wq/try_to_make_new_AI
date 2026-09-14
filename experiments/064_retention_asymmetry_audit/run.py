#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter
from pathlib import Path


def load_exp057():
    path = Path(__file__).resolve().parents[1] / "057_self_delimiting_k8" / "run.py"
    spec = importlib.util.spec_from_file_location("exp057", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def query(exp, state, probe, pos, size, width, core_width):
    state = exp.write_window(state, pos, probe, core_width, size)
    event = exp.candidate(state, pos, size, width)
    if event is None:
        return None
    return event[2][0], event[4], len(event[1])


def step_variant(exp, state, size, width, policy, variant):
    event = exp.choose_event(state, size, width, policy)
    if event is None:
        return state
    _, positions, values, outputs, field = event
    for p, value in zip(positions, outputs):
        state = exp.write_window(state, p, value, width, size)
    trace_pos = (positions[-1] + width) % size
    if trace_pos in positions:
        return state
    if variant == "field":
        state = exp.write_window(state, trace_pos, field, width, size)
    elif variant == "copy":
        state = exp.write_window(state, trace_pos, outputs[0], width, size)
    elif variant == "recurrent-copy" and values.count(values[0]) >= 2:
        state = exp.write_window(state, trace_pos, values[0], width, size)
    return state


def train(exp, sequence, pos, initial, size, width, core_width, event_budget, policy, variant):
    state = initial
    for value in sequence:
        state = exp.write_window(state, pos, value, core_width, size)
        for _ in range(event_budget):
            state = step_variant(exp, state, size, width, policy, variant)
    return state


def sweep(exp, variant, width, backgrounds, args):
    size = width * args.window_capacity
    counts = Counter()
    for seed in range(backgrounds):
        initial = random.Random(seed).getrandbits(size)
        for policy in ("min", "max"):
            for pos in range(0, size, width):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    sa = train(exp, (a,) * args.repeats, pos, initial, size, width, args.core_width, args.event_budget, policy, variant)
                    sb = train(exp, (b,) * args.repeats, pos, initial, size, width, args.core_width, args.event_budget, policy, variant)
                    aa = query(exp, sa, a, pos, size, width, args.core_width)
                    ba = query(exp, sb, a, pos, size, width, args.core_width)
                    ab = query(exp, sa, b, pos, size, width, args.core_width)
                    bb = query(exp, sb, b, pos, size, width, args.core_width)
                    if aa and ba and aa[:2] == ba[:2]:
                        if aa[2] < ba[2]: counts["match"] += 1
                        elif aa[2] > ba[2]: counts["mismatch"] += 1
                    if ab and bb and ab[:2] == bb[:2]:
                        if bb[2] < ab[2]: counts["match"] += 1
                        elif bb[2] > ab[2]: counts["mismatch"] += 1
                    if aa and ba and ab and bb and aa[:2] == ba[:2] and ab[:2] == bb[:2]:
                        if aa[2] < ba[2] and bb[2] < ab[2]: counts["strict"] += 1
    print(f"variant={variant} width={width} backgrounds={backgrounds} match={counts['match']} mismatch={counts['mismatch']} strict={counts['strict']}")


def main():
    exp = load_exp057()
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=3)
    parser.add_argument("--backgrounds", type=int, default=16)
    parser.add_argument("--window-capacity", type=int, default=6)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--event-budget", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    for variant in ("field", "copy", "recurrent-copy"):
        sweep(exp, variant, args.width, args.backgrounds, args)


if __name__ == "__main__":
    main()
