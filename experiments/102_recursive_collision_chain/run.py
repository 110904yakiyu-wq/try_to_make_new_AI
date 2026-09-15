#!/usr/bin/env python3
import importlib.util
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE100 = ROOT / "100_localized_organization_collisions" / "run.py"
BASE101 = ROOT / "101_collision_product_persistence" / "run.py"

spec100 = importlib.util.spec_from_file_location("exp100", BASE100)
exp100 = importlib.util.module_from_spec(spec100)
spec100.loader.exec_module(exp100)

spec101 = importlib.util.spec_from_file_location("exp101", BASE101)
exp101 = importlib.util.module_from_spec(spec101)
spec101.loader.exec_module(exp101)


def phase0_frame(info):
    # Accept Experiment-100 five-tuples or Experiment-101 six-tuples.
    if len(info) == 5:
        _, begin, _, cycle, _ = info
        phase0 = begin % 3
    else:
        _, _, _, cycle, _, phase0 = info
    candidates = []
    for i, frame in enumerate(cycle):
        phase = (phase0 + i) % 3
        if phase == 0:
            candidates.append(frame)
    return max(candidates, key=lambda frame: sum(value != 0 for value in frame))


def add_parent(frame, pair, start):
    out = list(frame)
    if out[start] or out[(start + 1) % len(out)]:
        return None
    out[start] = pair[0]
    out[(start + 1) % len(out)] = pair[1]
    return tuple(out)


def key_of(info):
    if len(info) == 5:
        return exp100.orbit_key(info)
    return exp101.orbit_key_phase(info)


def interaction_time(frame, pair, start, direction, horizon=1000):
    parent = exp100.seed_state(pair, start)
    combined = add_parent(frame, pair, start)
    if combined is None:
        return None

    left = tuple(frame)
    right = tuple(parent)
    joint = tuple(combined)

    for age in range(horizon):
        phase = age % 3
        left = exp100.step(left, phase, direction)
        right = exp100.step(right, phase, direction)
        joint = exp100.step(joint, phase, direction)

        if any(a and b for a, b in zip(left, right)):
            return age + 1
        if joint != tuple(a | b for a, b in zip(left, right)):
            return age + 1
    return None


def collide_from_phase0(frame, pair, start, direction):
    combined = add_parent(frame, pair, start)
    if combined is None:
        return "initial_overlap", None
    if interaction_time(frame, pair, start, direction) is None:
        return "independent", None
    result = exp101.orbit_from_phase(combined, 0, direction, max_ticks=3000)
    return result[0], result


def build_g1(direction):
    pairs, g0_catalog, _ = exp100.localized_catalog(direction)
    g1 = []
    for pair in pairs:
        info = exp100.orbit(exp100.two_seed_state(pair, pair, 3), direction)
        if info[0] != "localized":
            continue
        key = exp100.orbit_key(info)
        if key not in g0_catalog:
            g1.append((pair, info, key))
    return g0_catalog, g1


def run(direction):
    g0, g1 = build_g1(direction)
    g1_catalog = {item[2] for item in g1}

    g2 = []
    counts2 = Counter()
    for pair, info, _ in g1:
        frame = phase0_frame(info)
        kind, result = collide_from_phase0(frame, pair, 17, direction)
        counts2[kind] += 1
        if kind == "localized":
            key = key_of(result)
            if key not in g0 and key not in g1_catalog:
                g2.append((pair, result, key))

    g2_catalog = {item[2] for item in g2}
    g3 = []
    counts3 = Counter()
    for pair, info, _ in g2:
        frame = phase0_frame(info)
        kind, result = collide_from_phase0(frame, pair, 14, direction)
        counts3[kind] += 1
        if kind == "localized":
            key = key_of(result)
            if key not in g0 and key not in g1_catalog and key not in g2_catalog:
                g3.append((pair, result, key))

    g3_catalog = {item[2] for item in g3}
    counts4 = Counter()
    novel4 = 0
    for pair, info, _ in g3:
        frame = phase0_frame(info)
        kind, result = collide_from_phase0(frame, pair, 26, direction)
        counts4[kind] += 1
        if kind == "localized":
            key = key_of(result)
            if key not in g0 | g1_catalog | g2_catalog | g3_catalog:
                novel4 += 1

    print(f"direction={direction}")
    print(f"g0_catalog={len(g0)} g1_novel={len(g1)}")
    print(f"g1_plus_parent_at17={dict(counts2)} g2_novel={len(g2)} distinct_g2={len(g2_catalog)}")
    print(f"g2_plus_parent_at14={dict(counts3)} g3_novel={len(g3)} distinct_g3={len(g3_catalog)}")
    print(f"g3_plus_parent_at26={dict(counts4)} g4_novel={novel4}")


def main():
    run("left")
    run("right")


if __name__ == "__main__":
    main()
