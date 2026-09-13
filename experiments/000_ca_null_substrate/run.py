#!/usr/bin/env python3
import argparse
from collections import OrderedDict

RULE = 110


def rule_bit(left: int, center: int, right: int, rule: int = RULE) -> int:
    idx = (left << 2) | (center << 1) | right
    return (rule >> idx) & 1


def step_ring(state, rule: int = RULE):
    n = len(state)
    return [
        rule_bit(state[(i - 1) % n], state[i], state[(i + 1) % n], rule)
        for i in range(n)
    ]


def run_history(initial, steps: int, rule: int = RULE):
    history = [initial[:]]
    state = initial[:]
    for _ in range(steps):
        state = step_ring(state, rule)
        history.append(state)
    return history


def bits_to_int(bits) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def int_to_bits(value: int, width: int):
    return [(value >> (width - 1 - i)) & 1 for i in range(width)]


def circular_slice(row, start: int, length: int):
    n = len(row)
    return [row[(start + j) % n] for j in range(length)]


def collect_contexts(history, upto_t: int, core_width: int, radius: int, context_limit: int):
    """Collect left/right flanks in first-appearance order."""
    seen = OrderedDict()
    n = len(history[0])

    for t, row in enumerate(history[: upto_t + 1]):
        for i in range(n):
            left = circular_slice(row, i - radius, radius)
            core = circular_slice(row, i, core_width)
            right = circular_slice(row, i + core_width, radius)
            key = (bits_to_int(left), bits_to_int(right))
            if key not in seen:
                seen[key] = {
                    "first_t": t,
                    "first_i": i,
                    "observed_core": bits_to_int(core),
                }
                if len(seen) >= context_limit:
                    return list(seen.keys()), seen

    return list(seen.keys()), seen


def evolve_open(state, steps: int, rule: int = RULE):
    """Finite local assay field with zero outside its boundaries."""
    state = state[:]
    for _ in range(steps):
        nxt = []
        n = len(state)
        for i in range(n):
            left = state[i - 1] if i > 0 else 0
            center = state[i]
            right = state[i + 1] if i + 1 < n else 0
            nxt.append(rule_bit(left, center, right, rule))
        state = nxt
    return state


def assay_outcome(core_value: int, context, core_width: int, radius: int, horizon: int):
    left_value, right_value = context

    left = int_to_bits(left_value, radius)
    core = int_to_bits(core_value, core_width)
    right = int_to_bits(right_value, radius)

    # Keep the outer assay boundary outside the center's light cone.
    pad = horizon + 2
    field = [0] * pad + left + core + right + [0] * pad
    center_index = pad + radius + core_width // 2

    field = evolve_open(field, horizon)
    return field[center_index]


def signature(core_value: int, contexts, core_width: int, radius: int, horizon: int):
    return tuple(
        assay_outcome(core_value, ctx, core_width, radius, horizon)
        for ctx in contexts
    )


def partition_cores(cores, contexts, core_width: int, radius: int, horizon: int):
    by_signature = OrderedDict()
    for core in cores:
        sig = signature(core, contexts, core_width, radius, horizon)
        by_signature.setdefault(sig, []).append(core)
    return list(by_signature.values())


def pair_relation(partition):
    relation = set()
    for group in partition:
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                relation.add((min(a, b), max(a, b)))
    return relation


def format_core(value: int, width: int) -> str:
    return format(value, f"0{width}b")


def format_partition(partition, width: int) -> str:
    groups = []
    for group in partition:
        groups.append("{" + ",".join(format_core(x, width) for x in group) + "}")
    return " ".join(groups)


def make_initial(size: int, mode: str):
    state = [0] * size
    if mode == "single":
        state[size // 2] = 1
    elif mode == "alternating":
        for i in range(size):
            state[i] = i & 1
    else:
        raise ValueError(f"unsupported seed mode: {mode}")
    return state


def parse_checkpoints(text: str, max_step: int):
    values = sorted({int(x.strip()) for x in text.split(",") if x.strip()})
    if not values:
        raise ValueError("at least one checkpoint is required")
    if values[0] < 0 or values[-1] > max_step:
        raise ValueError("checkpoints must be within [0, steps]")
    return values


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 000: bounded operational-equivalence assay on Rule 110."
    )
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--steps", type=int, default=16)
    parser.add_argument("--checkpoints", default="0,1,2,4,8,16")
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--radius", type=int, default=8)
    parser.add_argument("--horizon", type=int, default=3)
    parser.add_argument("--context-limit", type=int, default=64)
    parser.add_argument("--seed-mode", choices=["single", "alternating"], default="single")
    args = parser.parse_args()

    if args.size < 2 * args.radius + args.core_width + 1:
        raise SystemExit("size is too small for the requested assay geometry")
    if args.horizon > args.radius:
        raise SystemExit("horizon must be <= radius so external assay boundaries stay irrelevant")

    checkpoints = parse_checkpoints(args.checkpoints, args.steps)
    initial = make_initial(args.size, args.seed_mode)
    history = run_history(initial, args.steps)

    cores = list(range(1 << args.core_width))
    previous_relation = None

    print("checkpoint  contexts  classes  newly_split_pairs  partition")

    for t in checkpoints:
        contexts, _ = collect_contexts(
            history,
            upto_t=t,
            core_width=args.core_width,
            radius=args.radius,
            context_limit=args.context_limit,
        )
        partition = partition_cores(
            cores,
            contexts,
            core_width=args.core_width,
            radius=args.radius,
            horizon=args.horizon,
        )
        relation = pair_relation(partition)

        if previous_relation is None:
            newly_split = []
        else:
            newly_split = sorted(previous_relation - relation)

        split_text = "-"
        if newly_split:
            split_text = ",".join(
                f"{format_core(a, args.core_width)}!={format_core(b, args.core_width)}"
                for a, b in newly_split
            )

        print(
            f"{t:>10}  {len(contexts):>8}  {len(partition):>7}  "
            f"{split_text:<28}  {format_partition(partition, args.core_width)}"
        )

        previous_relation = relation


if __name__ == "__main__":
    main()
