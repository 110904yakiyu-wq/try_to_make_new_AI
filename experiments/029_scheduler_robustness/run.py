#!/usr/bin/env python3
import argparse
import heapq
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


def enabled(state, rule, index, size):
    return local_target(state, rule, index, size) != bit(state, index, size)


def set_bit(state, index, value, size):
    index %= size
    if value:
        return state | (1 << index)
    return state & ~(1 << index)


def inject(state, pos, value, width, size):
    changed = []
    for j in range(width):
        index = (pos + j) % size
        value_bit = (value >> (width - 1 - j)) & 1
        if bit(state, index, size) != value_bit:
            state = set_bit(state, index, value_bit, size)
            changed.append(index)
    return state, changed


def patch_value(state, pos, width, radius, size):
    value = 0
    for j in range(width + 2 * radius):
        index = (pos - radius + j) % size
        value = (value << 1) | bit(state, index, size)
    return value


class Machine:
    def __init__(self, rule, mode, size):
        self.rule = rule
        self.mode = mode
        self.size = size
        self.state = 1 << (size // 2)
        self.pending = set()
        self.updates = 0

        if mode == "fifo":
            self.queue = deque()
        elif mode in ("lifo", "min"):
            self.queue = []
        else:
            raise ValueError(mode)

        for index in range(size):
            self.enqueue(index)

    def enqueue(self, index):
        index %= self.size
        if index in self.pending:
            return
        self.pending.add(index)
        if self.mode == "min":
            heapq.heappush(self.queue, index)
        else:
            self.queue.append(index)

    def pop(self):
        if not self.queue:
            return None
        if self.mode == "fifo":
            index = self.queue.popleft()
        elif self.mode == "lifo":
            index = self.queue.pop()
        else:
            index = heapq.heappop(self.queue)
        self.pending.remove(index)
        return index

    def disturb(self, indices):
        for index in indices:
            for candidate in (index - 1, index, index + 1):
                self.enqueue(candidate)

    def external_inject(self, value, pos, width):
        self.state, changed = inject(
            self.state, pos, value, width, self.size
        )
        self.disturb(changed)

    def run_budget(self, budget):
        for _ in range(budget):
            index = self.pop()
            if index is None:
                continue
            target = local_target(self.state, self.rule, index, self.size)
            if target != bit(self.state, index, self.size):
                self.state = set_bit(self.state, index, target, self.size)
                self.updates += 1
                for candidate in (index - 1, index, index + 1):
                    self.enqueue(candidate)


def run_sequence(rule, sequence, mode, args):
    machine = Machine(rule, mode, args.size)

    for value in sequence:
        machine.external_inject(value, args.train_pos, args.core_width)
        machine.run_budget(args.event_budget)

    recurrent_enabled = Counter()
    for block in range(args.post_blocks + 1):
        current = {
            patch_value(
                machine.state, pos,
                args.core_width, args.radius, args.size,
            )
            for pos in range(args.size)
            if enabled(machine.state, rule, pos, args.size)
        }
        for patch in current:
            recurrent_enabled[patch] += 1
        if block < args.post_blocks:
            machine.run_budget(args.post_block_budget)

    repertoire = {
        patch for patch, count in recurrent_enabled.items()
        if count >= args.min_snapshots
    }
    return repertoire, machine.updates


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
        description="Experiment 029: scheduler robustness of K1 enabled-event repertoire."
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

    modes = ("fifo", "lifo", "min")
    relations = {mode: Counter() for mode in modes}
    changed_cases = {mode: set() for mode in modes}
    update_count_changed = Counter()

    for rule in range(256):
        for a in range(1 << (args.core_width - 1)):
            b = a ^ ((1 << args.core_width) - 1)
            seq1 = (a, a, a, b, b)
            seq2 = (b, b, a, a, a)
            case = (rule, a)

            for mode in modes:
                rep1, updates1 = run_sequence(rule, seq1, mode, args)
                rep2, updates2 = run_sequence(rule, seq2, mode, args)
                kind = relation(rep1, rep2)
                relations[mode][kind] += 1
                if kind != "same":
                    changed_cases[mode].add(case)
                update_count_changed[mode] += int(updates1 != updates2)

    for mode in modes:
        counts = relations[mode]
        changed = len(changed_cases[mode])
        print(
            f"{mode}: same={counts['same']} reorganize={counts['reorganize']} "
            f"seq1_superset={counts['seq1_superset']} "
            f"seq2_superset={counts['seq2_superset']} changed={changed} "
            f"update_count_changed={update_count_changed[mode]}"
        )

    all_changed = set.intersection(*(changed_cases[mode] for mode in modes))
    any_changed = set.union(*(changed_cases[mode] for mode in modes))
    print()
    print(f"changed_all_three={len(all_changed)}")
    print(f"changed_any_scheduler={len(any_changed)}")

    for i, left in enumerate(modes):
        for right in modes[i + 1:]:
            intersection = changed_cases[left] & changed_cases[right]
            union = changed_cases[left] | changed_cases[right]
            print(
                f"overlap_{left}_{right}={len(intersection)} "
                f"jaccard={len(intersection) / len(union):.9f}"
            )


if __name__ == "__main__":
    main()
