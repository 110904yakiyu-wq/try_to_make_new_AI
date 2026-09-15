#!/usr/bin/env python3
# Null audit for Experiment 095.
# The donor/recipient remote difference support and per-position Hamming distance
# are preserved, but recipient bit identities are resampled independently.

import itertools
import random
from collections import Counter

WIDTH = 4
WINDOWS = 12
TRAIN_TICKS = 2
MAX_PROBE_TICKS = 24


def rotl(v):
    return ((v << 1) & 15) | (v >> 3)


def rotr(v):
    return (v >> 1) | ((v & 1) << 3)


def update(values, rotation):
    x, y, z = values
    f = rotl if rotation == "left" else rotr
    return x ^ f(y & z), y ^ f(z & x), z ^ f(x & y)


def step(state, phase, rotation):
    old = state[:]
    new = state[:]
    used = set()
    for start in range(phase, phase + WINDOWS, 3):
        ids = (start % WINDOWS, (start + 1) % WINDOWS, (start + 2) % WINDOWS)
        if any(i in used for i in ids):
            continue
        used.update(ids)
        out = update(tuple(old[i] for i in ids), rotation)
        for i, value in zip(ids, out):
            new[i] = value
    return new


def run_ticks(state, phase, ticks, rotation):
    for _ in range(ticks):
        state = step(state, phase, rotation)
        phase = (phase + 1) % 3
    return state, phase


def train(initial, pos, a, b, rotation):
    out = []
    for seq in ((a, a, b, b, a), (b, b, a, a, a)):
        state = initial[:]
        phase = 0
        for value in seq:
            state[pos] = value
            state, phase = run_ticks(state, phase, TRAIN_TICKS, rotation)
        out.append((state, phase))
    return out


def canonicalize_local(a, b, initial, pos, final_value):
    a, b = a[:], b[:]
    for i, value in (
        ((pos - 1) % WINDOWS, initial[(pos - 1) % WINDOWS]),
        (pos, final_value),
        ((pos + 1) % WINDOWS, initial[(pos + 1) % WINDOWS]),
    ):
        a[i] = b[i] = value
    return a, b


def distance(a, b):
    d = abs(a - b) % WINDOWS
    return min(d, WINDOWS - d)


def profile(state, phase, pos, rotation):
    control = state[:]
    probe = state[:]
    probe[pos] ^= 1
    costs = {d: MAX_PROBE_TICKS + 1 for d in range(1, 7)}
    for age in range(1, MAX_PROBE_TICKS + 1):
        control = step(control, phase, rotation)
        probe = step(probe, phase, rotation)
        phase = (phase + 1) % 3
        for i, (x, y) in enumerate(zip(control, probe)):
            if x != y:
                d = distance(pos, i)
                if d and costs[d] == MAX_PROBE_TICKS + 1:
                    costs[d] = age
    return tuple(costs[d] for d in range(1, 7))


def regions(pos):
    return [
        [(pos + d) % WINDOWS for d in (2, 3, 4)],
        [(pos + d) % WINDOWS for d in (5, 6, 7)],
        [(pos + d) % WINDOWS for d in (8, 9, 10)],
    ]


def transplant(recipient, donor, pos, subset):
    out = recipient[:]
    rs = regions(pos)
    for rid in subset:
        for i in rs[rid]:
            out[i] = donor[i]
    return out


def minimum_regions(recipient, donor, phase, pos, rotation, target, full_profile):
    for count in range(1, 4):
        for subset in itertools.combinations(range(3), count):
            p = profile(transplant(recipient, donor, pos, subset), phase, pos, rotation)
            value = p if full_profile else p[-1]
            if value == target:
                return count
    return 3


def same_hd_value(value, hamming, rng):
    out = value
    for bit in rng.sample(range(WIDTH), hamming):
        out ^= 1 << bit
    return out


def make_null(donor, recipient, pos, seed):
    rng = random.Random(seed)
    out = donor[:]
    local = {(pos - 1) % WINDOWS, pos, (pos + 1) % WINDOWS}
    for i in range(WINDOWS):
        if i in local:
            continue
        hd = (donor[i] ^ recipient[i]).bit_count()
        if hd:
            out[i] = same_hd_value(donor[i], hd, rng)
    return out


def audit(full_profile):
    trained = Counter()
    null = Counter()
    paired_delta = Counter()
    trained_cases = null_cases = 0

    for seed in range(16):
        initial = [random.Random(seed * 1000 + i).randrange(16) for i in range(WINDOWS)]
        for rindex, rotation in enumerate(("left", "right")):
            for pos in range(WINDOWS):
                for a in range(8):
                    b = a ^ 15
                    (donor, phase), (recipient, _) = train(initial, pos, a, b, rotation)
                    donor, recipient = canonicalize_local(donor, recipient, initial, pos, a)
                    donor_profile = profile(donor, phase, pos, rotation)
                    recipient_profile = profile(recipient, phase, pos, rotation)
                    target = donor_profile if full_profile else donor_profile[-1]
                    observed = recipient_profile if full_profile else recipient_profile[-1]
                    if observed == target:
                        continue

                    trained_cases += 1
                    m_train = minimum_regions(recipient, donor, phase, pos, rotation, target, full_profile)
                    trained[m_train] += 1

                    control = make_null(
                        donor, recipient, pos,
                        seed * 100000 + rindex * 10000 + pos * 100 + a,
                    )
                    cp = profile(control, phase, pos, rotation)
                    cvalue = cp if full_profile else cp[-1]
                    if cvalue == target:
                        continue

                    null_cases += 1
                    m_null = minimum_regions(control, donor, phase, pos, rotation, target, full_profile)
                    null[m_null] += 1
                    paired_delta[m_train - m_null] += 1

    label = "profile" if full_profile else "distance6"
    print(f"{label}_trained_cases={trained_cases}")
    for n in range(1, 4):
        print(f"{label}_trained_min_regions_{n}={trained[n]}")
    print(f"{label}_null_cases={null_cases}")
    for n in range(1, 4):
        print(f"{label}_null_min_regions_{n}={null[n]}")
    print(f"{label}_paired_trained_less={sum(v for d, v in paired_delta.items() if d < 0)}")
    print(f"{label}_paired_equal={paired_delta[0]}")
    print(f"{label}_paired_trained_more={sum(v for d, v in paired_delta.items() if d > 0)}")
    numerator = sum(d * v for d, v in paired_delta.items())
    denominator = sum(paired_delta.values())
    print(f"{label}_mean_region_delta={numerator / denominator:.9f}")


def main():
    audit(False)
    audit(True)


if __name__ == "__main__":
    main()
