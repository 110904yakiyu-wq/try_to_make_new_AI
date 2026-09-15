#!/usr/bin/env python3
import itertools
import random
from collections import Counter

WIDTH = 4
WINDOWS = 12
TRAIN_TICKS = 2
MAX_PROBE_TICKS = 24


def rotl(value):
    return ((value << 1) & 15) | (value >> 3)


def rotr(value):
    return (value >> 1) | ((value & 1) << 3)


def update(values, rotation):
    x, y, z = values
    f = rotl if rotation == "left" else rotr
    return x ^ f(y & z), y ^ f(z & x), z ^ f(x & y)


def step(state, phase, rotation):
    old = state[:]
    new = state[:]
    used = set()
    for start in range(phase, phase + WINDOWS, 3):
        indices = (start % WINDOWS, (start + 1) % WINDOWS, (start + 2) % WINDOWS)
        if any(i in used for i in indices):
            continue
        used.update(indices)
        values = tuple(old[i] for i in indices)
        outputs = update(values, rotation)
        for i, out in zip(indices, outputs):
            new[i] = out
    return new


def run_ticks(state, phase, ticks, rotation):
    for _ in range(ticks):
        state = step(state, phase, rotation)
        phase = (phase + 1) % 3
    return state, phase


def train(initial, pos, a, b, rotation):
    out = []
    for sequence in ((a, a, b, b, a), (b, b, a, a, a)):
        state = initial[:]
        phase = 0
        for value in sequence:
            state[pos] = value
            state, phase = run_ticks(state, phase, TRAIN_TICKS, rotation)
        out.append((state, phase))
    return out


def canonicalize_local(h1, h2, initial, pos, a):
    h1, h2 = h1[:], h2[:]
    values = {
        (pos - 1) % WINDOWS: initial[(pos - 1) % WINDOWS],
        pos: a,
        (pos + 1) % WINDOWS: initial[(pos + 1) % WINDOWS],
    }
    for index, value in values.items():
        h1[index] = value
        h2[index] = value
    return h1, h2


def distance(a, b):
    d = abs(a - b) % WINDOWS
    return min(d, WINDOWS - d)


def propagation_profile(state, phase, pos, rotation):
    control = state[:]
    probe = state[:]
    probe[pos] ^= 1
    costs = {d: MAX_PROBE_TICKS + 1 for d in range(1, WINDOWS // 2 + 1)}
    for age in range(1, MAX_PROBE_TICKS + 1):
        control = step(control, phase, rotation)
        probe = step(probe, phase, rotation)
        phase = (phase + 1) % 3
        for i, (x, y) in enumerate(zip(control, probe)):
            if x == y:
                continue
            d = distance(pos, i)
            if d and costs[d] == MAX_PROBE_TICKS + 1:
                costs[d] = age
    return tuple(costs[d] for d in range(1, WINDOWS // 2 + 1))


def remote_regions(pos):
    return [
        [(pos + d) % WINDOWS for d in (2, 3, 4)],
        [(pos + d) % WINDOWS for d in (5, 6, 7)],
        [(pos + d) % WINDOWS for d in (8, 9, 10)],
    ]


def transplant(recipient, donor, regions, subset):
    out = recipient[:]
    for region_id in subset:
        for index in regions[region_id]:
            out[index] = donor[index]
    return out


def min_regions_for_target(recipient, donor, phase, pos, rotation, target, metric):
    regions = remote_regions(pos)
    for size in range(1, 4):
        for subset in itertools.combinations(range(3), size):
            state = transplant(recipient, donor, regions, subset)
            profile = propagation_profile(state, phase, pos, rotation)
            observed = profile[-1] if metric == "distance6" else profile
            if observed == target:
                return size
    raise RuntimeError("all three remote regions must reproduce the donor after local canonicalization")


def main():
    scalar = Counter()
    profile_counts = Counter()
    scalar_cases = profile_cases = 0

    for seed in range(32):
        initial = [random.Random(seed * 1000 + i).randrange(16) for i in range(WINDOWS)]
        for rotation in ("left", "right"):
            for pos in range(WINDOWS):
                for a in range(8):
                    b = a ^ 15
                    (h1, p1), (h2, p2) = train(initial, pos, a, b, rotation)
                    h1, h2 = canonicalize_local(h1, h2, initial, pos, a)
                    donor_profile = propagation_profile(h1, p1, pos, rotation)
                    recipient_profile = propagation_profile(h2, p2, pos, rotation)

                    if donor_profile[-1] != recipient_profile[-1]:
                        scalar_cases += 1
                        scalar[min_regions_for_target(
                            h2, h1, p2, pos, rotation, donor_profile[-1], "distance6"
                        )] += 1

                    if donor_profile != recipient_profile:
                        profile_cases += 1
                        profile_counts[min_regions_for_target(
                            h2, h1, p2, pos, rotation, donor_profile, "profile"
                        )] += 1

    print(f"distance6_cases={scalar_cases}")
    for size in range(1, 4):
        print(f"distance6_min_regions_{size}={scalar[size]}")
    print(f"profile_cases={profile_cases}")
    for size in range(1, 4):
        print(f"profile_min_regions_{size}={profile_counts[size]}")


if __name__ == "__main__":
    main()
