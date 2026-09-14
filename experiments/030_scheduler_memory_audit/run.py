#!/usr/bin/env python3
import argparse
from collections import Counter, deque


def bit(state, index, size):
    return (state >> (index % size)) & 1


def local_target(state, rule, index, size):
    code = (
        (bit(state, index - 1, size) << 2)
        | (bit(state, index, size) << 1)
        | bit(state, index + 1, size)
    )
    return (rule >> code) & 1


def enabled_positions(state, rule, size):
    return [
        index for index in range(size)
        if local_target(state, rule, index, size) != bit(state, index, size)
    ]


def set_bit(state, index, value, size):
    index %= size
    if value:
        return state | (1 << index)
    return state & ~(1 << index)


def inject(state, pos, value, width, size):
    for j in range(width):
        index = (pos + j) % size
        value_bit = (value >> (width - 1 - j)) & 1
        if bit(state, index, size) != value_bit:
            state = set_bit(state, index, value_bit, size)
    return state


def patch_value(state, pos, width, radius, size):
    value = 0
    for j in range(width + 2 * radius):
        index = (pos - radius + j) % size
        value = (value << 1) | bit(state, index, size)
    return value


class ResetFIFO:
    """No queue state survives across physical work blocks."""

    def __init__(self, rule, args):
        self.rule = rule
        self.args = args
        self.state = 1 << (args.size // 2)
        self.updates = 0

    def external_inject(self, value):
        self.state = inject(
            self.state, self.args.train_pos, value,
            self.args.core_width, self.args.size,
        )

    def run_budget(self, budget):
        queue = deque(enabled_positions(self.state, self.rule, self.args.size))
        pending = set(queue)

        for _ in range(budget):
            if not queue:
                continue
            index = queue.popleft()
            pending.remove(index)
            target = local_target(self.state, self.rule, index, self.args.size)
            if target != bit(self.state, index, self.args.size):
                self.state = set_bit(
                    self.state, index, target, self.args.size
                )
                self.updates += 1
                for candidate in (index - 1, index, index + 1):
                    candidate %= self.args.size
                    if candidate not in pending:
                        pending.add(candidate)
                        queue.append(candidate)


class StatelessMin:
    """Every slot derives the next event from the current ring alone."""

    def __init__(self, rule, args):
        self.rule = rule
        self.args = args
        self.state = 1 << (args.size // 2)
        self.updates = 0

    def external_inject(self, value):
        self.state = inject(
            self.state, self.args.train_pos, value,
            self.args.core_width, self.args.size,
        )

    def run_budget(self, budget):
        for _ in range(budget):
            enabled = enabled_positions(
                self.state, self.rule, self.args.size
            )
            if not enabled:
                continue
            index = enabled[0]
            target = local_target(
                self.state, self.rule, index, self.args.size
            )
            self.state = set_bit(
                self.state, index, target, self.args.size
            )
            self.updates += 1


def recurrent_enabled(machine, args):
    times = Counter()
    for block in range(args.post_blocks + 1):
        current = {
            patch_value(
                machine.state, pos,
                args.core_width, args.radius, args.size,
            )
            for pos in enabled_positions(
                machine.state, machine.rule, args.size
            )
        }
        for patch in current:
            times[patch] += 1
        if block < args.post_blocks:
            machine.run_budget(args.post_block_budget)

    return {
        patch for patch, count in times.items()
        if count >= args.min_snapshots
    }


def run_sequence(machine_type, rule, sequence, args):
    machine = machine_type(rule, args)
    for value in sequence:
        machine.external_inject(value)
        machine.run_budget(args.event_budget)
    return recurrent_enabled(machine, args), machine.updates


def relation(left, right):
    if left == right:
        return "same"
    if left < right:
        return "seq2_superset"
    if right < left:
        return "seq1_superset"
    return "reorganize"


def main():
    parser = argparse.ArgumentParser(
        description="Experiment 030: remove hidden scheduler memory from K1."
    )
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--core-width", type=int, default=3)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--train-pos", type=int, default=0)
    parser.add_argument("--event-budget", type=int, default=128)
    parser.add_argument("--post-block-budget", type=int, default=64)
    parser.add_argument("--post-blocks", type=int, default=8)
    parser.add_argument("--min-snapshots", type=int, default=2)
    args = parser.parse_args()

    schedulers = (
        ("reset_fifo", ResetFIFO),
        ("stateless_min", StatelessMin),
    )

    for name, machine_type in schedulers:
        relations = Counter()
        update_count_changed = 0

        for rule in range(256):
            for a in range(1 << (args.core_width - 1)):
                b = a ^ ((1 << args.core_width) - 1)
                seq1 = (a, a, a, b, b)
                seq2 = (b, b, a, a, a)

                rep1, updates1 = run_sequence(
                    machine_type, rule, seq1, args
                )
                rep2, updates2 = run_sequence(
                    machine_type, rule, seq2, args
                )
                relations[relation(rep1, rep2)] += 1
                update_count_changed += int(updates1 != updates2)

        total = sum(relations.values())
        changed = total - relations["same"]
        print(
            f"{name}: same={relations['same']} "
            f"reorganize={relations['reorganize']} "
            f"seq1_superset={relations['seq1_superset']} "
            f"seq2_superset={relations['seq2_superset']} "
            f"changed={changed} update_count_changed={update_count_changed}"
        )


if __name__ == "__main__":
    main()
