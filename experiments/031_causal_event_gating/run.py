#!/usr/bin/env python3
import argparse


def bit(state, index, size):
    return (state >> (index % size)) & 1


def synchronous_step(state, rule, size):
    mask = (1 << size) - 1
    left = ((state << 1) & mask) | (state >> (size - 1))
    right = (state >> 1) | ((state & 1) << (size - 1))
    center = state
    nl = (~left) & mask
    nc = (~center) & mask
    nr = (~right) & mask
    out = 0
    for code in range(8):
        if not ((rule >> code) & 1):
            continue
        l = (code >> 2) & 1
        c = (code >> 1) & 1
        r = code & 1
        out |= (
            (left if l else nl)
            & (center if c else nc)
            & (right if r else nr)
        )
    return out


def enabled_mask(state, rule, size):
    return state ^ synchronous_step(state, rule, size)


def choose_event(mask, policy):
    if not mask:
        return None
    if policy == "min":
        low = mask & -mask
        return low.bit_length() - 1
    if policy == "max":
        return mask.bit_length() - 1
    raise ValueError(f"unknown policy: {policy}")


def run_budget(state, rule, size, budget, policy, trace=False):
    events = []
    for _ in range(budget):
        enabled = enabled_mask(state, rule, size)
        index = choose_event(enabled, policy)
        if index is None:
            if trace:
                events.append(-1)
            continue
        state ^= 1 << index
        if trace:
            events.append(index)
    return (state, events) if trace else state


def inject(state, pos, value, width, size):
    for j in range(width):
        index = (pos + j) % size
        target = (value >> (width - 1 - j)) & 1
        if bit(state, index, size) != target:
            state ^= 1 << index
    return state


def train(rule, sequence, pos, args, policy):
    state = 1 << (args.size // 2)
    for value in sequence:
        state = inject(state, pos, value, args.core_width, args.size)
        state = run_budget(
            state, rule, args.size, args.event_budget, policy
        )
    return state


def transplant(dst, src, pos, args):
    start = pos - args.radius
    width = args.core_width + 2 * args.radius
    for j in range(width):
        index = (start + j) % args.size
        src_bit = bit(src, index, args.size)
        if bit(dst, index, args.size) != src_bit:
            dst ^= 1 << index
    return dst


def trace_distance(left, right):
    return sum(a != b for a, b in zip(left, right))


def parse_positions(text):
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 031: causal transfer of event gating by a local history-generated context."
    )
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--event-budget", type=int, default=128)
    parser.add_argument("--cascade-budget", type=int, default=32)
    parser.add_argument("--positions", default="0,8,16,24,32,40,48,56")
    parser.add_argument("--control-offset", type=int, default=32)
    args = parser.parse_args()

    total = 0
    improved = 0
    exact = 0
    control_improved = 0

    print("policy pos eligible improved exact control_improved")

    for policy in ("min", "max"):
        for pos in parse_positions(args.positions):
            local_total = 0
            local_improved = 0
            local_exact = 0
            local_control = 0

            for rule in range(256):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    seq1 = (a, a, a, b, b)
                    seq2 = (b, b, a, a, a)

                    state1 = train(rule, seq1, pos, args, policy)
                    state2 = train(rule, seq2, pos, args, policy)

                    _, trace1 = run_budget(
                        state1, rule, args.size,
                        args.cascade_budget, policy, trace=True,
                    )
                    _, trace2 = run_budget(
                        state2, rule, args.size,
                        args.cascade_budget, policy, trace=True,
                    )

                    if trace1 == trace2:
                        continue

                    local_total += 1
                    baseline_distance = trace_distance(trace2, trace1)

                    transplanted = transplant(state2, state1, pos, args)
                    _, transferred_trace = run_budget(
                        transplanted, rule, args.size,
                        args.cascade_budget, policy, trace=True,
                    )
                    transferred_distance = trace_distance(
                        transferred_trace, trace1
                    )

                    control_pos = (pos + args.control_offset) % args.size
                    control_state = transplant(
                        state2, state1, control_pos, args
                    )
                    _, control_trace = run_budget(
                        control_state, rule, args.size,
                        args.cascade_budget, policy, trace=True,
                    )
                    control_distance = trace_distance(control_trace, trace1)

                    local_improved += int(
                        transferred_distance < baseline_distance
                    )
                    local_exact += int(transferred_trace == trace1)
                    local_control += int(
                        control_distance < baseline_distance
                    )

            print(
                f"{policy:>6} {pos:>3} {local_total:>8} "
                f"{local_improved:>8} {local_exact:>5} "
                f"{local_control:>16}"
            )

            total += local_total
            improved += local_improved
            exact += local_exact
            control_improved += local_control

    print()
    print(f"eligible_total={total}")
    print(f"local_patch_improved={improved}")
    print(f"local_patch_improved_fraction={improved / total:.9f}")
    print(f"local_patch_exact_transfer={exact}")
    print(f"local_patch_exact_transfer_fraction={exact / total:.9f}")
    print(f"antipodal_control_improved={control_improved}")
    print(f"antipodal_control_improved_fraction={control_improved / total:.9f}")


if __name__ == "__main__":
    main()
