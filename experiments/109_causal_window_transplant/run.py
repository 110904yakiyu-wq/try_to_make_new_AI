#!/usr/bin/env python3
"""Experiment 109: minimum causal patch transfer vs randomized donor null.

The signatures here cover SIX test inputs, not all 30 Experiment-108
material inputs. This is a bounded exploratory test, not proof of emergent
composition or distributed cognition.
"""
import importlib.util
import itertools
import random
import statistics
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "108_cycle_union_geometry_match" / "run.py"
spec = importlib.util.spec_from_file_location("exp108", BASE)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
m = v.m

PROBES = (1, 7, 15)
REPEATS = 2

def signature(frame, parent_union):
    support_positions = sorted(parent_union)
    sites = ((support_positions[0] - 1) % m.SIZE,
             (support_positions[-1] + 1) % m.SIZE)
    outcome = []
    for site in sites:
        assert frame[site] == 0
        for raw in PROBES:
            s = bytearray(frame)
            s[site] = raw
            r = m.orbit(bytes(s), phase=0, direction="left")
            is_connected = (r["status"] == "cycle"
                and r["active"]
                and len(m.components(r["support"], m.SIZE)) == 1)
            outcome.append(bool(is_connected))
    return tuple(outcome)

def minimal_transfer(donor, recipient, union, cached_recipient=None):
    target = signature(donor, union)
    baseline = cached_recipient if cached_recipient is not None else signature(recipient, union)
    if target == baseline:
        return 0
    changed = [i for i in range(m.SIZE) if donor[i] != recipient[i]]
    for count in range(1, len(changed) + 1):
        for subset in itertools.combinations(changed, count):
            copied = bytearray(recipient)
            for site in subset:
                copied[site] = donor[site]
            if signature(bytes(copied), union) == target:
                return count
    raise AssertionError("copying all changed positions must exactly transfer the donor signature")

def main():
    original = m.orbit
    def bounded(*args, **kw):
        kw.setdefault("max_ticks", 500)
        return original(*args, **kw)
    m.orbit = bounded

    count_actual = Counter()
    count_null = Counter()
    comparisons = []
    accepted = 0
    for index, (_, original_frame, parent) in enumerate(m.parents("left")):
        match = v.matched_control(index, original_frame, parent, 100)
        if match is None:
            continue
        accepted += 1
        recipient, _, _ = match
        rec_sig = signature(recipient, parent["support"])
        active_changed = [i for i in range(m.SIZE)
                          if original_frame[i] != recipient[i]]
        observed_min = minimal_transfer(original_frame, recipient, parent["support"], rec_sig)
        count_actual[observed_min] += 1
        replicate_min = []
        for repeat in range(REPEATS):
            rng = random.Random(109000 + index*53 + repeat)
            null = bytearray(recipient)
            for site in active_changed:
                choices = [value for value in range(1, 16)
                           if value != recipient[site]]
                null[site] = rng.choice(choices)
            msize = minimal_transfer(bytes(null), recipient, parent["support"], rec_sig)
            count_null[msize] += 1
            replicate_min.append(msize)
        comparisons.append((observed_min, statistics.mean(replicate_min)))
    print(f"parents={accepted} random_donors_per_parent={REPEATS} six_probe_signature=yes")
    print("probes_per_side=" + ",".join(map(str, PROBES)))
    for label, hist in (("actual", count_actual), ("null", count_null)):
        print(label+"_min_transfer="+",".join(str(hist[k]) for k in range(6)))
        print(label+"_mean_min="+f"{statistics.mean(list(hist.elements())):.6f}")
    print("pairwise actual_greater="+str(sum(a>b for a,b in comparisons))+
          " null_greater="+str(sum(a<b for a,b in comparisons))+
          " ties="+str(sum(a==b for a,b in comparisons)))

if __name__ == "__main__":
    main()
