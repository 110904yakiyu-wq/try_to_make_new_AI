#!/usr/bin/env python3
import math
import random
import statistics


def rotl(value, width):
    mask = (1 << width) - 1
    return ((value << 1) & mask) | (value >> (width - 1))


def rotr(value, width):
    return (value >> 1) | ((value & 1) << (width - 1))


def update(values, width, rotation):
    x, y, z = values
    if rotation == "left":
        f = lambda v: rotl(v, width)
    elif rotation == "right":
        f = lambda v: rotr(v, width)
    elif rotation == "none":
        f = lambda v: v
    else:
        raise ValueError(rotation)
    return (
        x ^ f(y & z),
        y ^ f(z & x),
        z ^ f(x & y),
    )


def step(state, width, phase, rotation):
    n = len(state)
    old = state[:]
    new = state[:]
    events = []
    used = set()
    for start in range(phase, phase + n, 3):
        indices = (start % n, (start + 1) % n, (start + 2) % n)
        if any(index in used for index in indices):
            continue
        used.update(indices)
        values = tuple(old[index] for index in indices)
        outputs = update(values, width, rotation)
        if outputs == values:
            continue
        for index, output in zip(indices, outputs):
            new[index] = output
        events.append((indices, values, outputs))
    return new, events


def circular_distance(a, b, size):
    d = abs(a - b) % size
    return min(d, size - d)


def activity_support(events):
    return {index for indices, _, _ in events for index in indices}


def jaccard(a, b):
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def autonomous(width=4, rotation="left", seeds=64, ticks=2000, windows=12):
    event_counts = []
    changed_counts = []
    active_final = 0
    periods = []
    for seed in range(seeds):
        rng = random.Random(seed)
        state = [rng.randrange(1 << width) for _ in range(windows)]
        seen = {(tuple(state), 0): 0}
        period = None
        recent = []
        for tick in range(ticks):
            new_state, events = step(state, width, tick % 3, rotation)
            event_counts.append(len(events))
            changed_counts.append(sum(a != b for a, b in zip(state, new_state)))
            recent.append(len(events))
            state = new_state
            key = (tuple(state), (tick + 1) % 3)
            if period is None and key in seen:
                period = tick + 1 - seen[key]
            else:
                seen[key] = tick + 1
        active_final += int(any(recent[-100:]))
        if period is not None:
            periods.append(period)
    print(
        f"autonomous rotation={rotation} width={width} seeds={seeds} ticks={ticks} "
        f"events_per_tick={statistics.mean(event_counts):.6f} "
        f"changed_windows_per_tick={statistics.mean(changed_counts):.6f} "
        f"active_final100={active_final}/{seeds} cycles_detected={len(periods)}/{seeds} "
        f"cycle_median={statistics.median(periods) if periods else 0} "
        f"cycle_max={max(periods) if periods else 0}"
    )


def causal_cone(width=4, rotation="left", seeds=64, windows=12):
    targets = {1: [], 2: [], 3: [], 6: [], 12: []}
    for seed in range(seeds):
        base = [random.Random(10000 + seed * 31 + i).randrange(1 << width) for i in range(windows)]
        pos = random.Random(20000 + seed).randrange(windows)
        perturbed = base[:]
        perturbed[pos] ^= 1
        a = base[:]
        b = perturbed[:]
        for tick in range(12):
            a, _ = step(a, width, tick % 3, rotation)
            b, _ = step(b, width, tick % 3, rotation)
            age = tick + 1
            if age in targets:
                different = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
                targets[age].append((
                    len(different),
                    max((circular_distance(pos, i, windows) for i in different), default=0),
                ))
    for age, values in targets.items():
        print(
            f"causal_cone tick={age} differing_windows={statistics.mean(v[0] for v in values):.6f} "
            f"max_window_distance={statistics.mean(v[1] for v in values):.6f}"
        )


def support_persistence(width=4, rotation="left", seeds=128, ticks=1000, windows=12):
    observed1 = []
    observed3 = []
    null1 = []
    null3 = []
    positive3 = 0
    for seed in range(seeds):
        rng = random.Random(seed)
        state = [rng.randrange(1 << width) for _ in range(windows)]
        supports = []
        counts = []
        for tick in range(ticks):
            state, events = step(state, width, tick % 3, rotation)
            supports.append(activity_support(events))
            counts.append(len(events))

        null_rng = random.Random(777000 + seed)
        null_supports = []
        for tick, count in enumerate(counts):
            phase = tick % 3
            blocks = null_rng.sample(range(windows // 3), count) if count else []
            support = set()
            for block in blocks:
                start = phase + 3 * block
                support.update((start % windows, (start + 1) % windows, (start + 2) % windows))
            null_supports.append(support)

        seed_obs3 = []
        seed_null3 = []
        for lag, out_obs, out_null in ((1, observed1, null1), (3, observed3, null3)):
            values_obs = [jaccard(supports[t - lag], supports[t]) for t in range(lag, ticks)]
            values_null = [jaccard(null_supports[t - lag], null_supports[t]) for t in range(lag, ticks)]
            out_obs.extend(values_obs)
            out_null.extend(values_null)
            if lag == 3:
                seed_obs3 = values_obs
                seed_null3 = values_null
        positive3 += int(statistics.mean(seed_obs3) > statistics.mean(seed_null3))

    print(
        f"support rotation={rotation} adjacent_observed={statistics.mean(observed1):.6f} "
        f"adjacent_null={statistics.mean(null1):.6f} lag3_observed={statistics.mean(observed3):.6f} "
        f"lag3_null={statistics.mean(null3):.6f} lag3_positive={positive3}/{seeds}"
    )


def sign_test_two_sided(positive, negative):
    n = positive + negative
    k = min(positive, negative)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n))


def perturbation(width=4, rotation="left", seeds=128, windows=12, warmup=100, horizon=48):
    observed = []
    nulls = []
    hammings = []
    paired = []
    for seed in range(seeds):
        rng = random.Random(seed)
        state = [rng.randrange(1 << width) for _ in range(windows)]
        phase = 0
        for _ in range(warmup):
            state, _ = step(state, width, phase, rotation)
            phase = (phase + 1) % 3

        control = state[:]
        perturbed = state[:]
        bit_pos = random.Random(50999 + seed).randrange(windows * width)
        perturbed[bit_pos // width] ^= 1 << (bit_pos % width)

        independent = [random.Random(90000 + seed * 31 + i).randrange(1 << width) for i in range(windows)]
        phase2 = 0
        for _ in range(warmup):
            independent, _ = step(independent, width, phase2, rotation)
            phase2 = (phase2 + 1) % 3

        local_obs = []
        local_null = []
        local_hamming = []
        for age in range(horizon):
            control, ec = step(control, width, phase, rotation)
            perturbed, ep = step(perturbed, width, phase, rotation)
            independent, en = step(independent, width, phase, rotation)
            phase = (phase + 1) % 3
            if age >= 24:
                local_obs.append(jaccard(activity_support(ec), activity_support(ep)))
                local_null.append(jaccard(activity_support(ec), activity_support(en)))
                local_hamming.append(sum((a ^ b).bit_count() for a, b in zip(control, perturbed)))
        observed.append(statistics.mean(local_obs))
        nulls.append(statistics.mean(local_null))
        hammings.append(statistics.mean(local_hamming))
        paired.append(observed[-1] - nulls[-1])

    positive = sum(value > 0 for value in paired)
    negative = sum(value < 0 for value in paired)
    print(
        f"perturbation support_observed={statistics.mean(observed):.6f} "
        f"support_independent={statistics.mean(nulls):.6f} raw_hamming={statistics.mean(hammings):.6f} "
        f"positive={positive} negative={negative} tie={seeds-positive-negative} "
        f"sign_p={sign_test_two_sided(positive, negative):.9f}"
    )


def main():
    for rotation in ("left", "right", "none"):
        autonomous(rotation=rotation)
    causal_cone()
    support_persistence(rotation="left")
    support_persistence(rotation="right")
    perturbation()


if __name__ == "__main__":
    main()
