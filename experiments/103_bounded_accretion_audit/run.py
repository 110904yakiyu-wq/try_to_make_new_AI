#!/usr/bin/env python3
import importlib.util
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


exp100 = load("exp100", ROOT / "100_localized_organization_collisions" / "run.py")
exp101 = load("exp101", ROOT / "101_collision_product_persistence" / "run.py")
exp102 = load("exp102", ROOT / "102_recursive_collision_chain" / "run.py")


def embed(frame, size, shift=0):
    out = [0] * size
    for i, value in enumerate(frame):
        if value:
            out[(i + shift) % size] = value
    return tuple(out)


def support_period(info):
    period = None if info[1] is None else info[2] - info[1]
    return len(info[4]), period


def nearest_start(info, side, size):
    support = info[4]
    lo = min(support)
    hi = max(support)
    if side == "right":
        for start in range(hi + 1, size - 1):
            if start % 3 == 2 and start not in support and start + 1 not in support:
                return start
    else:
        for start in range(lo - 2, -1, -1):
            if start % 3 == 2 and start not in support and start + 1 not in support:
                return start
    raise RuntimeError("no phase-compatible adjacent parent position")


def seed(pair, start, size):
    out = [0] * size
    out[start] = pair[0]
    out[start + 1] = pair[1]
    return tuple(out)


def add_parent(frame, pair, start):
    out = list(frame)
    if out[start] or out[start + 1]:
        return None
    out[start] = pair[0]
    out[start + 1] = pair[1]
    return tuple(out)


def interaction_time(left, right, joint, direction="left", horizon=1000):
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


def motif_count(info, width):
    radius = width // 2
    motifs = set()
    for frame in info[3]:
        n = len(frame)
        for center in range(n):
            motif = tuple(frame[(center + j - radius) % n] for j in range(width))
            if any(motif):
                motifs.add(motif)
    return len(motifs)


def build_g2(direction="left"):
    g0, g1 = exp102.build_g1(direction)
    g1_catalog = {x[2] for x in g1}
    g2 = []
    for pair, info, _ in g1:
        frame = exp102.phase0_frame(info)
        kind, result = exp102.collide_from_phase0(frame, pair, 17, direction)
        if kind != "localized":
            continue
        key = exp102.key_of(result)
        if key not in g0 and key not in g1_catalog:
            g2.append((pair, result, key))
    return g2


def corrected_stage3(direction="left"):
    out = []
    for pair, info, _ in build_g2(direction):
        frame = exp102.phase0_frame(info)
        combined = add_parent(frame, pair, 14)
        parent = seed(pair, 14, len(frame))
        if interaction_time(frame, parent, combined, direction) is None:
            continue
        result = exp101.orbit_from_phase(combined, 0, direction, max_ticks=4000)
        out.append((pair, result))
    return out


def ring_scaling():
    stage3 = corrected_stage3("left")
    signatures = Counter()
    for _, info in stage3:
        frame = exp102.phase0_frame(info)
        values = []
        for size in (60, 90, 120):
            result = exp101.orbit_from_phase(embed(frame, size), 0, "left", max_ticks=5000)
            values.append(support_period(result))
        signatures[tuple(values)] += 1
    print("ring_scaling")
    for signature, count in signatures.items():
        print(f"count={count} signatures={signature}")


def growth_audit():
    stage3 = corrected_stage3("left")
    period6 = [(pair, info) for pair, info in stage3 if support_period(info) == (13, 6)]

    support_sequences = Counter()
    motif3_sequences = Counter()
    motif5_sequences = Counter()
    motif7_sequences = Counter()

    for pair, info in period6:
        frame = exp102.phase0_frame(info)
        start = 26
        joint = add_parent(frame, pair, start)
        if interaction_time(frame, seed(pair, start, len(frame)), joint) is None:
            continue
        info = exp101.orbit_from_phase(joint, 0, "left", max_ticks=5000)

        frame = exp102.phase0_frame(info)
        start = 11
        joint = add_parent(frame, pair, start)
        if interaction_time(frame, seed(pair, start, len(frame)), joint) is None:
            continue
        info = exp101.orbit_from_phase(joint, 0, "left", max_ticks=5000)

        # The current support is 19. Re-center by a multiple of three so the
        # scheduler phase relation is preserved, then continue on a larger ring.
        info = exp101.orbit_from_phase(embed(exp102.phase0_frame(info), 120, shift=30), 0, "left", max_ticks=6000)

        supports = []
        motifs3 = []
        motifs5 = []
        motifs7 = []
        side = "right"

        for stage in range(6):
            supports.append(len(info[4]))
            motifs3.append(motif_count(info, 3))
            motifs5.append(motif_count(info, 5))
            motifs7.append(motif_count(info, 7))
            if stage == 5:
                break

            frame = exp102.phase0_frame(info)
            start = nearest_start(info, side, len(frame))
            joint = add_parent(frame, pair, start)
            parent = seed(pair, start, len(frame))
            if interaction_time(frame, parent, joint) is None:
                raise RuntimeError("expected accretion interaction did not occur")
            info = exp101.orbit_from_phase(joint, 0, "left", max_ticks=7000)
            side = "left" if side == "right" else "right"

        support_sequences[tuple(supports)] += 1
        motif3_sequences[tuple(motifs3)] += 1
        motif5_sequences[tuple(motifs5)] += 1
        motif7_sequences[tuple(motifs7)] += 1

    print("growth_audit")
    print(f"chains={len(period6)}")
    print(f"support_sequences={dict(support_sequences)}")
    print(f"motif3_sequences={dict(motif3_sequences)}")
    print(f"motif5_sequences={dict(motif5_sequences)}")
    print(f"motif7_sequences={dict(motif7_sequences)}")


def main():
    ring_scaling()
    growth_audit()


if __name__ == "__main__":
    main()
