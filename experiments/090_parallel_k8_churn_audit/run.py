#!/usr/bin/env python3
import random
import statistics
from collections import Counter


def bit(state, index, size):
    return (state >> (index % size)) & 1


def read_window(state, pos, width, size):
    value = 0
    for j in range(width):
        value = (value << 1) | bit(state, pos + j, size)
    return value


def rotl(value, width):
    mask = (1 << width) - 1
    return ((value << 1) & mask) | (value >> (width - 1))


def candidate(state, start, size, width, max_arity=None):
    capacity = size // width
    if max_arity is not None:
        capacity = min(capacity, max_arity)
    values = []
    positions = []
    xor_value = 0
    mask = (1 << width) - 1
    for offset in range(capacity):
        pos = (start + offset * width) % size
        value = read_window(state, pos, width, size)
        positions.append(pos)
        values.append(value)
        xor_value ^= value
        if len(values) < 2 or xor_value != 0:
            continue
        field = rotl(sum(values) & mask, width)
        outputs = tuple((value + field) & mask for value in values)
        if outputs == tuple(values):
            continue
        return tuple(positions), tuple(values), outputs, field
    return None


def event_support(event, width, size):
    support = set()
    for pos in event[0]:
        for j in range(width):
            support.add((pos + j) % size)
    return support


def event_delta(state, event, width, size):
    delta = 0
    positions, _, outputs, _ = event
    for pos, output in zip(positions, outputs):
        for j in range(width):
            index = (pos + j) % size
            target = (output >> (width - 1 - j)) & 1
            if bit(state, index, size) != target:
                delta ^= 1 << index
    return delta


def events_at(state, size, width, max_arity=None):
    out = []
    for start in range(size):
        event = candidate(state, start, size, width, max_arity)
        if event is not None:
            out.append((start, event, event_support(event, width, size), event_delta(state, event, width, size)))
    return out


def parallel_step(state, size, width, max_arity=None, mode="xor"):
    events = events_at(state, size, width, max_arity)
    delta = 0
    if mode == "xor":
        for _, _, _, d in events:
            delta ^= d
    elif mode == "exclusive_events":
        for i, (_, _, support, d) in enumerate(events):
            if all(not (support & other[2]) for j, other in enumerate(events) if i != j):
                delta ^= d
    elif mode == "unique_support_bits":
        touches = Counter()
        for _, _, support, _ in events:
            for index in support:
                touches[index] += 1
        for _, _, support, d in events:
            for index in support:
                if touches[index] == 1 and ((d >> index) & 1):
                    delta ^= 1 << index
    elif mode == "unique_delta" or mode.startswith("maxcount:"):
        requests = Counter()
        for _, _, _, d in events:
            for index in range(size):
                if (d >> index) & 1:
                    requests[index] += 1
        limit = 1 if mode == "unique_delta" else int(mode.split(":")[1])
        for index, count in requests.items():
            if 0 < count <= limit:
                delta ^= 1 << index
    else:
        raise ValueError(mode)
    return state ^ delta, events


def circular_distance(a, b, size):
    d = abs(a - b) % size
    return min(d, size - d)


def audit(width, max_arity=None, mode="xor", seeds=16, sweeps=100, capacity=12):
    size = width * capacity
    rows = []
    propagation = []
    active_final = 0
    arities = Counter()

    for seed in range(seeds):
        state = random.Random(seed).getrandbits(size)
        previous_roles = None
        last_events = []
        for _ in range(sweeps):
            new_state, events = parallel_step(state, size, width, max_arity, mode)
            supports = [entry[2] for entry in events]
            roles = set()
            for _, event, _, _ in events:
                positions, values, _, field = event
                roles.add((values[0], field, len(positions)))
                arities[len(positions)] += 1

            pairs = len(supports) * (len(supports) - 1) // 2
            overlap = 0.0
            if pairs:
                overlaps = 0
                for i in range(len(supports)):
                    for j in range(i + 1, len(supports)):
                        overlaps += bool(supports[i] & supports[j])
                overlap = overlaps / pairs

            jaccard = None
            if previous_roles is not None:
                union = roles | previous_roles
                jaccard = len(roles & previous_roles) / len(union) if union else 1.0

            rows.append((len(events), overlap, (state ^ new_state).bit_count(), len(roles), jaccard))
            previous_roles = roles
            state = new_state
            last_events = events

        active_final += int(bool(last_events))

        base = random.Random(100000 + seed).getrandbits(size)
        pos = random.Random(200000 + seed).randrange(size)
        out0, _ = parallel_step(base, size, width, max_arity, mode)
        out1, _ = parallel_step(base ^ (1 << pos), size, width, max_arity, mode)
        diff = out0 ^ out1
        changed = [index for index in range(size) if (diff >> index) & 1]
        propagation.append((len(changed), max((circular_distance(pos, index, size) for index in changed), default=0)))

    jaccards = [row[4] for row in rows if row[4] is not None]
    total_arity = sum(arities.values())
    return {
        "width": width,
        "size": size,
        "events": statistics.mean(row[0] for row in rows),
        "overlap": statistics.mean(row[1] for row in rows),
        "hamming": statistics.mean(row[2] for row in rows),
        "roles": statistics.mean(row[3] for row in rows),
        "jaccard": statistics.mean(jaccards),
        "prop_bits": statistics.mean(item[0] for item in propagation),
        "prop_dist": statistics.mean(item[1] for item in propagation),
        "active_final": active_final,
        "arity_ge6": (sum(count for arity, count in arities.items() if arity >= 6) / total_arity) if total_arity else 0.0,
    }


def show(prefix, result):
    fields = " ".join(f"{key}={value:.6f}" if isinstance(value, float) else f"{key}={value}" for key, value in result.items())
    print(prefix, fields)


def main():
    for width in (3, 4, 5):
        show("full", audit(width))

    for max_arity in (2, 3, 4, 6, 8, 12):
        show(f"cap max_arity={max_arity}", audit(4, max_arity=max_arity))

    for mode in ("xor", "exclusive_events", "unique_support_bits", "unique_delta", "maxcount:2", "maxcount:3", "maxcount:4"):
        show(f"resolution mode={mode}", audit(4, mode=mode))


if __name__ == "__main__":
    main()
