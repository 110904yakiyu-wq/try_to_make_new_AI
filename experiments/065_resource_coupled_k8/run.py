#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter, defaultdict
from pathlib import Path


def load_exp057():
    path = Path(__file__).resolve().parents[1] / "057_self_delimiting_k8" / "run.py"
    spec = importlib.util.spec_from_file_location("exp057", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def candidate_budgeted(exp, state, start, size, width, max_reads):
    capacity = size // width
    values = []
    positions = []
    xor_value = 0
    mask = (1 << width) - 1
    reads = 0
    for offset in range(capacity):
        if reads >= max_reads:
            return None, reads
        pos = (start + offset * width) % size
        value = exp.read_window(state, pos, width, size)
        reads += 1
        positions.append(pos)
        values.append(value)
        xor_value ^= value
        if len(values) < 2 or xor_value != 0:
            continue
        field = exp.rotl(sum(values) & mask, width)
        outputs = tuple((value + field) & mask for value in values)
        if outputs == tuple(values):
            continue
        return (tuple(positions), tuple(values), outputs, field), reads
    return None, reads


def find_event(exp, state, size, width, policy, remaining):
    starts = range(size) if policy == "min" else range(size - 1, -1, -1)
    used = 0
    for start in starts:
        if used >= remaining:
            break
        event, cost = candidate_budgeted(exp, state, start, size, width, remaining - used)
        used += cost
        if event is not None:
            return event, used
    return None, used


def run_work(exp, state, work_budget, size, width, policy):
    remaining = work_budget
    events = 0
    while remaining > 0:
        event, reads = find_event(exp, state, size, width, policy, remaining)
        remaining -= reads
        if event is None:
            break
        positions, values, outputs, field = event
        write_cost = len(outputs)
        if write_cost > remaining:
            break
        for pos, value in zip(positions, outputs):
            state = exp.write_window(state, pos, value, width, size)
        remaining -= write_cost
        events += 1
    return state, events


def train(exp, value, repeats, pos, initial, size, width, core_width, work_budget, policy):
    state = initial
    event_count = 0
    for _ in range(repeats):
        state = exp.write_window(state, pos, value, core_width, size)
        state, n = run_work(exp, state, work_budget, size, width, policy)
        event_count += n
    return state, event_count


def query(exp, state, probe, pos, size, width, core_width):
    state = exp.write_window(state, pos, probe, core_width, size)
    event = exp.candidate(state, pos, size, width)
    if event is None:
        return None
    return event[2][0], event[4], len(event[1])


def sweep(exp, args, budget):
    width = args.key_width
    size = width * args.window_capacity
    counts = Counter()
    by_pair = defaultdict(Counter)
    for seed in range(args.backgrounds):
        initial = random.Random(seed).getrandbits(size)
        for policy in ("min", "max"):
            for pos in range(0, size, width):
                for a in range(1 << (args.core_width - 1)):
                    b = a ^ ((1 << args.core_width) - 1)
                    sa, _ = train(exp, a, args.repeats, pos, initial, size, width, args.core_width, budget, policy)
                    sb, _ = train(exp, b, args.repeats, pos, initial, size, width, args.core_width, budget, policy)
                    aa = query(exp, sa, a, pos, size, width, args.core_width)
                    ba = query(exp, sb, a, pos, size, width, args.core_width)
                    ab = query(exp, sa, b, pos, size, width, args.core_width)
                    bb = query(exp, sb, b, pos, size, width, args.core_width)
                    if aa and ba and aa[:2] == ba[:2]:
                        if aa[2] < ba[2]: counts["match"] += 1; by_pair[a]["match"] += 1
                        elif aa[2] > ba[2]: counts["mismatch"] += 1; by_pair[a]["mismatch"] += 1
                    if ab and bb and ab[:2] == bb[:2]:
                        if bb[2] < ab[2]: counts["match"] += 1; by_pair[a]["match"] += 1
                        elif bb[2] > ab[2]: counts["mismatch"] += 1; by_pair[a]["mismatch"] += 1
                    if aa and ba and ab and bb and aa[:2] == ba[:2] and ab[:2] == bb[:2]:
                        if aa[2] < ba[2] and bb[2] < ab[2]: counts["strict"] += 1
    print(f"work_budget={budget} match={counts['match']} mismatch={counts['mismatch']} strict={counts['strict']}")
    for a in sorted(by_pair):
        print(f"pair_a={a:03b} match={by_pair[a]['match']} mismatch={by_pair[a]['mismatch']}")


def main():
    exp = load_exp057()
    p = argparse.ArgumentParser()
    p.add_argument("--key-width", type=int, default=3)
    p.add_argument("--window-capacity", type=int, default=6)
    p.add_argument("--core-width", type=int, default=3)
    p.add_argument("--repeats", type=int, default=5)
    p.add_argument("--backgrounds", type=int, default=16)
    p.add_argument("--work-budgets", default="24,48,96")
    args = p.parse_args()
    for budget in [int(x) for x in args.work_budgets.split(",") if x.strip()]:
        sweep(exp, args, budget)


if __name__ == "__main__":
    main()
