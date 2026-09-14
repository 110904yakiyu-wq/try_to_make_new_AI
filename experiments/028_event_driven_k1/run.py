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


class EventDrivenCA:
    def __init__(self, rule, size):
        self.rule = rule
        self.size = size
        self.state = 1 << (size // 2)
        self.queue = deque()
        self.pending = set()
        self.successful_updates = 0
        self.processed_slots = 0

        # Initial physical state may contain enabled sites anywhere.
        for index in range(size):
            self.enqueue(index)

    def enqueue(self, index):
        index %= self.size
        if index not in self.pending:
            self.pending.add(index)
            self.queue.append(index)

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
        before = self.successful_updates

        # A budget slot is consumed even when the queue is empty. This keeps
        # the external physical work budget equal across compared histories.
        for _ in range(budget):
            self.processed_slots += 1
            if not self.queue:
                continue

            index = self.queue.popleft()
            self.pending.remove(index)
            target = local_target(self.state, self.rule, index, self.size)

            if target != bit(self.state, index, self.size):
                self.state = set_bit(self.state, index, target, self.size)
                self.successful_updates += 1

                # Only the changed site and its local causal neighbors can
                # have their enabledness changed by this event.
                for candidate in (index - 1, index, index + 1):
                    self.enqueue(candidate)

        return self.successful_updates - before


def recurrent_repertoires(machine, args):
    patch_times = Counter()
    enabled_patch_times = Counter()

    for block in range(args.post_blocks + 1):
        patches = {
            patch_value(
                machine.state, pos,
                args.core_width, args.radius, args.size,
            )
            for pos in range(args.size)
        }
        enabled_patches = {
            patch_value(
                machine.state, pos,
                args.core_width, args.radius, args.size,
            )
            for pos in range(args.size)
            if enabled(machine.state, machine.rule, pos, args.size)
        }

        for patch in patches:
            patch_times[patch] += 1
        for patch in enabled_patches:
            enabled_patch_times[patch] += 1

        if block < args.post_blocks:
            machine.run_budget(args.post_block_budget)

    contexts = {
        patch for patch, count in patch_times.items()
        if count >= args.min_snapshots
    }
    enabled_contexts = {
        patch for patch, count in enabled_patch_times.items()
        if count >= args.min_snapshots
    }
    return contexts, enabled_contexts


def run_sequence(rule, sequence, args):
    machine = EventDrivenCA(rule, args.size)

    for value in sequence:
        machine.external_inject(value, args.train_pos, args.core_width)
        machine.run_budget(args.event_budget)

    contexts, enabled_contexts = recurrent_repertoires(machine, args)
    return (
        contexts,
        enabled_contexts,
        machine.successful_updates,
        machine.processed_slots,
    )


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
        description="Experiment 028: minimal event-driven asynchronous K1 substrate."
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

    context_relations = Counter()
    enabled_relations = Counter()
    update_count_changed = 0
    absolute_update_difference = 0
    updates_seq1 = 0
    updates_seq2 = 0

    for rule in range(256):
        for a in range(1 << (args.core_width - 1)):
            b = a ^ ((1 << args.core_width) - 1)
            seq1 = (a, a, a, b, b)
            seq2 = (b, b, a, a, a)

            contexts1, enabled1, update1, slots1 = run_sequence(
                rule, seq1, args
            )
            contexts2, enabled2, update2, slots2 = run_sequence(
                rule, seq2, args
            )

            if slots1 != slots2:
                raise RuntimeError("physical work-slot budgets diverged")

            context_relations[relation(contexts1, contexts2)] += 1
            enabled_relations[relation(enabled1, enabled2)] += 1
            update_count_changed += int(update1 != update2)
            absolute_update_difference += abs(update2 - update1)
            updates_seq1 += update1
            updates_seq2 += update2

    total = sum(context_relations.values())
    context_changed = total - context_relations["same"]
    enabled_changed = total - enabled_relations["same"]

    print(f"cases={total}")
    print(f"context_same={context_relations['same']}")
    print(f"context_reorganize={context_relations['reorganize']}")
    print(f"context_seq1_superset={context_relations['seq1_superset']}")
    print(f"context_seq2_superset={context_relations['seq2_superset']}")
    print(f"context_changed={context_changed}")
    print(f"context_changed_fraction={context_changed / total:.9f}")
    print()
    print(f"enabled_same={enabled_relations['same']}")
    print(f"enabled_reorganize={enabled_relations['reorganize']}")
    print(f"enabled_seq1_superset={enabled_relations['seq1_superset']}")
    print(f"enabled_seq2_superset={enabled_relations['seq2_superset']}")
    print(f"enabled_changed={enabled_changed}")
    print(f"enabled_changed_fraction={enabled_changed / total:.9f}")
    print()
    print(f"update_count_changed={update_count_changed}")
    print(f"update_count_changed_fraction={update_count_changed / total:.9f}")
    print(f"mean_abs_update_difference={absolute_update_difference / total:.9f}")
    print(f"mean_updates_seq1={updates_seq1 / total:.9f}")
    print(f"mean_updates_seq2={updates_seq2 / total:.9f}")


if __name__ == "__main__":
    main()
