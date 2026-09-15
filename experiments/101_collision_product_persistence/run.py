#!/usr/bin/env python3
import importlib.util
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "100_localized_organization_collisions" / "run.py"
spec = importlib.util.spec_from_file_location("exp100", BASE)
exp100 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp100)


def orbit_from_phase(initial, phase0, direction, max_ticks=2500):
    state = tuple(initial)
    seen = {(state, phase0): 0}
    history = [state]
    phases = [phase0]
    for age in range(max_ticks):
        phase = (phase0 + age) % 3
        state = exp100.step(state, phase, direction)
        next_phase = (phase + 1) % 3
        history.append(state)
        phases.append(next_phase)
        key = (state, next_phase)
        if key in seen:
            begin = seen[key]
            end = age + 1
            cycle = tuple(history[begin:end])
            support = {i for frame in cycle for i, value in enumerate(frame) if value}
            if len(set(cycle)) == 1:
                kind = "static"
            elif len(support) <= 13:
                kind = "localized"
            else:
                kind = "expansive_cycle"
            return kind, begin, end, cycle, support, phases[begin]
        seen[key] = age + 1
    support = {i for frame in history[-100:] for i, value in enumerate(frame) if value}
    kind = "expansive_noncycle" if len(support) > 13 else "localized_noncycle"
    return kind, None, None, tuple(history[-100:]), support, None


def orbit_key_phase(info):
    _, begin, _, cycle, _, phase0 = info
    if begin is None:
        return None
    return min(
        exp100.canonical_extended_state(frame, (phase0 + offset) % 3)
        for offset, frame in enumerate(cycle)
    )


def choose_max_support_phase(info):
    _, begin, _, cycle, _ = info
    index = max(range(len(cycle)), key=lambda i: sum(value != 0 for value in cycle[i]))
    return cycle[index], (begin + index) % 3


def boundary_zero(frame):
    n = len(frame)
    candidates = set()
    for i, value in enumerate(frame):
        if not value:
            continue
        for j in ((i - 1) % n, (i + 1) % n):
            if frame[j] == 0:
                candidates.add(j)
    return min(candidates)


def randomize_occupied(frame, rng):
    out = list(frame)
    for i, value in enumerate(out):
        if value:
            out[i] = rng.randrange(1, 16)
    return tuple(out)


def products(direction):
    pairs, catalog, _ = exp100.localized_catalog(direction)
    out = []
    for pair in pairs:
        initial = exp100.two_seed_state(pair, pair, 3)
        info = exp100.orbit(initial, direction)
        if info[0] != "localized":
            continue
        key = exp100.orbit_key(info)
        if key in catalog:
            continue
        out.append((pair, info, key))
    return out


def assay(direction, null_repeats=10):
    items = products(direction)
    actual = Counter()
    nulls = Counter()

    for index, (_, info, product_key) in enumerate(items):
        frame, phase = choose_max_support_phase(info)
        active = [i for i, value in enumerate(frame) if value]

        internal = list(frame)
        internal[active[len(active) // 2]] ^= 1
        internal = tuple(internal)

        boundary = list(frame)
        boundary[boundary_zero(frame)] ^= 1
        boundary = tuple(boundary)

        for label, damaged in (("internal", internal), ("boundary", boundary)):
            result = orbit_from_phase(damaged, phase, direction)
            if result[0] == "localized":
                actual[label + "_localized"] += 1
                if orbit_key_phase(result) == product_key:
                    actual[label + "_exact_microcycle"] += 1

        for repeat in range(null_repeats):
            rng_i = random.Random(300000 + index * 100 + repeat)
            rng_b = random.Random(400000 + index * 100 + repeat)
            if orbit_from_phase(randomize_occupied(internal, rng_i), phase, direction)[0] == "localized":
                nulls["internal_localized"] += 1
            if orbit_from_phase(randomize_occupied(boundary, rng_b), phase, direction)[0] == "localized":
                nulls["boundary_localized"] += 1

    print(f"direction={direction} products={len(items)} null_repeats={null_repeats}")
    print(f"internal_localized={actual['internal_localized']}/{len(items)}")
    print(f"boundary_localized={actual['boundary_localized']}/{len(items)}")
    print(f"internal_exact_microcycle={actual['internal_exact_microcycle']}/{len(items)}")
    print(f"boundary_exact_microcycle={actual['boundary_exact_microcycle']}/{len(items)}")
    denominator = len(items) * null_repeats
    print(f"internal_matched_null_localized={nulls['internal_localized']}/{denominator}")
    print(f"boundary_matched_null_localized={nulls['boundary_localized']}/{denominator}")


def main():
    assay("left", null_repeats=10)
    # The actual-damage aggregate is symmetry-checked under right rotation.
    # Null repetition is kept on the left kernel to avoid duplicating an expensive control.


if __name__ == "__main__":
    main()
