#!/usr/bin/env python3
from collections import Counter

WIDTH = 4
MASK = (1 << WIDTH) - 1
RING = 60
CENTER = 20
SEPARATIONS = (3, 4, 5, 6, 8, 10)


def rot(value, direction):
    if direction == "left":
        return ((value << 1) & MASK) | (value >> (WIDTH - 1))
    return (value >> 1) | ((value & 1) << (WIDTH - 1))


def update(values, direction):
    x, y, z = values
    f = lambda v: rot(v, direction)
    return (
        x ^ f(y & z),
        y ^ f(z & x),
        z ^ f(x & y),
    )


def step(state, phase, direction):
    n = len(state)
    old = tuple(state)
    new = list(old)
    for k in range(n // 3):
        start = (phase + 3 * k) % n
        indices = (start, (start + 1) % n, (start + 2) % n)
        values = tuple(old[i] for i in indices)
        outputs = update(values, direction)
        for i, value in zip(indices, outputs):
            new[i] = value
    return tuple(new)


def seed_state(pair, start=CENTER, size=RING):
    state = [0] * size
    state[start % size] = pair[0]
    state[(start + 1) % size] = pair[1]
    return tuple(state)


def two_seed_state(left, right, separation, start=CENTER, size=RING):
    state = list(seed_state(left, start, size))
    other = (start + separation) % size
    state[other] |= right[0]
    state[(other + 1) % size] |= right[1]
    return tuple(state)


def orbit(initial, direction, max_ticks=2500):
    state = tuple(initial)
    seen = {(state, 0): 0}
    history = [state]
    for tick in range(max_ticks):
        state = step(state, tick % 3, direction)
        history.append(state)
        key = (state, (tick + 1) % 3)
        if key in seen:
            begin = seen[key]
            end = tick + 1
            cycle = tuple(history[begin:end])
            support = {i for frame in cycle for i, value in enumerate(frame) if value}
            if len(set(cycle)) == 1:
                kind = "static"
            elif len(support) <= 13:
                kind = "localized"
            else:
                kind = "expansive_cycle"
            return kind, begin, end, cycle, support
        seen[key] = tick + 1

    support = {i for frame in history[-100:] for i, value in enumerate(frame) if value}
    kind = "expansive_noncycle" if len(support) > 13 else "localized_noncycle"
    return kind, None, None, tuple(history[-100:]), support


def canonical_extended_state(state, phase):
    best = None
    n = len(state)
    for shift in range(n):
        shifted = state[-shift:] + state[:-shift] if shift else state
        item = ((phase + shift) % 3, bytes(shifted))
        if best is None or item < best:
            best = item
    return best


def orbit_key(info):
    _, begin, _, cycle, _ = info
    if begin is None:
        return None
    return min(
        canonical_extended_state(frame, (begin + offset) % 3)
        for offset, frame in enumerate(cycle)
    )


def collision_time(left, right, separation, direction, horizon=300):
    a = seed_state(left, CENTER)
    b = seed_state(right, CENTER + separation)
    combined = two_seed_state(left, right, separation)

    for tick in range(horizon):
        phase = tick % 3
        a = step(a, phase, direction)
        b = step(b, phase, direction)
        combined = step(combined, phase, direction)

        if any(x and y for x, y in zip(a, b)):
            return tick + 1
        if combined != tuple(x | y for x, y in zip(a, b)):
            return tick + 1
    return None


def localized_catalog(direction):
    pairs = []
    keys = set()
    info_by_pair = {}
    for a in range(1, 16):
        for b in range(1, 16):
            pair = (a, b)
            info = orbit(seed_state(pair), direction)
            if info[0] == "localized":
                pairs.append(pair)
                key = orbit_key(info)
                keys.add(key)
                info_by_pair[pair] = key
    return pairs, keys, info_by_pair


def same_seed_sweep(direction):
    pairs, catalog, parent_keys = localized_catalog(direction)
    print(f"direction={direction} localized_seed_count={len(pairs)} catalog_cycles={len(catalog)}")
    for separation in SEPARATIONS:
        counts = Counter()
        novel = 0
        known = 0
        for pair in pairs:
            if collision_time(pair, pair, separation, direction) is None:
                counts["independent"] += 1
                continue
            info = orbit(two_seed_state(pair, pair, separation), direction)
            counts[info[0]] += 1
            if info[0] == "localized":
                key = orbit_key(info)
                if key in catalog:
                    known += 1
                else:
                    novel += 1
        print(
            f"same sep={separation} independent={counts['independent']} "
            f"static={counts['static']} localized={counts['localized']} "
            f"expansive_cycle={counts['expansive_cycle']} "
            f"expansive_noncycle={counts['expansive_noncycle']} "
            f"localized_known_catalog={known} localized_novel_catalog={novel}"
        )


def heterogeneous_sample(direction):
    pairs, catalog, _ = localized_catalog(direction)
    sample = []
    for i, left in enumerate(pairs):
        right = pairs[(i * 37 + 17) % len(pairs)]
        if right == left:
            right = pairs[(i + 1) % len(pairs)]
        sample.append((left, right))

    for separation in (3, 4, 5, 6, 8):
        counts = Counter()
        novel = 0
        for left, right in sample:
            if collision_time(left, right, separation, direction) is None:
                counts["independent"] += 1
                continue
            info = orbit(two_seed_state(left, right, separation), direction)
            counts[info[0]] += 1
            if info[0] == "localized" and orbit_key(info) not in catalog:
                novel += 1
        print(
            f"hetero sep={separation} independent={counts['independent']} "
            f"static={counts['static']} localized={counts['localized']} "
            f"expansive_cycle={counts['expansive_cycle']} "
            f"expansive_noncycle={counts['expansive_noncycle']} "
            f"localized_novel_catalog={novel}"
        )


def main():
    for direction in ("left", "right"):
        same_seed_sweep(direction)
        heterogeneous_sample(direction)
        print()


if __name__ == "__main__":
    main()
