#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_exp020():
    path = Path(__file__).resolve().parents[1] / "020_autonomous_quotient_divergence" / "run.py"
    spec = importlib.util.spec_from_file_location("exp020", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def train_states(exp, rule, pattern, schedule, args):
    initial = 1 << (args.size // 2)
    states = []
    for pos in range(0, args.size, args.position_stride):
        states.append(
            exp.train(
                initial, pattern, schedule, args.training_time,
                pos, args.core_width, rule, args.size,
            )
        )
    return states


def quotient_from_states(exp, rule, states, delay, args):
    signatures = [[] for _ in range(1 << args.core_width)]
    positions = range(0, args.size, args.position_stride)

    for pos, state in zip(positions, states):
        state = exp.evolve(state, rule, args.size, delay)
        q = (pos + args.assay_offset) % args.size
        for probe in range(1 << args.core_width):
            signatures[probe].append(
                exp.effect(
                    state, probe, q, args.core_width,
                    args.probe_steps, rule, args.size,
                )
            )

    signatures = [tuple(values) for values in signatures]
    groups = []
    used = set()
    for i, signature in enumerate(signatures):
        if i in used:
            continue
        group = [i]
        used.add(i)
        for j in range(i + 1, len(signatures)):
            if j not in used and signatures[j] == signature:
                group.append(j)
                used.add(j)
        groups.append(tuple(group))
    return tuple(groups)


def interval_indices(q, radius, width, size):
    return {(q - radius + j) % size for j in range(width + 2 * radius)}


def copy_indices(recipient, donor, indices):
    out = recipient
    for index in indices:
        bit = (donor >> index) & 1
        if bit:
            out |= 1 << index
        else:
            out &= ~(1 << index)
    return out


def transplant(states, donor_states, delay, mode, args):
    out = []
    for pos, recipient, donor in zip(
        range(0, args.size, args.position_stride), states, donor_states
    ):
        q = (pos + args.assay_offset) % args.size
        center = interval_indices(
            q, args.probe_steps, args.core_width, args.size
        )
        expanded = interval_indices(
            q, args.probe_steps + delay, args.core_width, args.size
        )
        annulus = expanded - center

        if mode == "center":
            indices = center
        elif mode == "annulus":
            indices = annulus
        elif mode == "expanded":
            indices = expanded
        elif mode == "distant_annulus":
            indices = {(i + args.size // 2) % args.size for i in annulus}
        else:
            raise ValueError(mode)

        out.append(copy_indices(recipient, donor, indices))
    return out


def main():
    exp = load_exp020()
    parser = argparse.ArgumentParser(
        description="Experiment 025: determine whether autonomous quotient divergence comes from hidden local state or incoming outer context."
    )
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--position-stride", type=int, default=8)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--single-schedule", default="0")
    parser.add_argument("--repeat-schedule", default="0,4,8,12,16")
    parser.add_argument("--training-time", type=int, default=48)
    parser.add_argument("--assay-offset", type=int, default=20)
    parser.add_argument("--probe-steps", type=int, default=8)
    parser.add_argument("--max-depth", type=int, default=8)
    args = parser.parse_args()

    single = exp.parse_schedule(args.single_schedule)
    repeat = exp.parse_schedule(args.repeat_schedule)

    cases = []
    for rule in range(256):
        for pattern in range(1 << args.core_width):
            single_states = train_states(exp, rule, pattern, single, args)
            repeat_states = train_states(exp, rule, pattern, repeat, args)

            q0_single = quotient_from_states(exp, rule, single_states, 0, args)
            q0_repeat = quotient_from_states(exp, rule, repeat_states, 0, args)
            if q0_single != q0_repeat:
                continue

            for depth in range(1, args.max_depth + 1):
                q_single = quotient_from_states(exp, rule, single_states, depth, args)
                q_repeat = quotient_from_states(exp, rule, repeat_states, depth, args)
                if q_single != q_repeat:
                    cases.append((
                        rule, pattern, depth,
                        single_states, repeat_states,
                        q_single, q_repeat,
                    ))
                    break

    modes = ("center", "annulus", "expanded", "distant_annulus")
    results = {
        mode: {"repeat_to_single": 0, "single_to_repeat": 0, "bidirectional": 0}
        for mode in modes
    }

    for rule, pattern, depth, single_states, repeat_states, q_single, q_repeat in cases:
        for mode in modes:
            repeat_into_single = transplant(
                single_states, repeat_states, depth, mode, args
            )
            single_into_repeat = transplant(
                repeat_states, single_states, depth, mode, args
            )
            q_repeat_into_single = quotient_from_states(
                exp, rule, repeat_into_single, depth, args
            )
            q_single_into_repeat = quotient_from_states(
                exp, rule, single_into_repeat, depth, args
            )

            a = q_repeat_into_single == q_repeat
            b = q_single_into_repeat == q_single
            results[mode]["repeat_to_single"] += int(a)
            results[mode]["single_to_repeat"] += int(b)
            results[mode]["bidirectional"] += int(a and b)

    print(f"eligible_future_divergence_cases={len(cases)}")
    for mode in modes:
        r = results[mode]
        print(
            f"{mode}: repeat_to_single={r['repeat_to_single']} "
            f"single_to_repeat={r['single_to_repeat']} "
            f"bidirectional={r['bidirectional']}"
        )


if __name__ == "__main__":
    main()
