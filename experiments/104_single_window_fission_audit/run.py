#!/usr/bin/env python3
"""Experiment 104: phase-aware reproduction of the strict-fission assay.

No agent, reward, explicit object boundary or replication instruction.
The <=13-window daughter criterion is the historical G0 assay convention,
NOT a general physical definition of boundedness (see Experiment 103).
"""
from collections import Counter
from functools import lru_cache

SIZE = 60
CENTER = 30  # Phase-zero aligned; shifting by 1 or 2 changes the experiment.
assert CENTER % 3 == 0

@lru_cache(maxsize=16)
def blocks(size, phase):
    assert size % 3 == 0
    return tuple(tuple((phase + 3*j + k) % size for k in range(3))
                 for j in range(size // 3))

def rotate(x, direction):
    return (((x << 1) & 15) | (x >> 3)) if direction == "left" else ((x >> 1) | ((x & 1) << 3))

def step(s, phase, direction="left"):
    out = bytearray(s)
    for i, j, k in blocks(len(s), phase):
        x, y, z = s[i], s[j], s[k]
        out[i] = x ^ rotate(y & z, direction)
        out[j] = y ^ rotate(x & z, direction)
        out[k] = z ^ rotate(x & y, direction)
    return bytes(out)

def orbit(s, phase=0, direction="left", max_ticks=2500):
    s = bytes(s)
    seen = {(s, phase): 0}
    frames = [s]
    for t in range(1, max_ticks + 1):
        s = step(s, (phase + t - 1) % 3, direction)
        key = (s, (phase + t) % 3)
        if key in seen:
            begin = seen[key]
            cycle = frames[begin:t]
            support = {i for frame in cycle for i, value in enumerate(frame) if value}
            return dict(status="cycle", cycle=cycle, phase=(phase + begin) % 3,
                        period=t-begin, support=support, active=len(set(cycle)) > 1)
        seen[key] = t
        frames.append(s)
    return dict(status="timeout", cycle=frames[-100:], phase=None, period=None,
                support={i for f in frames[-100:] for i, v in enumerate(f) if v},
                active=None)

def seed(pair):
    s = bytearray(SIZE)
    s[CENTER:CENTER+2] = pair
    return bytes(s)

def parents(direction="left"):
    for a in range(1, 16):
        for b in range(1, 16):
            res = orbit(seed((a, b)), direction=direction)
            if res["status"] != "cycle" or not res["active"] or len(res["support"]) > 13:
                continue
            phase0 = [f for j, f in enumerate(res["cycle"])
                      if (res["phase"] + j) % 3 == 0]
            frame = max(phase0, key=lambda f: sum(bool(v) for v in f))
            yield (a, b), frame, res

def boundary(union_support_frame, side):
    occupied = [i for i, value in enumerate(union_support_frame) if value]
    assert occupied
    return (min(occupied)-1 if side == "left" else max(occupied)+1) % len(union_support_frame)

def components(support, n):
    remaining = set(support)
    found = []
    while remaining:
        p = min(remaining)
        remaining.remove(p)
        frontier = [p]
        comp = {p}
        while frontier:
            i = frontier.pop()
            for j in ((i-1) % n, (i+1) % n):
                if j in remaining:
                    remaining.remove(j)
                    frontier.append(j)
                    comp.add(j)
        found.append(comp)
    return found

def daughters(result, direction="left"):
    if result["status"] != "cycle":
        return "timeout", []
    if not result["active"]:
        return "static", []
    parts = components(result["support"], SIZE)
    if len(parts) < 2:
        return "active_connected", []
    frames = [f for j, f in enumerate(result["cycle"])
              if (result["phase"] + j) % 3 == 0]
    frame = max(frames, key=lambda f: sum(bool(v) for v in f))
    viable = []
    for part in parts:
        if not any(frame[i] for i in part):
            continue
        isolated = bytes(frame[i] if i in part else 0 for i in range(SIZE))
        r = orbit(isolated, phase=0, direction=direction)
        if r["status"] == "cycle" and r["active"] and len(r["support"]) <= 13:
            viable.append(r)
    return ("strict_fission", viable) if len(viable) >= 2 else ("fragmented_not_independent", viable)

def evaluate(frame, pos, raw, direction="left"):
    assert not frame[pos]
    out = bytearray(frame)
    out[pos] = raw
    result = orbit(out, phase=0, direction=direction)
    label, children = daughters(result, direction)
    return label, len(children), result, children

def trials(direction="left"):
    for idx, (pair, frame, parent_orbit) in enumerate(parents(direction)):
        union = bytes(int(i in parent_orbit["support"]) for i in range(SIZE))
        for side in ("left", "right"):
            pos = boundary(union, side)
            for raw in range(1, 16):
                label, n, res, children = evaluate(frame, pos, raw, direction)
                yield idx, pair, side, raw, label, n, res, children

def main():
    counts = Counter()
    children = []
    for _, _, _, _, label, _, _, daughter in trials("left"):
        counts[label] += 1
        if label == "strict_fission":
            children.extend(daughter)
    print("direction=left")
    print("parents=130")
    print("trials=3900")
    for key in ("strict_fission", "fragmented_not_independent",
                "active_connected", "static", "timeout"):
        print(f"{key}={counts[key]}")
    print(f"daughters={len(children)}")
    period = Counter(d["period"] for d in children)
    support = Counter(len(d["support"]) for d in children)
    print("daughter_periods=" + str(dict(sorted(period.items()))))
    print("daughter_support=" + str(dict(sorted(support.items()))))

if __name__ == "__main__":
    main()
