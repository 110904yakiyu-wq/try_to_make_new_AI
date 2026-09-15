#!/usr/bin/env python3
import random
import statistics

WIDTH = 4
WINDOWS = 12
TRAIN_TICKS = 2
MAX_PROBE_TICKS = 24


def rotl(value, width=WIDTH):
    mask = (1 << width) - 1
    return ((value << 1) & mask) | (value >> (width - 1))


def rotr(value, width=WIDTH):
    return (value >> 1) | ((value & 1) << (width - 1))


def update(values, rotation):
    x, y, z = values
    f = rotl if rotation == "left" else rotr
    return (
        x ^ f(y & z),
        y ^ f(z & x),
        z ^ f(x & y),
    )


def step(state, phase, rotation):
    old = state[:]
    new = state[:]
    used = set()
    events = []
    for start in range(phase, phase + len(state), 3):
        indices = (start % len(state), (start + 1) % len(state), (start + 2) % len(state))
        if any(i in used for i in indices):
            continue
        used.update(indices)
        values = tuple(old[i] for i in indices)
        outputs = update(values, rotation)
        if outputs == values:
            continue
        for i, out in zip(indices, outputs):
            new[i] = out
        events.append((indices, values, outputs))
    return new, events


def run_ticks(state, phase, ticks, rotation):
    for _ in range(ticks):
        state, _ = step(state, phase, rotation)
        phase = (phase + 1) % 3
    return state, phase


def train(initial, pos, a, b, rotation):
    histories = []
    for sequence in ((a, a, b, b, a), (b, b, a, a, a)):
        state = initial[:]
        phase = 0
        for value in sequence:
            state[pos] = value
            state, phase = run_ticks(state, phase, TRAIN_TICKS, rotation)
        histories.append((state, phase))
    return histories


def circular_distance(a, b, size):
    d = abs(a - b) % size
    return min(d, size - d)


def propagation_cost(state, phase, pos, rotation, target_distance=6):
    control = state[:]
    probe = state[:]
    probe[pos] ^= 1
    for age in range(1, MAX_PROBE_TICKS + 1):
        control, _ = step(control, phase, rotation)
        probe, _ = step(probe, phase, rotation)
        phase = (phase + 1) % 3
        differing = [i for i, (x, y) in enumerate(zip(control, probe)) if x != y]
        if any(circular_distance(pos, i, len(state)) >= target_distance for i in differing):
            return age
    return MAX_PROBE_TICKS + 1


def activity_support(state, phase, rotation):
    _, events = step(state, phase, rotation)
    return frozenset(i for indices, _, _ in events for i in indices)


def main():
    total = different = seq1_faster = seq2_faster = 0
    support_match = support_match_different = 0
    local_match = local_match_different = 0
    both_match = both_match_different = 0

    for seed in range(64):
        initial = [random.Random(seed * 1000 + i).randrange(1 << WIDTH) for i in range(WINDOWS)]
        for rotation in ("left", "right"):
            for pos in range(WINDOWS):
                for a in range(1 << (WIDTH - 1)):
                    b = a ^ ((1 << WIDTH) - 1)
                    (h1, p1), (h2, p2) = train(initial, pos, a, b, rotation)
                    c1 = propagation_cost(h1, p1, pos, rotation)
                    c2 = propagation_cost(h2, p2, pos, rotation)
                    total += 1
                    is_different = c1 != c2
                    if is_different:
                        different += 1
                        seq1_faster += int(c1 < c2)
                        seq2_faster += int(c2 < c1)

                    same_support = activity_support(h1, p1, rotation) == activity_support(h2, p2, rotation)
                    same_local = tuple(h1[(pos + d) % WINDOWS] for d in (-1, 0, 1)) == tuple(
                        h2[(pos + d) % WINDOWS] for d in (-1, 0, 1)
                    )
                    if same_support:
                        support_match += 1
                        support_match_different += int(is_different)
                    if same_local:
                        local_match += 1
                        local_match_different += int(is_different)
                    if same_support and same_local:
                        both_match += 1
                        both_match_different += int(is_different)

    print(f"cases={total}")
    print(f"distance6_cost_diff={different}")
    print(f"seq1_faster={seq1_faster}")
    print(f"seq2_faster={seq2_faster}")
    print(f"same_next_activity_support={support_match}")
    print(f"same_support_but_cost_diff={support_match_different}")
    print(f"same_local_three_windows={local_match}")
    print(f"same_local_but_cost_diff={local_match_different}")
    print(f"same_support_and_local={both_match}")
    print(f"same_support_and_local_but_cost_diff={both_match_different}")


if __name__ == "__main__":
    main()
